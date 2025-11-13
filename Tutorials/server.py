
"""
IMPORTANT: This server must NEVER print anything except valid JSON protocol responses to stdout.
All debug, info, or error output must go to stderr.

This script now includes a global stdout guard: any accidental writes to sys.stdout (outside the protocol loop) will be redirected to sys.stderr.
"""

# --- Global stdout guard ---
import sys
import io
class StdoutGuard(io.TextIOBase):
    def write(self, s):
        sys.stderr.write("[stdout-guarded] " + str(s))
        sys.stderr.flush()
        return len(s)
    def flush(self):
        sys.stderr.flush()

# Only allow protocol loop to write to stdout
_real_stdout = sys.stdout
sys.stdout = StdoutGuard()

import json
import os
import sys
import time
import traceback
from typing import Any, Dict, Optional, List

# Try to import arcpy (only available in ArcGIS Pro's Python environment)
try:
    import arcpy
    ARCPY_AVAILABLE = True
except ImportError:
    ARCPY_AVAILABLE = False
    arcpy = None  # type: ignore

# Minimal MCP stdio server pattern (pseudo; adjust depending on actual MCP python sdk)
# We'll implement a very small request loop responding to 'ping' and 'list_layers'.
# For 'list_layers', we forward an IPC request to the existing Named Pipe used by the .NET AddIn.
# Pipe name: \\?\pipe\ArcGisProBridgePipe or \\.\pipe\ArcGisProBridgePipe depending on platform.
# On Windows the canonical form for CreateFile is r"\\.\pipe\ArcGisProBridgePipe".
PIPE_NAME = r"\\.\pipe\ArcGisProBridgePipe"

# Helper: Validate required arguments
def validate_args(args: Dict[str, Any], required: List[str]) -> Optional[str]:
    """Validate that required arguments are present and non-empty."""
    missing = []
    for arg in required:
        if arg not in args or not args[arg]:
            missing.append(arg)
    if missing:
        return f"Missing required arguments: {', '.join(missing)}"
    return None

# Helper: Create error response
def error_response(message: str, code: str = "error") -> Dict[str, Any]:
    """Create a standardized error response."""
    return {"ok": False, "error": message, "code": code}

# Helper: Create success response
def success_response(data: Any) -> Dict[str, Any]:
    """Create a standardized success response."""
    return {"ok": True, "data": data, "error": None}

# Helper to call the existing bridge pipe (JSON line protocol)
def call_bridge(op: str, args: Optional[Dict[str, str]] = None, timeout: float = 2.0) -> Dict[str, Any]:
    start = time.time()
    while True:
        try:
            import msvcrt  # type: ignore  # Windows only
            # Open the named pipe as a file
            with open(PIPE_NAME, 'r+b', buffering=0) as f:  # binary allows manual write/read
                req = {"op": op, "args": args}
                data = (json.dumps(req) + "\n").encode('utf-8')
                f.write(data)
                # Read until newline
                chunks: List[bytes] = []
                while True:
                    b = f.read(1)
                    if not b:
                        raise IOError("EOF from pipe")
                    if b == b'\n':
                        break
                    chunks.append(b)
                resp_raw = b''.join(chunks).decode('utf-8')
                resp = json.loads(resp_raw)
                return resp
        except FileNotFoundError:
            if time.time() - start > timeout:
                return {"ok": False, "error": f"pipe not found: {PIPE_NAME}"}
            time.sleep(0.1)
        except Exception as e:
            return {"ok": False, "error": f"bridge error: {e}"}

# --- ArcPy Data Management Helpers ---
def arcpy_delete_dataset(dataset: str) -> Dict[str, Any]:
    """Delete a dataset (feature class, table, etc.)."""
    if not ARCPY_AVAILABLE:
        return error_response("arcpy not available", "arcpy_missing")
    try:
        if not arcpy.Exists(dataset):
            return error_response(f"Dataset not found: {dataset}", "not_found")
        arcpy.management.Delete(dataset)
        return success_response({"deleted": True})
    except Exception as e:
        return error_response(str(e), "arcpy_error")
def arcpy_list_feature_classes(workspace: str, feature_type: str = "All") -> Dict[str, Any]:
    """List feature classes in a workspace."""
    if not ARCPY_AVAILABLE:
        return error_response("arcpy not available", "arcpy_missing")
    try:
        if not os.path.exists(workspace):
            return error_response(f"Workspace not found: {workspace}", "not_found")
        arcpy.env.workspace = workspace
        fcs = arcpy.ListFeatureClasses(feature_type=feature_type)
        return success_response(fcs if fcs else [])
    except Exception as e:
        return error_response(str(e), "arcpy_error")

def arcpy_describe_dataset(dataset: str) -> Dict[str, Any]:
    """Describe a dataset (feature class, table, etc.)."""
    if not ARCPY_AVAILABLE:
        return error_response("arcpy not available", "arcpy_missing")
    try:
        if not arcpy.Exists(dataset):
            return error_response(f"Dataset not found: {dataset}", "not_found")
        desc = arcpy.Describe(dataset)
        info = {
            "name": desc.name,
            "dataType": desc.dataType,
            "shapeType": getattr(desc, "shapeType", None),
            "spatialReference": getattr(desc, "spatialReference", None).name if hasattr(desc, "spatialReference") else None,
            "featureCount": int(arcpy.management.GetCount(dataset)[0]) if desc.dataType == "FeatureClass" else None
        }
        return success_response(info)
    except Exception as e:
        return error_response(str(e), "arcpy_error")

def arcpy_count_features(feature_class: str) -> Dict[str, Any]:
    """Count features in a feature class."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        count = int(arcpy.management.GetCount(feature_class)[0])
        return {"ok": True, "data": {"count": count}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_buffer_features(input_features: str, output_features: str, buffer_distance: str) -> Dict[str, Any]:
    """Buffer features."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        arcpy.analysis.Buffer(input_features, output_features, buffer_distance)
        return {"ok": True, "data": {"output": output_features}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_clip_features(input_features: str, clip_features: str, output_features: str) -> Dict[str, Any]:
    """Clip features."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        arcpy.analysis.Clip(input_features, clip_features, output_features)
        return {"ok": True, "data": {"output": output_features}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_copy_features(input_features: str, output_features: str, where_clause: str = None) -> Dict[str, Any]:
    """Copy features (optionally filtered)."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        arcpy.management.CopyFeatures(input_features, output_features, where_clause=where_clause)
        return {"ok": True, "data": {"output": output_features}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_project_features(input_features: str, output_features: str, output_coordinate_system: str) -> Dict[str, Any]:
    """Project features to a new coordinate system."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        # Handle EPSG codes (e.g., "32633" or "EPSG:32633")
        if output_coordinate_system.isdigit():
            # Plain EPSG code like "32633"
            sr = arcpy.SpatialReference(int(output_coordinate_system))
        elif output_coordinate_system.upper().startswith("EPSG:"):
            # Format like "EPSG:32633"
            epsg_code = int(output_coordinate_system.split(":")[1])
            sr = arcpy.SpatialReference(epsg_code)
        else:
            # Assume it's a spatial reference name or WKT
            sr = output_coordinate_system
        
        arcpy.management.Project(input_features, output_features, sr)
        return {"ok": True, "data": {"output": output_features}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_select_by_attribute(input_features: str, output_features: str, where_clause: str) -> Dict[str, Any]:
    """Select features by attribute query."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        arcpy.analysis.Select(input_features, output_features, where_clause)
        count = int(arcpy.management.GetCount(output_features)[0])
        return {"ok": True, "data": {"output": output_features, "count": count}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_delete_features(feature_class: str, where_clause: str = None) -> Dict[str, Any]:
    """Delete features from a feature class."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        if where_clause:
            layer = "temp_layer"
            arcpy.management.MakeFeatureLayer(feature_class, layer, where_clause)
            arcpy.management.DeleteFeatures(layer)
            arcpy.management.Delete(layer)
        else:
            arcpy.management.DeleteFeatures(feature_class)
        return {"ok": True, "data": {"deleted": True}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_delete_dataset(dataset: str) -> Dict[str, Any]:
    """Delete an entire dataset (feature class, table, etc.)."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        if not arcpy.Exists(dataset):
            return {"ok": False, "error": f"Dataset not found: {dataset}"}
        arcpy.management.Delete(dataset)
        return {"ok": True, "data": {"deleted": True, "dataset": dataset}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_export_to_shapefile(input_features: str, output_folder: str, output_name: str) -> Dict[str, Any]:
    """Export feature class to shapefile."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        output_path = os.path.join(output_folder, output_name  + ".shp")
        arcpy.conversion.FeatureClassToShapefile(input_features, output_folder)
        return {"ok": True, "data": {"output": output_path}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_add_field(dataset: str, field_name: str, field_type: str, field_length: int = None, field_alias: str = None) -> Dict[str, Any]:
    """Add a field to a feature class or table."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        arcpy.management.AddField(dataset, field_name, field_type, field_length=field_length, field_alias=field_alias)
        return {"ok": True, "data": {"field": field_name}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_calculate_field(table: str, field_name: str, expression: str, where_clause: str = None) -> Dict[str, Any]:
    """Calculate field values using a Python expression."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        arcpy.management.CalculateField(table, field_name, expression, "PYTHON3", where_clause=where_clause)
        return {"ok": True, "data": {"calculated": field_name}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_get_spatial_reference(dataset: str) -> Dict[str, Any]:
    """Get spatial reference information for a dataset."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        desc = arcpy.Describe(dataset)
        sr = desc.spatialReference
        info = {
            "name": sr.name,
            "type": sr.type,
            "factoryCode": sr.factoryCode,
            "wkt": sr.exportToString()
        }
        return {"ok": True, "data": info}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_create_feature_class(workspace: str, name: str, geometry_type: str, spatial_reference: str = None) -> Dict[str, Any]:
    """Create a new feature class."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        arcpy.management.CreateFeatureclass(workspace, name, geometry_type, spatial_reference=spatial_reference)
        output = os.path.join(workspace, name)
        return {"ok": True, "data": {"output": output}}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def arcpy_get_field_info(dataset: str) -> Dict[str, Any]:
    """Get field information for a dataset."""
    if not ARCPY_AVAILABLE:
        return {"ok": False, "error": "arcpy not available"}
    try:
        fields = arcpy.ListFields(dataset)
        field_info = []
        for field in fields:
            field_info.append({
                "name": field.name,
                "type": field.type,
                "length": field.length,
                "alias": field.aliasName,
                "nullable": field.isNullable
            })
        return {"ok": True, "data": field_info}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# --- End ArcPy Helpers ---


# MCP JSON-RPC 2.0 protocol implementation
# Expects: {"jsonrpc": "2.0", "method": "...", "id": ..., "params": {...}}
# Responds: {"jsonrpc": "2.0", "result": {...}, "id": ...} or {"jsonrpc": "2.0", "error": {...}, "id": ...}

def send_response(msg_id: Any, result: Any = None, error: Any = None):
    """Send a JSON-RPC 2.0 response."""
    if error:
        response = {"jsonrpc": "2.0", "error": error, "id": msg_id}
        sys.stderr.write(f"[server] Sending error response: id={msg_id} error={error}\n")
    else:
        response = {"jsonrpc": "2.0", "result": result, "id": msg_id}
        sys.stderr.write(f"[server] Sending success response: id={msg_id}\n")
    sys.stderr.flush()
    
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()

def handle_tool_response(msg_id: Any, resp: Dict[str, Any]):
    """Convert internal response format to JSON-RPC response with MCP content format."""
    if resp.get("ok"):
        data = resp.get("data")
        # Format as MCP content
        result = {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(data, indent=2)
                }
            ]
        }
        send_response(msg_id, result=result)
    else:
        send_response(msg_id, error={"code": -32000, "message": resp.get("error")})

def main():
    # Ensure stdin is unbuffered for line-by-line reading
    sys.stderr.write("[server] Starting main protocol loop, waiting for requests...\n")
    sys.stderr.flush()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        sys.stderr.write(f"[server] Received: {line[:100]}...\n")
        sys.stderr.flush()
        
        try:
            msg = json.loads(line)
        except Exception as e:
            # No id available for malformed JSON
            sys.stderr.write(f"[server] JSON parse error: {e}\n")
            sys.stderr.flush()
            send_response(None, error={"code": -32700, "message": f"Parse error: {e}"})
            continue
        
        msg_id = msg.get("id")
        method = msg.get("method")
        params = msg.get("params", {})
        
        sys.stderr.write(f"[server] Processing method={method} id={msg_id}\n")
        sys.stderr.flush()
        
        # MCP protocol: initialize
        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "arcpy-mcp",
                    "version": "1.0"
                },
                "capabilities": {
                    "tools": {}
                }
            }
            send_response(msg_id, result=result)
            continue
        
        # MCP protocol: tools/list
        if method == "tools/list":
            tools = [
                {"name": "ping", "description": "Ping test (Python MCP server)", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "list_layers", "description": "List layers via ArcGIS Pro bridge", "inputSchema": {"type": "object", "properties": {}}},
                {"name": "list_feature_classes", "description": "List feature classes in a workspace (arcpy)", "inputSchema": {"type": "object", "properties": {"workspace": {"type": "string"}, "feature_type": {"type": "string"}}, "required": ["workspace"]}},
                {"name": "describe_dataset", "description": "Describe a dataset (arcpy)", "inputSchema": {"type": "object", "properties": {"dataset": {"type": "string"}}, "required": ["dataset"]}},
                {"name": "count_features_arcpy", "description": "Count features in a feature class (arcpy)", "inputSchema": {"type": "object", "properties": {"feature_class": {"type": "string"}}, "required": ["feature_class"]}},
                {"name": "buffer_features", "description": "Buffer features (arcpy)", "inputSchema": {"type": "object", "properties": {"input_features": {"type": "string"}, "output_features": {"type": "string"}, "buffer_distance": {"type": "string"}}, "required": ["input_features", "output_features", "buffer_distance"]}},
                {"name": "clip_features", "description": "Clip features (arcpy)", "inputSchema": {"type": "object", "properties": {"input_features": {"type": "string"}, "clip_features": {"type": "string"}, "output_features": {"type": "string"}}, "required": ["input_features", "clip_features", "output_features"]}},
                {"name": "copy_features", "description": "Copy features (arcpy)", "inputSchema": {"type": "object", "properties": {"input_features": {"type": "string"}, "output_features": {"type": "string"}, "where_clause": {"type": "string"}}, "required": ["input_features", "output_features"]}},
                {"name": "project_features", "description": "Project features to new coordinate system (arcpy)", "inputSchema": {"type": "object", "properties": {"input_features": {"type": "string"}, "output_features": {"type": "string"}, "output_coordinate_system": {"type": "string"}}, "required": ["input_features", "output_features", "output_coordinate_system"]}},
                {"name": "select_by_attribute", "description": "Select features by attribute query (arcpy)", "inputSchema": {"type": "object", "properties": {"input_features": {"type": "string"}, "output_features": {"type": "string"}, "where_clause": {"type": "string"}}, "required": ["input_features", "output_features", "where_clause"]}},
                {"name": "delete_dataset", "description": "Delete a dataset (feature class, table, etc.) (arcpy)", "inputSchema": {"type": "object", "properties": {"dataset": {"type": "string"}}, "required": ["dataset"]}},
                {"name": "delete_features", "description": "Delete features from a feature class (arcpy)", "inputSchema": {"type": "object", "properties": {"feature_class": {"type": "string"}, "where_clause": {"type": "string"}}, "required": ["feature_class"]}},
                {"name": "delete_dataset", "description": "Delete an entire dataset (feature class/table) (arcpy)", "inputSchema": {"type": "object", "properties": {"dataset": {"type": "string"}}, "required": ["dataset"]}},
                {"name": "export_to_shapefile", "description": "Export feature class to shapefile (arcpy)", "inputSchema": {"type": "object", "properties": {"input_features": {"type": "string"}, "output_folder": {"type": "string"}, "output_name": {"type": "string"}}, "required": ["input_features", "output_folder", "output_name"]}},
                {"name": "add_field", "description": "Add a field to a feature class or table (arcpy)", "inputSchema": {"type": "object", "properties": {"dataset": {"type": "string"}, "field_name": {"type": "string"}, "field_type": {"type": "string"}, "field_length": {"type": "integer"}, "field_alias": {"type": "string"}}, "required": ["dataset", "field_name", "field_type"]}},
                {"name": "calculate_field", "description": "Calculate field values using a Python expression (arcpy)", "inputSchema": {"type": "object", "properties": {"table": {"type": "string"}, "field_name": {"type": "string"}, "expression": {"type": "string"}, "where_clause": {"type": "string"}}, "required": ["table", "field_name", "expression"]}},
                {"name": "get_spatial_reference", "description": "Get spatial reference information for a dataset (arcpy)", "inputSchema": {"type": "object", "properties": {"dataset": {"type": "string"}}, "required": ["dataset"]}},
                {"name": "create_feature_class", "description": "Create a new feature class (arcpy)", "inputSchema": {"type": "object", "properties": {"workspace": {"type": "string"}, "name": {"type": "string"}, "geometry_type": {"type": "string"}, "spatial_reference": {"type": "string"}}, "required": ["workspace", "name", "geometry_type"]}},
                {"name": "get_field_info", "description": "Get field information for a dataset (arcpy)", "inputSchema": {"type": "object", "properties": {"dataset": {"type": "string"}}, "required": ["dataset"]}}
            ]
            send_response(msg_id, result={"tools": tools})
            continue
        # MCP protocol: tools/call
        if method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})
            
            try:
                if name == "ping":
                    result = {
                        "content": [
                            {
                                "type": "text",
                                "text": f"pong {time.time()}"
                            }
                        ]
                    }
                    send_response(msg_id, result=result)
                    continue
            
                if name == "list_layers":
                    resp = call_bridge("pro.listLayers")
                    handle_tool_response(msg_id, resp)
                    continue
                
                # ArcPy tools
                if name == "list_feature_classes":
                    workspace = args.get("workspace")
                    feature_type = args.get("feature_type", "All")
                    if not workspace:
                        send_response(msg_id, error={"code": -32602, "message": "workspace required"})
                        continue
                    resp = arcpy_list_feature_classes(workspace, feature_type)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "describe_dataset":
                    dataset = args.get("dataset")
                    if not dataset:
                        send_response(msg_id, error={"code": -32602, "message": "dataset required"})
                        continue
                    resp = arcpy_describe_dataset(dataset)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "count_features_arcpy":
                    feature_class = args.get("feature_class")
                    if not feature_class:
                        send_response(msg_id, error={"code": -32602, "message": "feature_class required"})
                        continue
                    resp = arcpy_count_features(feature_class)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "buffer_features":
                    input_features = args.get("input_features")
                    output_features = args.get("output_features")
                    buffer_distance = args.get("buffer_distance")
                    if not all([input_features, output_features, buffer_distance]):
                        send_response(msg_id, error={"code": -32602, "message": "input_features, output_features, buffer_distance required"})
                        continue
                    resp = arcpy_buffer_features(input_features, output_features, buffer_distance)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "clip_features":
                    input_features = args.get("input_features")
                    clip_features = args.get("clip_features")
                    output_features = args.get("output_features")
                    if not all([input_features, clip_features, output_features]):
                        send_response(msg_id, error={"code": -32602, "message": "input_features, clip_features, output_features required"})
                        continue
                    resp = arcpy_clip_features(input_features, clip_features, output_features)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "copy_features":
                    input_features = args.get("input_features")
                    output_features = args.get("output_features")
                    where_clause = args.get("where_clause")
                    if not all([input_features, output_features]):
                        send_response(msg_id, error={"code": -32602, "message": "input_features, output_features required"})
                        continue
                    resp = arcpy_copy_features(input_features, output_features, where_clause)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "project_features":
                    input_features = args.get("input_features")
                    output_features = args.get("output_features")
                    output_coordinate_system = args.get("output_coordinate_system")
                    if not all([input_features, output_features, output_coordinate_system]):
                        send_response(msg_id, error={"code": -32602, "message": "input_features, output_features, output_coordinate_system required"})
                        continue
                    resp = arcpy_project_features(input_features, output_features, output_coordinate_system)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "select_by_attribute":
                    input_features = args.get("input_features")
                    output_features = args.get("output_features")
                    where_clause = args.get("where_clause")
                    if not all([input_features, output_features, where_clause]):
                        send_response(msg_id, error={"code": -32602, "message": "input_features, output_features, where_clause required"})
                        continue
                    resp = arcpy_select_by_attribute(input_features, output_features, where_clause)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "delete_features":
                    feature_class = args.get("feature_class")
                    where_clause = args.get("where_clause")
                    if not feature_class:
                        send_response(msg_id, error={"code": -32602, "message": "feature_class required"})
                        continue
                    resp = arcpy_delete_features(feature_class, where_clause)
                    handle_tool_response(msg_id, resp)
                    continue
            
                if name == "delete_dataset":
                    dataset = args.get("dataset")
                    if not dataset:
                        send_response(msg_id, error={"code": -32602, "message": "dataset required"})
                        continue
                    resp = arcpy_delete_dataset(dataset)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "export_to_shapefile":
                    input_features = args.get("input_features")
                    output_folder = args.get("output_folder")
                    output_name = args.get("output_name")
                    if not all([input_features, output_folder, output_name]):
                        send_response(msg_id, error={"code": -32602, "message": "input_features, output_folder, output_name required"})
                        continue
                    resp = arcpy_export_to_shapefile(input_features, output_folder, output_name)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "add_field":
                    dataset = args.get("dataset")
                    field_name = args.get("field_name")
                    field_type = args.get("field_type")
                    field_length = args.get("field_length")
                    field_alias = args.get("field_alias")
                    if not all([dataset, field_name, field_type]):
                        send_response(msg_id, error={"code": -32602, "message": "dataset, field_name, field_type required"})
                        continue
                    if field_length:
                        field_length = int(field_length)
                    resp = arcpy_add_field(dataset, field_name, field_type, field_length, field_alias)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "calculate_field":
                    table = args.get("table")
                    field_name = args.get("field_name")
                    expression = args.get("expression")
                    where_clause = args.get("where_clause")
                    if not all([table, field_name, expression]):
                        send_response(msg_id, error={"code": -32602, "message": "table, field_name, expression required"})
                        continue
                    resp = arcpy_calculate_field(table, field_name, expression, where_clause)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "get_spatial_reference":
                    dataset = args.get("dataset")
                    if not dataset:
                        send_response(msg_id, error={"code": -32602, "message": "dataset required"})
                        continue
                    resp = arcpy_get_spatial_reference(dataset)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "create_feature_class":
                    workspace = args.get("workspace")
                    name_arg = args.get("name")
                    geometry_type = args.get("geometry_type")
                    spatial_reference = args.get("spatial_reference")
                    if not all([workspace, name_arg, geometry_type]):
                        send_response(msg_id, error={"code": -32602, "message": "workspace, name, geometry_type required"})
                        continue
                    resp = arcpy_create_feature_class(workspace, name_arg, geometry_type, spatial_reference)
                    handle_tool_response(msg_id, resp)
                    continue
                
                if name == "get_field_info":
                    dataset = args.get("dataset")
                    if not dataset:
                        send_response(msg_id, error={"code": -32602, "message": "dataset required"})
                        continue
                    resp = arcpy_get_field_info(dataset)
                    handle_tool_response(msg_id, resp)
                    continue
            
                send_response(msg_id, error={"code": -32601, "message": f"unknown tool: {name}"})
                continue
            
            except Exception as e:
                # Catch any errors during tool execution
                sys.stderr.write(f"[server] Tool execution error: {e}\n")
                sys.stderr.write(traceback.format_exc() + "\n")
                sys.stderr.flush()
                send_response(msg_id, error={"code": -32603, "message": f"Internal error: {str(e)}"})
                continue
        
        # Unknown method
        send_response(msg_id, error={"code": -32601, "message": f"unknown method: {method}"})

def print_debug_info():
    import platform
    sys.stderr.write("[MCP Python Server Debug Info]" + "\n")
    sys.stderr.write(f"Python: {platform.python_version()} | Executable: {sys.executable}\n")
    sys.stderr.write(f"ARCPY_AVAILABLE: {ARCPY_AVAILABLE}\n")
    if ARCPY_AVAILABLE:
        sys.stderr.write(f"arcpy env.workspace: {getattr(arcpy.env, 'workspace', None)}\n")
    # List all tools
    tool_count = 17  # Update if you add more tools
    sys.stderr.write(f"Registered tools: {tool_count}\n")
    sys.stderr.flush()


if __name__ == "__main__":
    print_debug_info()
    # Restore real stdout for protocol loop only
    sys.stdout = _real_stdout
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # Always output a valid JSON-RPC error to stdout
        try:
            error_response = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": str(e),
                    "data": {"traceback": traceback.format_exc()}
                },
                "id": None
            }
            sys.stdout.write(json.dumps(error_response) + "\n")
            sys.stdout.flush()
        except Exception:
            # If even this fails, write to stderr
            sys.stderr.write("[fatal] Could not write JSON error to stdout.\n")
            sys.stderr.write(traceback.format_exc() + "\n")

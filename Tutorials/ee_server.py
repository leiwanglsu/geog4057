"""
Earth Engine MCP Server (JSON-RPC 2.0 over stdio)

- Only JSON responses on stdout. All debug/info goes to stderr.
- Provides tools under MCP methods: initialize, tools/list, tools/call
- First tool implemented: ee_initialize (authenticate & initialize Earth Engine)

Usage expectations:
- Run with unbuffered I/O: python -u ee_server.py
- Provide credentials via one of:
  1) method="adc" -> Application Default Credentials (GOOGLE_APPLICATION_CREDENTIALS set, or gcloud login)
  2) method="service_account" with service_account_email and either key_file_path OR key_json
  3) method omitted -> try ee.Initialize() and let EE locate credentials

Result format (MCP):
- Successful tool calls must return: { "content": [ { "type": "text", "text": "..." } ] }
"""

import io
import json
import os
import sys
import tempfile
import traceback
from typing import Any, Dict, List, Tuple
import time
import urllib.request

# --- Global stdout guard to prevent non-JSON on stdout ---
class StdoutGuard(io.TextIOBase):
    def write(self, s):
        sys.stderr.write("[stdout-guarded] " + str(s))
        sys.stderr.flush()
        return len(s)
    def flush(self):
        sys.stderr.flush()

_real_stdout = sys.stdout
sys.stdout = StdoutGuard()

# Try to import Earth Engine
try:
    import ee  # type: ignore
    EE_AVAILABLE = True
except Exception as e:
    EE_AVAILABLE = False
    ee = None  # type: ignore
    sys.stderr.write(f"[ee] Import error: {e}\n")
    sys.stderr.flush()


def send_response(msg_id: Any, result: Any = None, error: Dict[str, Any] | None = None):
    """Send a JSON-RPC 2.0 response to stdout (line-delimited)."""
    if error is not None:
        response = {"jsonrpc": "2.0", "error": error, "id": msg_id}
    else:
        response = {"jsonrpc": "2.0", "result": result, "id": msg_id}
    _real_stdout.write(json.dumps(response) + "\n")
    _real_stdout.flush()


def mcp_result_text(text: str) -> Dict[str, Any]:
    return {"content": [{"type": "text", "text": text}]}


# --- Public EE catalog search (GitHub dataset list) ---
CATALOG_URL = (
    "https://raw.githubusercontent.com/samapriya/Earth-Engine-Datasets-List/master/gee_catalog.json"
)
_CATALOG_CACHE: Tuple[float, Any] | None = None  # (timestamp, data)


def _fetch_catalog(force_refresh: bool = False, cache_ttl: int = 3600) -> Any:
    """Fetch and cache the public EE catalog JSON.

    Returns parsed JSON (list or dict depending on upstream format).
    """
    global _CATALOG_CACHE
    now = time.time()
    if (not force_refresh) and _CATALOG_CACHE is not None:
        ts, data = _CATALOG_CACHE
        if now - ts < cache_ttl:
            return data
    # Fetch from network
    sys.stderr.write(f"[ee] Fetching catalog: {CATALOG_URL}\n")
    sys.stderr.flush()
    with urllib.request.urlopen(CATALOG_URL, timeout=15) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    data = json.loads(raw)
    _CATALOG_CACHE = (now, data)
    return data


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    if isinstance(value, list):
        return ", ".join(_stringify(v) for v in value)
    if isinstance(value, dict):
        # flatten one level
        return "; ".join(f"{k}: {_stringify(v)}" for k, v in value.items())
    return str(value)


def tool_ee_search_catalog(params: Dict[str, Any]) -> Dict[str, Any]:
    """Search public Earth Engine assets from the community catalog.

    Params:
    - query (str, required): search term (substring match)
    - fields (list[str], optional): restrict search to these fields
    - case_sensitive (bool, optional): default False
    - limit (int, optional): default 20
    - force_refresh (bool, optional): bypass cache
    """
    query = params.get("query")
    if not query:
        return {"ok": False, "error": "query is required"}
    fields: List[str] | None = params.get("fields")
    case_sensitive = bool(params.get("case_sensitive", False))
    force_refresh = bool(params.get("force_refresh", False))
    try:
        limit = int(params.get("limit", 20))
    except Exception:
        limit = 20

    try:
        catalog = _fetch_catalog(force_refresh=force_refresh)
    except Exception as e:
        sys.stderr.write("[ee] Catalog fetch error:\n" + traceback.format_exc() + "\n")
        sys.stderr.flush()
        return {"ok": False, "error": f"failed to fetch catalog: {e}"}

    # The catalog may be a list of dicts or dict with items
    items: List[Dict[str, Any]]
    if isinstance(catalog, list):
        items = [x for x in catalog if isinstance(x, dict)]
    elif isinstance(catalog, dict):
        # try common container keys
        if "data" in catalog and isinstance(catalog["data"], list):
            items = [x for x in catalog["data"] if isinstance(x, dict)]
        else:
            items = [v for v in catalog.values() if isinstance(v, dict)]
    else:
        return {"ok": False, "error": "unexpected catalog format"}

    q = query if case_sensitive else query.lower()
    results: List[Dict[str, Any]] = []
    for rec in items:
        # pick fields to search
        to_scan = fields if fields else list(rec.keys())
        haystack_parts: List[str] = []
        matched_fields: List[str] = []
        for f in to_scan:
            if f in rec:
                s = _stringify(rec.get(f))
                if not case_sensitive:
                    s_cmp = s.lower()
                else:
                    s_cmp = s
                if q in s_cmp:
                    matched_fields.append(f)
                haystack_parts.append(s)
        if matched_fields:
            # Build a compact summary
            summary = {
                k: rec.get(k)
                for k in ["id", "uid", "name", "title", "type", "provider", "snippet", "tags"]
                if k in rec
            }
            summary["matched_fields"] = matched_fields
            results.append(summary)
            if len(results) >= limit:
                break

    out = {
        "query": query,
        "count": len(results),
        "source": CATALOG_URL,
        "results": results,
    }
    return {"ok": True, "data": out}


def _parse_bbox(bbox_param: Any) -> Tuple[float, float, float, float]:
    """Parse bbox from list [west, south, east, north] or dict with keys.

    Returns (west, south, east, north) in EPSG:4326.
    """
    if isinstance(bbox_param, (list, tuple)) and len(bbox_param) == 4:
        west, south, east, north = bbox_param
        return float(west), float(south), float(east), float(north)
    if isinstance(bbox_param, dict):
        keys = {k.lower(): v for k, v in bbox_param.items()}
        return (
            float(keys.get("west")),
            float(keys.get("south")),
            float(keys.get("east")),
            float(keys.get("north")),
        )
    raise ValueError("bbox must be [west, south, east, north] or {west,south,east,north}")


def tool_ee_extract_image(params: Dict[str, Any]) -> Dict[str, Any]:
    """Download an Earth Engine Image asset clipped to a rectangle.

    Required params:
    - asset_id: EE Image asset id (e.g., 'COPERNICUS/S2/20210101T...')
                For ImageCollections, use collection_mode='first' or 'mosaic'
    - bbox: [west, south, east, north] in EPSG:4326 or dict with keys
    - workspace: local folder to save the file

    Optional params:
    - file_name: output file name (without extension). Default derived from asset_id
    - collection_mode: if asset is ImageCollection: 'first' (default), 'mosaic', or 'mean'
    - crs: output projection (default 'EPSG:4326')
    - scale: pixel size in meters (default 30)
    - file_per_band: bool (default False)
    - max_pixels: int (default 1_000_000_000)
    - overwrite: bool (default True)
    - format: 'GEO_TIFF' or 'GeoTIFF' (default 'GEO_TIFF')
    """
    if not EE_AVAILABLE:
        return {"ok": False, "error": "earthengine-api (ee) not available. Install and run ee_initialize first."}

    asset_id = params.get("asset_id")
    if not asset_id:
        return {"ok": False, "error": "asset_id is required"}
    workspace = params.get("workspace")
    if not workspace:
        return {"ok": False, "error": "workspace is required"}

    try:
        west, south, east, north = _parse_bbox(params.get("bbox"))
    except Exception as e:
        return {"ok": False, "error": f"invalid bbox: {e}"}

    file_name = params.get("file_name")
    collection_mode = params.get("collection_mode", "first")
    crs = params.get("crs", "EPSG:4326")
    scale = params.get("scale", 30)
    try:
        scale = float(scale)
    except Exception:
        scale = 30.0
    file_per_band = bool(params.get("file_per_band", False))
    max_pixels = int(params.get("max_pixels", 1_000_000_000))
    overwrite = bool(params.get("overwrite", True))
    fmt = params.get("format", "GEO_TIFF")

    # Load the asset: if collection_mode is specified, treat as ImageCollection
    # Otherwise try Image first, then fallback to ImageCollection
    image = None
    if collection_mode and collection_mode != "none":
        # User explicitly wants ImageCollection handling
        try:
            collection = ee.ImageCollection(asset_id)  # type: ignore[name-defined]
            if collection_mode == "mosaic":
                image = collection.mosaic()  # type: ignore[attr-defined]
            elif collection_mode == "mean":
                image = collection.mean()  # type: ignore[attr-defined]
            else:  # default: first
                image = collection.first()  # type: ignore[attr-defined]
            sys.stderr.write(f"[ee] Loaded as ImageCollection, using mode: {collection_mode}\n")
            sys.stderr.flush()
        except Exception as coll_error:
            return {"ok": False, "error": f"failed to load asset as ImageCollection with mode={collection_mode}: {coll_error}"}
    else:
        # Try as single Image
        try:
            image = ee.Image(asset_id)  # type: ignore[name-defined]
            sys.stderr.write(f"[ee] Loaded as Image\n")
            sys.stderr.flush()
        except Exception as img_error:
            # Fallback: try as ImageCollection with first()
            try:
                collection = ee.ImageCollection(asset_id)  # type: ignore[name-defined]
                image = collection.first()  # type: ignore[attr-defined]
                sys.stderr.write(f"[ee] Loaded as ImageCollection, using first image\n")
                sys.stderr.flush()
            except Exception as coll_error:
                return {"ok": False, "error": f"failed to load asset as Image or ImageCollection. Image error: {img_error}. Collection error: {coll_error}"}

    try:
        region = ee.Geometry.Rectangle([west, south, east, north])  # type: ignore[name-defined]
        url = image.getDownloadURL({  # type: ignore[attr-defined]
            "region": region,
            "scale": scale,
            "crs": crs,
            "format": fmt,
            "filePerBand": file_per_band,
            "maxPixels": max_pixels,
        })
    except Exception as e:
        sys.stderr.write("[ee] getDownloadURL error:\n" + traceback.format_exc() + "\n")
        sys.stderr.flush()
        return {"ok": False, "error": f"failed to create download URL: {e}"}

    # Prepare output path
    try:
        os.makedirs(workspace, exist_ok=True)
        base = file_name or asset_id.replace("/", "_").replace(":", "_")
        # decide extension
        ext = ".zip" if file_per_band else ".tif"
        out_path = os.path.join(workspace, base + ext)
        if os.path.exists(out_path) and not overwrite:
            return {"ok": True, "data": {"path": out_path, "url": url, "skipped": True}}
    except Exception as e:
        return {"ok": False, "error": f"failed to prepare output path: {e}"}

    # Download
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=120) as resp, open(out_path, "wb") as f:
            chunk = resp.read(8192)
            total = 0
            while chunk:
                f.write(chunk)
                total += len(chunk)
                chunk = resp.read(8192)
    except Exception as e:
        sys.stderr.write("[ee] download error:\n" + traceback.format_exc() + "\n")
        sys.stderr.flush()
        return {"ok": False, "error": f"download failed: {e}", "data": {"url": url}}

    return {
        "ok": True,
        "data": {
            "path": out_path,
            "bytes": os.path.getsize(out_path) if os.path.exists(out_path) else None,
            "url": url,
            "asset_id": asset_id,
            "bbox": [west, south, east, north],
            "crs": crs,
            "scale": scale,
        },
    }


def tool_ee_initialize(params: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize the Earth Engine client.
    try:
        ee.Initialize(f"project={params['project']}")
        return {"ok": True, "data": {"initialized": True, "method": method or "default", "project": project}}
    except Exception as e:
        sys.stderr.write("[ee] Initialize error:\n" + traceback.format_exc() + "\n")
        sys.stderr.flush()
        return {"ok": False, "error": str(e)}
    Params:
    - method: "adc" | "service_account" | (optional)
    - service_account_email: string (for service_account)
    - key_file_path: path to service account key JSON file (optional)
    - key_json: JSON string of service account key (optional, alternative to file)
    - project: optional GCP project id
    """
    if not EE_AVAILABLE:
        return {"ok": False, "error": "earthengine-api (ee) not available. Install earthengine-api and retry."}

    method = params.get("method")
    service_account_email = params.get("service_account_email")
    key_file_path = params.get("key_file_path")
    key_json = params.get("key_json")
    project = params.get("project")

    try:
        creds = None
        temp_file = None

        if method == "service_account":
            if not service_account_email:
                return {"ok": False, "error": "service_account_email is required for method=service_account"}
            if key_file_path:
                creds = ee.ServiceAccountCredentials(service_account_email, key_file_path)
            elif key_json:
                # Write JSON to temp file for ee.ServiceAccountCredentials
                fd, tpath = tempfile.mkstemp(prefix="ee-key-", suffix=".json")
                os.close(fd)
                with open(tpath, "w", encoding="utf-8") as f:
                    f.write(key_json)
                temp_file = tpath
                creds = ee.ServiceAccountCredentials(service_account_email, temp_file)
            else:
                return {"ok": False, "error": "Provide key_file_path or key_json for service_account auth"}

            if project:
                ee.Initialize(credentials=creds, project=project)
            else:
                ee.Initialize(credentials=creds)
        elif method == "adc":
            # Application Default Credentials (env var GOOGLE_APPLICATION_CREDENTIALS or gcloud)
            if project:
                ee.Initialize(project=project)
            else:
                ee.Initialize()
        else:
            # Try default EE initialization
            if project:
                ee.Initialize(project=project)
            else:
                ee.Initialize()

        # Cleanup temp file if used
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass

        # Optional: Avoid network calls here; just report success
        return {"ok": True, "data": {"initialized": True, "method": method or "default", "project": project}}
    except Exception as e:
        sys.stderr.write("[ee] Initialize error:\n" + traceback.format_exc() + "\n")
        sys.stderr.flush()
        return {"ok": False, "error": str(e)}


# --- Main JSON-RPC loop ---

def main():
    sys.stdout = _real_stdout  # allow protocol writes
    sys.stderr.write("[ee] Earth Engine MCP server starting...\n")
    sys.stderr.write(f"[ee] EE_AVAILABLE={EE_AVAILABLE}\n")
    sys.stderr.flush()

    while True:
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        try:
            msg = json.loads(line)
        except Exception as e:
            send_response(None, error={"code": -32700, "message": f"Parse error: {e}"})
            continue

        msg_id = msg.get("id")
        method = msg.get("method")
        params = msg.get("params", {})

        # initialize handshake
        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "earthengine-mcp", "version": "0.1"},
                "capabilities": {"tools": {}}
            }
            send_response(msg_id, result=result)
            continue

        # list tools
        if method == "tools/list":
            tools = [
                {
                    "name": "ee_initialize",
                    "description": "Initialize Google Earth Engine client",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "method": {"type": "string", "enum": ["adc", "service_account"]},
                            "service_account_email": {"type": "string"},
                            "key_file_path": {"type": "string"},
                            "key_json": {"type": "string"},
                            "project": {"type": "string"}
                        }
                    }
                },
                {
                    "name": "ee_search_catalog",
                    "description": "Search the public Earth Engine dataset catalog (community-maintained)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "fields": {"type": "array", "items": {"type": "string"}},
                            "case_sensitive": {"type": "boolean"},
                            "limit": {"type": "integer"},
                            "force_refresh": {"type": "boolean"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "ee_extract_image",
                    "description": "Download an EE image subset by asset_id and rectangle to a local workspace (GeoTIFF). Supports both Image and ImageCollection assets.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "asset_id": {"type": "string"},
                            "bbox": {
                                "oneOf": [
                                    {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4},
                                    {"type": "object", "properties": {
                                        "west": {"type": "number"},
                                        "south": {"type": "number"},
                                        "east": {"type": "number"},
                                        "north": {"type": "number"}
                                    }}
                                ]
                            },
                            "workspace": {"type": "string"},
                            "file_name": {"type": "string"},
                            "collection_mode": {"type": "string", "enum": ["first", "mosaic", "mean"]},
                            "crs": {"type": "string"},
                            "scale": {"type": "number"},
                            "file_per_band": {"type": "boolean"},
                            "max_pixels": {"type": "integer"},
                            "overwrite": {"type": "boolean"},
                            "format": {"type": "string"}
                        },
                        "required": ["asset_id", "bbox", "workspace"]
                    }
                }
            ]
            send_response(msg_id, result={"tools": tools})
            continue

        # call tools
        if method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})
            try:
                if name == "ee_initialize":
                    resp = tool_ee_initialize(arguments)
                    if resp.get("ok"):
                        data = resp.get("data", {})
                        send_response(msg_id, result=mcp_result_text(json.dumps(data)))
                    else:
                        send_response(msg_id, error={"code": -32000, "message": resp.get("error")})
                    continue

                if name == "ee_search_catalog":
                    resp = tool_ee_search_catalog(arguments)
                    if resp.get("ok"):
                        data = resp.get("data", {})
                        send_response(msg_id, result=mcp_result_text(json.dumps(data, indent=2)))
                    else:
                        send_response(msg_id, error={"code": -32000, "message": resp.get("error")})
                    continue

                if name == "ee_extract_image":
                    resp = tool_ee_extract_image(arguments)
                    if resp.get("ok"):
                        data = resp.get("data", {})
                        send_response(msg_id, result=mcp_result_text(json.dumps(data, indent=2)))
                    else:
                        send_response(msg_id, error={"code": -32000, "message": resp.get("error")})
                    continue

                send_response(msg_id, error={"code": -32601, "message": f"unknown tool: {name}"})
                continue
            except Exception as e:
                sys.stderr.write("[ee] tools/call error:\n" + traceback.format_exc() + "\n")
                sys.stderr.flush()
                send_response(msg_id, error={"code": -32603, "message": str(e)})
                continue

        # unknown method
        send_response(msg_id, error={"code": -32601, "message": f"unknown method: {method}"})


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        err = {"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": None}
        _real_stdout.write(json.dumps(err) + "\n")
        _real_stdout.flush()

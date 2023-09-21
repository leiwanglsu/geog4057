# Geoprocessing with ArcPy

## Introduction

- ArcPy was introduced in version 10 of ArcGIS Desktop (ArcMap)
- ArcPy is a *package* including many modules. 
- Prior to ArcPy, the major scripting package is "arcgisscripting". (Still supported, but not recommended)
- To use ArcPy, simply use ```import arcpy```

## importing arcpy

- Check the environment if there is a package called arcpy
- You can use conda list to find arcpy in the package list
- To add the environment of arcgispro-py3 to anaconda environment list


```python
conda config --append envs_dirs "C:\Program Files\ArcGIS\Pro\bin\Python\envs"
```

- To clone the environment


```conda
conda create --name arcpy_clone --clone "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"
```

- import error will occur if there is no arcpy available:

```message
ImportError: No module named arcpy
```

- arcpy always needs a valid ArcGIS Pro license. If not, the error message will show:

```message
RuntimeError: NotInitialized

```

- If ArcPy is installed and licensed, any external IDLE can use it, for example, in VS Code

## ArcPy modules

- In ArcPy, functionality is organized into modules
>Charts module (arcpy.charts)
Data Access module (arcpy.da)
Geocoding module (arcpy.geocoding)
Image Analysis module (arcpy.ia)
Mapping module (arcpy.mp)
Metadata module (arcpy.metadata)
Network Analyst modules (arcpy.nax and arcpy.na)
Sharing module (arcpy.sharing)
Spatial Analyst module (arcpy.sa)
Workflow Manager (Classic) module (arcpy.wmx)

## Setting up a workspace

- A *workspace* is a default location for files you work with in the python session. 
- Inputs and outputs of geoprocessing tools use the workspace for file access
- To set the current workspace to <q>c:\data </q>

```python
import arcpy
arcpy.env.workspace = "c:/data"

```

- Note that use the forward slash / in the path name
- If you really want to use backslash, use double backslashes. Or use the raw string operator: <q> r"c:\data"</q>
- To check the current workspace name, use print(arcpy.env.workspace)

#ArcPy

# Clone the ArcGIS Pro Python environment and install Google Earth Engine

## Install Anaconda

- Anaconda website and download the free version: https://www.anaconda.com/download
- Install to your computer by following the instruction
- Read the cheating sheet about Anaconda: https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf

## Clone the ArcGIS Pro environment
In Anaconda prompt, type the followiing command
```
conda create --name arcpy_clone --clone "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"
```
## Install Google Earth Engine and do Authentication

In Anaconda prompt, type the following command

```
conda activate arcpy_clone
pip install earthengine-api --upgrade
```

- Authenticate:
type: python and in the python interpreter, use the following command

```python
import ee
ee.Authenticate()
ee.Initialize()
print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())
```

## Activate the python environment in ArcGIS Pro

- In ArcGIS Pro, click Project
- Click Package manager
- Click Active Environment ->Environment Manager
- Click Add Existing Envionment
- Find the where arcpy_clone is located (by using conda env list)
- Click the Activate option on the newly added environment arcpy_clone
- Restart ArcGIS Pro
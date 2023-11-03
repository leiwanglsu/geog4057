# ArcGIS API for Python

## Introduction

- The ArcGIS API for Python is a Python package for working directly with web GIS independent of ArcGIS Pro
- Functions include creating maps, geocoding, vector and raster analysis, and managing data
- In addition, the ArcGIS API for Python provides tools to manage the organization of web GIS, such as managing users, groups, and items
- To work effectively with web GIS, you need an IDE that has built-in tools for visualization. This is where Jupyter Notebook comes in

## What is ArcGIS API for Python

- The ArcGIS API for Python is implemented using the ArcGIS REST API powered by ArcGIS Online and ArcGIS Enterprise.
- he ArcGIS API for Python is not only a Python package but also an application programming interface (API)
- Representational state transfer (REST) is a style that organizes a site in a way that allows users to read URLs.
- The ArcGIS API for Python can be considered a pythonic wrapper around the ArcGIS Rest API, and both APIs work together as the interface between Python code and the web GIS portal

## Installation of ArcGIS API for Python

- The ArcGIS API for Python is distributed as a Python package called arcgis. 
- The arcgis package is installed as part of the arcgispro-py3 default environment of ArcGIS Pro, which makes it easy to get started using the API.
- In older versions of ArcGIS Pro, you were required to install the arcgis package using either the Python Package Manager or conda using command prompt
- The API is platform agnostic, which means you can install it on Windows, Linux, or macOS operating systems
- To take full advantage of the API, however, it is beneficial to have Esri user credentials.

## Using arcgis

- To start using arcgis
```python
import arcgis
```
- The following code print the arcgis version
```python
import arcgis
import sys
print("Python version: ", + sys.version)
print("arcgis API version:" + arcgis.__version__)
```

### the GIS class

- The GIS class is the main class in the arcgis module
- you can import it by ```from arcgis import GIS```
- Create an object from GIS: ```mygis = GIS()```
- The syntax is

```python
class arcgis.gis.GIS(url=None, username=None, password=None, 
                     key_file=None, cert_file=None, 
                     verify_cert=True, set_active=True, 
                     client_id=None, profile=None, **kwargs)
```

- The **kwargs stands for keyworded or named arguments. The double * means the argument can have variable length of inputs. If multiple arguments are supplied, they will be passed to the functions as a  dictionary with the argument name as the key and the supplied values as values
- Another variable length argument is *args.
  
```python
def myFun(*argv):
    for arg in argv:
        print(arg)
 
 
myFun('Hello', 'Welcome', 'to', 'GeeksforGeeks')
```

### Credentials

- The GIS class have several optional arguments: URL, user name, and password
- If the optional arguments are used, you are using an anoymous login to ArcGIS Online
- Without credential, you have limited access to the ArcGIS Online resources
- Alternative ways to authenticate your user credentials are provided
- One useful alternative is the connect using pro authentication, with ArcGIS Pro installed locally and running concurrently

```python
from arcgis.gis import GIS
mygis = GIS("pro")
```

### Start with a map

- You can view a map in the Jupter Notebook by 

```python
from arcgis.gis import GIS
mygis = GIS("pro")
mymap = mygis.map("Baton Rouge")
mymap
```

- To change the basemap

```mymap.basemap = "gray-vector```


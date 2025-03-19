# Working with Rasters

- ArcPy includes two modules arcpy.sa and arcpy.ia to work with raster and imagery data
- Modules in ArcPy for raster analyasis and image processing: arcpy.ia and arcpy.sa

`from arcpy.sa import *`
`from arcpy.ia import *`


## Raster data structure

- Raster cells or pixels are the basic units of raster data
- Each cell represents a certail portion of the earth with a value
- The size of the area occupied by a cell is called cell size, usually represented by the length of the cell edge. Sometime is also referred to as spatial resolution
- The storate of a raster is a 2D array in the computer
- Some raster datasets contain more than one 2D arrays, and each is called a raster band
- Raster dataset with only one band is called a single-band raster; otherwise, it is a multiband raster

### Raster and imagery

- The terms imagery and raster are often used interchangeably, but they are not identical.
  - An image is a two-dimensional pictorial representation
  - A raster is a the data model in GIS to store information in the form of cells
  - In GIS, imagery is stored as raster datasets: a raster spatial data model in a geodatabase
  
### Raster bands

- A raster band is a one layer in a raster dataset
- An image may have more than one bands - called a multi-band raster
- A DEM is a single-band raster

### Raster cell size

- THe distance on the ground of which a raster cell occupies
- The cell size of a raster is also referred to as the raster *spatial resolution*
- A small cell size means a higher spatial resolution

### Raster types

- Continues raster - for phenomena such as elevation or rainfall - values of the cells changes continuously without boundaries
- Discrete raster - for phenomena of categorical values such as land cover types, vegetation types, or soil types

### Pixel bit depth and types

- Raster pixels can be in integer or float point numbers
- Integers of different depths represent different value ranges: for example, a 8-bit integer only represents 256 numbers.
  - Signed or unsigned: An unsigned integer represents the positive values, while a signed integer can represent both negative or positive values
  - The first digit of the binary representation of a signed integer is used as the sign.
  - An unsigned 8-bit integer (Byte) represents numbers from 0 ~ 255
  - A signed 8-bit integer represents numbers from -128 ~ 127
- The following is a table of ArcGIS raster data bit depth
  
| Bit depth             | Range of values that each cell can contain |
|-----------------------|--------------------------------------------|
| 1 bit                 | 0 to 1                                     |
| 2 bit                 | 0 to 3                                     |
| 4 bit                 | 0 to 15                                    |
| Unsigned 8 bit        | 0 to 255                                   |
| Signed 8 bit          | -128 to 127                                |
| Unsigned 16 bit       | 0 to 65535                                 |
| Signed 16 bit         | -32768 to 32767                            |
| Unsigned 32 bit       | 0 to 4294967295                            |
| Signed 32 bit         | -2147483648 to 2147483647                  |
| Floating-point 32 bit | -3.402823466e+38 to 3.402823466e+38        |
| Unsigned 64 bit       | 0 to 18446744073709551616                  |

### getRasterInfo() 

- getRasterInfo() will return a RasterInfo object
- The RasterInfo object contains functions to get and set raster properties
- For example getPixelType and setPixelType will get access to the pixel type property of the raster
- Use getRasterInfo to create an empty raster copied from an input raster

```python
r_information = raster.getRasterInfo()
print(dir(r_information))
newRaster = Raster(r_information)
```

### Render the raster in the Jupter notebook

- Render() function
- Render (elev, colormap="Elevation #1")

### Raster data formats

- Raster datasets can be stored in several formats, including TIFF (.tf), Imagine image (.img), JPEG (.jpg), or in a geodatabase (geodatabase raster)
- A mosaic dataset is a collection of raster datasets stored in a geodatabase to manage a large extent of raster datasets

## ArcPy modules to work with raster datasets

- In Data Management Toolbox, a Raster toolset provides geoprocessing tools for raster data, including Mosaicking, Raster processing, and Raster properties
- In 3D Analyst Toolbox, a Raster toolset provides geoprocessing tools for functions related to DEM and 3D analysis
- The Spatial Analyst and Image Analyst extensions of ArcGIS Pro by the arcp.sa and arcpy.ia modules
- Raster datasets can also be converted to Numpy array for additional analysis functionality

### Working with the arcpy.sa module

- To use the sa module, you can import all functions from it by ```from arcpy.sa import * ```
- For example, the following code uses the slope function

```python
import arcpy
from arcpy.sa import *
elev = arcpy.Raster("C:/Raster/elevation")
outraster = Slope(elev)

```

- Like other extensions, Spatial Analyst and Image Analyst extensions require a license. If the license is not checked, you code might fail and stops working
- Use the CheckExtension function to make sure the license is valid on the target machine

```python
import arcpy
arcpy.env.workspace = "C:/Raster"
if arcpy.CheckExtension("Spatial") == "Available":
    print("Spatial Analyst license is available.")
    <map algebra or geoprocessing tools>
    print("Processing complete.")
else:
    print("Spatial Analyst license is unavailable.")

```

- Some functions are both available in arcpy.ia or arcpy.sa, and therefore you can use either license for those functions depending their availability

### Raster objects

- The Raster class in ArcPy defines properties and behaviors of raster datasets
- A raster object can be created in three ways
  - Referencing an existing raster in the workspace
  - Output from a geoprocessing tool
  - Map algebra

- To reference to a raster dataset in the workpace:

```python
Raster(inRaster, {is_multidimensional})
```

- A multidimensional raster is for multidimenional datasets such as netCDF and HDF
- Raster objects have many properties including ```bandCount, compressionType, format, height, width, pixelType, noDataValue, spatialReference, etc.```
- These properties can also be obtained by da.Describe() function

```python
import arcpy
from arcpy.sa import *
arcpy.env.workspace = "C:/Raster/Study.gdb"
ras = Raster("elevation")
print(ras.catalogPath)
print(ras.compressionType)
print(ras.format)
print(ras.pixelType)
print(ras.spatialReference.name)
```

- Raster objects have a function save(), which saves the raster to your workspace permanently

```python
import arcpy
from arcpy.sa import *
arcpy.env.workspace = "C:/Raster"
outraster = Slope("elevation")
outraster.save("slope")
```

### Use da.Describe() for raster datasets

- Like other GIS datasets, raster datasets can be understood by the da.Describe() function
- The function returns a Describe object, which stores inforamtion as a dictionary with keys correspond to properties
- The keys from the Describe() function are:
  - bandCount—the number of bands in the raster dataset
  - compressionType—the compression type (LZ77, JPEG, JPEG2000, or None), where compression reduces the size of the file on disk
  - format—the raster format (GRID, IMAGINE, TIFF, and more)
  - permanent—indicates the permanent state of the raster: False if the raster is  temporary, True if the raster is permanent
  - sensorType–the sensor type used to capture the image

```python
import arcpy
from arcpy import env
env.workspace = "C:/Raster"
raster = "landcover.tif"
desc = arcpy.da.Describe(raster)
print(desc["dataType"])
print(desc["bandCount"])
print(desc["compressionType"])
```

### Properties of single-band rasters

- The spatial resolution of a raster datasets can vary by bands
- Some properties are specific to raster bands:
- height and width, isInteger, noDataValue, pixelType, meanCellHeight, etc.
- The following code generates an error because the meanCellHeight is only for single bands, not the entire raster

```python
import arcpy
from arcpy import env
#env.workspace = "C:/Raster"
raster = arcpy.Raster("tm_24sep98")
print(raster.catalogPath)
desc = arcpy.da.Describe(raster)
print(desc["meanCellHeight"])
```

- To get an individual band's information from the Describe dictionary, use "children"

```python
import arcpy
from arcpy import env
#env.workspace = "C:/Raster"
raster = arcpy.Raster("tm_24sep98")
print(raster.catalogPath)
desc = arcpy.da.Describe(raster)
print(desc["children"][0]["meanCellHeight"])
for rband in desc["children"]:
    print(rband["name"])
```

### Multi-band rasters

- To determine the number of bands, use "bandCount"
- Individual bands can be access by their band names (Band_#) from the raster dataset

```python
import arcpy
from arcpy import env
rastername ="tm_24sep98"
bandcount = rdesc["bandCount"]
if bandcount == 1:
    print("Raster name: " + str(rdesc["baseName"]))
    print("No. rows: " + str(rdesc["height"]))
    print("No. columns: " + str(rdesc["width"]))
if bandcount > 1:
    counter = 1
    while counter <= bandcount:
        bandname = "Band_" + str(counter)
        band = arcpy.Raster(rastername + "/" + bandname)
        print(bandname)
        print("pixelType: " + band.pixelType)
        print("Height: " + str(band.height))
        print("Width: " + str(band.width))
        print("NoData Value: " + str(band.noDataValue))
        print("Spatial Reference: " + band.spatialReference.name)
        counter += 1
```

### Multidimensional Raster

- Contains spatial, temporal, and vertical dimensions
- Contains one or multiple variables in one file
  - One variable is a cube
  - Has atime and/or depth
  - Each slice is a 2D array

### Raster management in ArcGIS

- Raster dataset: presents a single dataset 
- Mosaic dataset
  - Dynamic mosaic of imagery collection
  - Table of records
  - A raster Dataset
  - Lives in Geodatabase 

### List rasters

- Previously, we learned the List functions in ArcPy, which includes ListRasters()
- ListRasters() returns the raster names in a list in the workspace
- The syntax is ```ListRasters({wild_card}, {raster_type})```
- These two optional arguments help filter out unwanted rasters to be listed
- Specifically, the {raster_type} can be "IMG", "TIF", "JPG", "GRID", etc.
- "GRID" means the ArcGIS Grid format
- The following code list all rasters with the type "IMG" or imagine image 

```python
import arcpy
arcpy.env.workspace = "C:/Raster"
rasterlist = arcpy.ListRasters("*", "IMG")
for raster in rasterlist:
    print(raster)
```

- The following script prints the name and format of each raster object

```python
import arcpy
arcpy.env.workspace = "C:/Raster"
rasterlist = arcpy.ListRasters()
for raster in rasterlist:
    myras = arcpy.Raster(raster)
    print(myras.name)
    print(myras.format)
```

### The Raster class

- The Raster class is used for certain type of analysis to access the raster bands
- By iterating over the bands, each band can create a Raster object

```python
import arcpy
arcpy.env.workspace = "C:/Raster"
landsat = "tm.img"
desc = arcpy.da.Describe(landsat)
for rband in desc["children"]:
    name = rband["name"]
    ras = arcpy.Raster("tm.img" + "/" + name)
    print(ras.catalogPath)
```

## Raster analysis using arcpy.sa and arcpy.ia classes

- The sa module contains some classes to define parameters of raster tools
- For example, the Reclassify tool uses a parameter defined by the Remap class

```python
Reclassify(in_raster, reclass_field, remap, {missing_values})
```

- To create a Remap object, you can use the table defined by a Python list of lists, with each list containing two elements

```python
import arcpy
from arcpy.sa import *
arcpy.env.workspace = "C:/Raster"
myremap = RemapValue([["Brush/transitional", 2],
                      ["Water", 0], ["Barren land", 1],
                      ["Built up", 1], ["Agriculture", 3],
                      ["Forest", 5], ["Wetlands", 4]])
outreclass = Reclassify("landuse", "LANDUSE", myremap)
outreclass.save("lu_reclass")
```

#### Slope

- The Slope() function does not require an output as in the syntax ```Slope(in_raster, {output_measurement}, {z_factor}, {method}, {z_unit})```
- The following code runs a Slope() function in arcpy.sa

```python
import arcpy
from arcpy.sa import *
elev = arcpy.Raster("topo30m")
outraster = Slope(elev)
``` 

- In the geoprocessing tool Slope, however, the output raster is a required argument.
- Unless the raster is explicitly saved by calling the save() function, the raster generated from the python function Slope() is a temporary raster.

- The following script will clip the raster

```python
from arcpy.sa import *
from arcpy.ia import *
elev_clip = Clip(elev, "bh_wshds83")
elev_clip
```

#### Viewshed

- determines the locations visible to a set of observer locations

```python
import arcpy
from arcpy.sa import *
arcpy.env.workspace = "C:/Visibility"
dem = Raster("elevation")
obs = "summits.shp"
view = Viewshed(dem, obs)
view.save("view.tif")
```

#### Tabulate Area

- Not all raster tools create raster datasets as outputs.
- Tabulate Area tool, which creates a cross tabulation between two datasets and outputs the results as a table
- A typical application of this tool is to use a raster of elevation zones (e.g., low, medium, high) and land cover (water, grassland, forest, and so on) and determine the area of each land cover class in each elevation zone. 

```python
import arcpy
from arcpy.sa import *
arcpy.env.workspace = "C:/Raster/Study.gdb"
zones = Raster("elev_zones")
lc = Raster("landcover")
TabulateArea(zones, "VALUE", lc, "VALUE", "crosstab")
```

#### Map algebra operators

- The Math toolset in the geoprocessing toolboxes have python script in arcpy.sa and arcpy.ia to do map algebra
- The script below converts the vertical units from meters to feet using the Times() tool

```python
import arcpy
from arcpy.sa import *
inras = arcpy.Raster("topo30m")
outras = Times(inras, 3.28)
outras.save("elev_ft")
```

- You can actually use the multiplication operator (*) instead of Times()

```python
import arcpy
from arcpy.sa import *
inras = arcpy.Raster("topo30m")
outras = inras * 3.28
outras.save("elev_ft")
```

- Math operators including Arithmetic, Bitwise, Boolean, and Relational 
  - Arithmetic * / // + **
  - Bitwise >> <<
  - Boolean & | ^ ~
  - Relational < <= > >= == != 

```python
import arcpy
from arcpy.sa import *
elev = arcpy.Raster("topo30m")
goodelev = (elev < 1000) | (elev > 1500)
```

- Remember to put parentheses around the relational operators

#### Reclassify

- raster cells are given a new value on the basis of a remap table, also referred to as a “reclassification table.” 
- The remap table shows how each old value is mapped to a new value. 

```python
import arcpy
from arcpy.sa import *
arcpy.env.workspace = "C:/Raster"
myremap = RemapValue([["Brush/transitional", 2],
                      ["Water", 0], ["Barren land", 1],
                      ["Built up", 1], ["Agriculture", 3],
                      ["Forest", 5], ["Wetlands", 4]])
outreclass = Reclassify("landuse", "LANDUSE", myremap)
outreclass.save("lu_reclass")
```

#### Focal statistics

- Defines a neighborhood object and uses it in the FocalStatistics function
- FocalStatistics calculates the statistics in the neighborhood
  
```python
import arcpy
from arcpy.sa import *
arcpy.env.workspace = "C:/Raster"
mynbr = NbrRectangle(5, 5, "CELL")
outraster = FocalStatistics("landuse", mynbr, "VARIETY")
outraster.save("lu_var")
```


#### Using Raster Cell Iterator

- The arcpy.sa module includes the Raster Cell Iterator (RCI) to work with individual cells
- You can read and write individual cell values by referring to their locations in the raster using an indexing system

```python
from arcpy.sa import *
topo = Raster("topo30m")
print(topo[100,200])
```

- The first number refers to the row number and the second number refers to the column number
- You may use RCI to change the raster values by turn the readOnly property of the raster to False

```python
from arcpy.sa import *
slopecon = Raster("Con_slope")
slopecon.readOnly = False
for i, j in vegras:
    if slopecon[i, j] == 1:
        slopecon[i, j] = 2
slopecon.save()
```

### Using arcpy.ia and arcpy.sa functions

- Additional functions in the two modules provide functionalities for Raster
- In ArcGIS Pro, you can access these functions through Imagery->Raster Functions
- The functions may overlap with the tools defined in the system toolboxes, and some are unique functions such as "Wind Chill"
- The interface of the Raser Functions are similar to geoprocessing tools
- The major difference is that the output from a Raster Function is a new virtual raster layer (the Run button is replaced by "Create new layer" button)
- Raster functions are written in Python scripts located at your ArcGIS installation folder->Resources->Raster->Functions->System
- These Raster Functions do not import arcpy, and therefore will be dependent on other packages such as numpy

```python
# example of using Raster Functions
from arcpy.sa import *
arcpy.env.workspace = "C:/Raster"
t = "temperature.tif"
ws = "windspeed.tif"
chill = WindChill(t, ws)
chill.save("windchill.tif")
```

### Python Raster Function

- Python raster functions are not part of ArcPy or ArcGIS API for Python
- The functions are defined by Python classes implementing image processing and analysis algorithms
- ArcGIS invokes python code through built-in python runtime and a Python Adapter Function
- Can be combined with other built-in raster Functions to create Raster Function Template
- A Raster function template is like a model that contains one or more raster functions chained to produce a processing workflow
- You can build a raster function template using the Function Editor and the Raster Functions pane.
- Check out the ESRI's raster functions repository on Github: https://github.com/Esri/raster-functions/tree/master

#### Class defintion of a raster function

- The `__init__` function
  - Customize the function object
  - Define raster function name & descripton
- getParameterInfo()
  - Defines all input parameters to the function
  - Parameters are defined by
    - Name
    - Display Name
    - Data Type
    - Default Value
    - Required vs Optional
- getCOnfiguration()
  - How are input Rasters read - Padding, Mask, or others?
  - How is the output Raster constructed - NoData, Metadata, ...
- selectRaster()
  - Define a subset of input Rasters
  - Pixels read from selected Rasters
- updateRasterInfo()
  - Defines the output raster
  - returns the Raster Info of the output raster
- updatePixels()
  - Main operation of the function
  - Process Pixels of the input Rasters
  - returns Pixels+ mask of requested pixel blocks

#### An example of the Raster function class

```python
imoprt numpy as np
class HelloWorld():
  def __init__(self):
    self.name = "Hello World Function"
    self.description = "An example of raster functions"
  def getParameterInfo(self):
    return[{
      'name':'r',
      'dateType':'raster'
    }]
  def updatePixels(self,tlc,shape,props,**pixelBlocks):
    r = pixelBlocks['r_pixels'] + 10
    pixelBlocks['output_pixels'] = r.astype(props['pixelType'])
    return pixelBlocks
```

### Work with NumPy arrays

- NumPy, short for "Numerical Python," is a popular open-source Python library for performing numerical and mathematical operations.
- NumPy's primary data structure is the "ndarray" or n-dimensional array
- ArcPy provides two functions to interface with NumPy by NumPyArrayToRaster() and RasterToNumPyArray()

```python
import arcpy
import numpy
raster = "tm_24spe98/Band_1"
array = arcpy.RasterToNumPyArray(raster)
print(array.min())
print(array.max())
print(array.mean())
print(array.std())
```

- You can compare the direct properties of the raster with the numpy results:

```python
import arcpy
raster = Raster("tm_24spe98/Band_1")
print(raster.minimum)
print(raster.maximum)
print(raster.mean)
print(raster.standardDeviation)
```

- In fact, not only rasters, feature class attribute tables can also be converted to numpy using ```arcpy.da.FeatureClassToNumPyArray()```
- NumPy array can also be used to create feature classes ```arcpy.da.NumPyArrayToFeatureClass()```

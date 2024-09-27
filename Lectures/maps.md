# Working with maps and layouts

- This chapter will show how to work with map and layout components using python
- The main module is from ```arcpy.mp```
- The components are the projects (.aprx) and layers (.lyr)

## The arcpy.mp module

ArcPy mapping module are as follows:

- Finding a layer with a specific data source and replacing it with another data source
- Modifying the display properties of a specific layer in multiple maps
- Generating reports that describe the contents of projects, including maps, layers, tables, and layouts
- Searching for and replacing a text string in multiple layouts in a project

### Starting from the project file

- A project in ArcGIS is stored as a .aprx file
- Using arcpy.mp, you can access the aprx file and manipulate the components
- The syntax is ```arcpy.mp.ArcGISProject(aprx_path)```

```python
aprx4057 = arcpy.mp.ArcGISProject(r"C:\Users\leiwang\Documents\ArcGIS\Projects\GEOG4057\GEOG4057.aprx")
```

- If the script is run from an ArcGIS instance, you can access the current project by using the "CURRENT" keyword in the argument

```python
aprx4057 = arcpy.mp.ArcGISProject("CURRENT")
```

### Attributes and methods of the ArcGISProject object

- To obtain a complete list of the attributes and methods, check this link: https://pro.arcgis.com/en/pro-app/latest/arcpy/mapping/arcgisproject-class.htm
- The commonly used attributes include:
  - defaultGeodatabase, databases
  - defaultToolbox
  - homeFolder
  - filePath, documentVersion, isReadOnly, dateSaved, etc
  - activeView, activewMap
- The methods include:
  - listMaps()
  - createMaps()
  - deleteItem()
  - listBasemaps()
  - listMaps()
  - listLayouts()
  - listReport()
  - listColorRamps()
  - save() and saveACopy()
  - etc.

![alt text](images/image-11.png)

- For example, you can use ```aprx4057.save()" to save the updates made by the script
- Note that once the project file is referenced in a script, it is locked from other applications for updating
- To remove the reference explicitely in the script, use ```del aprx4057```

### Maps

- A map in ArcGIS Pro represents a view of a collection of symbolized spatial data
- A project can have numerous maps, each containing layers, tables
- Map objects can be obtained from an ArcGISProject object by listMaps()

```python
import arcpy
aprx = arcpy.mp.ArcGISProject(r"C:\Users\leiwang\Documents\ArcGIS\Projects\GEOG4057\GEOG4057.aprx")
maps = aprx.listMaps()
for index, m in enumerate(maps):
    print(f"{index} :{m.name}")
del aprx
```

- Another way to access maps it through the Layout class's mapFrame.map property
- Each Layout may contain one more more map frames, and each map frame only contains one map

#### Properties and methods of a Map object

- Useful properties of a Map object include name, mapType, mapUnits, referenceScale, etc.
- Methods include addBasemap(), addDataFromPath(), addLayer(), addTable(), moveLayer(), removeLayer(), listLayers(), listTables(), listFeatureClasses(), etc.
- You can get a layer object from a map by listLayers()

### Layers

- A layer can be referenced from within a project using listLayers method on the Map class or from a layer file (.lyr or lyrx) on the LayerFile class
- A Layer object can access the general properties and methods of layers
- Specific layers classes such as 3DLayer, FeatureLayer, GroupLayer, RasterLayer can be defined according the layer's type
  
```python
import arcpy
aprx = arcpy.mp.ArcGISProject(r"C:\Users\leiwang\Documents\ArcGIS\Projects\GEOG4057\GEOG4057.aprx")
m = aprx.listMaps()[0]
lyrs = m.listLayers()
for lyr in lyrs:
    if lyr.isBasemapLayer:
        print(lyr.name + " is a basemap layer")
    if lyr.isFeatureLayer:
        print(lyr.name + " is a feature layer")
    if lyr.isRasterLayer:
        print(lyr.name + " is a raster layer")
del aprx
```

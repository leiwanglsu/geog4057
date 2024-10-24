
# Assignment 8

## Data preparation 

- Extract data from the zip file "ex8"
- Locate the Austin.aprx file and open it with ArcGIS Pro. Check the maps and databases in the project.
- Close the project without saving

### Manipulate the project in VS Code

#### Open the project and print some information (10 pnts)

- In Visual Studio Code, open the ex8 folder as a workspace
- Create a new notebook in it, and name it as "ex8.ipynb"
- In the frist block, run the following code to get information about the Austin.aprx project file
- Remember to modify the path name of the project file to make it work

```python
import arcpy
import os
pathname = r"path-to-your-project"
aprx = arcpy.mp.ArcGISProject(os.path.join(pathname,"Austin.aprx"))
print(aprx.defaultGeodatabase)
```

#### Save a copy of the project (10 pnts)

- Use the project.saveAsCopy() function to save the project file to a copy of it
- In the notebook, add a new code block and run the following code
- Make sure you modify the pathname to fit your current working environment

```python
aprx.saveACopy(os.path.join(pathname,'Austin_Copy.aprx'))

```

#### Examine the new project file (10 pnts)

- Open the new project file you created in ArcGIS Pro to check the items in the project
- Is everything the same as the original project?  (Compare the difference in the file sizes) and why?
- Leave the ArcGIS Pro and the project opened because the following instructions will be based on this project
- Add the notebook you created for this exercise into the project - notebooks
- Open the added notebook

### Work with maps

#### Use the following code to print a list of maps in the project (10 pnts)

```python
aprx = arcpy.mp.ArcGISProject('CURRENT')
maps = aprx.listMaps()
for m in maps:
    print(m.name)
    print(m.mapUnits)
del aprx
```

- What does del do in the last line? Was the project file deleted?

#### Use the following code to change the name of a map (10 pnts)

```python
aprx = arcpy.mp.ArcGISProject('CURRENT')
m = aprx.listMaps("Region")[0]
m.name = "County"
del aprx
```

- In the project catelog pane, check the maps to confirm the name is changed

#### Use the following code to list the layers in a map (10 pnts)

```python
aprx = arcpy.mp.ArcGISProject('CURRENT')
maps = aprx.listMaps()
for m in maps:
    print("Map: " + m.name)
    lyrs = m.listLayers()
    for lyr in lyrs:
        print(lyr.name)
del aprx
```

- Additionally, use the following code to print if a layer is a basemap or a feature layer

```python
aprx = arcpy.mp.ArcGISProject('CURRENT')
m = aprx.listMaps("Downtown")[0]
lyrs = m.listLayers()
for lyr in lyrs:
    if lyr.isBasemapLayer:
        print(lyr.name + " is a basemap layer")
    if lyr.isFeatureLayer:
        print(lyr.name + " is a feature layer")
del aprx

```

#### Change the basemap (5 pnts)

- Use the following code to change the basemap of Downtown

```python
aprx = arcpy.mp.ArcGISProject('CURRENT')
m = aprx.listMaps("Downtown")[0]
m.addBasemap("Light Gray Canvas")
```

- After running the code, open the map and confirm the basemap is changed

### Work with layers

#### Modify layer symbology (5 pnts)

- Run the following code in a block to change the symbology of layers

```python
aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.listMaps("Downtown")[0]
lyr = m.listLayers("parks")[0]
sym = lyr.symbology
green = {"RGB": [100, 175, 0, 100]}
if lyr.isFeatureLayer and hasattr(sym, "renderer"):
    sym.renderer.symbol.color = green
    lyr.symbology = sym
```

- What type is the 'green' variable? What do the numbers in the list mean? If you want to show a brown color, what numbers you would fill it with? Change it in the block and confirm the color is changed to brown.

### Work with a layout

#### Add a layout to the project ((5 pnts))

- Run the following code to create a layout and insert the map "Downtown" in the layout

```python
m = aprx.listMaps("Downtown")[0]

lyt = aprx.createLayout( 11,8.5, 'INCH', 'New Layout with Rectangles')

def MakeRec_LL(llx, lly, w, h):
    xyRecList = [[llx, lly], [llx, lly+h], [llx+w,lly+h], [llx+w,lly], [llx,lly]]
    array = arcpy.Array([arcpy.Point(*coords) for coords in xyRecList])
    rec = arcpy.Polygon(array)
    return rec

mf = lyt.createMapFrame(MakeRec_LL(0.5,0.5,10,7.5), m, "New Map Frame")
```

- What is the size of the layout in inches?
- What is the size of the map frame?
- Comparing the layout and map frames you created manually, what are the advantages of creating it in Python?

#### Add layout elements (5 pnts)

- Run the following code to create a north arrow and a scale bar

```python
#Create a north arrow
naStyle = aprx.listStyleItems('ArcGIS 2D', 'North_Arrow', 'Compass North 1')[0]
na = lyt.createMapSurroundElement(arcpy.Point(9.5,7.5), 'North_Arrow', mf,
                                      naStyle, "Compass North Arrow")
na.elementWidth = 0.5  

#Create a scale bar
sbName = 'Double Alternating Scale Bar 1 Metric'
sbStyle = aprx.listStyleItems('ArcGIS 2D', 'Scale_bar', sbName)[0]
sbEnv = MakeRec_LL(5.5, 0.1, 4, 0.5)
sb = lyt.createMapSurroundElement(sbEnv, 'Scale_bar', mf, sbStyle, 'New Scale Bar')
```

- Run the follow code to create a legend

```python
legSi = aprx.listStyleItems('ArcGIS 2D', 'LEGEND', 'Legend 3' )[0]
leg = lyt.createMapSurroundElement(arcpy.Point(1,7), 'LEGEND', mf, legSi, 'New Legend Element')
leg.elementWidth = 3
leg.elementHeight = 3
leg.fittingStrategy = 'AdjustFontSize'
leg.columnCount = 1
leg.title = 'Downtown'
```

#### Export the layout to a pdf (10 pnts)

- Run the following code to export the layout to a pdf file

```python
lyt.exportToPDF(os.path.join(pathname, 'downtown.pdf'))
```

## Submission requirements

- Run through every steps of the instruction
- In a markdown block following each step, answer questions if any
- Make sure all the outputs are correct in each block in the Jupyter notebook
- Submit your notebook and the pdf map expored from the last step to your Github page and provide the link for the TA to evaluate
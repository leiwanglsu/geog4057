# Project 2 notes

## Step 1 prepare the running environment

- Clone the ArcPy enviornment in Anaconda if you have not done it before

`conda create -n arcpy_clone --clone "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"`

- Install earth engine api to the cloned environment

```
conda activate arcpy_clone
pip install earthengine-api
```

### Step 2 Explore ee DEM

`dem = ee.Image('USGS/3DEP/10m')`

`geom = ee.Geometry.Point([-91.0989573,30.3529013])`

`geom_col = ee.FeatureCollection([geom])`

`elev = dem.sampleRegions(geom_col).getInfo()`

### Step 3 Explore the csv file

`import pandas as pd
table = pd.read_csv(r"C:\Users\leiwang\Documents\geog4057\project\data\boundary.csv")`

`ra1 = arcpy.Raster(r"C:\Users\leiwang\Documents\geog4057\project\data\flood_2class.tif")
ra1.spatialReference.factoryCode`

`import geopandas
gdf = geopandas.GeoDataFrame(table)

gdf.set_geometry(
    geopandas.points_from_xy(gdf['X'], gdf['Y']),
    inplace=True, crs=f'EPSG:{ra1.spatialReference.factoryCode}')`


### Step 4 obtain elevations from GEE with the coordinates from the shapefile

- Add a new field
  
```
shapefile = r'E:\tmp\boundary1.shp'

arcpy.management.AddField(shapefile,'elevation',field_type='FLOAT')
```
- Read elevation from gee

```python
geom_list = []
with arcpy.da.SearchCursor(shapefile,['SHAPE@XY'],spatial_reference=4326) as cursor:
    for row in cursor:
        X,Y = row[0]
        geom = ee.Geometry.Point([X,Y])
        geom_list.append(geom)
geom_col = ee.FeatureCollection(geom_list)
elev = dem.sampleRegions(geom_col).getInfo().get('features')

```

- Use the update cursor to get and put data to the shapefile

```python
i = 0
with arcpy.da.UpdateCursor(shapefile,['elevation']) as cursor:
    for row in cursor:
        elevation = elev[i]['properties']['elevation']
        row[0] = elevation
        cursor.updateRow(row)
        i += 1
```

#### Step 5 Put the codes to a python script file 

- Copy the blocks from the jupyter notebook to a python file
- Make sure it runs as expected

#### Step 6 Organize the code as a function 

- Define a function with parameters
- Define a main() function to test the function


#### Write a python toolbox script and call the python script in the ArcGIS interface

- Create a new .pyt file
- in the Execute() function of the tool class, call the defined function from the last step
- Make sure it works
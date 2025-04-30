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

- Use the update cursor to get and put data to the shapefile

```
with arcpy.da.UpdateCursor(shapefile,['SHAPE@XY','elevation'],spatial_reference = 4326) as cursor:
    for row in cursor:
        X,Y = row[0]
        geom = ee.Geometry.Point([X,Y])
        geom_col = ee.FeatureCollection([geom])
        elev = dem.sampleRegions(geom_col).getInfo()
        row[1] = elev['features'][0]['properties']['elevation']
        cursor.updateRow(row)
```


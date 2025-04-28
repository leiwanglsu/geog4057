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



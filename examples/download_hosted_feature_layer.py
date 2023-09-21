
import arcpy
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# Connect to your ArcGIS Online or ArcGIS Enterprise account
gis = GIS()
# Create a FeatureLayer object representing your hosted feature layer

fl = FeatureLayer("https://services1.arcgis.com/fe3XWHMASK948q2c/arcgis/rest/services/EBRParcels/FeatureServer/0")

# Query features from the hosted feature layer
features = fl.query(where="OBJECTID > 0", out_fields="*")

# Save features as a shapefile
sdf = features.sdf
sdf.spatial.to_featureclass(location= r"C:\\tmp\\ebr_parcel.shp")


import json
with open('no_tax.json','r') as file:
    tax_json = json.load(file)

import arcpy
for row in tax_json['data']:
    row[8] = arcpy.FromWKT(row[8])


import os
fcname = 'notax_fc.shp'
workspace = r'C:\Users\leiwang\Downloads'
fc_fullname = os.path.join(workspace,fcname)
if arcpy.Exists(fc_fullname):
    arcpy.management.Delete(fc_fullname)

arcpy.management.CreateFeatureclass(out_path=workspace,out_name=fcname,
                                    geometry_type='POLYGON',
                                    spatial_reference=4236)

desc = arcpy.da.Describe(fc_fullname)
for field in desc['fields']:
    print(field.name)


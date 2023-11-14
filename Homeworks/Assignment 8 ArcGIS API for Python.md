
1. Download this notebook
2. Add the notebook to ArcGIS
3. Run through the code blocks in the notebook under the section Method 1
4. For each code block, create a markdown block and summarize what ArcGIS API for Python classes and their properties and functions are used in the block. Use print(type(variable)) to find out the classes. Check with this ArcGIS online documentation: https://developers.arcgis.com/python/api-reference/ to find the matching classes, properties, and functions 

For example: 

```python
stops_cities_fl = FeatureLayer(sample_cities.url + "/0")

print(type(stops_cities_fl))

```

<class 'arcgis.features.layer.FeatureLayer'>


The function query() of the FeatureLayer class was used in the notebook block: 

```python
stops_cities_fset = stops_cities_fl.query(where="ST in ('CA', 'NV', 'TX', 'AZ', 'LA', 'FL')  AND NAME IN ({0})".format(values), as_df=False)

```
 and it generates another variable stops_cities_fset as class FeatureSet

In the table, put the classes and functions you found from the code block like this:

| Class    | Functions | Properties|
| -------- | ------- |------|
| FeatureLayer  | query()    | |
|FeatureSet | | |

To learn how to create a table in markdown, try this link:

https://www.codecademy.com/resources/docs/markdown/tables





1. Download this notebook

2. Add the notebook to ArcGIS
3. Run through the code blocks in the notebook
4. Summarize what ArcGIS API for Python classes and functions are used in the notebook. Use print(type(variable)) to find out the classes 

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
 and it generates another class <FeatureSet> as the variable stops_cities_fset

In a table, put the classes and functions like this:


| Class | Functions| Properties|
---
|FeatureLayer| query()| |
|FeatureSet| | | 


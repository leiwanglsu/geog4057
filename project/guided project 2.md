# Guided project 2 - Google Earth Engine

- If you are a graduate student, you must complete this project if you want to use the guided project option
- Install Earth Engine api is needed.

## Project summary and objectives

In the folder data, a [csv file](./data/boundary.csv) is for location of water boundaries extracted from the geotiff file [flood_2class.tif](./data/flood_2class.tif). Your work is to use python to write script to obtain elevation values for the points from the csv file from Google Earth Engine and write the values to the shapefile. An ArcGIS toolbox will be developed to provide a user interface

### Data description

- The CSV file contains four columns: row, column, X, and Y
- The coordinates X,Y are defined as the coordinate system from the flood_2class.tif file
- Google Earth Engine provides elevation model from USGS 3DEP: [USGS 3DEP 10m National Map Seamless](https://developers.google.com/earth-engine/datasets/catalog/USGS_3DEP_10m)

### Tools and packages

- Installing Google Earth Engine library to a cloned ArcPy environment is needed

### Project development and deliverables

- Convert the csv to a shapefile
- Read the shapefile and the coordinates
- Obtain the USG 3DEP in EarthEngine for elevation values extracted for those points
- Write the extracted elevation back to the shapefile
- Interface design for a Toolbox

### Data visualization

- Create a new project or use an existing project
- Create a new map
- Add the shapefile to the map. 
- Change symbology
- Add a layout
- Add a mapframe to the layout and other elements
- Print the layout to a pdf

## Report

- Provide the link to your github repository
- In the repository of the project, write a report including how the code was developed and how to use the code
- Include the layout print in the repository
# Guided project 1

- This guided project is used by the instructor to show case a class project for students
- The project will be illlustrated in the class
- You can choose this project as your class project if you are a undergaduate student and do not want to develop your own project
- Graduate students must complete the other guided project as well if you want to use the guided project option

## Project summary

A JSON file was downloaded from the [data.gov](https://catalog.data.gov/dataset/?q=new+orleans+land+parcels&sort=views_recent+desc&res_format=CSV&res_format=JSON&groups=local&publisher=data.nola.gov&ext_location=&ext_bbox=&ext_prev_extent=&page=1) page of the 2018 Land Value for New Orleans. The JSON file contains WKT (well-known text) format of geometries and attributes that could be used in GIS. However, ArcGIS cannot directly import it using the Tools in Toolboxes (such as JSON to Feature). The objective is to provide a script tool to import the JSON file to a shapefile and visualize it in a project. 

## Data format and description

The data is available in project/data as "no_tax.json". The data file is in the JavaScript Object Notion (JSON) format. Using the python json package can help interpret the file. Two parts in the json file are useful: "meta" and "data". 'Meta" includes descrpitons of fields. "Data" includes geometries and field value. 

## Walk through and deliverables

### Jupyter notebook for code testing

- First, using a Jupyter notebook to explore the data
- Develop and test code to read from the JSON file
- Convert the information from JSON to feature class records in a shapefile

### Interface design

- Use Python Toolbox (pyt) to develop a user interface in ArcGIS Pro
- The interface allows user to select the JSON file and output shapefile name

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


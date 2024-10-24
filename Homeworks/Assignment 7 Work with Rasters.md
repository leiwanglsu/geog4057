# Assignment 7 Work with Rasters

## Part 1: Raster Basics and Properties

### Raster Dataset preparation: (10 pnts)

- From the ../data folder in this repository, find the Ex10.zip file as the input datasets
- Extract the zip file to a folder,for example, "c:/Documents/ex10"
- Check the files in the ex10 folder
- In ArcGIS Pro, create a new notebook for this exercise,
- In the first block, Use arcpy.Walk() function to list all raster datasets in the folder.
- Make sure the output of this code block shows correct results


### Basic Properties Documentation: (20 pnts)

- Document and discuss the basic properties of the raster datasets in the ex10 folder.
  - Determine and record the number of bands in the raster dataset using the bandCount property.
  - Explore the spatial resolution, cell size, and pixel bit depth using relevant properties provided by ArcPy.
  - Print the spatial reference information of the rasters

## Part 2: Raster Analysis

### Slope Analysis: (10 pnts)

- Apply the Slope analysis using the arcpy.sa.Slope tool on the "elevation" dataset.
- Save the output raster generated after applying the Slope analysis.
- Render the output raster in your Jupyter Notebook and discuss the changes observed in the dataset after the Slope analysis. You may explain any topographic insights or landscape information derived from the slope analysis.

### Clipping Operation: (10 pnts)

- Perform a Clipping operation on the elevation dataset using the arcpy.sa.Clip tool using the "watershed_HUC12.shp" feature class as the clip layer
- Save and analyze the clipped raster. 
- Discuss the importance and relevance of the clipped raster in relation to the original dataset.

## Part 3: Raster Manipulation

### Map Algebra Operators: (10 pnts)

- Use bands in "tm.img" as rasters to perform a raster calculator with the formula: "(band 3 - band 1) / (band 3 + band 1)"
- Note, in the above formula, you need to create raster from the tm.img file
- Show the result in the notebook
- Save the data to your workspace by using .save() function of the raster
- Document and explain the transformation carried out, and discuss the purpose or utility of the operation.

### Raster Cell Iterator: (15 pnts)

- Demonstrate how to use the Raster Cell Iterator to access and modify individual cell values in the raster dataset.
- Provide explanations of the specific cells you modified, the reasoning behind the modification, and the significance of these changes in the context of the raster data.

## Part 4: NumPy and Raster Integration

### NumPy Array Conversion: (15 pnts)

- Convert the chosen raster dataset to a NumPy array using the arcpy.RasterToNumPyArray() function.
- Use the min(), max(), mean(), and std() functions from Numpy to compute the raster data statistics.
- Discuss the advantages and applications of using NumPy arrays for raster data processing in GIS.

## Submission Guidelines:

- Present a well-documented Jupyter Notebook containing all your code, outputs, observations, and analysis for each part of the assignment. 
- Use the markdown blocks to include detailed explanations and interpretations of the results obtained from various raster operations.
- Provide visualizations wherever necessary to support your analysis.

## Evaluation Criteria:

- Accuracy and completeness of the documentation regarding raster properties and functionalities utilized.
- Effective use of geoprocessing tools and libraries (arcpy.sa and NumPy) for raster manipulation and analysis.
- Critical analysis and interpretations of the transformed raster dataset.

Note: Experiment with various operations, conduct comparisons, and explore the practical utility of each function or tool on the chosen raster dataset to broaden your understanding of working with raster data in ArcPy.
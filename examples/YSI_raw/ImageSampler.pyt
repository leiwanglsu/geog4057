# -*- coding: utf-8 -*-

import arcpy
from arcpy.sa import *
import numpy as np
from statistics import mean, median

class Toolbox(object):
    def __init__(self):
        self.label = "ImageSampler"
        self.alias = "ImageSampler"
        # List of tool classes associated with this toolbox
        self.tools = [sampleImage]


class sampleImage(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "sampleImage"
        self.description = "Compute median within a window from an image"
        self.canRunInBackground = False
        self.params = arcpy.GetParameterInfo()

    def getParameterInfo(self):
        """Define parameter definitions"""
        InputImage= arcpy.Parameter(
            displayName="Input Image",
            name="InputImage",
            datatype=["DERasterDataset", "DERasterCatalog"],
            parameterType="Required",
            direction="Input") 
     
        InputFeature = arcpy.Parameter(
            displayName="Location FeatureClass",
            name="Location Feature Class",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        
        WindowSize = arcpy.Parameter(
            displayName = "Windows Size",
            name = "Window_Size",
            datatype = "GPLong",
            parameterType = "Required",
            direction="Input"
        )
        WindowSize.filter.type = "ValueList"
        WindowSize.filter.list = [1,3,5,7,9]
        Stat = arcpy.Parameter(
            displayName = "Statistic type",
            name = "Statistics",
            datatype = "GPString",
            parameterType = "Required",
            direction="Input",
            
        )
      
        # Set up the  parameter's value list
        Stat.filter.type = "ValueList"
        Stat.filter.list = ["Median", "Mean"]      
        params = [InputImage, InputFeature,WindowSize,Stat]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        w_size = int(parameters[2].valueAsText)
        stat = parameters[3].valueAsText
      
        in_raster = arcpy.Raster(parameters[0].valueAsText)
        pixelarray = arcpy.RasterToNumPyArray(in_raster)
        nbands,nrows,ncols = np.shape(pixelarray)
        #outFocalStat = FocalStatistics(in_raster,NbrRectangle(w_size,w_size,"CELL"),stat)
        #outFocalStat.save("focalmean")
        pointFC = parameters[1].valueAsText
        SR = arcpy.Describe(pointFC).spatialReference  
        #check the fields, add them if needed
        lstFields = arcpy.ListFields(pointFC)
        fields = ["SHAPE@XY"]
        for nb in range(nbands):
            bndname = "b{}".format(nb+1)
            if not bndname in lstFields:
                arcpy.management.AddField(pointFC,bndname,"Float")
                fields.append(bndname)
              
        with arcpy.da.UpdateCursor(pointFC, fields) as cursor:
            for record in cursor:
                x,y = record[0]
                col, row = xytoRowCol(in_raster,x,y,SR)
                if col < 0 or col >= ncols or row < 0 or row >= nrows:
                    continue
                else:
                    
                    for band in range(nbands):
                        data_ext = extractByWindow(pixelarray[band],row, col, w_size)
                        if len(data_ext) == 0:
                            continue
                        if stat == "Mean":
                            record[band + 1] = mean(data_ext)
                        elif stat == "Median":
                            record[band + 1] = median(data_ext)
                            
                cursor.updateRow(record)
        return                     


def extractByWindow(npArrayData, row, col, window_size):
    data_extract = []
    nrows,ncols = np.shape(npArrayData)
    half = int(window_size / 2)
    for i in range(0,window_size):
        for j in range(0,window_size):
            r = row + i - half
            c = col + j - half
            if c < 0 or c >= ncols or r < 0 or r >= nrows:
                continue
            else:
                data_extract.append(npArrayData[r,c])
    return data_extract
def xytoRowCol(in_raster,x, y, srs):
    r_info = in_raster.getRasterInfo ()
    srOut = r_info.getSpatialReference()
    pt = arcpy.Point()
    pt.X = x
    pt.Y = y
    pt1 = arcpy.PointGeometry(pt,srs)
    pt2 = pt1.projectAs(srOut)
    pt1 = pt2.lastPoint
    cellsize = r_info.getCellSize()
    extent = r_info.getExtent ()
   
    col = int((pt1.X - extent.XMin) / cellsize[0])
    row = int((extent.YMax - pt1.Y) / cellsize[1])
    return col, row

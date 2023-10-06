# -*- coding: utf-8 -*-

import arcpy
import os
from readYSI import readYSI,readECM
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [readYSITool,readECMTool]
        


class readYSITool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "YSI2FeatureClass"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        InputFolder= arcpy.Parameter(
            displayName="Data Path of raw data",
            name="image1",
            datatype=["DEFolder"],
            parameterType="Required",
            direction="Input") 
     
        OutputFeatureClass = arcpy.Parameter(
            displayName="Out FeatureClass",
            name="Out_Fcls",
            datatype=["DEFeatureClass"],
            parameterType="Required",
            direction="Output")
        SpatialRef = arcpy.Parameter(
            displayName = "Spatial reference",
            name = "SpRefence",
            datatype = "GPSpatialReference",
            parameterType = "Required"
            
            )
        params = [InputFolder, OutputFeatureClass,SpatialRef]
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
        #messages.addMessage("Input: " + parameters[0].valueAsText)
        #messages.addMessage("Output: " +  parameters[1].valueAsText)
        #messages.addMessage("Spatial reference: " + parameters[2].valueAsText)
        spc = arcpy.CreateSpatialReference_management(parameters[2].valueAsText)
        path,outname = os.path.split(os.path.abspath(parameters[1].valueAsText))
        #messages.addMessage(path)
        fc = arcpy.CreateFeatureclass_management(path,outname,"POINT",spatial_reference=spc)
        arcpy.AddField_management(fc, "temp", "float","","")
        arcpy.AddField_management(fc, "SpCond", "float","","")
        arcpy.AddField_management(fc, "Sal", "float","","")
        arcpy.AddField_management(fc, "Turbidity", "float","","")
        arcpy.AddField_management(fc, "Chlorophyll", "float","","")
        arcpy.AddField_management(fc, "fDOM", "float","","")
        arcpy.AddField_management(fc, "BGA", "float","","")
        messages.addMessage(outname + " created")
        out_dict = readYSI(parameters[0].valueAsText)
        messages.addMessage("RAW data read, writting to featureclass")
        cursor = arcpy.da.InsertCursor(fc,("SHAPE@XY","temp","SpCond","Sal","Turbidity",
                                       "Chlorophyll","fDOM","BGA"))
        for ysi_pos in out_dict.items():
            row = [[ysi_pos[1][1][0],ysi_pos[1][1][1]],ysi_pos[1][2][0],ysi_pos[1][2][1],ysi_pos[1][2][2],
                        ysi_pos[1][2][3],ysi_pos[1][2][4],ysi_pos[1][2][5],ysi_pos[1][2][6]]
            cursor.insertRow(row)
        del(cursor)
    
        messages.addMessage("done!")
        return
class readECMTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "ECM2FeatureClass"
        self.description = "Read bathymetry M9 raw data"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        InputFolder= arcpy.Parameter(
            displayName="Data Path of raw data",
            name="image1",
            datatype=["DEFolder"],
            parameterType="Required",
            direction="Input") 
     
        OutputFeatureClass = arcpy.Parameter(
            displayName="Out FeatureClass",
            name="Out_Fcls",
            datatype=["DEFeatureClass"],
            parameterType="Required",
            direction="Output")
        SpatialRef = arcpy.Parameter(
            displayName = "Spatial reference",
            name = "SpRefence",
            datatype = "GPSpatialReference",
            parameterType = "Required"
            
            )
        params = [InputFolder, OutputFeatureClass,SpatialRef]
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
        #messages.addMessage("Input: " + parameters[0].valueAsText)
        #messages.addMessage("Output: " +  parameters[1].valueAsText)
        #messages.addMessage("Spatial reference: " + parameters[2].valueAsText)
        spc = arcpy.CreateSpatialReference_management(parameters[2].valueAsText)
        path,outname = os.path.split(os.path.abspath(parameters[1].valueAsText))
        #messages.addMessage(path)
        fc = arcpy.CreateFeatureclass_management(path,outname,"POINT",spatial_reference=spc)
        arcpy.AddField_management(fc, "ECM1", "float","","")
        arcpy.AddField_management(fc, "ECM2", "float","","")
        arcpy.AddField_management(fc, "ECM3", "float","","")
        arcpy.AddField_management(fc, "ECM4", "float","","")
        arcpy.AddField_management(fc, "ECM5", "float","","")
        arcpy.AddField_management(fc, "ECM6", "float","","")
        arcpy.AddField_management(fc, "ECM7", "float","","")
        arcpy.AddField_management(fc, "ECM8", "float","","")
        arcpy.AddField_management(fc, "ECM9", "float","","")

        messages.addMessage(outname + " created")
        out_dict = readECM(parameters[0].valueAsText)
        messages.addMessage("RAW data read, writting to featureclass")
        cursor = arcpy.da.InsertCursor(fc,("SHAPE@XY","ECM1","ECM2","ECM3","ECM4",
                                       "ECM5","ECM6","ECM7","ECM8","ECM9"))
        for ecm_pos in out_dict.items():
            row = [[ecm_pos[1][1][0],ecm_pos[1][1][1]],ecm_pos[1][2][0],
                             ecm_pos[1][2][1],ecm_pos[1][2][2],ecm_pos[1][2][3],ecm_pos[1][2][4],
                             ecm_pos[1][2][5],ecm_pos[1][2][6],ecm_pos[1][2][7],ecm_pos[1][2][8]]
      
            cursor.insertRow(row)
        del(cursor)
    
        messages.addMessage("done!")
        return

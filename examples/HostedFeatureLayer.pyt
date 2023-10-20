# -*- coding: utf-8 -*-

import arcpy


class Toolbox(object):
    def __init__(self):
        """
        Define the toolbox (the name of the toolbox is the name of the
        .pyt file).
        
        """
        self.label = "Hosted Feature layers"
        self.alias = "HostedFeatureLayers"

        # List of tool classes associated with this toolbox
        self.tools = [DowloadHFL]


class DowloadHFL(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Download Hosted Feature Layer to feature class"
        self.description = "Download Hosted Feature Layer to feature class"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        paraInputUrl = arcpy.Parameter(
            name="input_url",
            displayName="URL of Hosted Feature Layer",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        paraOutput = arcpy.Parameter(
            name="output feature class",
            displayName="Output Feature Class",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Output")
        params = [paraInputUrl, paraOutput]
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
        
        import arcpy
        from arcgis.gis import GIS
        from arcgis.features import FeatureLayer

        # Connect to your ArcGIS Online or ArcGIS Enterprise account
        gis = GIS()
        # Create a FeatureLayer object representing your hosted feature layer
        featurelayerurl = parameters[0].valueAsText
        output = parameters[1].valueAsText

        fl = FeatureLayer(featurelayerurl)
        messages.addMessage(f"Featurelayer Name {fl.properties.name}")
        messages.addMessage(f"Featurelayer Type {fl.properties.type}")
      
        # Query features from the hosted feature layer
        features = fl.query(where="1=1", out_fields="*")
        # Save features as a shapefile
        arcpy.AddMessage(f"Saving feature class: {output}")
        sdf = features.sdf
        sdf.spatial.to_featureclass(location=output)
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return

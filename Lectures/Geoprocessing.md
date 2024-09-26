# Geoprocessing with ArcPy

## Introduction

- ArcPy was introduced in version 10 of ArcGIS Desktop (ArcMap)
- ArcPy is a *package* including many modules. 
- Prior to ArcPy, the major scripting package is "arcgisscripting". (Still supported, but not recommended)
- To use ArcPy, simply use ```import arcpy```

## importing arcpy

- Check the environment if there is a package called arcpy
- You can use conda list to find arcpy in the package list
- To add the environment of arcgispro-py3 to anaconda environment list

```python
conda config --append envs_dirs "C:\Program Files\ArcGIS\Pro\bin\Python\envs"
```

- To clone the environment

```conda
conda create --name arcpy_clone --clone "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"
```

- import error will occur if there is no arcpy available:

```message
ImportError: No module named arcpy
```

- arcpy always needs a valid ArcGIS Pro license. If not, the error message will show:

```message
RuntimeError: NotInitialized

```

- If ArcPy is installed and licensed, any external IDLE can use it, for example, in VS Code

## ArcPy modules

- In ArcPy, functionality is organized into modules

>Charts module (arcpy.charts)
Data Access module (arcpy.da)
Geocoding module (arcpy.geocoding)
Image Analysis module (arcpy.ia)
Mapping module (arcpy.mp)
Metadata module (arcpy.metadata)
Network Analyst modules (arcpy.nax and arcpy.na)
Sharing module (arcpy.sharing)
Spatial Analyst module (arcpy.sa)
Workflow Manager (Classic) module (arcpy.wmx)

- To use a module in ArcPy, just use the format of

``` ArcPy.Module```
- Use ```print(dir(ArcPy))``` to see a list of modules and classes in the package

## Setting up a workspace

- A *workspace* is a default location for files you work with in the python session. 
- Inputs and outputs of geoprocessing tools use the workspace for file access
- To set the current workspace to <q>c:\data </q>

```python
import arcpy
arcpy.env.workspace = "c:/data"

```

- Note that use the forward slash / in the path name
- If you really want to use backslash, use double backslashes. Or use the raw string operator: <q> r"c:\data"</q>
- To check the current workspace name, use print(arcpy.env.workspace)
- Check your knowledge of python classes:
  - env is the class name for environment
  - Workspace is one property of class env
  - By running the statement "arcpy.env.workspace = "c:/data", you set the property "workspace" of "env" python object to "c:/data"
  - 

## Using Geoprocessing tools

- Geoprocessing tools are accessed through their names
  >For example: addField
- *Toolbox alias*:
  - One Geoprocessing tool could exist in multiple modules
  - Clip tool are avaiable from management, analysis, etc.
  - The Clip tool in the Analysis toolbox is referenced as Clip_analysis()
  - The Clip tool in the data management toolbox is rferenced as Clip_management()
- The syntax to call a function is ArcPy is:
  >arcpy.<toolname_toolboxalias>(<parameters>)
- An alternative way to call a function is through its module name
    > arcpy.<toolboxalias>.<toolname>(<parameters>)
    
    > For example: arcpy.analysis.Clip()

## Issues in writing python code for geoprocessing

- Python code is case sensitive
  - Therefore, clip is not correct and should be Clip
  - Tool alias names are alway in small case and function names always start with the first upper case letter.
  - Quotation marks are different in python editor than in the Word processors
    - Use straight quotation marks in python "" 
    - Use curly quotation marks in Word (hold alt and type 0145 and 0146)
    - Be careful when copying codes from pdf or word files

## Understanding the python syntax documents in ArcGIS

  ### Tool arguments (parameters)

- Name
- Type: feature class, integer, string, or raster
- Direction: input or output
- Required: whether a value must be provided or it is optional
  - Required argument come first
  - Optional argument are in parenthese {}

```python
Buffer(in_features, out_feature_class, 
       buffer_distance_or_field, {line_side}, 
       {line_end_type}, {dissolve_option}, {dissolve_field})
```

### Skipping some optional argument

- For example, you want to specify the dissolve field paramete but not  other optional argument
- Use empty string, the number sign ("#"), or the value None for the skipped argument

```python
arcpy.Buffer_analysis("roads", "buffer", "100 METERS", "", "", 
                      "LIST", "CODE")
arcpy.Buffer_analysis("roads", "buffer", "100 METERS", "#", "#", 
                      "LIST", "CODE")
arcpy.Buffer_analysis("roads", "buffer", "100 METERS", None, None, 
                      "LIST", "CODE")
```

### Python argument types

- non-default vs. default arguments: 
  - a default argument is defined in the function with a default value assignment
  - the default value is used if the caller does not provide one
  - None-default arguments must be provided by the caller
  - Non-default arguments must be specified before the default arguments

```python
def divide_two(a, b = 1):
    return a / b
print(divide_two(3))
print(divide_two(3,2))
```

- positional vs. keyword arguments
  - Positional arguments are specified by their order
  - keyword arguments can stand by their own without following the order
  
```python
print(divide_two(5,2))
print(divide_two(b = 2, a = 5))
```

- Use keyword arguments to specify the values of default parameters without following the order

```python
arcpy.Buffer_analysis("roads", "buffer", "100 METERS", 
                      dissolve_option="LIST", dissolve_field="CODE")
```

### None value

- None is a specific built-in type in python - NoneType
- None means a null value or no value at all
- None represent the none object
- It is not the same as an empty string "" because "" is a string object

### Use parameters from user input

- Hard coded parameters only work for a specific case
- To make your code reusable, change the hard-coded parameters to variables
- use arcpy.GetParameterAsText() function to obtain user input

### Use variables

- Variable names can consist of any combination of valid characters
- Using naming styles is recommended. 
- For example, use only lower-case characters and combine words with underscores
- my_clip, clip_result, messge_out, output_file, etc.

### Work with toolboxes

- In ArcPy, all system toolboxes are available
- If you have a custom tool and want to call it from python, you can use the function arcpy.ImportToolbox()
- Once the tool is imported, you can use arcpy.toolname_toolboxalias to call the tool 
- Note that the alias is not the same as the name of the toolbox
- A new toolbox will be assigned by the system with a default alias (e.g. NewToolbox)
- It is a good practice to define a custom toolbox alias together with the tool name and label
- You can also set a temporary alias when importing a toolbox

```python
arcpy.ImportToolbox("Sampletools.tbx", "mytools")
arcpy.MyMode_mytools(<parameters>)
```

### ArcPy non-tool functions

- All geoprocessing tools are functions of ArcPy, but not all functions of ArcPy are geoprocessing tools
- The non-tool functions are built-in functions in ArcPy, and do not depend on the level of license
- Non-tool functions do not have module alias names like geoprocessing tools
- Non-tool functions are documented only under the ArcPy tab of the ArcGIS Pro help pages

```
import arcpy
print(arcpy.Exists("C:/Data.streams.shp"))
```

## Work with tool output messages

### Access the tool messages

- Tools' output messages are written about the success or failure of execution.
- User can read the message and understand the result of geoprocessing
- In geoprocessing tools, the message can be viewed by clicking the View Details link at the bottom of the tool dialog box
- ![Alt text](images/image.png)

- Messages also can be accessed in the History pane
- Use arcpy.GetMessages() function to display the messages in python

### Severity level of messages

- Severity = 0: there is no problem with the tool run. 
- severity = 1: warning messages indicate a possible problem. Warning messages do not stop the tool from running
- severity = 2: error messages indicate a situation prevents the tool from execution
- A six-digit ID code is provided with the messages. Using the ID can help in identifying the causes of potential problems and how to deal with them. 
- Use arcpy.GetMaxSeverity() to get the severity level

## Work with licences

### Licence levels

- ArcView (Basic)
- ArcEditor (Standard)
- ArcInfo (Advanced)
  
### License types

- Single use
- Concurrent

```python
arcpy.CheckProduct("arcinfo")
```

### Check out extension license

- When using concurrent license, use arcpy.CheckOutExtensions() to enable the extensions on the current computer


## Work with spatial reference

### SpatialReference class

- SpatialReference class is a frequently used ArcPy class
- Properties: GCS, XYResolution, XYTolerance, domain, name, projectionName, etc.
- Methods: create, createfromFile(prj_file), loadFromString(string), setDomain, etc.
- Can be accssed from existing datasets using Describe()
  
```python
dataset = "c:/data/landbase.gdb/Wetlands"
spatial_ref = arcpy.Describe(dataset).spatialReference
```

- SpatialReference objects can be compared to others using == or !=


### Create SpatialReference objects

- Obtained from existing datasets using Describe()
- Create from a .prj file
- Create from a well-known ID (WKID)
- Create from a projection name
- Create from a well-known text (WKT)

#### Well-known IDs

- Unique ID assigned for each coordinate system
- Two authorities: EPSG and ESRI
    - EPSG - European Petroleum Survey Group 
    - The IDs from the two authorities do not overlap. 
    - Use https://epsg.io/ to find the coordinate systems by name and their WKIDs. 
    - Some commonly used WKIDs:
    >WGS 84 GCS: WKID = EPSG: 4326
    
    >World Mercator Auxiliary Sphere: WKID = EPSG: 102100
    
    > NAD83:  WKID = EPSG:4269
    
    > North America Equidistant Conic with NAD83: WKID = ESRI:102010 
    
    > UTM zone 15N: WKID= EPSG:26915

- Use the "factorCode" property to get the WKID

#### Well-known text

- Well-known text (WKT) is a text markup language for representation of geometry and coordinate systems
- WKT strings are formatted by keywords and elements enclosed by square brackets. 
- The brackets are hierarchical 

```python
wkt = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],\
              PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];\
              -400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;\
              0.001;0.001;IsHighPrecision"
```

### projection names

- Names of coordinate systems can be used to create a SpatialReference object

```python
sr = arcpy.SpatialReference("NAD 1983 StatePlane Texas Central FIPS 
                            4203 (US Feet)")
```

- List the names of spatial references:
  - arcpy.ListSpatialReferences({wild_card}, {spatial_reference_type})

## Create a python script tool

### What is a script tool

Creating a script tool allows you to turn your Python scripts and functionality into your own geoprocessing tools. Once created, a script tool provides many advantages

- A script tool works under the geoprocessing framework of ArcGIS Pro
- The tool can be used in the same way as other built-in tools
- You can write messages to the Geoprocessing history
- ArcPy is fully aware of the application it was called from and applies the settings to the script tool

### How to create a script tool

To Create a script tool in a custom toolbox, you need three things:

- A script
- A custom toolbox
- A precise definition of the parameters of your script

### Create a script tool

- In a toolbox, right click and create -> new script
  - In General: Name the script "CopyFeatureClasses" and the same for the label
  - In parameters, add two parameters: InputWorkspace and OutputWorkspace
    - InputWorkspace: String type, Required, and Input
    - OutputWorkspace: String type, Required, and Output

![Alt text](images/image-1.png)

- In Execution, paste the following code

```python
import arcpy
import os
from arcpy import env
env.workspace = arcpy.GetParameterAsText(0)
outgdb = arcpy.GetParameterAsText(1)
fclist = arcpy.ListFeatureClasses()
for fc in fclist:
    fcdesc = arcpy.Describe(fc)
    arcpy.CopyFeatures_management(fc,os.path.join(outgdb,fcdesc.basename))

```

- Try to run the tool from the catalog pane

### Another example - select random features from input feature class and write out

- First, create a tool called Random Sample in your toolbox
- Second, create parameters for the tool like this

![alt text](images/image-9.png)

- The orginial script .py fromt the textbook:

```python
# Python script: random_sample.py
# Author: Paul Zandbergen
# This script creates a random sample of input features based on
# a specified count and saves the results as a new feature class.
# Import modules.
import arcpy
import random
# Set inputs and outputs. Inputfc can be a shapefile or geodatabase
# feature class. Outcount cannot exceed the feature count of inputfc.
inputfc = "C:/Random/Data.gdb/points"
outputfc = "C:Random/Data.gdb/random"
outcount = 5
# Create a list of all the IDs of the input features.
inlist = []
with arcpy.da.SearchCursor(inputfc, "OID@") as cursor:
    for row in cursor:
        id = row[0]
        inlist.append(id)
# Create a random sample of IDs from the list of all IDs.
randomlist = random.sample(inlist, outcount)
# Use the random sample of IDs to create a new feature class.
desc = arcpy.da.Describe(inputfc)
fldname = desc["OIDFieldName"]
sqlfield = arcpy.AddFieldDelimiters(inputfc, fldname)
sqlexp = f"{sqlfield} IN {tuple(randomlist)}"
arcpy.Select_analysis(inputfc, outputfc, sqlexp)
```

### Edit tool code to receive parameters

- The python script should read from user-specified arguments to run correctly
- The provided .py code only take hard-coded names for input and output and will not run if the input and output do not make sense (non-exist or incorrect path name)
- Change your default code editor in ArcGIS
![alt text](images/image-10.png)

- Right-click the script tool in the toolbox and click Edit. 
- Use GetParameterAsText() or GetParameter() to get user inputs because the latter will return an object (such as a number)
- When the input is not a text, use GetParameter() can return a value rather than a text
- Replace these lines in the code

```python
inputfc = GetParameterAsText(0)
outputfc = GetParameterASText(1)
outcount = GetParameter(2)
```

### Working with messages

- Messages from the script tool can be printed in the detailed view of the excuted tool 
- As other geoprocessing tools in ArcGIS Pro, your tool can return some messages to the users
- AddMessage - for general inforamtion
- AddWarning - for warning messages
- AddError - for error messages
- AddIDMessage - for both warning and error
- AddReturnMessage - for all messages and enables hyperlinks for errors in your script
- In the random feature tool example, if user put a number larger than the number of features available, the tool will fail. Therefore, we need to check if the number is appropriate
- If the number is too large or negative, we return an error message to the user and not running the rest of the code
- Add the following lines right after the lines you changed in the last time

```python
fcount = arcpy.GetCount_management(inputfc)[0]
if outcount > int(fcount):
  sys.exit(1)
elif outcout == int(fcount):
  arcpy.AddWarning("The number of features to be selected"
                     "is the same as the number of input features."
                     "This means the tool created a copy of the"
                     "input features without creating a sample.")
```

#### ID Messages

- ID messages are messages with ESRI system message ID 
- For example, ID = 12 indicates the output feature already exists

```python
import arcpy
infc = arcpy.GetParameterAsText(0)
outfc = arcpy.GetParameterAsText(1)
if arcpy.Exists(outfc):
    arcpy.AddIDMessage("ERROR", 12, outfc)
else:
    arcpy.CopyFeatures_management(infc, outfc)
```

- To list the IDs associated with a topic (e.g. Projection), you can use GetIDMessage() 

```python
import arcpy
dict_id = {}
for k in range(1000000):
    v = arcpy.GetIDMessage(k)
    if v:
        dict_id[k] = v
for k,v in dict_id.items():
    if "Projection" in v:
        print(k, v)      
```

### Show a progress information bar

- When running a tool that takes long time to finish, it is a good practice to show a progress indicator in the iinterface
- ArcPy progressor is the tool for this purpose. The methods include SetProgressor(), SetProgressorLable(), SetProgressorPosition(), and ResetProgressor()
- SetProgessor(type, {messsage},{min_range},{max_range},{step_value})
- Two types of progressors: default and step
- The message argument show a text  at the beginning of the tool execution.
- SetProgressorLabel() is to update the label of the progressor
- SetProgressorPosition() will move the step progressor by an increment 
- Once the progressor finishes, you can use ResetProgressor() to reset its position
- Let's use a progressor for copy features tool:

```python
import arcpy
import os
arcpy.env.workspace = arcpy.GetParameterAsText(0)
outworkspace = arcpy.GetParameterAsText(1)
fclist = arcpy.ListFeatureClasses()
fcount = len(fclist)
arcpy.SetProgressor("step", "Copying shapefiles to geodatabase...", 
                    0, fcount, 1)
for fc in fclist:
    arcpy.SetProgressorLabel("Copying " + fc + "...")
    fcdesc = arcpy.Describe(fc)
    outfc = os.path.join(outworkspace, fcdesc.baseName)
    arcpy.CopyFeatures_management(fc, outfc)
    arcpy.SetProgressorPosition()
```

## Python toolbox

### What is a Python toolbox

- Python toolboxes are geoprocessing toolboxes that are created entirely in Python. 
- Python toolboxes have the file extension of .pyt
- Python toolboxes can be created under a foler in the project

![Alt text](images/image-2.png)

### Create a Python toolbox

- In catalog pane, right click Toolboxes and select new Python toolbox
- Select a folder where the toolbox will be saved to
- Type a name for the toolbox.

### Understand the structure of the toolbox

- A .pyt file is not different from a regular python .py script file
- In the pyt file, tools are defined as classes (remember the object-oriented programming concept?)

### Define a custom class

- A class is defined by the keyword class and the name of the class.
- A class defines its attributes
- A class defines its behaviors
- Multiple objects can be created from the class with different identities but share the similar behaviors and comparable attributes

```python
class Dog:
 
    # A simple class
    # attribute
    attr1 = "mammal"
    attr2 = "dog"
 
    # A sample method
    def fun(self):
        print("I'm a", self.attr1)
        print("I'm a", self.attr2)
# Object instantiation
Rodger = Dog()
 # Accessing class attributes
# and method through objects
print(Rodger.attr1)
Rodger.fun()
```

### \__init\__() method (dunder)

- The dunder function init is similar to constructors in C++
- Constructors are used to initializing an object when it is created
- For example, when a dog object is created, the "age" attribute of the dog should be initlized with a non-negative value.
- The constructor function execute some statements at the time of the object construction

```python
class Person:
 
    # init method or constructor
    def __init__(self, name):
        self.name = name
 
    # Sample Method
    def say_hi(self):
        print('Hello, my name is', self.name)
 
 
p = Person('Nikhil')
p.say_hi()
```

### self parameter

- When a function in the class is executed, the first parameter is always referring to object itself
-  The user specified parameters are listed as the second, third, and so on.
  
### __str__() method (dunder)

- The dunder method __str__() is executed when an object is printed as a string
- It is useful for debugging and information about the classes

```python
class GFG:
    def __init__(self, name, company):
        self.name = name
        self.company = company
 
    def __str__(self):
        return f"My name is {self.name} and I work in {self.company}."
 
 my_obj = GFG("John", "GeeksForGeeks")
print(my_obj)
```


### Class inheritance

- Inheritance allow us to define a class that inherits all the methods and the properties from another class
- The class being inherited from is called the parent class or the base class
- The class that inherits from another class is called the child class or derived class

#### Method overriding

- The method inherited from the parent class can be modified by the child class. This is called method overriding
- Method overriding allows for the child class to inherit some methods from the parents while modifying some others
- For example, the Dog class can be inherited from the Animal class
- The Animal class has a move() function, but the Dog class overrides the move() function by defining the specific behavior of Dog.move(), not the Animal.move()


```python
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname
  def printname(self):
    print(self.firstname, self.lastname)
x = Person('John', 'Doe')
x.printname()

class Student (Person):
  pass
x = Student("Mike", "Olsen")
x.printname()

class Student(Person):
  def __init__(self, fname, lname, year):
    self.firstname = fname
    self.lastname = lname
    self.GraduationYear = year
  def printname(self):
    print(self.firstname, self.lastname,self.GraduationYear)
```

### The object class in ArcGIS ArcPy

- The object class is the parent class for all other ArcPy classes
- The toolbox class is also inherited from the object class


### Toolbox class

- The Toolbox class is used by ArcGIS to define the properties and  behaviors of a toolbox, including the alias, label, and description.
- The name of the Toolbox is defined by the name of the .pyt file
- The tools property must be set to a list containing all tool classes defined in the toolbox
- The Toolbox class is inherited from the object class in ArcPy that defines the toolbox label, alias, and the tools it contains
- self.tools stores a list of Tools defined in the .pyt file

```python
class Toolbox(object):
    def __init__(self):
        self.label = "Random Sampling Tools"
        self.alias = "randomsampling"
        self.tools = [MyTool]
```

#### Editing the toolbox class generated from a template

- When creating a new toolbox, the python code is copied from a template with a stubbed-out tool named Tool
- The Tool should be renamed, and can be duplicated and edited to create additional tools in your toolbox
- The tool name and the toolbox alias must begin with a letter and only consist of letters and numbers

### The Tool Class:

- Each tool class within the toolbox also inherits from object.
- It defines the tool's label, description, parameters, and execution logic
- You can override some methods such as getParameterInfo(), isLicensed(), updateParameters(), updateMessages()
- Override the execute() is always needed, as it defines the behavior of a tool

```python
class MyTool(object):
    def __init__(self):
        self.label = "My Tool"
        self.description = "Description of my tool"
        self.canRunInBackground = False

    def getParameterInfo(self):
        # Define parameters here
        return parameters

    def execute(self, parameters, messages):
        # Tool execution logic here
        pass
```

- Define as many Tool classes as you need, and add them in the Toolbox class's self.tool attribute list

```python
class Toolbox(object):
    def __init__(self):
        self.label = "My Cool Tools"
        self.alias = "mycooltools"
        self.tools = [CoolTool1, CoolTool2]
class CoolTool1(object):
    def __init__(self):
        self.label = "Cool Tool 1"
    def getParameterInfo(self)
        # Parameter definition
    def execute(self, parameters, messages):
        # Source code
class CoolTool2(object):
    def __init__(self):
        self.label = "Cool Tool 2"
    def getParameterInfo(self)
        # Parameter definition
    def execute(self, parameters, messages):
        # Source code
```

#### Defining parameters in a python toolbox

- Override the getParameterInfo() function and create arcpy.Parameter objects and setting their properties
- arcpy.Parameter class properties
  - name: the name of parameter as shown in the tool's syntax 
  - datatype: define the the valid parameter type such as "GPCoordinateSystem", "GPLayer", "DERasterDataset", etc. For a complete list of the datatypes, go to: <https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/defining-parameter-data-types-in-a-python-toolbox.htm>

  - parameterType: Required, Optional, or Derived
  - direction: Input or Output
  - multivalue: True or False 
- Parameters are returned by getParameterInfo() as a list

```python
def getParameterInfo(self):
    input_features = arcpy.Parameter(
        name="input_features",
        displayName="Input Features",
        datatype="GPFeatureLayer",
        parameterType="Required",
        direction="Input")
    parameters = [input_features]
    return parameters
```

### Define a parameter

- Use the arcpy.Parameter class
- Arguments include name, displayName, datatype,parameterType, direction
- Define filters for a parameter: type and list
  - type defines the type of the input that user can enter in the box
  - list can be defined by a ValueList, Range, FeatureClass, File, Field, or Workspace type
- Refer to this page for paramter types: https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/defining-parameter-data-types-in-a-python-toolbox.htm


```python
import arcpy
class Toolbox(object):
    def __init__(self):
        self.label = "Random Sampling Tools"
        self.alias = "randomsampling"
class Toolbox(object):
    def __init__(self):
        self.label = "Random Sampling Tools"
        self.alias = "randomsampling"
        self.tools = [RandomSample]
class RandomSample(object):
    def __init__(self):
        self.label = "Random Sample"
    def getParameterInfo(self):
        input_features = arcpy.Parameter(
        name="input_features",
        displayName="Input Features",
        datatype="GPFeatureLayer",
        parameterType="Required",
        direction="Input")
    output_features = arcpy.Parameter(
        name="output_features",
        displayName="Output Features",
        datatype="GPFeatureLayer",
        parameterType="Required",
        direction="Output")
    no_of_features = arcpy.Parameter(
        name="number_of_features",
        displayName="Number of Features",
        datatype="GPLong",
        parameterType="Required"
        direction="Input")
    no_of_features.filter.type = "Range"
    no_of_features.filter.list = [1, 1000000000]
    parameters = [input_features, output_features, no_of_features]
    return parameters

```

#### Accessing parameters in the execute() function

- The main body of the tool is found in the execute method
- You can call other tools and access ArcPy other custom or third party python functionality
- the syntax is ```def execue(self, parameters, messages):```
- Each parameter's value can be access from the list using the valueAsText method like ```parameters[0].valueAsText```

```python
def execute(self, parameters, messages):
    in_fc = parameters[0].valueAsText
    out_fc = parameters[1].valueAsText
```

#### Python toolbox messages

- When a tool is run, ArcPy defines the application it is called from and reads the messages from it and display them in the tool dialog box of ArcGIS Pro
- In a python toolbox, a message object can be accessed in the execute method to add messages back to the tool
- The five methods for writing the messages are:
  - addMessage(message)
  - addWarningMessage(message): a warning message will be shown in ArcGIS
  - addErrorMessage(message): an error message is added to the tool's message
  - addIDMessage: using geoprocessing message codes
  - addGPMessages(): message from the last geoprocessing tool run are added to the tools' messages

```python
def execute(self, parameters, messages):
    inputfc = parameters[0].valueAsText
    outputfc = parameters[1].valueAsText
    outcount = parameters[2].value
    inlist = []
    with arcpy.da.SearchCursor(inputfc, "OID@") as cursor:
        for row in cursor:
            id = row[0]
            inlist.append(id)
    randomlist = random.sample(inlist, outcount)
    desc = arcpy.da.Describe(inputfc)
    fldname = desc["OIDFieldName"]
    sqlfield = arcpy.AddFieldDelimiters(inputfc, fldname)
    sqlexp = f"{sqlfield} IN {tuple(randomlist)}"
    arcpy.Select_analysis(inputfc, outputfc, sqlexp)
    messages.addMessage(f"Random features are selected and written to {outputfc}")
```

### Comparison between script tools and python toolboxes

- Both script tools and Python toolboxes can be used to create custom tools using Python
- Both are integrated in the geoprocessing framework
- A script tool is a part of a custom toolbox (.tbx) and an associated python script file (.py)
- The design of the script tool is saved in the tbx file
- A single python toolbox (.pyt) stores both the tools design and functionality by the tools
- .pyt can standalone without an ArcGIS toolbox (.tbx)
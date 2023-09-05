#anaconda #python 
# Install Anaconda
- Anaconda website and download the free version: https://www.anaconda.com/download
- Install to your computer by following the instruction
- Read the cheating sheet about Anaconda: https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf
# Create new environments
- Create a new environment in Anaconda
- Notes: -n means the name of the new environment, python version can be specified as anything between 3.9 to 3.11
```
conda create -n geog4057 python=3.9
```
# List and manage environments
- Use Anaconda to help you manage the environments
- List environments
```
conda env list
```
- Remove an environment
```
conda env remove geog4057
```
- Add an existing environment
```
conda config --append envs_dirs "C:\Program Files\ArcGIS\Pro\bin\Python\envs"
```
- Cloning an environment
```
conda create --name arcpy_clone --clone "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"
```

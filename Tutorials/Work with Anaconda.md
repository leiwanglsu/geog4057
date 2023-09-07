#anaconda #python 
# Install Anaconda
- Anaconda website and download the free version: https://www.anaconda.com/download
- Install to your computer by following the instruction
- Read the cheating sheet about Anaconda: https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf
# Create and manage new environments
## Create a new environment in Anaconda
- Notes: -n means the name of the new environment, the python version can be specified as anything between 3.9 to 3.11
```
conda create -n geog4057 python=3.9
```
- Remember to activate the new environment you just created
```
conda activate geog4057
```
## Install a new package (for example, numpy and pandas) to the environment

```
pip install numpy pandas
```
- Removing a package if needed

```
pip uninstall numpy
```

## List and manage environments
- List environments
```
conda env list
```

- Remove an environment
```
conda env remove geog4057
```

- Cloning an environment
```
conda create --name arcpy_clone --clone "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3"
```

## Optional: change the default path for Anaconda to create new environments
- Open the file .condarc under c:\users\yourname using notepad or other text editors
- Add these lines to the file ("D:\envs" is the default folder in this example)
- Save the file

```
envs_dirs:
  - D:\envs
```

- Add an existing environment path to the list
```
conda config --append envs_dirs "C:\Program Files\ArcGIS\Pro\bin\Python\envs"
```

- After that, you will see C:\Program Files\ArcGIS\Pro\bin\Python\envs in the default path list of .condarc


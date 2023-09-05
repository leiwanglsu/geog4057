#jupyter #python #arcgis 

# Install Jupyter and notebook
```
pip install jupyter notebook
```

# Register or unregister Jupyter kernels

- Register a kernel by ipykernel
```
python -m ipykernel install --name test_kernel --display-name "test_kernel" --user
```

- List all kernels
```
jupyter kernelspec list
```
- Remove a kernel from the list
```
jupyter kernelspec uninstall test_kernel

```

# Manually create a kernel specification
- Find the path in your explorer: <q>C:\Users\yourname\AppData\Roaming\jupyter\kernels</q>
- Each folder is a kernel registered with Jupyter
- Make a copy of an existing folder
- Change the name of the copied folder to something you need
- Open the folder and open the file "kernel.json"
- Replace the string value in "argv": with the path to your python environment
- Change the value of the "display_name" to the desired kernel name
- Save and re-run Jupyter
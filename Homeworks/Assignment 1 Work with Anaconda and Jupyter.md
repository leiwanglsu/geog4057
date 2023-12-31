# Work with Anaconda and Juptyer

1. Use the these two tutorials as reference: [Work with Anaconda](../Tutorials/Work_with_Anaconda.md) and [Work with Jupyter Notebook](../Tutorials/Work_with_Jupyter_Notebook.md)
2. Install Anaconda on your work/home computer
3. Create a new environment using Anaconda with the name of "geog4057" and python 3.9 (remember to activate if you want to install packages)
	- Hint: find the solution from [Work with Anaconda](../Tutorials/Work_with_Anaconda.md)
4. Install jupyter notebook using pip or conda 
	- Solution is in  [Work with Jupyter Notebook](../Tutorials/Work_with_Jupyter_Notebook.md)
5. Register the anaconda environment "geog4057" with the ipykernel module
	- Solution is in  [Work with Jupyter Notebook](../Tutorials/Work_with_Jupyter_Notebook.md)
6. Run jupyter notebook from the anaconda prompt 
7. Create a new folder called "Scripts" in your "Document" folder
8. In the Scripts folder, create a new notebook with the name of "homework1.ipynb" and use the the kernel "geog4057"
9. In the first cell,  type (or copy and paste) the following code

 ```python
print("Hello World")
 ```

11. Clone the ArcGIS default environment to a new environment called "ArcPyClone"
12. Register the ArcPyClone environment with "ipykernel"
13. In the new notebook, switch the kernel to ArcPyClone
14. Go to menu->Inert -> Inser Cel Below to add the second cell in the notebook. 
15. In the second cell, run the following code to verify if ArcPy is working.

```python
import arcpy
print(arcpy.GetInstallInfo()['Version'])
```

## Screen capture

![screen capture](<../img/Pasted%20image%2020230905180829.png>)

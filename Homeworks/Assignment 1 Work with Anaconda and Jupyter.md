# Requirements
1. Use the these two tutorials as reference: [[Work with Anaconda]] and [[Work with Jupyter Notebook]]
2. Install Anaconda on your work/home computer
3. Create a new environment using Anaconda with the name of "geog4057" and python 3.9 (remember to activate if you want to install packages) 
	1. Hint: find the solution from [[Work with Anaconda]] 
4. Install jupyter notebook using pip or conda 
	1. Solution is in  [[Work with Jupyter Notebook]]
5. Register the anaconda environment "geog4057" with the ipykernel module 
	1. Solution is in  [[Work with Jupyter Notebook]]
6. Run Jupyter notebook from the anaconda prompt 
7. Create a new folder in your "document" folder
8. Create a new notebook using Jupyter and the kernel "geog4057"
9. In the first cell, print "Hello World"

 ```
print("Hello World")
 ```

10. Clone the ArcGIS default environment to a new environment called "ArcPyClone"
11. Register the ArcPyClone environment with "ipykernel"
12. In the new notebook, switch the kernel to ArcPyClone
13. In the second block, run the following code to verify if ArcPy is working. 

```
import arcpy
print(arcpy.GetInstallInfo()['Version'])
```

# Screen capture 


![](<Pasted image 20230905180829.png>)

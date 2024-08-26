

# Install Python extension to VSCode

##### Prerequisite: Check if Python is Already Installed

- From Windows menu, run Anaconda prompt
- If you cannot find Anaconda, follow [this instruction](Work_with_Anaconda.md) to install it.

---

### **Configuring VSCode to Recognize Python**

#### **Objective**
Students will install the Python extension in VSCode and configure it to recognize Python on their system.

#### **Step-by-Step Guide**

##### **1. Install Visual Studio Code (VSCode)**
- **Windows/macOS/Linux:**
  - Download VSCode from the official website: [https://code.visualstudio.com/](https://code.visualstudio.com/).
  - Follow the installation instructions based on your operating system.

##### **2. Open VSCode and Install the Python Extension**

1. **Open VSCode:**
   - After installing VSCode, launch the application.

2. **Install the Python Extension:**
   - Open the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or pressing `Ctrl+Shift+X` (`Cmd+Shift+X` on macOS).
   - In the search bar at the top of the Extensions view, type "Python".
   - The first result should be the official Python extension by Microsoft. It has a high number of downloads and a high rating.
   - Click "Install" to add the Python extension to VSCode.

3. **Select Python Interpreter:**
   - Once the Python extension is installed, VSCode may automatically prompt you to select a Python interpreter.
   - If not, open the Command Palette by pressing `Ctrl+Shift+P` (`Cmd+Shift+P` on macOS).
   - Type "Python: Select Interpreter" and select it from the dropdown.
   - A list of available Python interpreters will appear. Select the one that matches your Python installation (e.g., Python 3.x from the virtual environment or system Python).
   - If Python was installed correctly earlier, it should appear in this list.

##### **3. Verify Python Configuration in VSCode**

1. **Create a New Python File:**
   - Click on the "Explorer" icon in the Activity Bar and select "Open Folder" to create or open a project folder.
   - Inside the folder, create a new file with a `.py` extension (e.g., `test.py`).

2. **Write a Simple Python Script:**
   - In the new Python file, write a simple script such as:
     ```python
     print("Hello, Python in VSCode!")
     ```
   - Save the file.

3. **Run the Python Script:**
   - Run the script by right-clicking anywhere in the editor and selecting "Run Python File in Terminal".
   - Alternatively, you can use the integrated terminal by typing:
     ```bash
     python <filename>.py
     ```
   - The output should appear in the terminal, confirming that VSCode is correctly configured for Python.

---

### **Troubleshooting Tips**
- **Python Not Recognized:** If VSCode does not recognize Python, ensure that Python is added to your system's PATH.
- **Multiple Python Versions:** If you have multiple versions of Python installed, be sure to select the correct interpreter in VSCode using the Command Palette.

This activity ensures that all students have Python and VSCode set up correctly, allowing them to proceed with Python development efficiently.
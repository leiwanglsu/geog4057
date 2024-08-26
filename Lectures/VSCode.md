# **Python Development in Visual Studio Code**

## Description

### **Lesson Objectives**

By the end of this lesson, students will be able to:

1. Install and configure Visual Studio Code (VSCode) for Python development.
2. Understand and use essential VSCode features for Python coding.
3. Use Python-specific extensions to enhance their development workflow.
4. Debug Python code using VSCode's integrated debugger.
5. Manage Python environments and dependencies within VSCode.

### **Prerequisites**

- Basic knowledge of Python programming.
- Familiarity with programming concepts like variables, functions, and loops.
- A computer with an internet connection.

---
## Steps

### **Section 1: Introduction to Visual Studio Code**

#### **1.1 What is VSCode?**

- A lightweight, open-source code editor developed by Microsoft.
- Benefits of using VSCode for Python development: cross-platform, customizable, and equipped with an integrated terminal.

#### **1.2 Installing VSCode**

- **Activity**: Download and install VSCode from the fficial [Visual Studio Code website](https://code.visualstudio.com/).
- How to launch VSCode 
- User interface: Activity Bar, Side Bar, Editor Group, and Status Bar.
- Explorer intergration in Windows

#### **1.3 Setting Up VSCode for Python**

- **Activity**: Install Python on your system (if not already installed).
- Configure VSCode to recognize Python by installing the Python extension.

### **Section 2: Essential Python Extensions in VSCode**

#### **2.1 Python Extension for Visual Studio Code**

- Overview of features provided by the Python extension:
  - IntelliSense (code completion)
  - Linting
  - Debugging
  - Code navigation (Go to Definition, Find References)

#### **2.2 Additional Useful Extensions**

- **Pylance**: For advanced language support, including type checking and improved IntelliSense.
- **Python Docstring Generator**: For automatically generating docstrings for functions and classes.
- **Black Formatter**: For automatic code formatting.
- **Jupyter**: For running Jupyter notebooks inside VSCode.

### **Section 3: Writing and Running Python Code in VSCode**

#### **3.1 Creating a Python Project**

- **Activity**: Create a new directory for a Python project.
- How to create a new Python file (`.py`) and write a simple Python script.

#### **3.2 Running Python Code**

- **Activity**: How run Python code directly within VSCode using the integrated terminal.
  - Highlight the `Run Python File` button.
  - Demonstrate running code from the terminal using `python <filename>.py`.

[Tutorial for Section 3](<../Tutorials/Install Python extension for VSCode.md>)

### **Section 4: Debugging Python Code in VSCode**

#### **4.1 Introduction to Debugging**

- Discuss the importance of debugging and how VSCode simplifies this process with its integrated debugger.

#### **4.2 Setting Breakpoints and Debugging**

- **Activity**: Write a Python script with an intentional bug (e.g., a division by zero error).
- Demonstrate how to set breakpoints by clicking in the gutter next to the line numbers.
- **Activity**: Run the debugger by clicking the `Run and Debug` button.
- Show how to step through code, inspect variables, and view the call stack.
- Demonstrate the use of the Debug Console for evaluating expressions.

### **Section 5: Managing Python Environments**

#### **5.1 Virtual Environments in VSCode**

- Discuss the importance of using virtual environments in Python projects.
- **Activity**: Create a virtual environment using `python -m venv env` and activate it.
- Demonstrate how to select the Python interpreter for the project in VSCode.

#### **5.2 Installing and Managing Dependencies**

- **Activity**: Show how to install Python packages using the integrated terminal (`pip install <package>`).
- Demonstrate how VSCode's Python extension detects and lists installed packages.

### **Section 6: Version Control with Git**

#### **6.1 Integrating Git with VSCode**

- Git and its importance in version control.
- **Activity**: Initialize a Git repository in the project directory.
- Demonstrate basic Git operations (commit, push, pull) directly from VSCode’s Source Control panel.

### **Section 7: Working with Jupyter Notebooks**

#### **7.1 Introduction to Jupyter Notebooks in VSCode**

- Discuss the benefits of using Jupyter notebooks for data analysis and prototyping.
- **Activity**: Open a new Jupyter notebook within VSCode using the Jupyter extension.

#### **7.2 Running and Debugging Cells**

- **Activity**: Write and run Python code cells in the Jupyter notebook.
- Demonstrate debugging within a Jupyter notebook in VSCode.


### **Materials Required**

- Computers with VSCode installed.
- Python installed on each machine.
- Internet access for downloading extensions and updates.

### **Homework/Assignments**

1. Create a simple Python project in VSCode, including at least one module and one script.
2. Write a Python script that reads from a file, processes the data, and outputs results. Include error handling and debug the script using VSCode.
3. Document the code with proper docstrings and use the Python Docstring Generator extension to assist.
4. Push the project to a GitHub repository using VSCode's Git integration.


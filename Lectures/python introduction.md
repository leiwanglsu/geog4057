## Object-oriented programming language

- Everything is an **object** in python
- An object has its **attributes** and **methods**
    - A Dog class can have an attribute of "name" and a method of "bark"
```python
dog1 = Dog()
dog1.name = "Rover"
dog1.bark()
```

- Objects are defined by **classes**
- A class is a template to create your own data types

## Dunder

- Python reserves some names for special purposes
- Names enclosed by double underscores will invoke **dunder** (magic) functions associated with it.
- Dunders (double underscore) (magic) methods are to support internal Python behaviors, such as documentation, module names, etc.
- For example ```__name__``` calls a magic function to evaluates the name of the current module. The returned value is ```"__main__"``` when the module is excuted by ```python module.py```. It becomes the module file name if the module is imported by another module. 
- ```__file__``` shows the path to the module that is currently being imported
- ```__doc__``` shows the doc string (if any)in a function or class. A doc string is the triple-quote string at the beginning of a function or class definition. 
```python
def bark():
    """
    WUFF
    """
    pass
print(bark.__doc__)
```

## Packages and modules
- In Python, the programming is also called module programming
- Module programming refers to the process to break a large programming task to separate, smaller, and more manageable subtasks or modules
- Modularizing code
    - Simplicity: focus on a specific small problem
    - Maintainability: the module can be standalone by itself in the large task
    - Resuability: the module can be reused in more than one tasks
    - Scoping: module names are used as **namespace** to avoid naming conflicts
- Packages allows for a hiearchical structuring on the module namespace using **dot notation**. 
- Package can just be a folder with multiple Python module files in it. 

## Modules

- A module focuses on a specific problem
- A module can be written in Python or c languages
- Built-in modules are intrinsically contained in the interpreter. 

### Define and use a module

mod1.py

```python
s = "Some strings here"
a = [100, 200, 300]

def foo(arg):
    print(f'arg = {arg}')

class Foo:
    pass
```
- To use mod1.py

```python
>>> import mod
>>> print(mod.s)
Some strings here
>>> mod.a
[100, 200, 300]
>>> mod.foo(['quux', 'corge', 'grault'])
arg = ['quux', 'corge', 'grault']
>>> x = mod.Foo()
>>> x
<mod.Foo object at 0x03C181F0>
```
### How Python interpreters locate a module

- What happens when you import a module
- The interpreter searches for mod1.py in the list of sources:
    - The current directory where the interpreter works with
    - The list of directories in the PYTHONPATH environment variable
    - A installation-dependent list of directories when Python was installed
- Use module.\_\_file\_\_ to show the path of the module
    - \_\_file\_\_ indicates the path to the file from which a module was loaded.
### importing a module

- ```import mod1``` will import module to your local context
- Variables and functions of mod1 are not visible unless you use mod1 as the namespace: ```mod1.s``` or ```mod1.a```
- You can also use ```from mod1 import *``` to import all items from the module to the current context
- Import some items as a different name: ```from mod1 import a as a_plus```
- Use ```dir(mod1)``` to list all items in the module
- When importing a module, the lines in it will be executed, like running the module in ```python mod1.py```
- To avoid the issue, people usually put the executable lines into a main() function and check if the module is called by Python or just being imported by another module
```python
a = [100, 200, 300]
s = "Some strings here"

def foo(arg):
    print(f'arg = {arg}')

class Foo:
    pass

if (__name__ == '__main__'):
    print('Executing as standalone script')
    print(s)
    print(a)
    foo('quux')
    x = Foo()
    print(x)
```

### reloading a module

- Modules are loaded once per interpreter session. 
- The executable codes are only executed once.
- To enforce the execution or update the module, you need to restart your interpreter session or use the reload function from the importlib module
```python
import importlib
import mod1
importlib.reload(mod1)
```



## Comments

- Use # to comment a line
- Use triple quotes to comment multiple lines 
- Comments are important to for coding, especially designing software tools
- Many people start coding by structuring comments and fill the gaps after the comments
```python
""" 
Problem: Get the computer to output a message. 
Target Users: Me 
Target System: GNU/Linux 
Interface: Command-line 
Functional Requirements: Print out a message. 
 User must be able to input some text. 
Testing: Simple run test - expecting a message to appear. 
 - expecting: message == input text 
Maintainer: maintainer@website.com 
""" 
# 1. Print out a friendly message 
print("Hello World!") 
# 2. Input some text 
# 3. Print out the text we just entered 
```


## Indendation and subgroups

- Python is very strict about indentation. 
- Python regards any space or tab at the start of a line as an 
indentation. 
- Not to mix tabs with spaces, as the interpreter thinks these are two different things
- Use blank lines to separate the code into subgroups



## Basic data types

- Basic data types refer to objects that you will use in daily life and work
- numbers, text, and logical data

### Numbers

- Numbers can be float, integer, or complex in Python
- Integer numbers have no decimal places
    - In Python, integer numbers have no limit to how long an integer can be
    - However, converting a very long integer to string might cause trouble (over 4300 digits)
    - Use underscores to make numbers readible ```1_000_000```
    - Use prefix to represent integers of different bases 
        - 0b10 # Base 2
        - 0o10 # Base 8
        - 0x10 # Base 16
    - use ```int()``` to create integer values from different representations
        - ```int("42")```
        - An ValueError exception will be raised if the representation is not a number
    - Use type() to check the type of the number
- Float point numbers
    - The float type in Python designates floating-point numbers. 
    - use 4. instead of 4 to create a float type
    - Use e or E followed by a positive or negative integer to express the number using scientific notations: ```.4e7```
    - In Python, float values are 64-bit (double-precision) numbers.
    - The maximum is approximately $ 1.8\cdot 10^{308} $
    - Any number greater than that will be indicated by the "inf" string
    - The closest a non-zero number is approximately $5 \cdot10^{-324}$. Anything closer to zero will be considered zero. 
    - Use the built-in float() function
- Complex numbers
    - Python has built-in complex numbers
    - ```number = 2 + 3j```
    - Conjugate of a complex number 
```python
number = 2 + 3j
number.conjugate()
```
### Strings

- Strings are sequence of character data to store textual data
- In Python, strings are stored as str type
- You can use literals to create strings. Use single or double quotes to create a single-line string literal 
- You can create empty strings by enclosing nonthing between the quotes
- Use len() to measure length of a string ```len("this is a string")```
- Triple-quoted strings can build multiline string literals. 

```python
"""
This is 
a multiline
string literal
"""
```
- To include a single quote character in a string, you need to use double quote to enclose the string, and vice versa

``` "The string contains a single quote(') character"```

#### Escape sequences

- Escape sequences in strings (backslash) indicate special meaning
- Use \' for the character of single quote without using double quotes: ```'This string contains a single quote (\') character'```
- ``` "In this string, the backslash should be at the end \"``` does not work in Python because ```\"``` is interpreted as "
- Double backslash means the literal backslash character '\'
- ```\t``` indicates a tab character

#### Raw string literals

- A raw string is a string that does not tralate the escape sequences. 
- To create a raw string, precede the literal with an r or R: ```r"Before \tAfter"```
- It is useful to represent Window path names such as ```r"C:\Users\Youname"``` without the need to rewrite the backslashes to double-backslashes

#### F-String literal

- F-strings is shoft for formatted Strings, which allow you to interpolate values into your strings and format them
- To build an f-string, use the prefix f or F to the string literal. 
- Use **replace field** as place holders for the values you want to embed in the string literal. Replace fields are created by the curly brackets{}
```python
name = Joshua
print(f"Hello, {name}!")
income = 123.123
print(f"Income: ${income:.2f}")
```

## Booleans

- Booleans in Python are represented by True and False 
- Booleans are also integers (True = 1 and False = 0)
```python
print(True + True)
```
- the built-in bool() function can evaluate any objects for if it is empty or 0
```python
>>> bool(0)
False

>>> bool("")
False

>>> bool("Hello")
True
```





# Basic Python knowledge

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
- For example ```__name__``` calls a magic function to evaluates the name of the current module. The returned value is ```"__main__"``` when the module is executed by ```python module.py```. It becomes the module file name if the module is imported by another module. 
- ```__file__``` shows the path to the module that is currently being imported

## Docstring

- The text at the beginning of a module, function, or a class enclosed by trip quotes are called docstrings
- The text are not executed by Python
- Docstrings are used to print help documents using the ```__doc__``` dunder
- ```__doc__``` shows the doc string (if any)in a function or class. A doc string is the triple-quote string at the beginning of a function or class definition. 

```python
def bark():
    """
    WUFF
    """
    pass
print(bark.__doc__)
```

- Google style docstrings: the specific format  in Google's documentation style guide

```python
def multiply_numbers(a, b):
    """
    Multiplies two numbers and returns the result.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The product of a and b.
    """
    return a * b
print(multiply_numbers(3,5))
```

- Docstrings in a class: use the help() function to access the docstring

```python
class ComplexNumber:
    """
    This is a class for mathematical operations on complex numbers.

    Attributes:
        real (int): The real part of the complex number.
        imag (int): The imaginary part of the complex number.
    """

    def __init__(self, real, imag):
        """
        The constructor for ComplexNumber class.

        Parameters:
            real (int): The real part of the complex number.
            imag (int): The imaginary part of the complex number.
        """
        self.real = real
        self.imag = imag

    def add(self, num):
        """
        The function to add two Complex Numbers.

        Parameters:
            num (ComplexNumber): The complex number to be added.

        Returns:
            ComplexNumber: A complex number which contains the sum.
        """
        re = self.real + num.real
        im = self.imag + num.imag

        return ComplexNumber(re, im)

# Access the Class docstring using help()
help(ComplexNumber)

# Access the method docstring using help()
help(ComplexNumber.add)
```

## Packages and modules

- In Python, the programming is also called module programming
- Module programming refers to the process to break a large programming task to separate, smaller, and more manageable subtasks or modules
- Modularizing code
    - Simplicity: focus on a specific small problem
    - Maintainability: the module can be standalone by itself in the large task
    - Reusability: the module can be reused in more than one tasks
    - Scoping: module names are used as **namespace** to avoid naming conflicts
- Packages allows for a hierarchical structuring on the module namespace using **dot notation**. 
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

## Indentation and subgroups

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
    - Use underscores to make numbers readable ```1_000_000```
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
- You can create empty strings by enclosing nothing between the quotes
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

``` "The string contains a single quote(') character" ```

#### Escape sequences

- Escape sequences in strings (backslash) indicate special meaning
- Use \' for the character of single quote without using double quotes: ``` 'This string contains a single quote (\') character' ```
- ``` "In this string, the backslash should be at the end \" ``` does not work in Python because ```\"``` is interpreted as "
- Double backslash means the literal backslash character '\'
- ```\t``` indicates a tab character

#### Raw string literals

- A raw string is a string that does not translate the escape sequences.
- To create a raw string, precede the literal with an r or R: ``` r"Before \tAfter" ```
- It is useful to represent Window path names such as ``` r"C:\Users\Youname" ``` without the need to rewrite the backslashes to double-backslashes

#### F-String literal

- F-strings is short for formatted Strings, which allow you to interpolate values into your strings and format them
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

## Python data structures

- Data structures are a way of organizing data so that it can be efficiently handled 
- Basic structures: Lists, tuples, dictionaries, sets
- Advanced structures: trees, graphs, queues, etc.

### Lists

- A python list is a set of items store by some order
  - For example, a list of all the shapefile names in the directory
        ```["county", "State", "City"]```
- The items in a list do not need to be of the same type
- A list can add new items, but it will be costly because all the elements will be shifted after it. The time complexity for insertion and deletion is *O(n)*
- Items of a list can be accessed by an index number, starting at 0 and ending at N-1
- A negative index is counting from the last element

```python
# Creating a List with 
# the use of multiple values 
List = ["GIS", "Programming", "Class"] 
print("\nList containing multiple values: ") 
print(List)

# Creating a Multi-Dimensional List 
# (By Nesting a list inside a List) 
List2 = [['GIS', 'Programming'], ['Class']] 
print("\nMulti-Dimensional List: ") 
print(List2) 

# accessing a element from the  
# list using index number 
print("Accessing element from the list") 
print(List[0])  
print(List[2]) 

# accessing a element using 
# negative indexing 
print("Accessing element using negative indexing") 
    
# print the last element of list 
print(List[-1]) 
    
# print the third last element of list  
print(List[-3])
```

#### List slicing

- List slicing is the most used technique for programmers to solve most problems
- Slicing allow for accessing a range of elements in a list
- Lists are created by using square brackets[]
- List slicing uses colon(:) to define start,end, and step of the slicing

syntax: ```List[Initial:End:Step]```

- Note, the End element is not included in the result
- For positive slicing, the first element is 0 and the last element is N-1
- For negative slicing, the last element is -1 and the first element is -N
- An negative step will produce a reserved list
- Use slicing can insert and delete list elements
- Count a list using ```len()```
- List comprehension: an expression excluded for each element along with the for loop to form a list ``` newList = [ expression(element) for element in oldList if condition ] ```

```python
# Initialize list
Lst = [50, 70, 30, 20, 90, 10, 50]

# Display list
print(Lst[1:5])
```

```[70, 30, 20, 90]```

```python
print(Lst[::])
print(Lst[-7::1])
print(Lst[::-1])
Lst[:6] = []
Lst[2:4] = ["Added", "New", "Elements",0,0]
numbers = [12, 13, 14,] 
doubled = [x *2  for x in numbers] 
print(doubled)
list = [i for i in range(11) if i % 2 == 0] 
print(list)

```

### Tuples

- Like Lists, Tuples are collections of Python objects but are immutable
- Tuple elements cannot be added or removed once created
- Tuples are created by placing a sequence of values separated by comma WITH or WITHOUT parentheses for grouping them
- If no parentheses is used on a single element-Tuple, the element must have a tailing comma
- Tuples can be created from a List and sliced similarly
- Tuples are usually used in passing function parameters and return values

```python
Tuple = ('GIS', 'Programming')
print("\nTuple with the use of String: ")
print(Tuple)
    
# Creating a Tuple with
# the use of list
list1 = [1, 2, 4, 5, 6]
print("\nTuple using List: ")
Tuple = tuple(list1)

# Accessing element using indexing
print("First element of tuple")
print(Tuple[0])

# Accessing element from last
# negative indexing
print("\nLast element of tuple")
print(Tuple[-1])
  
print("\nThird last element of tuple")
print(Tuple[-3])
```

### Sets

- Sets are unordered collections of data that is mutable and does not allow duplications
- Sets are used to include membership testing and eliminating duplicated entries
- Sets are indicated by curly braces {}

```python
Set = set([1, 2, 'GIS', 4, 'For', 6, 'Programming']) 
print("\nSet with the use of Mixed Values") 
print(Set) 

# Accessing element using 
# for loop 
print("\nElements of set: ") 
for i in Set: 
    print(i, end =" ") 
print()

# Checking the element 
# using in keyword 
print("GIS" in Set) 
```

### Dictionaries

- Python **dictionary** is a collection of data made by key:value pairs grouped by curly braces{}
- Keys are used to index the elements and therefore cannot have duplication
- Use enumerate() to access elements 
- Dictionary comprehension: create dictionaries using simple expressions

```{key: value for (key, value) in iterable}```

```python
Dict = {'Name': 'GIS', 1: [1, 2, 3, 4]}
print("Creating Dictionary: ")
print(Dict)

# accessing a element using key 
print("Accessing a element using key:") 
print(Dict['Name']) 

# accessing a element using get() 
# method 
print("Accessing a element using get:") 
print(Dict.get(1)) 

# enumerate()
employees = {'E001': 'James', 'E002': 'Bobby', 'E003': 'Charles', 'E004': 'Vincent'}
for index, (key, value) in enumerate(employees.items()):
    print(f"Index {index}: ID = {key}, Name = {value}")
# or using key 
index = 0
for key in employees:
    value = employees[key]
    print(f"Index of '{key}': {value} is {index}")
    index += 1


# creation using Dictionary comprehension
myDict = {x: x**2 for x in [1,2,3,4,5]}
print(myDict)
# comprehension
myDict = {x: x**2 for x in [1,2,3,4,5]}
print (myDict)
```

## If Else conditional statements

- The If-Else statement provides a way to execute different blocks based on specific conditions

```python
if(condition):
    statement
elif (condition):
    statement
.
.
else:
    statement
```

- if condition can be used in List comprehension

```python
# Initializing list
List = [367, 111, 562, 945, 6726, 873]

# Using the function on odd elements of the list
newList = [digitSum(i) for i in List if i & 1]

# Displaying new list
print(newList)
```

## For loops in Python

- For Loop is a special type of loop statement that is used for sequential traversal
- For Loop only implement the collection-based iteration
- Syntax 

```python
for var in iterable:
    #statement
    pass
```

- For Loop with String

```python
# Iterating over a String
print("String Iteration")

s = "Programming"
for i in s:
    print(i)
```

- For loop with range

```python
for i in range(0, 10, 2):
    print(i)
```

- For Loop with Enumerate(): enumerate will iterate over an iterable and provides the index

```python
list1 = ["GIS", "Programming", "Class"]

for count, ele in enumerate(l1):
    print (count, ele)
```

- For Loop comprehension

```python
Numbers =[x for x in range(11)]
print(Numbers)
```

- For Loop with dictionary

```python
dict = {1:"GIS",2:"Programming",3:"Class"}
for key in dict:
    print(f"The key is {key}, and the value is {dict[key]}")
```

- Continue, break,and pass
    - continue: skip the rest of the block and move on to the next iteration
    - break: stop the iteration
    - pass: do nothing

```python
for letter in 'gisprogramming':

    if letter == 'g' or letter == 's':
        continue
    print('Current Letter :', letter)

for letter in 'gisprogramming':

    if letter == 'g' or letter == 's':
        break
    print('Current Letter :', letter)
for letter in 'gisprogramming':

    if letter == 'g' or letter == 's':
        pass
    print('Current Letter :', letter)
```

## Functions

### Overview of functions

- Functions are organized and reusable piece of code for a specific purpose
- Using functions can increase modulation and reusability of your code
- Python has many builtin functions such as print(), int(), type()
- Most functions used in Python programming are user-defined functions because they extend the functions of Python
- Functions are defined to take some **parameters**. **Arguments** are the values passed inside the parenthesis of the function to match the parameters

### Call functions 

- To uses or call a function, you just need to use the function name followed by a pair of parentheses and arguments in the parentheses ```print("Hello World")```
- In the above example, print is the name and "Hello World" is an argument of the str type sent to the function print.
- If you provide a wrong list of arguments, the function will return with error

### Type of arguments

- Python supports various types of arguments to be passed at the time of function call
- Default arguments
- Keyword arguments (named)
- Positional arguments
- Variable-length arguments

#### Positional arguments

- Positional arguments during a function call are assigned to the parameters according to their position in the list
- By changing the position or you forget the order of the positions, the values can be used in wrong places
  
```python
def nameAge(name, age):
    print("Hi, I am", name)
    print("My age is ", age)


# You will get correct output because 
# argument is given in order
print("Case-1:")
nameAge("SJ", 27)
# You will get incorrect output because
# argument is not in order
print("\nCase-2:")
nameAge(27, "SJ")
```

#### Default arguments

- A default argument is a parameter that assumes a default value if the argument is not provided by the user
- A default argument is define by assigning a value for the parameter

```python
def myFun(x, y=50, z = 30):
    print("x: ", x)
    print("y: ", y)
    print("z: ", z)

myFun(10)
myFun(10,20)
myFun(10,20,30)
```

- If a parameter has a default value, all the parameters to its right must have default values.
- If a parameter does not have a default value, it is required.
- All required parameters must be placed before default parameters

```python
def myFun(x, y=50, z):
    print("x: ", x)
    print("y: ", y)
    print("z: ", z)
myFun(10)
```

```SyntaxError: non-default argument follows default argument```

#### Keyword arguments

- User can specifically assign values to the parameters by their names. These are called keyword arguments or named arguments
- Using keyword arguments do not need to follow their order in the parameter list

```python
def myFun(x, y = 60, z = 10):
    print("x: ", x)
    print("y: ", y)
    print("z: ", z)
myFun(z = 5, x = 10)
```

#### Arbitrary and Arbitrary Keyword Arguments

##### Arbitrary argument: *args

- If you don't know how many arguments the user will send to your function, you can use an asterisk before the parameters
- This allows for a variable-length non-keyword argument or arbitrary argument
- The argument received by your function is a tuple of arguments

```python
def myFun(*argv):
    print(type(argv))
    for arg in argv:
        print(arg)

myFun('Hello', 'Welcome', 'to', 'GIS')
```

##### Arbitrary keyword argument: **kwargs

- If you don't know how many keyword arguments to be passed to your function, add two asterisk: ** before the parameter name in the function definition
- This way the function will receive a dictionary of arguments and can process it accordingly

```python
def my_function(**kid):
    print(type(kid))

    print("His last name is " + kid["lname"])

my_function(fname = "Tobias", lname = "Refsnes")
```

#### Pass by Reference 

- As Java, every variable name in Python is a reference to an object
- When passing a variable to a function, a copy of the **reference** is created in the function referring to the same object

```python
def myFun(x):
    x[0] = 20

# Driver Code (Note that lst is modified
# after function call.
lst = [10, 11, 12, 13, 14, 15]
myFun(lst)
print(lst)

```

- The reference is broken if the function assigns the variable to a new object

```python
def myFun(x):

    # After below line link of x with previous
    # object gets broken. A new object is assigned
    # to x.
    x = [20, 30, 40]


# Driver Code (Note that lst is not modified
# after function call.
lst = [10, 11, 12, 13, 14, 15]
myFun(lst)
print(lst)
```

### Docstring

- Add docstring at the beginning of your function definition
- It is optional but considered a good practice

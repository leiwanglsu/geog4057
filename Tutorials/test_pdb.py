def add_numbers(a, b):
    import pdb; pdb.set_trace()  # Set a breakpoint here
    return a + b

def main():
    num1 = 10
    num2 = "20"  # Intentional error: num2 should be an integer
    print("num1:", num1)
    print("num2:", num2)
    result = add_numbers(num1, num2)
    print("Result:", result)

if __name__ == "__main__":
    main()
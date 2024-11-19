def example_function(x, y):
    result = x + y
    import pdb; pdb.set_trace()  # Start debugger here

    result *= 2
    print(result)
    return result

print('pdb debugging')
example_function(3, 4)
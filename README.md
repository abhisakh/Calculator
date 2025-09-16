# Python Calculator
===========================
## Description:
------------
This is a command-line calculator program written in Python. It allows the user
to perform a series of basic arithmetic operations by entering expressions in
the form of: <number> <operator> <number>

The program supports the following operators:
    +  : Addition
    -  : Subtraction
    *  : Multiplication
    /  : Division (returns float)
    ~  : Floor Division (returns quotient and remainder)

## Features:
---------
- Handles calculations of multiple digit numbers
- Handles multiple calculations in a single run
- Ignores extra spaces in user input
- Prevents division by zero
- Checks return type of operations (single vs multiple results)
- Clean, modular function design for ease of maintenance
- Displays meaningful output based on the operation

## Limitations:
------------
- Only supports integer inputs
- Does not support decimal numbers, negative numbers, or parentheses
- Only handles expressions in the format: num1 operator num2

## Structure(FLOW):
---------------
1. Getting user input (number of calculations) → input()
2. Looping over the number of calculations → calculate_multiple(num)
3. For each calculation:
   - Getting calculation expression input → input() inside calculate_multiple
   - Parsing input into components → split_expression(text_input)
   - Performing calculation → calculate(num1, operator, num2)
   - Printing results based on return values → print_function(result)
  
### 👤 Author

- **Abhisakh Sarma** - [GitHub Profile]((https://github.com/abhisakh)
```text
========================================================================
```

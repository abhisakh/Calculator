"""
==============================================================================
                              PYTHON CALCULATOR
==============================================================================
Description:
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

Features:
---------
- Handles calculations of multiple digit numbers
- Handles multiple calculations in a single run
- Ignores extra spaces in user input
- Prevents division by zero
- Checks return type of operations (single vs multiple results)
- Clean, modular function design for ease of maintenance
- Displays meaningful output based on the operation

Limitations:
------------
- Only supports integer inputs
- Does not support decimal numbers, negative numbers, or parentheses
- Only handles expressions in the format: num1 operator num2

Structure(FLOW):
---------------
1. Getting user input (number of calculations) → input()
2. Looping over the number of calculations → calculate_multiple(num)
3. For each calculation:
   - Getting calculation expression input → input() inside calculate_multiple
   - Parsing input into components → split_expression(text_input)
   - Performing calculation → calculate(num1, operator, num2)
   - Printing results based on return values → print_function(result)
==============================================================================
Author: Abhisakh Sarma
==============================================================================
"""

#==================== FUNCTION TO PARSE INPUT ====================
def split_expression(text_input):
    """
    Splits the input string into two numbers and one operator.
    Returns (num1, operator, num2) if valid, otherwise (None, None, None).
    """
    operators = "+-*/~"
    for i, char in enumerate(text_input):
        if char in operators:
            num1 = text_input[:i].strip()
            operator = char
            num2 = text_input[i+1:].strip()

            # Validate numbers
            if not (num1.isdigit() and num2.isdigit()):
                return None, None, None
            return num1, operator, num2
    return None, None, None


#==================== FUNCTION TO PERFORM SINGLE CALCULATION ====================
def calculate(num1, operator, num2):
    """
    Performs calculation based on operator and integer inputs.
    Returns result or tuple (quotient, remainder) for '~'.
    """
    first_number = int(num1)
    second_number = int(num2)

    if operator == "+":
        return first_number + second_number
    elif operator == "-":
        return first_number - second_number
    elif operator == "*":
        return first_number * second_number
    elif operator == "/":
        if second_number == 0:
            return "--Error: Division by zero is not possible--"
        return first_number / second_number
    elif operator == "~":
        if second_number == 0:
            return "--Error: Division by zero is not possible--"
        return (first_number // second_number, first_number % second_number)
    else:
        return "--Error: Unsupported operator--"


#==================== FUNCTION TO PRINT RESULTS ====================
def print_function(result):
    """
    Prints the calculation result(s) based on the return type.
    If result is a tuple, prints quotient and remainder.
    """
    if isinstance(result, tuple):
        print(f"The answer is {result[0]}")
        print(f"The remainder is {result[1]}")
    else:
        print(f"The answer is {result}")


#==================== FUNCTION TO HANDLE MULTIPLE CALCULATIONS ====================
def calculate_multiple(num):
    """
    Handles multiple calculations requested by the user.
    Performs input parsing, calculation, and printing for each calculation.
    """
    try:
        num = int(num)
    except ValueError:
        print("--Error: Number of calculations must be an integer--")
        return

    for _ in range(num):
        user_input1 = input("What do you want to calculate? (e.g. 12 + 5) ")
        num1, operator, num2 = split_expression(user_input1)

        if num1 is None:
            print("--Error: Invalid expression. Use format: num1 operator num2 (e.g. 5 + 3)--")
            continue

        result = calculate(num1, operator, num2)
        print_function(result)


#==================== PROGRAM START ====================
if __name__ == "__main__":
    print("Welcome to the Python calculator!")
    user_input2 = input("How many calculations do you want to do? ")
    calculate_multiple(user_input2)

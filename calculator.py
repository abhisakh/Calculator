"""
==============================================================================
                              PYTHON CALCULATOR
==============================================================================
Description:
------------
This is a command-line calculator program written in Python. It allows the user
to perform a series of basic arithmetic operations by entering expressions in
the form: <number> <operator> <number>

The program supports the following operators:
    +  : Addition
    -  : Subtraction
    *  : Multiplication
    /  : Division (returns float)
    ~  : Floor Division (returns quotient and remainder)
    %  : Modulus
    ^  : Power

Features:
---------
- Handles integers and floating-point numbers
- Supports negative numbers
- Handles extra/missing spaces in input (e.g., "2*   6")
- Prevents division/modulus by zero
- Supports multiple calculations per session
- Interprets and validates single binary operations
- Displays separate output for quotient and remainder (with '~')
- Clean, modular function design for ease of maintenance
- ANSI-colored terminal output for better user experience

Limitations:
------------
- Does not support parentheses or expression chaining (e.g., "3 + 2 * 4")
- Only handles expressions in the format: num1 operator num2
- Does not retain history or save output to files

Structure (FLOW):
-----------------
1. Getting user input (number of calculations) → input()
2. Looping over the number of calculations → calculate_multiple(num)
3. For each calculation:
   - Getting calculation expression input → input() inside calculate_multiple
   - Parsing input into components → split_expression(text_input)
   - Performing calculation → calculate(num1, operator, num2)
   - Printing results based on return values → print_function(result)

==============================================================================
Author: Abhisakh Sarma
Updated: September 2025
==============================================================================
"""

import re

#==================== FUNCTION TO PARSE INPUT ====================
def split_expression(text_input):
    """
    Splits the input string into two numbers and one operator.
    Returns (num1, operator, num2) if valid, otherwise (None, None, None).
    """
    # Support: +, -, *, /, %, ~, ^ (basic power)
    operators = r'[\+\-\*/%~^]'

    # Remove spaces around
    text_input = text_input.strip()

    # Use regex to extract left operand, operator, and right operand
    match = re.match(r'^\s*(-?\d+(\.\d+)?)\s*([' + re.escape("+-*/%~^") + r'])\s*(-?\d+(\.\d+)?)\s*$', text_input)
    if not match:
        return None, None, None

    num1, _, operator, num2, _ = match.groups()
    return num1, operator, num2


#==================== FUNCTION TO PERFORM SINGLE CALCULATION ====================
def calculate(num1, operator, num2):
    """
    Performs calculation based on operator and float/int inputs.
    Returns result or tuple (quotient, remainder) for '~'.
    """
    try:
        first_number = float(num1)
        second_number = float(num2)
    except ValueError:
        return "\033[91m--Error: Non-numeric input--\033[0m"

    if operator == "+":
        return first_number + second_number
    elif operator == "-":
        return first_number - second_number
    elif operator == "*":
        return first_number * second_number
    elif operator == "/":
        if second_number == 0:
            return "\033[91m--Error: Division by zero is not possible--\033[0m"
        return round(first_number / second_number, 5)
    elif operator == "%":
        if second_number == 0:
            return "\033[91m--Error: Modulus by zero is not possible--\033[0m"
        return first_number % second_number
    elif operator == "~":
        if second_number == 0:
            return "\033[91m--Error: Division by zero is not possible--\033[0m"
        return (int(first_number) // int(second_number), int(first_number) % int(second_number))
    elif operator == "^":
        return first_number ** second_number
    else:
        return "\033[91m--Error: Unsupported operator--\033[0m"


#==================== FUNCTION TO PRINT RESULTS ====================
def print_function(result):
    """
    Prints the calculation result(s) based on the return type.
    If result is a tuple, prints quotient and remainder.
    """
    if isinstance(result, tuple):
        print(f"\033[92mThe answer is {result[0]}\033[0m")
        print(f"\033[94mThe remainder is {result[1]}\033[0m")
    else:
        print(f"\033[92mThe answer is {result}\033[0m")


#==================== FUNCTION TO HANDLE MULTIPLE CALCULATIONS ====================
def calculate_multiple(num):
    """
    Handles multiple calculations requested by the user.
    Performs input parsing, calculation, and printing for each calculation.
    """
    try:
        num = int(num)
    except ValueError:
        print("\033[91m--Error: Number of calculations must be an integer--\033[0m")
        return

    for _ in range(num):
        user_input1 = input("\033[93mWhat do you want to calculate? (e.g. 12 + 5 or type 'exit') \033[0m").strip()

        if user_input1.lower() == "exit":
            print("\033[94mGoodbye!\033[0m")
            break

        num1, operator, num2 = split_expression(user_input1)

        if num1 is None:
            print("\033[91m--Error: Invalid expression. Use format: num1 operator num2 (e.g. 5 + 3)--\033[0m")
            continue

        result = calculate(num1, operator, num2)
        print_function(result)


#==================== PROGRAM START ====================
if __name__ == "__main__":
    print("\033[94mWelcome to the Python calculator!\033[0m")
    user_input2 = input("\033[93mHow many calculations do you want to do? \033[0m")
    calculate_multiple(user_input2)

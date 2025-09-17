"""
==============================================================================
                             PYTHON CALCULATOR
==============================================================================

📝 Description:
--------------
A simple command-line calculator built in Python that allows users to perform
basic arithmetic operations by entering expressions in the format:

    <number> <operator> <number>

Supported Operators:
    +   → Addition
    -   → Subtraction
    *   → Multiplication
    /   → Division (returns float)
    ~   → Floor Division (returns quotient and remainder)

✨ Features:
-----------
- Accepts multi-digit integer inputs
- Supports multiple calculations in a single session
- Ignores extra spaces in user input
- Detects and prevents division by zero
- Differentiates between single and multiple return values
- Modular, clean function design for better readability and maintenance
- Outputs results in a user-friendly format

⚠️ Limitations:
---------------
- Only supports **positive integer inputs**
- Does not support:
    • Decimal (float) numbers
    • Negative numbers
    • Parentheses or complex expressions
- Input must strictly follow the format: num1 operator num2

🔁 Program Flow:
---------------
1. Prompt user for number of calculations → `input()`
2. Loop over that number → `calculate_multiple(num)`
3. For each calculation:
    - Accept expression from user → `input()` inside `calculate_multiple()`
    - Parse the expression → `split_expression(text_input)`
    - Perform the calculation → `calculate(num1, operator, num2)`
    - Display the result → `print_function(result)`

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
            return "\033[91m--Error: Division by zero is not possible--\033[0m"
        return first_number / second_number
    elif operator == "~":
        if second_number == 0:
            return "\033[91m--Error: Division by zero is not possible--\033[0m"
        return (first_number // second_number, first_number % second_number)
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
        user_input1 = input("\033[93mWhat do you want to calculate? (e.g. 12 + 5) \033[0m")
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

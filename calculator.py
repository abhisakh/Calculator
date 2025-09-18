"""
==============================================================================
                              PYTHON CALCULATOR (LEVEL 1)
==============================================================================
Description:
------------
This is a command-line calculator that supports full arithmetic expressions
including parentheses, operator precedence, float/negative numbers, and
common math functions (like abs, round, sqrt, etc.).

Features:
---------
- Supports full expressions: e.g., 3 + 4 * (2 - 1)
- Handles floating-point and negative numbers
- Supports common math functions: sqrt(), abs(), round(), etc.
- Gracefully handles division/modulus by zero
- Exit anytime by typing 'exit'

Operators & Functions:
----------------------
+    : Addition
-    : Subtraction
*    : Multiplication
/    : Division (float)
**   : Exponentiation
%    : Modulus
()   : Grouping
Functions: abs(), round(), pow(), sqrt(), sin(), cos(), log(), etc.

Limitations:
------------
- No support for variable assignment yet
- No memory/history storage yet

==============================================================================
Author: Abhisakh Sarma
Updated: Level 1 Sept 2025
==============================================================================
"""

import math

#==================== SAFE EVALUATION ENVIRONMENT ====================
# Only allow safe math functions
safe_functions = {
    k: v for k, v in math.__dict__.items() if not k.startswith("__")
}
safe_functions.update({
    'abs': abs,
    'round': round,
    'pow': pow,
})

def evaluate_expression(expression):
    """
    Safely evaluates a math expression using only allowed functions.
    """
    try:
        # Evaluate using restricted environment
        result = eval(expression, {"__builtins__": {}}, safe_functions)
        return result
    except ZeroDivisionError:
        return "\033[91m--Error: Division or modulus by zero--\033[0m"
    except Exception as e:
        return f"\033[91m--Error: Invalid expression ({e})--\033[0m"

#==================== HANDLE MULTIPLE CALCULATIONS ====================
def calculate_multiple(num):
    """
    Repeats expression evaluation 'num' times based on user input.
    """
    try:
        num = int(num)
    except ValueError:
        print("\033[91m--Error: Please enter a valid integer for number of calculations--\033[0m")
        return

    for _ in range(num):
        user_input = input("\033[93mEnter expression (or type 'exit'): \033[0m").strip()

        if user_input.lower() == "exit":
            print("\033[94mGoodbye!\033[0m")
            break

        result = evaluate_expression(user_input)
        print(f"\033[92mThe answer is: {result}\033[0m")

#==================== MAIN ====================
if __name__ == "__main__":
    print("\033[96m" + "="*78)
    print(" " * 28 + "PYTHON CALCULATOR - LEVEL 1")
    print("="*78 + "\033[0m")

    user_input = input("\033[93mHow many calculations do you want to do? \033[0m")
    calculate_multiple(user_input)

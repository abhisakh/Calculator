"""
==============================================================================
                           PYTHON CALCULATOR (LEVEL 2)
==============================================================================
Description:
------------
This is a stateful command-line calculator that supports:
- Full expressions
- Variables
- Memory commands
- Trigonometric functions (including degree-based ones)
- Math functions and safe evaluation
- Command handling (help, history, vars, etc.)

==============================================================================
Author: Abhisakh Sarma
Updated: Level 2 - Sept 2025
==============================================================================
"""

import math

# ==================== ENVIRONMENT SETUP ====================
# Allow safe math functions
safe_functions = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}

# Add custom safe functions
safe_functions.update({
    'abs': abs,
    'round': round,
    'pow': pow,

    # Trigonometric in degrees
    'sind': lambda x: math.sin(math.radians(x)),
    'cosd': lambda x: math.cos(math.radians(x)),
    'tand': lambda x: math.tan(math.radians(x)),

    # Degree/radian conversion
    'radians': math.radians,
    'degrees': math.degrees
})

# ==================== GLOBAL STATE ====================
variables = {}       # user-defined variables
history = []         # list of all expressions/results
memory = None        # for 'store' and 'recall'
last_result = None   # most recent result

# ==================== EVALUATOR ====================
def evaluate_expression(expression):
    """
    Evaluates an arithmetic expression or variable assignment.
    """
    global last_result, memory

    try:
        # Handle assignment (e.g. x = 5)
        if "=" in expression and "==" not in expression:
            var_name, expr = expression.split("=", 1)
            var_name = var_name.strip()
            expr = expr.strip()
            value = eval(expr, {"__builtins__": {}}, {**safe_functions, **variables})
            variables[var_name] = value
            last_result = value
            return f"\033[94m{var_name} = {value}\033[0m"

        # Regular expression evaluation
        result = eval(expression, {"__builtins__": {}}, {**safe_functions, **variables})
        last_result = result
        return result

    except ZeroDivisionError:
        return "\033[91m--Error: Division or modulus by zero--\033[0m"
    except NameError as e:
        return f"\033[91m--Error: Unknown variable or function: {e}--\033[0m"
    except Exception as e:
        return f"\033[91m--Error: Invalid expression: {e}--\033[0m"

# ==================== COMMAND HANDLER ====================
def handle_command(command):
    """
    Handles internal commands like help, store, recall, history, etc.
    """
    global memory, last_result

    cmd = command.lower().strip()

    if cmd == "help":
        print("""
\033[96mAvailable Commands:\033[0m
  \033[93mexit\033[0m     → Exit the calculator
  \033[93mhelp\033[0m     → Show this help message
  \033[93mhistory\033[0m  → Show previous calculations
  \033[93mstore\033[0m    → Store last result in memory
  \033[93mrecall\033[0m   → Recall stored result
  \033[93mclear\033[0m    → Clear memory and variables
  \033[93mvars\033[0m     → Show all defined variables

\033[96mTrig Functions:\033[0m
  \033[93msin(x)\033[0m   → x in radians
  \033[93msind(x)\033[0m  → x in degrees
  \033[93mcosd(x)\033[0m  → x in degrees
  \033[93mtand(x)\033[0m  → x in degrees
  \033[93mdegrees(x)\033[0m → Convert radians to degrees
  \033[93mradians(x)\033[0m → Convert degrees to radians
""")

    elif cmd == "exit":
        print("\033[94mGoodbye!\033[0m")
        return "exit"

    elif cmd == "history":
        if not history:
            print("\033[90m-- No history available --\033[0m")
        else:
            print("\033[96m--- History ---\033[0m")
            for i, h in enumerate(history, 1):
                print(f"{i}: {h}")

    elif cmd == "store":
        if last_result is not None:
            memory = last_result
            print(f"\033[92mStored: {memory}\033[0m")
        else:
            print("\033[90m-- Nothing to store --\033[0m")

    elif cmd == "recall":
        if memory is not None:
            print(f"\033[92mRecalled: {memory}\033[0m")
            return str(memory)
        else:
            print("\033[90m-- No memory stored --\033[0m")

    elif cmd == "clear":
        variables.clear()
        memory = None
        print("\033[92mMemory and variables cleared.\033[0m")

    elif cmd == "vars":
        if not variables:
            print("\033[90m-- No variables defined --\033[0m")
        else:
            print("\033[96m--- Variables ---\033[0m")
            for var, val in variables.items():
                print(f"{var} = {val}")

    else:
        print("\033[91m-- Unknown command. Type 'help' to see available commands --\033[0m")

# ==================== MAIN LOOP ====================
def calculate_loop():
    """
    Main REPL loop for continuous input and evaluation.
    """
    while True:
        user_input = input("\033[93mEnter expression or command: \033[0m").strip()

        if user_input == "":
            continue

        # Handle built-in commands
        if user_input.lower() in ["exit", "help", "store", "recall", "history", "clear", "vars"]:
            result = handle_command(user_input)
            if result == "exit":
                break
            elif isinstance(result, str):  # e.g., recall returns value
                user_input = result
            else:
                continue

        # Evaluate mathematical expression
        result = evaluate_expression(user_input)
        history.append(f"{user_input} = {result}")
        print(f"\033[92mThe answer is: {result}\033[0m")

# ==================== PROGRAM START ====================
if __name__ == "__main__":
    print("\033[96m" + "=" * 78)
    print(" " * 28 + "PYTHON CALCULATOR - LEVEL 2")
    print("=" * 78 + "\033[0m")
    print("Type \033[93mhelp\033[0m to see available commands.\n")
    calculate_loop()

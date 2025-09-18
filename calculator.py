"""
==============================================================================
                           PYTHON CALCULATOR - LEVEL 3A (GUI)
==============================================================================
Description:
------------
This GUI calculator uses Tkinter + ttk with a dark theme and glowing colored buttons.
Features:
- Larger buttons with glowing hover effect
- High contrast bright display area
- Support arithmetic, variables, trig functions (degrees/radians)
- Editable input field for expressions

Features:
---------
- GUI interface with clickable buttons and display field
- Supports basic operators: +, -, *, /, %, parentheses
- Supports floating point numbers and variable assignment (e.g., x = 10)
- Includes safe math functions: sin, cos, tan (degree versions: sind, cosd, tand)
- Displays results and error messages cleanly
- Clear ('C') and Equals ('=') buttons for easy use

Limitations:
------------
- Expression parsing is done using Python's eval with limited safe functions,
  so complex expressions or unsafe code are not supported.
- No history or memory buttons (can be added later)
- Only simple variable assignment supported

Structure (FLOW):
-----------------
1. Start program and open GUI window.
2. User inputs expression by clicking buttons (numbers/operators).
3. Expression is displayed in the entry widget.
4. When user clicks '=' button:
    - The current expression string is sent to the evaluator.
    - If expression contains '=', treat as variable assignment:
      * Split variable and value.
      * Evaluate value using safe math functions and stored variables.
      * Store variable and return result.
    - Else, evaluate expression safely using allowed math functions and variables.
    - Handle any exceptions (zero division, syntax errors) gracefully.
    - Display result or error in the entry field.
5. If user clicks 'C', clear the current expression.
6. Repeat steps 2-5 until user closes the window.
==============================================================================
Author:
-------
Abhisakh Sarma

==============================================================================
"""

import tkinter as tk
from tkinter import ttk
import math

# Safe functions for eval
safe_functions = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
safe_functions.update({
    'abs': abs,
    'round': round,
    'pow': pow,
    'sind': lambda x: math.sin(math.radians(x)),
    'cosd': lambda x: math.cos(math.radians(x)),
    'tand': lambda x: math.tan(math.radians(x)),
    'radians': math.radians,
    'degrees': math.degrees,
})

variables = {}
last_result = None

def evaluate_expression(expression: str):
    global last_result
    try:
        if "=" in expression and "==" not in expression:
            var, val = expression.split("=", 1)
            var = var.strip()
            val = val.strip()
            result = eval(val, {"__builtins__": {}}, {**safe_functions, **variables})
            variables[var] = result
            last_result = result
            return result
        else:
            result = eval(expression, {"__builtins__": {}}, {**safe_functions, **variables})
            last_result = result
            return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {e}"

class GlowingButton(ttk.Button):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.default_style = kw.get('style', 'Glowing.TButton')
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['style'] = self.default_style.replace('.TButton', 'Hover.TButton')

    def on_leave(self, e):
        self['style'] = self.default_style

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Calculator")
        self.root.geometry("420x570")
        self.root.configure(bg="#121212")  # Dark background
        self.root.resizable(False, False)

        # Styles
        style = ttk.Style(self.root)
        style.theme_use('clam')

        # Display Entry style
        style.configure('Display.TEntry',
                        foreground='white',
                        background='#1E1E1E',
                        fieldbackground='#1E1E1E',
                        font=('Segoe UI', 26, 'bold'),
                        borderwidth=2,
                        relief='sunken')

        # Cyan glowing style for digits/functions
        style.configure('Cyan.TButton',
                        font=('Segoe UI', 18, 'bold'),
                        padding=15,
                        foreground='#00fff7',
                        background='#121212',
                        borderwidth=2,
                        relief='raised')

        style.map('CyanHover.TButton',
                  foreground=[('active', '#00ffff')],
                  background=[('active', '#00aaaa')],
                  relief=[('active', 'groove')])

        # Orange glowing style for operators
        style.configure('Orange.TButton',
                        font=('Segoe UI', 20, 'bold'),
                        padding=15,
                        foreground='#ff9500',
                        background='#121212',
                        borderwidth=2,
                        relief='raised')

        style.map('OrangeHover.TButton',
                  foreground=[('active', '#ffb347')],
                  background=[('active', '#cc7a00')],
                  relief=[('active', 'groove')])

        # Main display entry
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(root, textvariable=self.entry_var, justify='right', style='Display.TEntry')
        self.entry.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=15, pady=20, ipady=20)

        for i in range(5):
            root.grid_columnconfigure(i, weight=1)
        for i in range(1, 8):
            root.grid_rowconfigure(i, weight=1)

        self.create_buttons()

    def create_buttons(self):
        # Define which buttons are operators
        operators = {'/', '*', '-', '+', '%', '=', 'C', '(', ')'}
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('C', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('(', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), (')', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('%', 4, 2), ('+', 4, 3), ('=', 4, 4),
            ('sin(', 5, 0), ('cos(', 5, 1), ('tan(', 5, 2), ('sin d(', 5, 3), ('cos d(', 5, 4),
            ('tan d(', 6, 0), ('x', 6, 1), ('y', 6, 2), ('z', 6, 3), ('=', 6, 4)
        ]

        for (text, row, col) in buttons:
            if text in operators:
                style = 'Orange.TButton'
            else:
                style = 'Cyan.TButton'

            btn = GlowingButton(self.root, text=text, style=style)
            btn.default_style = style
            btn.config(command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

    def on_button_click(self, char):
        # Map displayed button text to actual function call
        mapping = {
            'sin d(': 'sind(',
            'cos d(': 'cosd(',
            'tan d(': 'tand('
        }
        if char in mapping:
            char = mapping[char]

        if char == "=":
            expr = self.entry_var.get()
            result = evaluate_expression(expr)
            self.entry_var.set(str(result))
        elif char == "C":
            self.entry_var.set("")
        else:
            current = self.entry_var.get()
            new_expr = current + char
            self.entry_var.set(new_expr)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
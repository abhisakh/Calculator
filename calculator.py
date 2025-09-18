"""
==============================================================================
                           PYTHON CALCULATOR - LEVEL 4 (Web App)
==============================================================================
Description:
------------
This is a web-based Python calculator implemented as a single-file Flask app.
It provides a rich user interface with glowing colorful buttons and supports
advanced arithmetic including trigonometric functions in both radians and degrees,
variable assignment, and error handling.

The app serves an HTML/CSS/JS frontend and exposes a backend calculation API
that safely evaluates expressions submitted by the user.

Run the app and open http://127.0.0.1:5000/ in your browser to use the calculator.

External Modules:
-----------------
- Flask (web framework)

Install Flask if not already installed:
    pip install flask

Functionality:
--------------
- Basic arithmetic: +, -, *, /, %, power (pow function)
- Trigonometry: sin, cos, tan (radians) and sind, cosd, tand (degrees)
- Variable assignment and usage (e.g. x = 10, x * 2)
- Handles decimal numbers, parentheses, and complex expressions
- Prevents unsafe code execution by restricting available functions and no built-ins
- Shows meaningful error messages for invalid input or zero division
- Responsive UI with glowing colored buttons and input field
- Clear button and Enter key to calculate

==============================================================================
Program Flow:
--------------
1. User opens web page (GET `/`):
   - Server returns embedded HTML page with calculator UI.
2. User enters expression and clicks 'Calculate' (or presses Enter):
   - JavaScript sends expression to backend via POST `/calculate`.
3. Backend receives expression:
   - Parses and safely evaluates it using `eval` in restricted context.
   - Supports variables saved in memory.
   - Returns result or error message as JSON.
4. Frontend displays the result below input field.
5. User can clear input, continue calculations, or assign variables.

==============================================================================
Code Structure:
---------------
- Imports & Setup: flask, math, safe function dictionary, variable store
- Function: evaluate_expression(expr) - safely evaluates or assigns variables
- Flask Routes:
  - `/` : serves HTML/CSS/JS interface (rendered inline)
  - `/calculate` : accepts JSON POST with expression, returns JSON result
- Main block: runs app on localhost:5000 with debug mode

==============================================================================
Author:
-------
Abhisakh Sarma
==============================================================================
"""

from flask import Flask, request, jsonify, render_template_string
import math

app = Flask(__name__)

# Dictionary of safe math functions, including trig in degrees
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

# In-memory variable store
variables = {}

def evaluate_expression(expr):
    """
    Safely evaluates a mathematical expression.

    Supports variable assignment of the form 'var = expression'.

    Returns either the result of the expression or a meaningful error string.
    """
    try:
        # Check for assignment, but avoid comparison '=='
        if "=" in expr and "==" not in expr:
            var, val = expr.split("=", 1)
            var = var.strip()
            val = val.strip()
            # Only allow valid variable names (letters, digits, underscore, but not starting with digit)
            if not var.isidentifier():
                return "Error: Invalid variable name"
            # Evaluate right-hand side expression safely
            result = eval(val, {"__builtins__": {}}, {**safe_functions, **variables})
            # Store variable
            variables[var] = result
            return f"{var} = {result}"
        else:
            # Evaluate expression directly
            result = eval(expr, {"__builtins__": {}}, {**safe_functions, **variables})
            return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {e}"

# Embedded HTML, CSS and JavaScript frontend (glowing theme with improved button sizes)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Python Web Calculator</title>
<style>
  body {
    background: #121212;
    color: white;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0;
    padding: 20px;
  }
  #calculator {
    background: #1e1e1e;
    padding: 25px 30px 35px;
    border-radius: 15px;
    width: 360px;
    box-shadow: 0 0 20px #00fff7cc;
input[type="text"] {
  width: 100%;
  font-size: 28px;
  padding: 16px 20px;
  border-radius: 12px;
  border: none;
  margin-bottom: 20px;
  background: #121212;
  color: white;
  box-shadow: inset 0 0 10px #00fff7cc;
  text-align: right;

  box-sizing: border-box; /* Include padding within width */
  margin: 0 auto;         /* Center horizontally */
  display: block;         /* Needed for margin auto to work */
  padding-right: 20px;    /* Ensure enough padding on the right */
}

  button {
    font-size: 24px;
    padding: 18px 0;
    margin: 8px 6px;
    border-radius: 14px;
    border: none;
    cursor: pointer;
    color: #121212;
    width: 70px;
    box-shadow: 0 0 15px #000000;
    transition: all 0.2s ease-in-out;
    user-select: none;
  }
  button.operator {
    background-color: #ff9500;
    color: white;
    box-shadow: 0 0 15px #ff9500;
  }
  button.operator:hover {
    box-shadow: 0 0 40px #ffbb33;
    transform: scale(1.12);
  }
  button.digit {
    background-color: #00fff7;
    color: black;
    box-shadow: 0 0 15px #00fff7;
  }
  button.digit:hover {
    box-shadow: 0 0 40px #33ffff;
    transform: scale(1.12);
  }
  #result {
    margin-top: 28px;
    font-size: 26px;
    min-height: 36px;
    color: #4caf50;
    word-wrap: break-word;
    font-weight: 700;
    text-align: center;
    letter-spacing: 0.02em;
  }
  h1 {
    margin-bottom: 14px;
    font-weight: 700;
    letter-spacing: 0.06em;
  }
  /* Container for rows of buttons */
  .button-row {
    display: flex;
    justify-content: center;
    margin-bottom: 12px;
  }
  /* Special styling for the last row (clear & calculate) */
  #action-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  #action-buttons button {
    width: 165px;
    font-size: 24px;
    padding: 16px 0;
    border-radius: 16px;
    box-shadow: none;
  }
  #action-buttons button#clear-btn {
    background: #ff4444;
    color: white;
    box-shadow: 0 0 25px #ff4444;
  }
  #action-buttons button#clear-btn:hover {
    box-shadow: 0 0 45px #ff7777;
    transform: scale(1.1);
  }
  #action-buttons button#calc-btn {
    background: #4caf50;
    color: white;
    box-shadow: 0 0 25px #4caf50;
  }
  #action-buttons button#calc-btn:hover {
    box-shadow: 0 0 45px #7ee57e;
    transform: scale(1.1);
  }
</style>
</head>
<body>

<h1>Python Web Calculator</h1>
<div id="calculator">
  <input type="text" id="expression" placeholder="Enter expression..." autofocus autocomplete="off" spellcheck="false" />

  <div class="button-row">
    <button class="digit" onclick="addChar('7')">7</button>
    <button class="digit" onclick="addChar('8')">8</button>
    <button class="digit" onclick="addChar('9')">9</button>
    <button class="operator" onclick="addChar('/')">÷</button>
  </div>
  <div class="button-row">
    <button class="digit" onclick="addChar('4')">4</button>
    <button class="digit" onclick="addChar('5')">5</button>
    <button class="digit" onclick="addChar('6')">6</button>
    <button class="operator" onclick="addChar('*')">×</button>
  </div>
  <div class="button-row">
    <button class="digit" onclick="addChar('1')">1</button>
    <button class="digit" onclick="addChar('2')">2</button>
    <button class="digit" onclick="addChar('3')">3</button>
    <button class="operator" onclick="addChar('-')">−</button>
  </div>
  <div class="button-row">
    <button class="digit" onclick="addChar('0')">0</button>
    <button class="digit" onclick="addChar('.')">.</button>
    <button class="operator" onclick="addChar('%')">%</button>
    <button class="operator" onclick="addChar('+')">+</button>
  </div>

  <div class="button-row">
    <button class="operator" onclick="addChar('sin(')">sin(</button>
    <button class="operator" onclick="addChar('cos(')">cos(</button>
    <button class="operator" onclick="addChar('tan(')">tan(</button>
  </div>
  <div class="button-row">
    <button class="operator" onclick="addChar('sind(')">sin d(</button>
    <button class="operator" onclick="addChar('cosd(')">cos d(</button>
    <button class="operator" onclick="addChar('tand(')">tan d(</button>
  </div>

  <div id="action-buttons">
    <button id="clear-btn" onclick="clearInput()">Clear</button>
    <button id="calc-btn" onclick="calculate()">Calculate</button>
  </div>

  <div id="result"></div>
</div>

<script>
  function addChar(c) {
    const input = document.getElementById('expression');
    input.value += c;
    input.focus();
  }

  function clearInput() {
    document.getElementById('expression').value = '';
    document.getElementById('result').textContent = '';
  }

  async function calculate() {
    const expr = document.getElementById('expression').value;
    if (!expr.trim()) return;

    try {
      const response = await fetch('/calculate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({expression: expr})
      });
      const data = await response.json();
      document.getElementById('result').textContent = data.result;
    } catch (err) {
      document.getElementById('result').textContent = 'Error communicating with server';
    }
  }

  document.getElementById('expression').addEventListener('keypress', function(e){
    if (e.key === 'Enter') calculate();
  });
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get('expression', '')
    result = evaluate_expression(expression)
    return jsonify({'result': str(result)})

if __name__ == '__main__':
    print("Starting Python Web Calculator on http://127.0.0.1:5000/")
    app.run(debug=True)

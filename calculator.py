"""
==============================================================================
                     PYTHON CALCULATOR - LEVEL 5 (AI Enhanced)
==============================================================================
Description:
------------
This is an AI-inspired web calculator implemented in Flask with natural language
understanding of mathematical expressions via a rule-based parser.

Features:
---------
- Parses simple natural language math queries into Python expressions using pattern matching.
- Supports math operations including exponentiation, roots, trigonometry, constants, and variables.
- Provides user-friendly error handling.
- Web interface with glowing buttons.

AI Operation Logic
------------------
This calculator simulates AI by using a local, rule-based natural language processing
(NLP) module that interprets user input expressed in conversational math queries and
converts them into executable Python mathematical expressions.

The logic uses explicitly defined patterns and string replacements to recognize common
mathematical terms and functions within plain English sentences.

For example, phrases such as "square root of 16", "factorial of 5", or "2 to the power 5"
are translated into Python expressions like sqrt(16), factorial(5), and 2 ** 5.

This deterministic pattern matching allows the calculator to handle a variety of natural
language inputs without internet access or complex AI models.

AI Model Used
-------------
No machine learning or external AI model is used. The parser is a set of
regular expressions and string manipulation rules implemented in Python.

Future versions can integrate cloud-based large language models (LLMs) such as OpenAI's
GPT-4 for richer, context-aware interpretation and conversational math capabilities.

Why Do We Need AI in the Calculator?

- To allow users to input calculations in plain English rather than strict math syntax.
- To handle flexible expressions without requiring knowledge of programming syntax.
- To improve accessibility and usability for non-technical users.

External Modules:
-----------------
- Flask

Install:
--------
pip install flask

==============================================================================
Author:
-------
Abhisakh Sarma
==============================================================================
"""

from flask import Flask, request, jsonify, render_template_string
import math
import re

app = Flask(__name__)

# Safe math functions including trig in degrees
safe_functions = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
safe_functions.update({
    'abs': abs,
    'round': round,
    'pow': pow,
    'sqrt': math.sqrt,
    'factorial': math.factorial,
    'sind': lambda x: math.sin(math.radians(x)),
    'cosd': lambda x: math.cos(math.radians(x)),
    'tand': lambda x: math.tan(math.radians(x)),
    'radians': math.radians,
    'degrees': math.degrees,
    'pi': math.pi,
    'e': math.e,
})

variables = {}

def preprocess_expression(expr: str) -> str:
    """
    Convert natural language math phrases to valid Python expressions.

    This is the core of the 'AI-inspired' rule-based parser.

    Examples:
    - '2 to the power 5' -> '2 ** 5'
    - 'square root of 16' -> 'sqrt(16)'
    - 'pi' -> 'pi' (math constant)
    """
    expr = expr.lower()

    # Replace power phrases with Python exponent operator
    expr = re.sub(r'\bto the power of\b', '**', expr)
    expr = re.sub(r'\bto the power\b', '**', expr)
    expr = re.sub(r'\bpower of\b', '**', expr)
    expr = re.sub(r'\bpower\b', '**', expr)

    # Replace square root expressions
    expr = re.sub(r'square root of ([\d\.]+)', r'sqrt(\1)', expr)

    # Replace factorial expressions
    expr = re.sub(r'factorial of (\d+)', r'factorial(\1)', expr)

    # Replace math constants
    expr = re.sub(r'\bpi\b', 'pi', expr)
    expr = re.sub(r'\be\b', 'e', expr)

    # Replace division and multiplication words
    expr = re.sub(r'divided by', '/', expr)
    expr = re.sub(r'multiplied by', '*', expr)
    expr = re.sub(r'\btimes\b', '*', expr)

    # Remove filler words for simpler parsing
    expr = re.sub(r'\bthe\b', '', expr)
    expr = re.sub(r'\bof\b', '', expr)

    # Clean up extra whitespace
    expr = ' '.join(expr.split())

    return expr

def evaluate_expression(expr):
    """
    Evaluate the expression safely after preprocessing.

    Supports variable assignment (e.g. x = 10).
    """
    try:
        expr = preprocess_expression(expr)
        if "=" in expr and "==" not in expr:
            var, val = expr.split("=", 1)
            var = var.strip()
            val = val.strip()
            result = eval(val, {"__builtins__": {}}, {**safe_functions, **variables})
            variables[var] = result
            return f"{var} = {result}"
        else:
            result = eval(expr, {"__builtins__": {}}, {**safe_functions, **variables})
            return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {e}"

# The rest of your Flask app and HTML template remain unchanged
# ...

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

  h1 {
    text-align: center;
    width: 100%;
    margin-bottom: 24px;
    font-weight: 700;
    letter-spacing: 0.08em;
    font-size: 2.5rem;
  }

  #calculator {
    background: #1e1e1e;
    padding: 25px 30px 30px;
    border-radius: 15px;
    width: 480px;  /* wider */
    box-shadow: 0 0 25px #00fff7cc;
  }

  input[type="text"] {
    width: 100%;
    font-size: 28px;
    padding: 14px 20px;
    border-radius: 14px;
    border: none;
    margin-bottom: 24px;
    background: #121212;
    color: white;
    box-shadow: inset 0 0 10px #00fff7cc;
    text-align: right;
    box-sizing: border-box;
    display: block;
  }

  button {
    font-size: 24px;
    padding: 14px 0;    /* shorter height */
    margin: 8px 6px;
    border-radius: 14px;
    border: none;
    cursor: pointer;
    color: #121212;
    width: 90px;       /* wider buttons */
    box-shadow: 0 0 14px #000000;
    transition: all 0.25s ease-in-out;
    user-select: none;
  }

  button.operator {
    background-color: #ff9500;
    color: white;
    box-shadow: 0 0 14px #ff9500;
  }
  button.operator:hover {
    box-shadow: 0 0 40px #ffbb33;
    transform: scale(1.1);
  }

  button.digit {
    background-color: #00fff7;
    color: black;
    box-shadow: 0 0 14px #00fff7;
  }
  button.digit:hover {
    box-shadow: 0 0 40px #33ffff;
    transform: scale(1.1);
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

  .button-row {
    display: flex;
    justify-content: center;
    margin-bottom: 12px;
  }

  #action-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 24px;
  }

  #action-buttons button {
    width: 220px;  /* wider */
    font-size: 26px;
    padding: 16px 0;
    border-radius: 16px;
    box-shadow: none;
  }

  #clear-btn {
    background: #ff4444;
    color: white;
    box-shadow: 0 0 24px #ff4444;
  }
  #clear-btn:hover {
    box-shadow: 0 0 48px #ff7777;
    transform: scale(1.05);
  }

  #calc-btn {
    background: #4caf50;
    color: white;
    box-shadow: 0 0 24px #4caf50;
  }
  #calc-btn:hover {
    box-shadow: 0 0 48px #7ee57e;
    transform: scale(1.05);
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

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE)

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.json
    expr = data.get("expression", "")
    result = evaluate_expression(expr)
    return jsonify({"result": str(result)})

if __name__ == "__main__":
    print("Starting Python Web Calculator on http://127.0.0.1:5000/")
    app.run(debug=True)
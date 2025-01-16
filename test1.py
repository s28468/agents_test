import ollama
import yfinance as yf
from typing import Dict, Any, Callable
from sympy import symbols, Eq, solve
from math import gcd

def get_stock_price(symbol: str) -> float:
    ticker = yf.Ticker(symbol)
    price_attrs = ['regularMarketPrice', 'currentPrice', 'price']

    for attr in price_attrs:
        if attr in ticker.info and ticker.info[attr] is not None:
            return ticker.info[attr]

    fast_info = ticker.fast_info
    if hasattr(fast_info, 'last_price') and fast_info.last_price is not None:
        return fast_info.last_price

    raise Exception("Could not find valid price data")
def solve_quadratic(a, b, c):
    if a == 0:
        if b == 0:
            return "No solution" if c != 0 else "Infinite solutions"
        return [-c / b]
    x = symbols('x')
    equation = Eq(a * x**2 + b * x + c, 0)
    solutions = solve(equation, x)
    return solutions
def solve_cubic(a, b, c, d):
    """
    Solves a cubic equation of the form ax^3 + bx^2 + cx + d = 0.

    :param a: Coefficient of x^3
    :param b: Coefficient of x^2
    :param c: Coefficient of x
    :param d: Constant term
    :return: List of solutions
    """
    if a == 0:
        # If a is 0, it becomes a quadratic equation
        if b == 0:
            if c == 0:
                return "No solution" if d != 0 else "Infinite solutions"
            return [-d / c]
        x = symbols('x')
        equation = Eq(b * x**2 + c * x + d, 0)
        solutions = solve(equation, x)
        return solutions

    # Declare the variable x
    x = symbols('x')

    # Form the cubic equation
    equation = Eq(a * x**3 + b * x**2 + c * x + d, 0)

    # Solve the equation
    solutions = solve(equation, x)
    return solutions
def calculate_gcd_and_lcm(a, b):
    """
    Calculates the greatest common divisor (GCD) and least common multiple (LCM) of two numbers.

    :param a: First number
    :param b: Second number
    :return: A dictionary with GCD and LCM
    """
    if a == 0 or b == 0:
        return {"gcd": max(abs(a), abs(b)), "lcm": "Undefined (one number is zero)"}

    # Calculate GCD
    gcd_value = gcd(a, b)

    # Calculate LCM using the formula: lcm(a, b) = abs(a * b) / gcd(a, b)
    lcm_value = abs(a * b) // gcd_value

    return {"gcd": gcd_value, "lcm": lcm_value}

get_stock_price_tool = {
    'type': 'function',
    'function': {
        'name': 'get_stock_price',
        'description': 'Get the current stock price for any symbol',
        'parameters': {
            'type': 'object',
            'required': ['symbol'],
            'properties': {
                'symbol': {'type': 'string', 'description': 'The stock symbol (e.g., AAPL, GOOGL)'},
            },
        },
    },
}
solve_quadratic_tool = {
    'type': 'function',
    'function': {
        'name': 'solve_quadratic',
        'description': 'Solves a quadratic equation of the form ax^2 + bx + c = 0',
        'parameters': {
            'type': 'object',
            'required': ['a', 'b', 'c'],
            'properties': {
                'a': {
                    'type': 'number',
                    'description': 'The coefficient of x^2'
                },
                'b': {
                    'type': 'number',
                    'description': 'The coefficient of x'
                },
                'c': {
                    'type': 'number',
                    'description': 'The constant term'
                },
            },
        },
    },
}
solve_cubic_tool = {
    'type': 'function',
    'function': {
        'name': 'solve_cubic',
        'description': 'Solves a cubic equation of the form ax^3 + bx^2 + cx + d = 0',
        'parameters': {
            'type': 'object',
            'required': ['a', 'b', 'c', 'd'],
            'properties': {
                'a': {
                    'type': 'number',
                    'description': 'The coefficient of x^3'
                },
                'b': {
                    'type': 'number',
                    'description': 'The coefficient of x^2'
                },
                'c': {
                    'type': 'number',
                    'description': 'The coefficient of x'
                },
                'd': {
                    'type': 'number',
                    'description': 'The constant term'
                },
            },
        },
    },
}
calculate_gcd_and_lcm_tool = {
    'type': 'function',
    'function': {
        'name': 'calculate_gcd_and_lcm',
        'description': 'Calculates the GCD and LCM of two numbers',
        'parameters': {
            'type': 'object',
            'required': ['a', 'b'],
            'properties': {
                'a': {
                    'type': 'integer',
                    'description': 'The first number'
                },
                'b': {
                    'type': 'integer',
                    'description': 'The second number'
                },
            },
        },
    },
}


prompt = "i need a stock price for Apple"
#prompt = "solve pls this quadratic equation: 2x^(2)+13x+6=0"

available_functions: Dict[str, Callable] = {
    'solve_quadratic': solve_quadratic,
    'solve_cubic': solve_cubic,
    'calculate_gcd_and_lcm': calculate_gcd_and_lcm,
    'get_stock_price': get_stock_price,
}

response = ollama.chat(
    'mistral:latest',
    messages=[{'role': 'user', 'content': prompt}],
    tools=[solve_quadratic_tool, solve_cubic_tool, calculate_gcd_and_lcm_tool, get_stock_price_tool],
)

if response.message.tool_calls:
    for tool in response.message.tool_calls:
        if function_to_call := available_functions.get(tool.function.name):
            print('Calling function:', tool.function.name)
            print('Arguments:', tool.function.arguments)
            print('Function output:', function_to_call(**tool.function.arguments))
        else:
            print('Function', tool.function.name, 'not found')
else:
    print('No tools called')
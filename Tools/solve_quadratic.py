from langchain_core.tools import tool
from sympy import symbols, Eq, solve

@tool
def solve_quadratic(a, b, c):
    """
    Solves a quadratic equation of the form ax^2 + bx + c = 0.

    :param a: Coefficient of x^2
    :param b: Coefficient of x
    :param c: Constant term
    :return: List of solutions
    """
    if a == 0:
        if b == 0:
            return "No solution" if c != 0 else "Infinite solutions"
        return [-c / b]
    x = symbols('x')
    equation = Eq(a * x**2 + b * x + c, 0)
    solutions = solve(equation, x)
    return solutions



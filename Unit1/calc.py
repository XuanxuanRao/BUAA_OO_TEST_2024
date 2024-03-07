from sympy import symbols, exp, lambdify
import re
x, y, z = symbols('x y z')
def calc(expression: str, functions: list) -> str:
    for function in functions:
        func_name, func_body = function.split('=')
        func_declare = "def " + func_name + ":" + "return " + re.sub(r"\b0+(\d+)", r"\1", func_body)
        exec(func_declare)
    exec("expression =" + expression)
    return eval(expression).simplify().expand()


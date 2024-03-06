from sympy import symbols, exp, lambdify
import numpy as np

def calc(expression: str, functions: list, x_value: int) -> float:
    x, y, z = symbols('x y z')
    for function in functions:
        func_name, func_body = function.split('=')
        func_declare = "def " + func_name + ":" + "return " + func_body
        exec(func_declare)
    # 使用 lambdify 将表达式转换为可计算的函数
    expr_lambda = lambdify(x, eval(expression), modules=[{'exp': np.exp}])
    return expr_lambda(x_value)

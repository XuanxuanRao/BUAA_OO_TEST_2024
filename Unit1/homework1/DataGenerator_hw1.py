import random

ExpressionDepth = 5


def check(expression: str, parentheses_limit: int) -> bool:
    top = 0
    for char in expression:
        if char == '(':
            top += 1
            if top > parentheses_limit:
                return False
        elif char == ')':
            top -= 1
    return top == 0


def generate_expression(depth):
    if depth <= 0:
        return generate_factor()
    expression = generate_expression(depth-1)
    while random.random() < 0.4:
        expression += random.choice(["+", "-", "-+ ", "* ", "*", "*"]) + generate_expression(depth - 1)
    while random.random() < 0.4:
        op = random.choice(["+", "-", "*"])
        expression += f" {op} {generate_factor()}"
    if 'x' in expression and (depth == ExpressionDepth and random.random() < 0.2 or depth < ExpressionDepth and random.random() < 0.3):
        return '(' + expression + ')' + '^' + generate_exponent()
    else:
        return expression


def generate_factor():
    if random.random() < 0.15:
        return str(random.randint(0, 3)) + "*" + generate_variable_factor()
    elif random.random() < 0.3:
        return generate_variable_factor() + "*" + str(random.randint(0, 3))
    elif random.random() < 0.4:
        return generate_constant_factor() + "*" + generate_constant_factor() + "*" + generate_constant_factor()
    else:
        return generate_constant_factor()


def generate_variable_factor():
    result = "x"
    if random.random() < 0.25:
        result += random.choice([" ", "\t"]) + "^ " + generate_exponent()
    elif random.random() < 0.5:
        result += " ^ " + generate_exponent()
    return result


def generate_exponent():
    if random.random() < 0.25:
        return "+00" + str(random.randint(0, 8))
    elif random.random() < 0.5:
        return "+" + str(random.randint(0, 8))
    else:
        return str(random.randint(0, 8))


def generate_constant_factor():
    constant_factor = random.choice(["", " ", "  ", "\t"])
    while random.random() < 0.65:
        constant_factor += random.choice(["+", "-", ""])
    return str(random.randint(-20, 20))


if __name__ == "__main__":
    with open('TestData.txt', 'w') as infile:
        count = 0
        while count < 100:
            expression = generate_expression(ExpressionDepth)
            if check(expression, 2):
                infile.write(expression + '\n')
                count += 1

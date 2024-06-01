import re
import sympy
from sympy import symbols
from sympy.printing.latex import latex
from sympy.parsing.latex import parse_latex

def solve_latex_equation(latex_equation, symbol='x'):
    sympy_equation = sympy.Eq(parse_latex(latex_equation.split('=')[0].strip()), parse_latex(latex_equation.split('=')[1].strip()))
    solved_equation = sympy.solve(sympy_equation, sympy.symbols(symbol))
    r, q = symbols('r, q')
    #print([float(f.subs({r: 1,q:1.7})) for f in solved_equation])
    return [latex(item) for item in solved_equation]


def simplify_latex_equation(latex_equation, cancel=True):    
    # Parse the LaTeX equation into a sympy expression
    # This assumes the equation is in the form of 'x = expression'

    sympy_expr_left = parse_latex(latex_equation.split('=')[0].strip())
    sympy_expr_right = parse_latex(latex_equation.split('=')[1].strip())
    
    # Simplify the expression
    simplified_expr_left = sympy.simplify(sympy_expr_left)
    simplified_expr_right = sympy.simplify(sympy_expr_right)
    
    if cancel:
        simplified_expr_left = sympy.cancel(simplified_expr_left)
        simplified_expr_rigth = sympy.cancel(simplified_expr_right)

    # Convert the simplified expression back to LaTeX
    simplified_latex_left = latex(simplified_expr_left)
    simplified_latex_right = latex(simplified_expr_right)
    
    # Return the simplified LaTeX equation
    return f"{simplified_latex_left} = {simplified_latex_right}"

def simplify_latex_expression(latex_expression):    
    # Parse the LaTeX equation into a sympy expression
    # This assumes the equation is in the form of 'x = expression'

    sympy_expr = parse_latex(latex_expression)
    
    # Simplify the expression
    simplified_expr = sympy.simplify(sympy_expr)
    
    # Convert the simplified expression back to LaTeX
    simplified_latex = latex(simplified_expr)
    
    # Return the simplified LaTeX equation
    return f"{simplified_latex}"

def factor_latex_expression(latex_expression, cancel=True):    
    # Parse the LaTeX equation into a sympy expression
    # This assumes the equation is in the form of 'x = expression'

    sympy_expr = parse_latex(latex_expression)
    
    # Simplify the expression
    simplified_expr = sympy.factor(sympy_expr)

    # Cancel like terms
    if cancel:
        simplified_expr = sympy.cancel(simplified_expr)

    # Convert the simplified expression back to LaTeX
    simplified_latex = latex(simplified_expr)
    
    # Return the simplified LaTeX equation
    return f"{simplified_latex}"

def convert_to_latex(equation):
    """
    Converts a typical math equation into LaTeX format.
    
    Parameters:
    equation (str): The math equation to convert.
    
    Returns:
    str: The converted LaTeX equation.
    """
    # First, replace \left( and \right) with ( and )
    equation = equation.replace('\\left(', '(')
    equation = equation.replace('\\right)', ')')

    # Add LaTeX formatting for parentheses and plus/minus signs first
    equation = equation.replace('(', '\\left(')
    equation = equation.replace(')', '\\right)')
    equation = equation.replace('+', '+')
    equation = equation.replace('-', '-')
    
    # Replace division operations with LaTeX fractions
    equation = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', equation)
    
    # Replace square roots with LaTeX square roots
    equation = re.sub(r'sqrt\((.*?)\)', r'\\sqrt{\1}', equation)
    
    # Replace powers with LaTeX superscripts
    equation = re.sub(r'(\w+)\^(\d+)', r'\1^{\2}', equation)
    
    return equation


def format_file(file_name):
    # Step 1: Open the file in read mode
    with open(file_name, 'r') as file:
        content = file.read()
    print(content)
    content = convert_to_latex(content)
    print(content)
    solutions = solve_latex_equation(content)
    # print(type(solutions))
    # print(type(solutions[0]))
    # solutions = [simplify_latex_expression(item) for item in solutions]
    old_solutions = []
    while(solutions != old_solutions):
        old_solutions = solutions.copy()
        solutions = [simplify_latex_expression(item) for item in solutions]
        solutions = [factor_latex_expression(item) for item in solutions]


    # print(type(solutions))
    # print(type(solutions[0]))
    content = '\n\n'.join(solutions)
    with open("out.txt", 'w') as file:
        file.write(content)

def main():
    file_name = "equation.txt"
    print("Processing file")
    format_file(file_name)



if __name__ == "__main__":
    main()
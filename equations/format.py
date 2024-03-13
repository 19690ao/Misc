import re
from sympy import *
from sympy.printing.latex import latex

def simplify_latex_equation(latex_equation):
    # Initialize the variable
    x = symbols('x')
    
    # Parse the LaTeX equation into a sympy expression
    # This assumes the equation is in the form of 'x = expression'
    sympy_expr = parse_latex(latex_equation.split('=')[1].strip())
    
    # Simplify the expression
    simplified_expr = simplify(sympy_expr)
    
    # Convert the simplified expression back to LaTeX
    simplified_latex = latex(simplified_expr)
    
    # Return the simplified LaTeX equation
    return f"x = {simplified_latex}"

# Example usage
latex_equation = "x = \\frac{x^2 + 2x + 1}{x + 1}"
simplified_equation = simplify_latex_equation(latex_equation)
print(simplified_equation)


def convert_to_latex(equation):
    """
    Converts a typical math equation into LaTeX format.
    
    Parameters:
    equation (str): The math equation to convert.
    
    Returns:
    str: The converted LaTeX equation.
    """
    # Replace division operations with LaTeX fractions
    equation = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', equation)
    
    # Replace square roots with LaTeX square roots
    equation = re.sub(r'sqrt\((.*?)\)', r'\\sqrt{\1}', equation)
    
    # Replace powers with LaTeX superscripts
    equation = re.sub(r'(\w+)\^(\d+)', r'\1^{\2}', equation)
    
    # Add LaTeX formatting for parentheses and plus/minus signs
    equation = equation.replace('(', '\\left(')
    equation = equation.replace(')', '\\right)')
    equation = equation.replace('+', '+')
    equation = equation.replace('-', '-')
    
    return equation

def format_file(file_name):
    # Step 1: Open the file in read mode
    with open(file_name, 'r') as file:
        content = file.read()
        content = convert_to_latex(content)
    # # Step 2: Process the content
    # formatted_content = ''
    # depth = 0
    # for char in content:
    #     if char == '(':
    #         if False:
    #             formatted_content += '\n' + '(' + '\n'
    #         else:
    #             formatted_content += '('
    #         depth += 1
    #     elif char == ')':
    #         depth -= 1
    #         if depth == 0:
    #             formatted_content += ')' + '\n\n'
    #         else:
    #             formatted_content += ')'
    #     else:
    #         formatted_content += char
    # formatted_content = '\n'.join([convert_to_latex(item) for item in formatted_content.split('\n')])
    # Step 3: Write the processed content back to the file
    with open("out.txt", 'w') as file:
        #file.write(formatted_content)
        file.write(content)





if __name__ == "__main__":
    format_file("num.txt")
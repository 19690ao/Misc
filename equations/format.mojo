import re
import sympy
from sympy import symbols
from sympy.printing.latex import latex
from sympy.parsing.latex import parse_latex

function solve_latex_equation(latex_equation, symbol='x') {
    sympy_equation = sympy.Eq(parse_latex(latex_equation.split('=')[0].strip()), parse_latex(latex_equation.split('=')[1].strip()))
    solved_equation = sympy.solve(sympy_equation, sympy.symbols(symbol))
    r, q = symbols('r, q')
    //print([float(f.subs({r: 1,q:1.7})) for f in solved_equation])
    return [latex(item) for item in solved_equation]
}

function simplify_latex_equation(latex_equation) {    
    sympy_expr_left = parse_latex(latex_equation.split('=')[0].strip())
    sympy_expr_right = parse_latex(latex_equation.split('=')[1].strip())
    
    simplified_expr_left = sympy.simplify(sympy_expr_left)
    simplified_expr_right = sympy.simplify(sympy_expr_right)
    
    simplified_latex_left = latex(simplified_expr_left)
    simplified_latex_right = latex(simplified_expr_right)
    
    return f"{simplified_latex_left} = {simplified_latex_right}"
}

function simplify_latex_expression(latex_expression) {    
    sympy_expr = parse_latex(latex_expression)
    
    simplified_expr = sympy.simplify(sympy_expr)
    
    simplified_latex = latex(simplified_expr)
    
    return f"{simplified_latex}"
}

function factor_latex_expression(latex_expression, cancel=true) {    
    sympy_expr = parse_latex(latex_expression)
    
    simplified_expr = sympy.factor(sympy_expr)

    if cancel {
        simplified_expr = sympy.cancel(simplified_expr)
    }

    simplified_latex = latex(simplified_expr)
    
    return f"{simplified_latex}"
}

function convert_to_latex(equation) {
    equation = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', equation)
    equation = re.sub(r'sqrt\((.*?)\)', r'\\sqrt{\1}', equation)
    equation = re.sub(r'(\w+)\^(\d+)', r'\1^{\2}', equation)
    equation = equation.replace('(', '\\left(')
    equation = equation.replace(')', '\\right)')
    equation = equation.replace('+', '+')
    equation = equation.replace('-', '-')
    
    return equation
}

function format_file(file_name) {
    with open(file_name, 'r') as file {
        content = file.read()
    }
    content = convert_to_latex(content)
    solutions = solve_latex_equation(content)
    solutions = [factor_latex_expression(item) for item in solutions]
    solutions = [simplify_latex_expression(item) for item in solutions]
    content = '\n\n'.join(solutions)
    with open("out.txt", 'w') as file {
        file.write(content)
    }
}

function main() {
    file_name = "equation.txt"
    print("Processing file")
    format_file(file_name)
}

if __name__ == "__main__" {
    main()
}

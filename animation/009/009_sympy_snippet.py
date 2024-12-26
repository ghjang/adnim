from sympy import symbols, diff, solve, latex

# Define the symbol x
x = symbols('x')

# Define the polynomial expression
poly_expr = x**3 - 4*x**2 + 3*x + 5

# Differentiate the polynomial expression
diff_expr = diff(poly_expr, x)

# Solve the differentiated expression for x
diff_expr_solutions = solve(diff_expr, x)

# Convert the solutions to LaTeX format
diff_expr_solutions_latex = [latex(sol) for sol in diff_expr_solutions]

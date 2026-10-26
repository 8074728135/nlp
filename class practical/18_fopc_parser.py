import re

expression = input("Enter a logical expression: ")

tokens = re.findall(r'forall|exists|and|or|not|implies|[A-Za-z][A-Za-z0-9_]*|[(),.]', expression)
valid = "".join(tokens) == re.sub(r'\s+', '', expression)

if valid and tokens and tokens.count("(") == tokens.count(")") and tokens.count("(") > 0:
    print("Tokens:", tokens)
    print("Expression has valid basic token and parenthesis structure")
else:
    print("Invalid expression")

from problog.logic import *

term = Term('bla')

var_A = Var('A')
var_B = Var('B')
var_C = Var('C')

term_vars = term(var_A, var_B, var_C)
print(term_vars)

substitution = {}

# NOTE: all variables in the term need to be defined in the substitution
for var in term_vars.variables():
    substitution[var] = var

substitution[var_A] = Constant(3)

term_subst = term_vars.apply(substitution)

print(term_subst)

print(term_subst.args)
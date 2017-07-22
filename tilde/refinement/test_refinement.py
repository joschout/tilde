from problog.program import SimpleProgram

from tilde.refinement.RefinementController import *

X = Var('X')
Y = Var('Y')
Z = Var('Z')

sendback, fix, ok, worn, replaceable = \
    Term('sendback'), Term('fix'), Term('ok'), Term('worn'), Term('replaceable')

not_replaceable = Term('not_replaceable')

initial_query = SimpleProgram()
initial_query += Term('true')

conj_1 = replaceable(X)
dict_1 = {X.name: '-'}
rmode_1 = RefinementMode(5, conj_1, dict_1)

conj_2 = not_replaceable(X)
dict_2 = {X: '-'}
rmode_2 = RefinementMode(5, conj_2, dict_2)

conj_3 = not_replaceable(X)
dict_3 = {X: '-'}
rmode_3 = RefinementMode(5, conj_3, dict_3)

r_controller = RefinementController([rmode_1, rmode_2, rmode_3])


literal = Term('test')(X, Y, Z)

print(literal)

print(literal.signature)

counter = VariableIDCounter()

literal_new_vars = refine_add_literal("bla", literal, counter)

print(literal_new_vars)
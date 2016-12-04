from problog.logic import *
from problog.engine_unify import subsumes

# === test 1 =========================
# test(X, Y, Z) with substitution theta = {X/a, Y/b, Z/C}

X, Y, Z = Var('X'), Var('Y'), Var('Z')
a, b, c = Constant('a'), Constant('b'), Constant('c')
term = Term('test')

test = term(X, Y, Z)
subst = {X: a, Y: b, Z: c}

substituted1 = test.apply(subst)
print('test 1:', test, 'with substitution', subst, ': ', substituted1)

# === test 2======================
# test(X, Y, Z) with substitution {Y/X, Z/X}
# NOTE: apparently, there has to be a mapping from X to X

subst2 = {X: X, Y: X, Z: X}

substituted2 = test.apply(subst2)
print('test 2:', test, 'with substitution', subst2, ':', substituted2)

# === test 3 ========================
# testing for subsumption
# test(X, Y, Z) theta-subsumes test(X ,X , X)



does_theta_subsume = subsumes(test, substituted2)
print('test 3: does', test, 'theta-subsume', substituted2, '? : ', str(does_theta_subsume))
print('is -1 a variable ? ', is_variable(-1))

print('is', X, 'ground ? : ', is_ground(X))
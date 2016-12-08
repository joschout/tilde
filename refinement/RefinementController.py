import math
from problog.logic import Term, Var
from enum import Enum

# ONNODIG: gebruik .variables()
def get_variables_in_conjunction(conjunction):
    """Extracts the variables in a conjunction.

    conj = l ^ l ^ l ... ^l
    """
    variables = set()
    for literal in conjunction.to_list():
        for arg in literal.args:
            variables.add(arg)
    return variables


class RefinementMode:
    """
    A refinement mode, as specified by the user.

    """
    max_nb = math.inf
    conjunction = Term('true')
    variable_modes = None

    def __init__(self, max_nb_of_times, conjunction, variable_modes):
        self.max_nb = max_nb_of_times
        self.conjunction = conjunction
        self.variable_modes = variable_modes


class UnificationMode(Enum):
    must_be_unified = 1
    may_be_unified = 2
    new_variable = 3


class RefinementController:
    refinement_modes = []

    def __init__(self, refinement_modes):
        self.refinement_modes = refinement_modes

    def refine(self, conjunction):
        pass


class VariableIDCounter:
    counter = 0

    def get_new_variable(self):
        var_name = '_' + str(self.counter)
        self.counter += 1
        return Var(var_name)


def refine_add_literal(conjunction, literal, variable_id_counter):
    """
    This method has to add the literal to the conjunction.
    There are two ways the variables can be handled:

    1. a new variable is introduced for each variable in the literal.
    2. one or more variables in the literal can be unified
        with variables in the conjunction.
        Remember: a unifier of 2 expressions f1 and f2
                is a substitution theta such that
                f1 theta = f2 theta
        Note: (I think that) in this case,
        the unification is simply making the two variables the same.

    What we need:
        A list of al variables in the conjunction.
        A list of all variables in the literal.

    * adding a literal, no unification of the variables
        1. generate as many new variables as there are needed for the literal.
        2. create a new Term for the literal
        3. add the new term to the conjunction
        4. return the conjunction

    * adding a literal, unification of one or more variables
        possible substitutions:
            for each combination of variables of the literal:
                pick any variable form the list of variables in the conjunction
                    1. apply the substitution to the literal
                    2. create a new Term for the literal
                    3. add the new term to the conjunction
                    4. return the conjunction
    """

    # get the functor of the Term, which we assume is a literal
    functor = literal.functor
    variables = literal.variables()
    literal_new_vars = Term(functor)
    new_vars = []
    for var in variables:
        new_var = variable_id_counter.get_new_variable()
        new_vars.append(new_var)

    return literal_new_vars


# def get_possible_substitutions(variables_from_conj, variables_from_literal):
#     possible_substitutions = []
#     for

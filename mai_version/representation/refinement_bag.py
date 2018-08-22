from itertools import product
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from mai_version.representation.language import TypeModeLanguage

from mai_version.representation.TILDE_query import TILDEQuery


class RefinementBag:
    def __init__(self, conjunction, nb_of_times_addable='inf',):
        self.nb_of_times_addable = nb_of_times_addable  # type: Optional[int]
        self.conjunction = conjunction  # type: RefinementConjunction


class RefinementConjunction:
    def __init__(self):
        self.literal_list = []  # type: List[RefinementLiteral]

    def get_addable_conjunctions(self, variables_already_in_query):

        # a conjunction = 1+ literals
        # a literal = 1+ variables
        # we need all possible combinations of moded vars

        # dictionary: variable name to modes
        variables_in_conjunction = {}  # type: Dict[str, RefinementVar]
        for literal in self.literal_list:
            for var in literal.refinement_var_list:
                if var.name not in variables_in_conjunction:
                    variables_already_in_query[var.name] = var

        # list of list
        all_var_mode_combos = []  # type: List[List[Tuple[str, str]]]

        for var in variables_in_conjunction:
            var_mode_combos = []  # type: List[Tuple[str, str]]
            for mode_of_var in variables_in_conjunction[var].modes:
                var_mode_combos.append((var, mode_of_var))
            all_var_mode_combos.append(var_mode_combos)

        for combo in product(*all_var_mode_combos):

        # TODO: types for unification
        # TODO: unification with variables in query


class RefinementLiteral:
    def __init__(self, functor: str, vars: List[RefinementVar]):
        self.functor = functor  # type: str
        self.refinement_var_list = vars  # type: List[RefinementVar]


class RefinementVar:
    def __init__(self, name: str, modes: List[str], type: str):
        self.name = name  # type: str
        self.modes = modes  # type: List[str]
        self.type = type



def refine_conjunctions(query: TILDEQuery, language: TypeModeLanguage, refinement_bags: List[RefinementBag]):
    for refinement_bag in refinement_bags:
        possible_conjunction_generator = refinement_bag.conjunction.get_addable_conjunctions()

from typing import List
from typing import Optional


class RefinementBag:
    def __init__(self, conjunction, nb_of_times_addable='inf',):
        self.nb_of_times_addable = nb_of_times_addable  # type: Optional[int]
        self.conjunction = conjunction  # type: RefinementConjunction


class RefinementConjunction:
    def __init__(self):
        self.literal_list = []  # type: List[RefinementLiteral]

    def get_possible_conjunctions(self, variables_already_in_query):
        pass


class RefinementLiteral:
    def __init__(self, functor: str, vars: List[RefinementVar]):
        self.functor = functor  # type: str
        self.refinement_var_list = vars  # type: List[RefinementVar]


class RefinementVar:
    def __init__(self, name: str, modes: List[str]):
        self.name = name  # type: str
        self.modes = modes  # type: List[str]

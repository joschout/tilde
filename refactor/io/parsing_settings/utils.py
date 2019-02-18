from typing import List
from typing import Optional
from problog.logic import Term, Constant, Var

from refactor.representation.language import TypeModeLanguage
from refactor.representation.example import Label


class SettingsParsingError(Exception):
    pass


class ConstantBuilder:
    @staticmethod
    def parse_constant_str(constant_str: str) -> Constant:
        if ConstantBuilder.is_int(constant_str):
            return Constant(int(constant_str))
        elif ConstantBuilder.is_float(constant_str):
            return Constant(float(constant_str))
        else:
            return Term(constant_str)

    @staticmethod
    def is_float(x: str) -> bool:
        try:
            a = float(x)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def is_int(x: str) -> bool:
        try:
            a = float(x)
            b = int(a)
        except ValueError:
            return False
        else:
            return a == b


class KeysPredictionGoalHandler:
    def __init__(self, functor, modes, types):
        self.functor = functor  # type: str
        self.modes = modes  # type: List[str]
        self.types = types  # type: List[str]

    def get_prediction_goal(self) -> Term:
        prediction_goal_term = Term(self.functor)

        nb_of_args = len(self.modes)
        arguments = [Var('#')] * nb_of_args
        prediction_goal_term = prediction_goal_term(*arguments)

        prediction_goal_term = prediction_goal_term.apply(TypeModeLanguage.ReplaceNew(0))
        return prediction_goal_term

    def get_predicate_goal_index_of_label_var(self) -> int:
        for index, arg_mode in enumerate(self.modes):
            if arg_mode == "-":
                return index
        raise SettingsParsingError("predicate to predict has no argument with arg_mode '-'")


class FileSettings:
    def __init__(self):
        self.possible_labels = []  # type: List[Label]
        self.language = TypeModeLanguage(False)
        self.is_typed = None  # type: Optional[bool]
        self.prediction_goal_handler = None  # type: KeysPredictionGoalHandler

    def add_labels(self, labels: List[Label]):
        self.possible_labels.extend(labels)

    def add_label(self, label: Label):
        self.possible_labels.append(label)

    def get_prediction_goal_handler(self) -> KeysPredictionGoalHandler:
        return self.prediction_goal_handler

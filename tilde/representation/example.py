from enum import Enum
from typing import Optional, Union, Set, Dict, Iterable, Tuple

from problog.engine import ClauseDB
from problog.logic import Term
from problog.program import SimpleProgram, PrologString

Probability = float


class InternalExampleFormat(Enum):
    SIMPLEPROGRAM = 1
    CLAUSEDB = 2


class LabelError(Exception):
    pass


class Example:
    def __init__(self, label=None):
        self.label = label  # type: Optional[Union[Term, Dict[Term, Probability]]]

    def get_label(self) -> Optional[Term]:
        try:
            return self.label
        except AttributeError:
            return None

    def set_label(self, label: Term):
        self.label = label

    def get_key(self) -> Optional[Term]:
        try:
            return self.key
        except AttributeError:
            return None

    def get_label_dict(self) -> Dict[Term, Probability]:
        if isinstance(self.label, dict):
            return self.label
        else:
            raise LabelError("method expected label to be a dict, but its value was: " + str(self.label))

    def get_probability_of_label(self, label: Term) -> float:
        label_dict = self.get_label_dict()
        return label_dict[label]


class SimpleProgramExample(SimpleProgram, Example):
    """Wrapper class for an example.
    An example  consists of a prolog program (e.g. facts and/or clauses)
    and MIGHT have a label.
    """

    def __init__(self):
        SimpleProgram.__init__(self)
        Example.__init__(self)


class ClauseDBExample(ClauseDB, Example):
    def __init__(self, builtins=None, parent=None):
        ClauseDB.__init__(self, builtins=builtins, parent=parent)
        Example.__init__(self)


class PrologStringExample(PrologString, Example):
    def __init__(self, string):
        PrologString.__init__(self, string)
        Example.__init__(self)


def calculate_majority_class(examples: Iterable[Example]) -> Tuple[Term, int]:
    """Calculate the majority class label in the given set of examples.
    """
    label_counts = {}
    for example in examples:
        if example.label in label_counts:
            label_counts[example.label] += 1
        else:
            label_counts[example.label] = 1
    label_with_max_count = max(label_counts, key=(lambda key: label_counts[key]))  # type: Term
    count = label_counts[label_with_max_count]  # type: int
    return label_with_max_count, count


def calculate_label_frequencies(examples):
    """Assumes that the examples each have ONE label, and not a distribution over labels"""
    label_counts = {}  # type: Dict[Term, float]

    for example in examples:  # type: Example
        label = example.get_label()  # type: Term
        label_counts[label] = label_counts.get(label, 0) + 1

    for label in label_counts.keys():
        label_counts[label] = label_counts[label] / len(examples)

    return label_counts


def calculate_label_frequencies_and_absolute_counts(examples: Iterable[Example]) -> Tuple[
    Dict[Term, float], Dict[Term, float]]:
    """Assumes that the examples each have ONE label, and not a distribution over labels"""
    label_counts = {}  # type: Dict[Term, float]

    for example in examples:  # type: Example
        label = example.label  # type: Term

        #    label = example.get_label()  # type: Term
        label_counts[label] = label_counts.get(label, 0) + 1

    label_frequencies = {}

    for label in label_counts.keys():
        label_frequencies[label] = label_counts[label] / len(examples)

    return label_frequencies, label_counts

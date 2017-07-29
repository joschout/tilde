from enum import Enum
from typing import Optional, Union, Set, Dict, Iterable, Tuple, List

from problog.engine import DefaultEngine, ClauseDB
from problog.logic import Term
from problog.program import SimpleProgram, PrologString, LogicProgram

Probability = float
Label = Union[Term, str]


class InternalExampleFormatException(Exception):
    pass


class InternalExampleFormat(Enum):
    SIMPLEPROGRAM = 1
    CLAUSEDB = 2


class LabelError(Exception):
    pass

# class Example:
#     def __init__(self, label=None, key: Optional = None):
#         self.label = label  # type: Optional[Union[Term, Dict[Term, Probability]]]
#         self.key = key
#
#     def get_label(self) -> Optional[Term]:
#         try:
#             return self.label
#         except AttributeError:
#             return None
#
#     def set_label(self, label: Term):
#         self.label = label
#
#     def get_key(self) -> Optional[Term]:
#         try:
#             return self.key
#         except AttributeError:
#             return None
#
#     def get_label_dict(self) -> Dict[Term, Probability]:
#         if isinstance(self.label, dict):
#             return self.label
#         else:
#             raise LabelError("method expected label to be a dict, but its value was: " + str(self.label))
#
#     def get_probability_of_label(self, label: Term) -> float:
#         label_dict = self.get_label_dict()
#         return label_dict[label]


class ExampleWrapper:
    def __init__(self, label=None, key: Optional = None, logic_program: Optional[LogicProgram] = None,
                 classification_term: Optional[Term] = None):
        self.label = label  # type: Optional[Union[Term, Dict[Term, Probability]]]
        self.key = key
        self.logic_program = logic_program  # type: Optional[LogicProgram]
        self.classification_term = classification_term  # type: Term

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

    def __iadd__(self, clause_fact: Term):
        self.logic_program += clause_fact
        return self

    def __iter__(self):
        return self.logic_program.__iter__()

# Example = ExampleWrapper


class SimpleProgramExampleWrapper(ExampleWrapper):
    def __init__(self, label=None, key: Optional = None, logic_program: Optional[LogicProgram] = None):
        super().__init__(label=label, key=key, logic_program=SimpleProgram())


class ClauseDBExampleWrapper(ExampleWrapper):
    def __init__(self, label=None, key: Optional = None, logic_program: Optional[LogicProgram] = None,
                 classification_term: Optional[Term] = None):
        if logic_program is not None and not isinstance(logic_program, ClauseDB):
            raise InternalExampleFormatException("the logic program of a ClauseDBExampleWrapper has to be a clause_db")

        super().__init__(label=label, key=key, logic_program=logic_program, classification_term=classification_term)

    def extend(self) -> ClauseDB:
        return self.logic_program.extend()

    @staticmethod
    def get_clause_db_examples(simple_program_examples: Iterable[SimpleProgramExampleWrapper],
                               background_knowledge: Optional[LogicProgram] = None) -> List['ClauseDBExampleWrapper']:
        engine = DefaultEngine()
        engine.unknown = 1

        clausedb_examples = []  # type: List[ClauseDBExampleWrapper]

        if background_knowledge is not None:
            db = engine.prepare(background_knowledge)  # type: ClauseDB
            for example in simple_program_examples:
                db_example = db.extend()  # type: ClauseDB
                for statement in example:
                    db_example += statement

                example_wrapper = ClauseDBExampleWrapper(logic_program=db_example)
                clausedb_examples.append(example_wrapper)

                if example.classification_term is not None:
                    example_wrapper.classification_term = example.classification_term
                if example.key is not None:
                    example_wrapper.key = example.key
                if example.label is not None:
                    example_wrapper.label = example.label

        else:  # background knowledge is None
            for example in simple_program_examples:
                db_example = engine.prepare(example.logic_program)  # type: ClauseDB

                example_wrapper = ClauseDBExampleWrapper(logic_program=db_example)
                clausedb_examples.append(example_wrapper)

                if example.classification_term is not None:
                    example_wrapper.classification_term = example.classification_term
                if example.key is not None:
                    example_wrapper.key = example.key
                if example.label is not None:
                    example_wrapper.label = example.label
        return clausedb_examples


def calculate_majority_class(examples: Iterable[ExampleWrapper]) -> Tuple[Term, int]:
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

    for example in examples:  # type: ExampleWrapper
        label = example.get_label()  # type: Term
        label_counts[label] = label_counts.get(label, 0) + 1

    for label in label_counts.keys():
        label_counts[label] = label_counts[label] / len(examples)

    return label_counts


def calculate_label_frequencies_and_absolute_counts(examples: Iterable[ExampleWrapper]) -> Tuple[
    Dict[Term, float], Dict[Term, float]]:
    """Assumes that the examples each have ONE label, and not a distribution over labels"""
    label_counts = {}  # type: Dict[Term, float]

    for example in examples:  # type: ExampleWrapperWrapper
        label = example.label  # type: Term

        #    label = example.get_label()  # type: Term
        label_counts[label] = label_counts.get(label, 0) + 1

    label_frequencies = {}

    for label in label_counts.keys():
        label_frequencies[label] = label_counts[label] / len(examples)

    return label_frequencies, label_counts

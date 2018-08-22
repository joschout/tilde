from typing import Iterable, Optional, List

# python 3.6
from problog.engine import DefaultEngine, ClauseDB
from problog.logic import Term
from problog.program import LogicProgram, SimpleProgram

from mai_version.IO.parsing_examples_keys_format import parse_examples_key_format_with_key
from mai_version.IO.parsing_examples_models_format import ModelsExampleParser
from mai_version.representation.example import Label, InternalExampleFormat, InternalExampleFormatException, \
    ClauseDBExampleWrapper
from mai_version.representation.example import SimpleProgramExampleWrapper
from mai_version.representation.example_collection import ExampleCollection
from mai_version.utils import deprecated

try:
    from typing import Collection
except ImportError:
    Collection = Iterable


class NoExamplesParsedException(Exception):
    pass


class ExampleBuilder:
    def __init__(self, debug_printing: Optional[bool] = False):
        # contains ONLY the examples
        # self.example_wrappers_sp = None  # type: Optional[List[SimpleProgramExampleWrapper]]
        #
        # # containt the examples, possibly extended with a background knowledge
        # self.example_wrappers_clausedb = None  # type: Optional[List[ClauseDBExampleWrapper]]
        self.training_example_collection = None  # type: Optional[ExampleCollection]
        self.debug_printing = debug_printing

    def parse(self, internal_ex_format: InternalExampleFormat, fname_examples: str,
              background_knowledge: Optional[SimpleProgram] = None) -> ExampleCollection:

        if internal_ex_format is InternalExampleFormat.CLAUSEDB:
            return self._parse_ex_clausedb(fname_examples, background_knowledge)
        elif internal_ex_format is InternalExampleFormat.SIMPLEPROGRAM:
            return self._parse_ex_simpleprogram(fname_examples)
        else:
            raise InternalExampleFormatException("Only the internal formats SimpleProgram and ClauseDB are supported, "
                                                 "got: " + str(internal_ex_format))

    def _parse_ex_simpleprogram(self, fname_examples: str) -> ExampleCollection:
        if self.debug_printing:
            print('start parsing kb examples into SimpleProgramExampleWrappers')
        example_wrappers_sp = self._parse_ex_simpleprogram_input_format(fname_examples)
        # type: List[SimpleProgramExampleWrapper]

        example_collection = ExampleCollection()
        example_collection.set_example_wrappers_sp(example_wrappers_sp)

        self.training_example_collection = example_collection

        if self.debug_printing:
            print('end parsing kb examples into SimpleProgramExampleWrappers')
        return self.training_example_collection

    def _parse_ex_clausedb(self, fname_examples: str, background_knowledge: Optional[SimpleProgram] = None) -> ExampleCollection:
        self._parse_ex_simpleprogram(fname_examples)  # type: List[SimpleProgramExampleWrapper]

        if self.debug_printing:
            print('start converting SimpleProgramExampleWrappers to ClauseDBExampleWrappers')

        example_wrappers_sp = self.training_example_collection.get_example_wrappers_sp()
        example_wrappers_clausedb = ClauseDBExampleWrapper.get_clause_db_examples(example_wrappers_sp, background_knowledge,
                                                                         )  # type: List[ClauseDBExampleWrapper]
        self.training_example_collection.set_example_wrappers_clausedb(example_wrappers_clausedb)

        if self.debug_printing:
            print('end converting SimpleProgramExampleWrappers to ClauseDBExampleWrappers')
        return self.training_example_collection

    def _parse_ex_simpleprogram_input_format(self, fname_examples) -> List[SimpleProgramExampleWrapper]:
        raise NotImplementedError('abstract method')


class ModelsExampleBuilder(ExampleBuilder):
    def __init__(self, possible_labels: Optional[List[Label]] = None, debug_printing: Optional[bool] = False):
        super().__init__(debug_printing)
        self.possible_labels = possible_labels

    def _parse_ex_simpleprogram_input_format(self, fname_examples: str) -> List[SimpleProgramExampleWrapper]:
        return ModelsExampleParser.parse(fname_examples, self.possible_labels)


class KeysExampleBuilder(ExampleBuilder):
    def __init__(self, prediction_goal: Optional[Term] = None, debug_printing: Optional[bool] = False):
        super().__init__(debug_printing)
        self.prediction_goal = prediction_goal

    def _parse_ex_simpleprogram_input_format(self, fname_examples: str) -> List[SimpleProgramExampleWrapper]:
        return parse_examples_key_format_with_key(fname_examples, self.prediction_goal)


# class ExampleBuilderMapper:
#     @staticmethod
#     def get_example_builder(kb_format: KnowledgeBaseFormat, debug_printing: Optional[bool] = False):
#         if kb_format is KnowledgeBaseFormat.KEYS:
#             return KeysExampleBuilder(debug_printing)
#         elif kb_format is KnowledgeBaseFormat.MODELS:
#             return ModelsExampleBuilder(debug_printing)
#         else:
#             raise KnowledgeBaseFormatException('Only the input formats Models and Key are supported.')


# todo: move this to ClauseDBExampleWrapper as a static method
@deprecated
def get_example_databases(simple_program_examples: Iterable[SimpleProgramExampleWrapper],
                          background_knowledge: Optional[LogicProgram] = None,
                          models=False,
                          engine=None) -> List[ClauseDBExampleWrapper]:
    if engine is None:
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
            if models:
                example_wrapper.label = example.label
    else:
        for example in simple_program_examples:
            db_example = engine.prepare(example.logic_program)  # type: ClauseDB

            example_wrapper = ClauseDBExampleWrapper(logic_program=db_example)
            clausedb_examples.append(example_wrapper)

            if example.classification_term is not None:
                example_wrapper.classification_term = example.classification_term
            if example.key is not None:
                example_wrapper.key = example.key
            if models:
                example_wrapper.label = example.label
    return clausedb_examples

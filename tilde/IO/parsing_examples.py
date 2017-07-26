from typing import Iterable, Optional, List
# python 3.6
from problog.engine import DefaultEngine
from problog.program import PrologFile, LogicProgram

from tilde.IO.parsing_examples_keys_format import parse_examples_key_format_with_key
from tilde.IO.parsing_examples_models_format import ModelsExampleParser
from tilde.representation.example import Label, ClauseDBExample, InternalExampleFormat, InternalExampleFormatException, \
    Example
from tilde.IO.input_format import KnowledgeBaseFormat, KnowledgeBaseFormatException
from tilde.representation.example import SimpleProgramExample
from tilde.representation.example import Example

try:
    from typing import Collection
except ImportError:
    Collection = Iterable


class NoExamplesParsedException(Exception):
    pass


class ExampleFormatHandler:
    def __init__(self):
        self.examples = None  # type: Optional[List[SimpleProgramExample]]
        self.example_dbs = None  # type: Optional[List[ClauseDBExample]]

    def parse(self, internal_ex_format: InternalExampleFormat, fname_examples: str, possible_labels: Optional[List[Label]] = None,
              background_knowledge: Optional[PrologFile] = None) -> List[Example]:

        if internal_ex_format is InternalExampleFormat.CLAUSEDB:
            return self._parse_ex_clausedb(fname_examples, possible_labels, background_knowledge)
        elif internal_ex_format is InternalExampleFormat.SIMPLEPROGRAM:
            return self._parse_ex_simpleprogram(fname_examples, possible_labels)
        else:
            raise InternalExampleFormatException("Only the internal formats SimpleProgram and ClauseDB are supported, "
                                                 "got: " + str(internal_ex_format))

    def _parse_ex_clausedb(self, fname_examples: str, possible_labels: Optional[List[Label]] = None,
                           background_knowledge: Optional[PrologFile] = None) -> List[Example]:
        raise NotImplementedError('Abstract method')

    def _parse_ex_simpleprogram(self, fname_examples: str, possible_labels: Optional[List[Label]] = None) -> List[Example]:
        raise NotImplementedError('Abstract method')

    def get_examples_to_use(self):
        if self.example_dbs is not None:
            return self.example_dbs
        elif self.examples is not None:
            return self.examples
        else:
            raise NoExamplesParsedException('No examples have been parsed')


class ModelsExampleFormatHandler(ExampleFormatHandler):
    def __init__(self):
        super().__init__()

    def _parse_ex_simpleprogram(self, fname_examples: str, possible_labels: Optional[List[Label]] = None) -> List[Example]:
        self.examples = ModelsExampleParser.parse(fname_examples, possible_labels)  # type: List[Example]
        return self.examples

    def _parse_ex_clausedb(self, fname_examples: str, possible_labels: Optional[List[Label]] = None,
                           background_knowledge: Optional[PrologFile] = None) -> List[Example]:
        self.examples = ModelsExampleParser.parse(fname_examples,
                                                  possible_labels)  # type: List[SimpleProgramExample]
        self.example_dbs = get_example_databases(self.examples, background_knowledge,
                                                 models=True)  # type: List[ClauseDBExample]
        return self.example_dbs


class KeysExampleFormatHandler(ExampleFormatHandler):
    def __init__(self):
        super().__init__()

    def _parse_ex_simpleprogram(self, fname_examples: str, possible_label: Optional[List[Label]] = None) -> List[Example]:
        self.examples = parse_examples_key_format_with_key(fname_examples)  # type: List[SimpleProgramExample]
        return self.examples

    def _parse_ex_clausedb(self, fname_examples: str, possible_labels: Optional[List[Label]] = None,
                           background_knowledge: Optional[PrologFile] = None):
        self.examples = parse_examples_key_format_with_key(fname_examples)  # type: List[SimpleProgramExample]
        self.example_dbs = get_example_databases(self.examples, background_knowledge)  # type: List[ClauseDBExample]
        return self.example_dbs


class ExampleFormatHandlerMapper:

    @staticmethod
    def get_example_format_handler(kb_format:KnowledgeBaseFormat):
        if kb_format is KnowledgeBaseFormat.KEYS:
            return KeysExampleFormatHandler()
        elif kb_format is KnowledgeBaseFormat.MODELS:
            return ModelsExampleFormatHandler()
        else:
            raise KnowledgeBaseFormatException('Only the input formats Models and Key are supported.')


def get_example_databases(examples: Iterable[Example], background_knowledge: Optional[LogicProgram] = None,
                          models=False) -> List[ClauseDBExample]:
    engine = DefaultEngine()
    engine.unknown = 1

    example_dbs = []  # type: List[ClauseDBExample]

    if background_knowledge is not None:
        db = engine.prepare(background_knowledge)  # type: ClauseDB
        for example in examples:
            db_example = db.extend()  # type: ClauseDB
            for statement in example:
                db_example += statement
            example_dbs.append(db_example)
            if example.key is not None:
                db_example.key = example.key
            if models:
                db_example.label = example.label
    else:
        for example in examples:
            db_example = engine.prepare(example)  # type: ClauseDB
            example_dbs.append(db_example)
            if example.key is not None:
                db_example.key = example.key
            if models:
                db_example.label = example.label
    return example_dbs
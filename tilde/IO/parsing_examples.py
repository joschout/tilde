from typing import Iterable
# python 3.6
from IO.input_format import KnowledgeBaseFormat
from tilde.representation.example import Example

try:
    from typing import Collection
except ImportError:
    Collection = Iterable


class ModelsExampleParserHandler:
    def __init__(self):
        self.examples = None
        self.examples_dbs = None

    def parse(self, examples: Collection[Example], kb_input_format: KnowledgeBaseFormat):
        pass
        #TODO: dit is enkel voor models, maak het ook compatible met keys
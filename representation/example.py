from typing import Optional

from problog.engine import ClauseDB
from problog.logic import Term
from problog.program import SimpleProgram


class Example:
    def __init__(self, label=None):
        self.label = label  # type: Optional[Term]

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


class SimpleProgramExample(SimpleProgram, Example):
    """Wrapper class for an example.
    An example  consists of a prolog program (e.g. facts and/or clauses)
    and MIGHT have a label.
    """
    pass


class ClauseDBExample(ClauseDB, Example):
    pass

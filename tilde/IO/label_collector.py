from typing import Iterable, Set

from problog.engine import DefaultEngine

from tilde.classification.classification_helper import Label
from tilde.representation.example import SimpleProgramExample, ClauseDBExample


class LabelCollector:
    def __init__(self, predicate_to_query, index_of_label_var, background_knowledge=None):
        self.engine = DefaultEngine()
        self.engine.unknown = 1
        if background_knowledge is not None:
            self.db = self.engine.prepare(background_knowledge)
        else:
            self.db = None
        self.predicate_to_query = predicate_to_query
        self.labels = set()  # type: Set[Label]
        self.index_of_label_var = index_of_label_var

    def get_labels(self) -> Set[Label]:
        return self.labels


class SimpleProgramLabelCollector(LabelCollector):
    def extract_label(self, example: SimpleProgramExample):
        if self.db is not None:
            db_example = self.db.extend()
            for statement in example:
                db_example += statement
        else:
            db_example = self.engine.prepare(example)

        list_of_answers = self.engine.query(db_example, self.predicate_to_query)
        if len(list_of_answers) is 0:
            raise Exception("Querying the predicate", self.predicate_to_query, "on the example gives no results")
        for answer in list_of_answers:
            label = answer[self.index_of_label_var]
            self.labels.add(label)
            example.label = label

    def extract_labels(self, examples: Iterable[SimpleProgramExample]):
        for example in examples:
            self.extract_label(example)


class ClauseDBLabelCollector(LabelCollector):
    def extract_labels(self, example_dbs: Iterable[ClauseDBExample]):
        for db_example in example_dbs:  # type: ClauseDBExample
            list_of_answers = self.engine.query(db_example, self.predicate_to_query)
            if len(list_of_answers) is 0:
                raise Exception("Querying the predicate", self.predicate_to_query, "on the example gives no results")
            for answer in list_of_answers:
                label = answer[self.index_of_label_var]
                self.labels.add(label)
                db_example.label = label

from typing import Iterable, List, Optional, Dict

import problog
from problog.engine import DefaultEngine, ClauseDB
from problog.logic import Term
from problog.program import SimpleProgram, LogicProgram

from tilde.representation.example import Example, Label, InternalExampleFormat, InternalExampleFormatException
# python 3.6
from tilde.representation.query_result_label_extractor import QueryResultLabelExtractor

try:
    from typing import Collection
except ImportError:
    Collection = Iterable


# class ModelValidator:
#     """
#     This class will probably have a lot in common with ExamplePartitioner
#
#     """
#
#     # def __init__(self, possible_labels: Iterable[Label]):
#     #
#     #
#     #     self.possible_labels = possible_labels  # type: Iterable[Label]
#
#     def check_model(self, test_examples: Collection[Example], model: SimpleProgram, debug_printing: bool = False):
#         raise NotImplementedError('Abstract method')
#
#
# class SimpleProgramModelValidator(ModelValidator):
#     """
#     ASSUMES:
#         deterministic treebuilder
#         simpleprogram examples
#         keys format
#
#
#     """
#
#     def check_model(self, test_examples: Collection[Example], model: SimpleProgram, debug_printing: bool = False):
#         for example in test_examples:
#             true_label = example.label
#
#     def classify_example(self, example: Example, model, possible_labels, background_knowledge=None) -> Label:
#         return get_labels_single_example_models(example, model, possible_labels, background_knowledge)[0]
#

class Classifier:
    """"
    IMPORTANT: has a lot of overlap with LabelCollector
    """

    def __init__(self,
                 query_result_label_extractor: QueryResultLabelExtractor,
                 debug_printing: Optional[bool] = None):
        self.engine = DefaultEngine()
        self.engine.unknown = 1
        self.debug_printing = debug_printing

        self.query_result_label_extractor = query_result_label_extractor

    def classify(self, example: Example) -> List[Label]:
        raise NotImplementedError('Abstract method')

    def _query(self, db_to_query) -> Dict[Term, float]:
        return problog.get_evaluatable().create_from(db_to_query,
                                                     engine=self.engine).evaluate()  # type: Dict[Term, float]


# query_terms = [Term('query')(label) for label in possible_labels]
class SimpleProgramClassifier(Classifier):
    """
    MODELS:
        query_facts = [Term('query')(label) for label in possible_labels]
    KEYS:
        query_terms = [Term('query')(prediction_goal)]
    """

    def __init__(self, model: SimpleProgram,
                 query_facts: List[Term],
                 query_result_label_extractor: QueryResultLabelExtractor,
                 background_knowledge: Optional[LogicProgram] = None,
                 debug_printing: Optional[bool] = None):
        super().__init__(query_result_label_extractor, debug_printing)

        if background_knowledge is None:
            self.db = self.engine.prepare(model)
        else:
            self.db = self.engine.prepare(background_knowledge)
            for model_statement in model:
                self.db += model_statement
        # --------------------
        for qt in query_facts:
            self.db += qt

    def classify(self, example: SimpleProgram) -> List[Label]:
        """"
        Classifies a single example and returns a list of its labels.
        """
        db_to_query = self.db.extend()  # type: ClauseDB
        for ex_statement in example:
            db_to_query += ex_statement

        query_results = self._query(db_to_query)  # type: Dict[Term, float]
        labels = self.query_result_label_extractor.extract_labels(query_results)  # type: List[Label]

        if self.debug_printing:
            print('\nQueried database:')
            for model_db_statement in self.db:
                print('\t' + str(model_db_statement))
            for ex_statement in db_to_query:
                print('\t' + str(ex_statement))
            print('Query results:')
            print('\t' + str(query_results))
            print('Chosen class labels:')
            print('\t' + str(labels))

        return labels


class ClauseDBClassifier(Classifier):
    """
    MODELS:
        query_facts = [Term('query')(label) for label in possible_labels]
    KEYS:
        query_terms = [Term('query')(prediction_goal)]
    """

    def __init__(self, model: SimpleProgram,
                 query_facts: List[Term],
                 query_result_label_extractor: QueryResultLabelExtractor,
                 debug_printing: Optional[bool] = None):
        super().__init__(query_result_label_extractor, debug_printing)
        self.model = model  # type: SimpleProgram
        self.query_terms = query_facts

    def classify(self, example: ClauseDB):
        db_to_query = example.extend()

        for model_statement in self.model:
            db_to_query += model_statement

        for query_term in self.query_terms:
            db_to_query += query_term

        query_results = self._query(db_to_query)  # type: Dict[Term, float]
        labels = self.query_result_label_extractor.extract_labels(query_results)  # type: List[Label]

        if self.debug_printing:
            print('\nQueried database:')
            print('\tPossibly contains background knowledge, printing of extended ClauseDB not supported')
            for ex_statement in example:
                print('\t' + str(ex_statement))
            for statement in db_to_query:
                print('\t' + str(statement))
            print('Query results:')
            print('\t' + str(query_results))
            print('Chosen class labels:')
            print('\t' + str(labels))

        return labels


class ClassifierMapper:
    @staticmethod
    def get_classifier(internal_ex_format: InternalExampleFormat,
                       model: SimpleProgram,
                       query_facts: List[Term],
                       query_result_label_extractor: QueryResultLabelExtractor,
                       background_knowledge: Optional[LogicProgram] = None,
                       debug_printing: Optional[bool] = None
                       ):
        if internal_ex_format is InternalExampleFormat.CLAUSEDB:
            return ClauseDBClassifier(model, query_facts, query_result_label_extractor, debug_printing)
        elif internal_ex_format is InternalExampleFormat.SIMPLEPROGRAM:
            return SimpleProgramClassifier(model, query_facts, query_result_label_extractor,
                                           background_knowledge, debug_printing)
        else:
            raise InternalExampleFormatException("Only the internal formats SimpleProgram and ClauseDB are supported, "
                                                 "got: " + str(internal_ex_format))

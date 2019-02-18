from typing import Set, Tuple

from problog.engine import DefaultEngine, GenericEngine

from refactor.representation.example import InternalExampleFormat, InternalExampleFormatException, Label, \
    SimpleProgramExampleWrapper, ClauseDBExampleWrapper
from refactor.representation.example_collection import ExampleCollection


class LabelCollector:
    """"

    IMPORTANT:
        * ONLY for KEYS format
        * has a lot of overlap with Classifier
    """

    def __init__(self, predicate_to_query, index_of_label_var, background_knowledge=None, debug_printing=False, engine: GenericEngine=None):
        if engine is None:
            self.engine = DefaultEngine()
            self.engine.unknown = 1
        else:
            self.engine = engine
        if background_knowledge is not None:
            self.db = self.engine.prepare(background_knowledge)
        else:
            self.db = None
        self.predicate_to_query = predicate_to_query
        self.labels = set()  # type: Set[Label]
        self.index_of_label_var = index_of_label_var
        self.debug_printing = debug_printing

    def get_labels(self) -> Set[Label]:
        return self.labels

    def extract_labels(self, example_collection: ExampleCollection):
        raise NotImplementedError('Abstract method')


# TODO: refactor: use query_result_label_extractor
# TODO: INCORRECT: label could be defined in background knowledge
class SimpleProgramLabelCollector(LabelCollector):
    def extract_label(self, example: SimpleProgramExampleWrapper):
        if example.classification_term is not None:
            label = example.classification_term.args[self.index_of_label_var]
            self.labels.add(label)
            example.label = label
        else:
            if self.db is not None:
                db_example = self.db.extend()
                for statement in example:
                    db_example += statement
            else:
                db_example = self.engine.prepare(example.logic_program)

            query_results = self.engine.query(db_example, self.predicate_to_query)
            if len(query_results) is 0:
                raise Exception("Querying the predicate", self.predicate_to_query, "on the example gives no results")
            for answer in query_results:
                label = answer[self.index_of_label_var]
                self.labels.add(label)
                example.label = label

    def extract_labels(self, example_collection: ExampleCollection):
        for example_wrapper in example_collection.get_example_wrappers_sp():
            self.extract_label(example_wrapper)
        example_collection.are_sp_examples_labeled = True


class ClauseDBLabelCollector(LabelCollector):
    def extract_labels(self, example_collection: ExampleCollection):
        example_wrappers_sp = example_collection.get_example_wrappers_sp()
        example_wrappers_clausedb = example_collection.get_example_wrappers_clausedb()

        keys_of_unlabeled_examples = set()
        label_distribution = {}

        for ex_index, clause_db_ex in enumerate(example_wrappers_clausedb):  # type: Tuple[int, ClauseDBExampleWrapper]
            if clause_db_ex.classification_term is not None:
                label = clause_db_ex.classification_term.args[self.index_of_label_var]
                self.labels.add(label)
                clause_db_ex.label = label

                if label in label_distribution.keys():
                    label_distribution[label] = label_distribution[label] + 1
                else:
                    label_distribution[label] = 1
            else:
                # TODO: update this to the probabilistic way of querying
                query_results = self.engine.query(clause_db_ex.logic_program, self.predicate_to_query)
                if len(query_results) is 0:
                    example_str = ""
                    for ex_statement in clause_db_ex:
                        print(ex_statement)
                    print("--")
                    keys_of_unlabeled_examples.add(clause_db_ex.get_key())
                    # raise Exception("Querying the predicate", self.predicate_to_query, "on the example gives no results. Example: \n", example_str)
                for answer in query_results:
                    label = answer[self.index_of_label_var]
                    self.labels.add(label)
                    clause_db_ex.label = label

                    if label in label_distribution.keys():
                        label_distribution[label] = label_distribution[label] + 1
                    else:
                        label_distribution[label] = 1
            # --------------------------------
            example_wrappers_sp[ex_index].label = clause_db_ex.label
        # ---------------------------------------------
        # set flags
        example_collection.are_sp_examples_labeled = True
        example_collection.are_clausedb_examples_labeled = True

        nb_examples = len(example_wrappers_clausedb)
        print("nb of examples: " + str(nb_examples))
        nb_unlabeled_examples = len(keys_of_unlabeled_examples)
        print("nb of unlabeled examples: " + str(nb_unlabeled_examples))
        print("nb of labeled examples: " + str(nb_examples - nb_unlabeled_examples))
        print("indexes of unlabeled examples:")
        print(keys_of_unlabeled_examples)
        print("label distribution:")
        print(label_distribution)

        return keys_of_unlabeled_examples


class LabelCollectorMapper:
    @staticmethod
    def get_label_collector(internal_ex_format: InternalExampleFormat, predicate_to_query, index_of_label_var,
                            background_knowledge=None, engine: GenericEngine=None):
        if internal_ex_format is internal_ex_format.CLAUSEDB:
            return ClauseDBLabelCollector(predicate_to_query, index_of_label_var, background_knowledge, engine=engine)
        elif internal_ex_format is InternalExampleFormat.SIMPLEPROGRAM:
            return SimpleProgramLabelCollector(predicate_to_query, index_of_label_var, background_knowledge, engine=engine)
        else:
            raise InternalExampleFormatException("Only the internal formats SimpleProgram and ClauseDB are supported, "
                                                 "got: " + str(internal_ex_format))

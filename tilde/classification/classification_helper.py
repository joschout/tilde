import warnings
from typing import Iterable, List, Dict, Tuple

# python 3.6
from tilde.model_validation.model_validation import ClassifierMapper, Classifier
from tilde.representation.query_result_label_extractor import ModelsQueryResultLabelExtractor, \
    KeysQueryResultLabelExtractor

try:
    from typing import Collection
except ImportError:
    Collection = Iterable

from problog.logic import Term
from problog.program import SimpleProgram, LogicProgram

from tilde.representation.example import Example, InternalExampleFormat, Label


class ClassificationStatisticsHandler:
    def __init__(self, possible_labels: List[Label]):
        self.confusion_matrix = {}  # type: Dict[Tuple[Term, Term], int]
        self.possible_labels = possible_labels

        self.total_nb_of_examples = 0
        self.nb_ex_correctly_classified = 0
        self.nb_ex_incorrectly_classified = 0

    def update_statistics(self, actual_label, predicted_label):

        is_correctly_classified = (actual_label == predicted_label)
        if is_correctly_classified:
            self.nb_ex_correctly_classified += 1
        else:
            self.nb_ex_incorrectly_classified += 1

        self.total_nb_of_examples += 1

        key = (actual_label, predicted_label)
        old_value = self.confusion_matrix.get(key, 0)
        new_value = old_value + 1
        self.confusion_matrix[key] = new_value

    def get_confusion_matrix_str(self) -> str:

        max_label_str_len = max([len(str(label)) for label in self.possible_labels])

        result = ' ' * max_label_str_len + '|'

        column_sums = {}  # type: Dict[Term, int]

        # === create header row + initialize sum of columns ===
        for first_row_label in self.possible_labels:
            column_sums[first_row_label] = 0

            str_label = str(first_row_label)
            label_str_len = len(str_label)
            result = result + str(first_row_label) + ' ' * (max_label_str_len - label_str_len) + '|'
        # --------------------
        result = result + '\n'
        # =========================

        nb_of_labels = len(self.possible_labels)
        horizontal_bar_str = '-' * ((nb_of_labels + 2) * max_label_str_len + nb_of_labels + 1)
        result = result + horizontal_bar_str + '\n'

        # == create table rows ===
        for first_column_label in self.possible_labels:
            # first column value of this row is a label
            first_column_label_str = str(first_column_label)
            first_column_label_str_len = len(first_column_label_str)
            result = result + first_column_label_str + ' ' * (max_label_str_len - first_column_label_str_len) + '|'

            # initialize sum of this row
            row_sum = 0

            # other column values of this table
            for row_label in self.possible_labels:
                key = (first_column_label, row_label)
                value = self.confusion_matrix.get(key, 0)
                value_str = str(value)
                value_str_len = len(value_str)

                # update column and row sums
                column_sums[row_label] = column_sums.get(row_label, 0) + value
                row_sum += value

                result = result + ' ' * (max_label_str_len - value_str_len) + value_str + '|'
            # --------------------
            # close this row with the row sum
            result = result + '\tactual: ' + str(row_sum) + '\n'
        # =========================

        # last row: print the column sums
        result = result + horizontal_bar_str + '\n'

        total_nb_of_examples = 0

        result = result + ' ' * max_label_str_len + '|'
        for column_label in self.possible_labels:
            column_sum = column_sums[column_label]
            column_sum_str = str(column_sum)
            column_sum_str_len = len(column_sum_str)

            total_nb_of_examples += column_sum

            result = result + ' ' * (max_label_str_len - column_sum_str_len) + column_sum_str + '|'

        result = result + '\ttotal: ' + str(self.total_nb_of_examples)

        return result


def get_models_classifier(internal_ex_format: InternalExampleFormat, model: SimpleProgram,
                          possible_labels: Iterable[Label],
                          background_knowledge: LogicProgram, debug_printing: bool = False) -> Classifier:
    query_terms = [Term('query')(label) for label in possible_labels]
    query_result_label_extractor = ModelsQueryResultLabelExtractor()
    classifier = ClassifierMapper.get_classifier(internal_ex_format, model, query_terms, query_result_label_extractor,
                                                 background_knowledge, debug_printing=debug_printing)
    return classifier


def get_keys_classifier(internal_ex_format: InternalExampleFormat, model: SimpleProgram,
                        prediction_goal: Term, index_of_label_arg: int,
                        background_knowledge: LogicProgram, debug_printing: bool = False):
    query_terms = [Term('query')(prediction_goal)]
    query_result_label_extractor = KeysQueryResultLabelExtractor()
    query_result_label_extractor.set_index_of_label_arg(index_of_label_arg)
    classifier = ClassifierMapper.get_classifier(internal_ex_format, model, query_terms, query_result_label_extractor,
                                                 background_knowledge, debug_printing=debug_printing)
    return classifier


def do_labeled_examples_get_correctly_classified(classifier: Classifier, examples: Collection[Example],
                                                 possible_labels: List[Label],
                                                 debug_printing: bool = False):
    warnings.warn("Model verification only supports deterministic models")

    if debug_printing:
        print('\n=== CHECKING MODEL ===')
        print("Model verification only supports deterministic models")

    statistics_handler = ClassificationStatisticsHandler(possible_labels)

    for example in examples:
        actual_label = example.label
        found_labels = classifier.classify(example)
        a_predicted_label = found_labels[0]

        statistics_handler.update_statistics(actual_label, a_predicted_label)
    # -------------

    nb_of_examples = len(examples)
    nb_of_correcty_labeled_examples = statistics_handler.nb_ex_correctly_classified
    nb_of_incorrecty_labeled_examples = statistics_handler.nb_ex_incorrectly_classified

    if debug_printing:
        print("total nb of examples: " + str(nb_of_examples))
        print(
            "examples labeled correctly: " + str(nb_of_correcty_labeled_examples) + "/" + str(
                nb_of_examples) + ", " + str(
                nb_of_correcty_labeled_examples / nb_of_examples * 100) + "%")
        print("examples labeled incorrectly: " + str(nb_of_incorrecty_labeled_examples) + "/" + str(
            nb_of_examples) + ", " + str(
            nb_of_incorrecty_labeled_examples / nb_of_examples * 100) + "%")
        print("confusion matrix:")
        print("------------------\n")
        print(statistics_handler.get_confusion_matrix_str())

# def do_labeled_examples_get_correctly_classified_keys(labeled_examples, rules_as_program, prediction_goal: Term,
#                                                       index_of_label_var: int, possible_labels: Iterable[str],
#                                                       background_knowledge, debug_printing: bool = False) -> bool:
#     """
#     Accepts both SimpleProgram Examples as ClauseDB examples.
#
#     :param labeled_examples:
#     :param rules_as_program:
#     :param prediction_goal:
#     :param index_of_label_var:
#     :param possible_labels:
#     :param background_knowledge:
#     :param debug_printing:
#     :return:
#     """
#
#     if debug_printing:
#         print('\n=== Model validation ===')
#
#     nb_of_examples = len(labeled_examples)
#     nb_of_correcty_labeled_examples = 0
#     nb_of_incorrecty_labeled_examples = 0
#
#     all_training_examples_labeled_correctly = True
#
#     for example in labeled_examples:
#         true_label = example.label
#
#         # NOTE: we strip the statements from the example and put it into a new example.
#         # This is why this method works for both SimplePrograms and ClauseDBs
#
#         # remove the labeling from the labeled example
#         example_without_label = SimpleProgram()
#         for statement in example:  # type: Term
#             if statement.functor != prediction_goal.functor:
#                 example_without_label += statement
#
#         found_label = \
#             get_labels_single_example_keys(example_without_label, rules_as_program, prediction_goal, index_of_label_var,
#                                            possible_labels,
#                                            background_knowledge)[0]
#
#         label_is_correct = (true_label == found_label)
#         if label_is_correct:
#             nb_of_correcty_labeled_examples += 1
#             # output = 'correct\treal label: ' + str(true_label) + '\tfound label: ' + str(found_label)
#             # print(output)
#         else:
#             all_training_examples_labeled_correctly = False
#             nb_of_incorrecty_labeled_examples += 1
#             if debug_printing:
#                 output = 'incorrect\n\treal label: ' + str(true_label) + '\n\tfound label: ' + str(found_label)
#                 print(output)
#                 print('\tincorrectly labeled example:')
#                 for statement in example:
#                     print('\t\t' + str(statement))
#                 get_labels_single_example_models(example, rules_as_program, possible_labels, background_knowledge,
#                                                  debug_printing)
#                 print('----------------')
#
#     if debug_printing:
#         print("total nb of examples: " + str(nb_of_examples))
#         print("examples labeled correctly: " + str(nb_of_correcty_labeled_examples) + "/" + str(
#             nb_of_examples) + ", " + str(
#             nb_of_correcty_labeled_examples / nb_of_examples * 100) + "%")
#         print("examples labeled incorrectly: " + str(nb_of_incorrecty_labeled_examples) + "/" + str(
#             nb_of_examples) + ", " + str(
#             nb_of_incorrecty_labeled_examples / nb_of_examples * 100) + "%")
#
#     return all_training_examples_labeled_correctly

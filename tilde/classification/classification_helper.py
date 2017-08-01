import warnings
from typing import Iterable, List

# from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, precision_score, recall_score

# python 3.6
from tilde.classification.classification_statistics_handler import ClassificationStatisticsHandler
from tilde.model_validation.model_validation import ClassifierMapper, Classifier
from tilde.representation.query_result_label_extractor import ModelsQueryResultLabelExtractor, \
    KeysQueryResultLabelExtractor

try:
    from typing import Collection
except ImportError:
    Collection = Iterable

from problog.logic import Term
from problog.program import SimpleProgram, LogicProgram

from tilde.representation.example import ExampleWrapper, InternalExampleFormat, Label


def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""
    columnwidth = max([len(x) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * columnwidth
    # Print header
    print("    " + empty_cell, end=" ")
    for label in labels:
        print("%{0}s".format(columnwidth) % label, end=" ")
    print()
    # Print rows
    for i, label1 in enumerate(labels):
        print("    %{0}s".format(columnwidth) % label1, end=" ")
        for j in range(len(labels)):
            cell = "%{0}.1f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()


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


def do_labeled_examples_get_correctly_classified(classifier: Classifier, examples: Collection[ExampleWrapper],
                                                 possible_labels: List[Label],
                                                 debug_printing: bool = False) -> ClassificationStatisticsHandler:
    warnings.warn("Model verification only supports deterministic models")

    if debug_printing:
        print('\n=== CHECKING MODEL ===')
        print("Model verification only supports deterministic models")

    statistics_handler = ClassificationStatisticsHandler(possible_labels)

    # classifier.debug_printing = True

    actual_labels = []
    predicted_labels = []

    for example in examples:
        actual_label = example.label
        found_labels = classifier.classify(example)
        if len(found_labels) > 1:
            print('actual label: ', actual_label)
            print('found labels: ', found_labels)

        a_predicted_label = found_labels[0]

        # TEST
        actual_labels.append(str(actual_label))
        predicted_labels.append(str(a_predicted_label))

        statistics_handler.update_statistics(actual_label, a_predicted_label)
    # -------------

    # conf_matrix = confusion_matrix(actual_labels, predicted_labels)
    # accuracy = accuracy_score(actual_labels, predicted_labels)
    #
    # possible_labels_str = [str(label) for label in possible_labels]

    # print("sklearn confusion matrix:")
    # print(conf_matrix)
    # print("pretty print:")
    # print_cm(conf_matrix, labels=possible_labels_str)
    print("===  MODEL VERIFICATION STATISTICS ===")

    print(statistics_handler.get_accuracy()[1])

    # precision = precision_score(actual_labels, predicted_labels)
    # recall = recall_score(actual_labels, predicted_labels)
    # print('precision:')
    # print('\t' + str(precision))
    # print('recall:')
    # print('\t' + str(recall))

    print(statistics_handler.get_classification_report_str())
    print(statistics_handler.get_nb_of_examples_str_verbose() + '\n')
    print(statistics_handler.get_confusion_matrix_str())

    # nb_of_examples = len(examples)
    # nb_of_correcty_labeled_examples = statistics_handler.nb_ex_correctly_classified
    # nb_of_incorrecty_labeled_examples = statistics_handler.nb_ex_incorrectly_classified
    #
    # if debug_printing:
    #     print("total nb of examples: " + str(nb_of_examples))
    #     print(
    #         "examples labeled correctly: " + str(nb_of_correcty_labeled_examples) + "/" + str(
    #             nb_of_examples) + ", " + str(
    #             nb_of_correcty_labeled_examples / nb_of_examples * 100) + "%")
    #     print("examples labeled incorrectly: " + str(nb_of_incorrecty_labeled_examples) + "/" + str(
    #         nb_of_examples) + ", " + str(
    #         nb_of_incorrecty_labeled_examples / nb_of_examples * 100) + "%\n")
    #     print("--- confusion matrix: true/predicted --- :")
    #     print(statistics_handler.get_confusion_matrix_str())

    return statistics_handler

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

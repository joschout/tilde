import warnings
from typing import Iterable, List, Union, Optional

# python 3.6
from tilde.model_validation.model_validation import ClassifierMapper, Classifier
from tilde.representation.query_result_label_extractor import ModelsQueryResultLabelExtractor, \
    KeysQueryResultLabelExtractor

try:
    from typing import Collection
except ImportError:
    Collection = Iterable

from problog.engine import ClauseDB, DefaultEngine
from problog.logic import Term
from problog.program import SimpleProgram, LogicProgram

from tilde.classification.classification import get_labels_single_example_models, get_labels_single_example_keys
from tilde.representation.example import ClauseDBExample, Example, InternalExampleFormat, Label


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
                                                        debug_printing: bool = False):
    warnings.warn("Model verification only supports deterministic models")

    if debug_printing:
        print('\n=== CHECKING MODEL ===')
        print("Model verification only supports deterministic models")

    nb_of_examples = len(examples)
    nb_of_correcty_labeled_examples = 0
    nb_of_incorrecty_labeled_examples = 0

    for example in examples:
        true_label = example.label
        found_labels = classifier.classify(example)
        a_found_label = found_labels[0]
        label_is_correct = (true_label == a_found_label)

        if label_is_correct:
            nb_of_correcty_labeled_examples += 1
        else:
            nb_of_incorrecty_labeled_examples += 1

    if debug_printing:
        print("total nb of examples: " + str(nb_of_examples))
        print(
            "examples labeled correctly: " + str(nb_of_correcty_labeled_examples) + "/" + str(
                nb_of_examples) + ", " + str(
                nb_of_correcty_labeled_examples / nb_of_examples * 100) + "%")
        print("examples labeled incorrectly: " + str(nb_of_incorrecty_labeled_examples) + "/" + str(
            nb_of_examples) + ", " + str(
            nb_of_incorrecty_labeled_examples / nb_of_examples * 100) + "%")


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

from typing import Iterable, List

from problog.engine import ClauseDB, DefaultEngine
from problog.logic import Term
from problog.program import SimpleProgram

from classification.classification import get_labels_single_example_models, get_labels_single_example_keys
from representation.example import ClauseDBExample


def do_labeled_examples_get_correctly_classified_models(labeled_examples, rules_as_program, possible_labels,
                                                        background_knowledge):
    nb_of_examples = len(labeled_examples)
    nb_of_correcty_labeled_examples = 0
    nb_of_incorrecty_labeled_examples = 0
    for example in labeled_examples:
        true_label = example.label
        found_label = \
            get_labels_single_example_models(example, rules_as_program, possible_labels, background_knowledge)[0]

        label_is_correct = (true_label == found_label)
        if label_is_correct:
            nb_of_correcty_labeled_examples += 1
            # output = 'correct\treal label: ' + str(true_label) + '\tfound label: ' + str(found_label)
            # print(output)
        else:
            nb_of_incorrecty_labeled_examples += 1
            output = 'incorrect\n\treal label: ' + str(true_label) + '\n\tfound label: ' + str(found_label)
            print(output)
            print('\tincorrectly labeled example:')
            for statement in example:
                print('\t\t' + str(statement))
            get_labels_single_example_models(example, rules_as_program, possible_labels, background_knowledge,
                                             debug_printing=True)
            print('----------------')

    print("total nb of examples: " + str(nb_of_examples))
    print(
        "examples labeled correctly: " + str(nb_of_correcty_labeled_examples) + "/" + str(nb_of_examples) + ", " + str(
            nb_of_correcty_labeled_examples / nb_of_examples * 100) + "%")
    print("examples labeled incorrectly: " + str(nb_of_incorrecty_labeled_examples) + "/" + str(
        nb_of_examples) + ", " + str(
        nb_of_incorrecty_labeled_examples / nb_of_examples * 100) + "%")


def do_labeled_examples_get_correctly_classified_keys(labeled_examples, rules_as_program, prediction_goal: Term,
                                                      index_of_label_var: int, possible_labels: Iterable[str],
                                                      background_knowledge):
    nb_of_examples = len(labeled_examples)
    nb_of_correcty_labeled_examples = 0
    nb_of_incorrecty_labeled_examples = 0
    for example in labeled_examples:
        true_label = example.label

        # remove the labeling from the labeled example
        example_without_label = SimpleProgram()
        for statement in example:  # type: Term
            if statement.functor != prediction_goal.functor:
                example_without_label += statement

        found_label = \
            get_labels_single_example_keys(example_without_label, rules_as_program, prediction_goal, index_of_label_var,
                                           possible_labels,
                                           background_knowledge)[0]

        label_is_correct = (true_label == found_label)
        if label_is_correct:
            nb_of_correcty_labeled_examples += 1
            # output = 'correct\treal label: ' + str(true_label) + '\tfound label: ' + str(found_label)
            # print(output)
        else:
            nb_of_incorrecty_labeled_examples += 1
            output = 'incorrect\n\treal label: ' + str(true_label) + '\n\tfound label: ' + str(found_label)
            print(output)
            print('\tincorrectly labeled example:')
            for statement in example:
                print('\t\t' + str(statement))
            get_labels_single_example_models(example, rules_as_program, possible_labels, background_knowledge,
                                             debug_printing=True)
            print('----------------')

    print("total nb of examples: " + str(nb_of_examples))
    print("examples labeled correctly: " + str(nb_of_correcty_labeled_examples) + "/" + str(
            nb_of_examples) + ", " + str(
            nb_of_correcty_labeled_examples / nb_of_examples * 100) + "%")
    print("examples labeled incorrectly: " + str(nb_of_incorrecty_labeled_examples) + "/" + str(
        nb_of_examples) + ", " + str(
        nb_of_incorrecty_labeled_examples / nb_of_examples * 100) + "%")


def get_example_databases(examples, background_knowledge=None) -> List[ClauseDBExample]:
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
    else:
        for example in examples:
            db_example = engine.prepare(example)  # type: ClauseDB
            example_dbs.append(db_example)
    return example_dbs

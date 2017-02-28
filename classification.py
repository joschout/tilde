from typing import Iterable, List, Tuple, Set

from problog.engine import ClauseDB
from problog.engine import DefaultEngine
from problog.program import SimpleProgram
from problog.program import Term

from representation.example import Example


def get_label_old(examples: Iterable[SimpleProgram], rules: SimpleProgram, possible_labels: Iterable[str]) -> List[str]:
    label_list = []
    eng = DefaultEngine()
    eng.unknown = 1
    db_rules = eng.prepare(rules)

    for example in examples:
        db_example = db_rules.extend()
        for statement in example:
            db_example += statement

        result_list = [eng.query(db_example, x) for x in possible_labels]
        labels_str = ''
        for i in range(0, len(possible_labels)):
            labels_str = labels_str + str(possible_labels[i]) + ': ' + str(bool(result_list[i])) + ", "
        label_list.append(labels_str)
    return label_list


def get_label(examples: Iterable[SimpleProgram], rules: SimpleProgram, possible_labels: Iterable[str]) -> List[Tuple[SimpleProgram, List[str]]]:
    """
    Labels a collection of example using the given rules and the given collection of possible labels
    :param examples:
    :param rules:
    :param possible_labels:
    :return:
    """
    labeled_examples = []
    eng = DefaultEngine()
    eng.unknown = 1
    rule_db = eng.prepare(rules)  # type: ClauseDB

    for example in examples:
        example_db = rule_db.extend()  # type: ClauseDB
        for statement in example:
            example_db += statement

        example_labels = []
        for label in possible_labels:
            has_label = bool(eng.query(example_db, label))
            if has_label:
                example_labels.append(label)
        labeled_examples.append((example, example_labels))
    return labeled_examples


def get_label_single_example(example: SimpleProgram, rules: SimpleProgram, possible_labels: Iterable[str], background_knowledge=None, debug_printing=False) -> List[str]:
    """
    Classifies a single example and returns a list of its labels
    :param example:
    :param rules:
    :param possible_labels:
    :return:
    """
    eng = DefaultEngine()
    eng.unknown = 1

    if background_knowledge is not None:
        db = eng.prepare(background_knowledge)
        for statement in example:
            db += statement
        for rule in rules:
            db += rule
    else:
        db = eng.prepare(rules)
        for statement in example:
            db += statement

    if debug_printing:
        print('\nQueried database:')
        for statement in db:
            print('\t' + str(statement))
        #print('\n')

    result_list = [eng.query(db, x) for x in possible_labels]
    zipped = zip(result_list, possible_labels)
    labels_ex = []
    if debug_printing:
        print('\nQueries on the database:')
    for result_ex, label in zipped:
        if result_ex == [()]:
            labels_ex.append(label)
        if debug_printing:
            print('\tquery: ' + str(label) + ', result: ' + str(bool(result_ex)))
    return labels_ex


def get_examples_satisfying_query(examples: Iterable[Example], query, background_knowledge: SimpleProgram) -> Set[Example]:
    engine = DefaultEngine()
    engine.unknown = 1

    db = engine.prepare(background_knowledge)
    to_query = Term('to_query')
    db += (to_query << query)

    query_results = set()

    for example in examples:
        db_example = db.extend()
        for statement in example:
            db_example += statement

        example_satisfies_query = engine.query(db_example, to_query)
        if bool(example_satisfies_query):
            query_results.add(example)
    return query_results
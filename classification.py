from typing import Iterable, List, Tuple

from problog.engine import ClauseDB
from problog.engine import DefaultEngine
from problog.program import SimpleProgram


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


def get_label_single_example(example: SimpleProgram, rules: SimpleProgram, possible_labels: Iterable[str]) -> List[str]:
    """
    Classifies a single example and returns a list of its labels
    :param example:
    :param rules:
    :param possible_labels:
    :return:
    """
    eng = DefaultEngine()
    eng.unknown = 1
    db = eng.prepare(rules)
    for statement in example:
        db += statement
    result_list = [eng.query(db, x) for x in possible_labels]
    zipped = zip(result_list, possible_labels)
    labels_ex = []
    for result_ex, label in zipped:
        if result_ex == [()]:
            labels_ex.append(label)
    return labels_ex
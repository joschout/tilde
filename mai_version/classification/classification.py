from typing import Iterable, List

import problog
import time
from problog.engine import DefaultEngine, ClauseDB
from problog.program import SimpleProgram
from problog.program import Term

from mai_version.utils import deprecated


@deprecated
def get_labels_single_example_models(example: SimpleProgram, rules: SimpleProgram, possible_labels: Iterable[str],
                                     background_knowledge=None, debug_printing=False) -> List[str]:
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
            # print('\n')

    result_list = []
    for label in possible_labels:
        db_to_query = db.extend()
        db_to_query += Term('query')(label)
        start_time = time.time()
        result = problog.get_evaluatable().create_from(db_to_query, engine=eng).evaluate()
        end_time = time.time()
        print("call time:", end_time-start_time)

        if result[label] > 0.5:
            result_list.append(label)

    return result_list
    # # result_list = [eng.query(db, x) for x in possible_labels]
    # zipped = zip(result_list, possible_labels)
    # labels_ex = []
    # if debug_printing:
    #     print('\nQueries on the database:')
    # for result_ex, label in zipped:
    #     if result_ex == [()]:
    #         labels_ex.append(label)
    #     if debug_printing:
    #         print('\tquery: ' + str(label) + ', result: ' + str(bool(result_ex)))
    # return labels_ex


@deprecated
def get_labels_single_example_probabilistic_models(example: SimpleProgram, rules: SimpleProgram,
                                                   possible_labels: Iterable[str], background_knowledge=None,
                                                   debug_printing=False) -> List[str]:
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
            # print('\n')

    query_terms = [Term('query')(label) for label in possible_labels]

    db_to_query = db.extend()
    for query_term in query_terms:
        db_to_query += query_term

    query_results = problog.get_evaluatable().create_from(db_to_query, engine=eng).evaluate()

    return query_results


@deprecated
def get_labels_single_example_keys(example: SimpleProgram, rules: SimpleProgram, prediction_goal: Term,
                                   index_of_label_arg: int, possible_labels: Iterable[str], background_knowledge=None,
                                   debug_printing=False) -> List[str]:
    """
    Classifies a single example and returns a list of its labels
    :param prediction_goal: 
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

    query_results = eng.query(db, prediction_goal)

    labels_ex = []
    for query_result in query_results:
        labels_ex.append(query_result[index_of_label_arg])
    return labels_ex

import statistics
import timeit

import gc
import problog
from problog import get_evaluatable
from problog.program import PrologString
from problog.engine import DefaultEngine
from problog.logic import Term


def test_query_method1(engine, model_db, query_term):
    times_query = []
    for i in range(0, 100):
        start = timeit.default_timer()
        results = engine.query(model_db, query_term)
        end = timeit.default_timer()
        gc.collect()
        times_query.append(end - start)
        # print([query1(*args) for args in results])
        # print(results)
    return times_query


def test_query_method2(engine, model_db, query_term):
    times_query = []

    extended_model_db = model_db.extend()
    extended_model_db += Term('query')(query_term)
    evaluatable = problog.get_evaluatable()

    for i in range(0, 100):
        start = timeit.default_timer()
        query_result = evaluatable.create_from(extended_model_db, engine=engine).evaluate()
        end = timeit.default_timer()
        gc.collect()
        times_query.append(end - start)
        # print(query_result)
    return times_query


def main():
    p = PrologString("""
    mother_child(trude, sally).
    
    father_child(tom, sally).
    father_child(tom, erica).
    father_child(mike, tom).
    
    sibling(X, Y) :- parent_child(Z, X), parent_child(Z, Y).
    
    parent_child(X, Y) :- father_child(X, Y).
    parent_child(X, Y) :- mother_child(X, Y).
    """)

    sibling = Term('sibling')
    query_term = sibling(None, None)
    engine = DefaultEngine()

    # prepare the model for querying
    model_db = engine.prepare(p)  # This compiles the Prolog model into an internal format.
    # This step is optional, but it might be worthwhile if you
    #  want to query the same model multiple times.

    times_query = test_query_method1(engine, model_db, query_term)
    times_query_extended = test_query_method2(engine, model_db, query_term)

    print("average duration query:", statistics.mean(times_query), "seconds")
    print("average duration query:", statistics.mean(times_query_extended), "seconds")
    # for statement in p:
    #     print(statement)
    #
    # knowledge = get_evaluatable().create_from(p)
    #
    # print(knowledge.evaluate())


if __name__ == '__main__':
    main()

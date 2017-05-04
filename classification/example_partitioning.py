from typing import Iterable, Set

from problog import get_evaluatable
from problog.engine import DefaultEngine, ClauseDB
from problog.program import SimpleProgram
from problog.program import Term

from representation.example import Example, SimpleProgramExample, ClauseDBExample


class ExamplePartitioner:
    def __init__(self):
        self.engine = DefaultEngine()
        self.engine.unknown = 1

        self.to_query = Term('to_query')

    def get_examples_satisfying_query(self, examples: Iterable[Example], query) -> Set[Example]:
        raise NotImplementedError("abstract method")


class SimpleProgramExamplePartitioner(ExamplePartitioner):
    def __init__(self, background_knowledge=SimpleProgram()):
        super().__init__()
        self.db = self.engine.prepare(background_knowledge)

    def get_examples_satisfying_query(self, examples: Iterable[SimpleProgramExample], query) -> Set[SimpleProgramExample]:
        examples_satisfying_query = set()

        for example in examples:  # type: SimpleProgramExample
            db_to_query = self.db.extend()  # type: ClauseDB
            for statement in example:
                db_to_query += statement
            db_to_query += Term('query')(self.to_query)
            db_to_query += (self.to_query << query)

            query_result = get_evaluatable().create_from(db_to_query).evaluate()
            if query_result[self.to_query] > 0:
                examples_satisfying_query.add(example)

        return examples_satisfying_query


class ClauseDBExamplePartitioner(ExamplePartitioner):
    def __init__(self):
        super().__init__()

    def get_examples_satisfying_query(self, example_dbs: Iterable[ClauseDBExample], query) -> Set[ClauseDBExample]:
        examples_satisfying_query = set()

        for example_db in example_dbs:  # type: ClauseDBExample
            db_to_query = example_db.extend()
            db_to_query += Term('query')(self.to_query)
            db_to_query += (self.to_query << query)
            query_result = get_evaluatable().create_from(db_to_query).evaluate()

            if query_result[self.to_query] > 0:
                examples_satisfying_query.add(example_db)

        return examples_satisfying_query

# def get_examples_satisfying_query(examples: Iterable[Example], query, background_knowledge: SimpleProgram)
#                                    -> Set[Example]:
#     engine = DefaultEngine()
#     engine.unknown = 1
#
#     db = engine.prepare(background_knowledge)
#     to_query = Term('to_query')
#     db += (to_query << query)
#
#     query_results = set()
#
#     # print("\n================")
#
#     for example in examples:
#         db_example = db.extend()
#         for statement in example:
#             db_example += statement
#         # if example.key == Constant(1) and "27" in str(query):
#         #     for statement in db:
#         #         print(str(statement) + ".")
#         #     for statement in db_example:
#         #         print(str(statement) + ".")
#
#         example_satisfies_query = engine.query(db_example, to_query)
#         if bool(example_satisfies_query):
#             query_results.add(example)
#         # print("--------------\n")
#
#     # print("================\n")
#     return query_results

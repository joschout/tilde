from typing import Iterable, Set, Optional

import problog
from problog.engine import DefaultEngine, ClauseDB
from problog.program import SimpleProgram, LogicProgram
from problog.program import Term

from tilde.representation.example import Example, SimpleProgramExample, ClauseDBExample, InternalExampleFormat


class ExamplePartitioner:
    def __init__(self):
        self.engine = DefaultEngine()
        self.engine.unknown = 1

        self.to_query = Term('to_query')

    def get_examples_satisfying_query(self, examples: Iterable[Example], query) -> Set[Example]:
        raise NotImplementedError("abstract method")

    # def _query(self, db_to_query: ClauseDB) -> Dict[Term, float]:
    #     lf = self.engine.ground_all(db_to_query)  # type: LogicFormula
    #     dag = LogicDAG.create_from(lf)  # break cycles in the ground program
    #     cnf = CNF.create_from(dag)  # convert to CNF
    #     ddnnf = DDNNF.create_from(cnf)
    #     return ddnnf.evaluate()


class SimpleProgramExamplePartitioner(ExamplePartitioner):
    def __init__(self, background_knowledge: Optional[LogicProgram]=None):
        super().__init__()
        if background_knowledge is None:
            self.db = self.engine.prepare(SimpleProgram())
        else:
            self.db = self.engine.prepare(background_knowledge)

    def get_examples_satisfying_query(self, examples: Iterable[SimpleProgramExample], query) -> Set[SimpleProgramExample]:
        examples_satisfying_query = set()

        for example in examples:  # type: SimpleProgramExample
            db_to_query = self.db.extend()  # type: ClauseDB
            for statement in example:
                db_to_query += statement
            db_to_query += Term('query')(self.to_query)
            db_to_query += (self.to_query << query)

            query_result = problog.get_evaluatable().create_from(db_to_query, engine=self.engine).evaluate()

            if query_result[self.to_query] > 0.5:
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
            query_result = problog.get_evaluatable().create_from(db_to_query, engine=self.engine).evaluate()
            # query_result = self._query(db_to_query)

            if query_result[self.to_query] > 0.5:
                examples_satisfying_query.add(example_db)

        return examples_satisfying_query


class PartitionerBuilder:

    # def __init__(self, internal_ex_format: InternalExampleFormat):
    #     self.internal_ex_format = internal_ex_format

    def build_partitioner(self, internal_ex_format: InternalExampleFormat, background_knowledge: Optional[LogicProgram]=None) -> ExamplePartitioner:
        if internal_ex_format is InternalExampleFormat.SIMPLEPROGRAM:
            return SimpleProgramExamplePartitioner(background_knowledge)
        elif internal_ex_format is InternalExampleFormat.CLAUSEDB:
            return ClauseDBExamplePartitioner()
        else:
            raise NotImplementedError("Only the internal formats SimpleProgram and ClauseDB are supported.")


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
from typing import Iterable, Set, Optional, Tuple

import problog
from problog.engine import DefaultEngine, ClauseDB
from problog.program import SimpleProgram, LogicProgram
from problog.program import Term

from tilde.representation.example import InternalExampleFormat, InternalExampleFormatException, \
    ClauseDBExampleWrapper, SimpleProgramExampleWrapper, ExampleWrapper


class ExamplePartitioner:
    def __init__(self):
        self.engine = DefaultEngine()
        self.engine.unknown = 1

        self.to_query = Term('to_query')

    def get_examples_satisfying_query(self, examples: Iterable[ExampleWrapper], query) -> Tuple[Set[ExampleWrapper], Set[ExampleWrapper]]:
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

# TODO: return hier een tuple van sets -> satisfying and not satisfying
    def get_examples_satisfying_query(self, examples: Iterable[SimpleProgramExampleWrapper], query) -> Tuple[Set[ExampleWrapper], Set[ExampleWrapper]]:
        examples_satisfying_query = set()
        examples_not_satifying_query = set()

        for example in examples:  # type: SimpleProgramExampleWrapper
            db_to_query = self.db.extend()  # type: ClauseDB
            if example.classification_term is not None:
                db_to_query += example.classification_term
            for statement in example:
                db_to_query += statement
            db_to_query += Term('query')(self.to_query)
            db_to_query += (self.to_query << query)

            query_result = problog.get_evaluatable().create_from(db_to_query, engine=self.engine).evaluate()

            if query_result[self.to_query] > 0.5:
                examples_satisfying_query.add(example)
            else:
                examples_not_satifying_query.add(example)

        return examples_satisfying_query, examples_not_satifying_query


class ClauseDBExamplePartitioner(ExamplePartitioner):
    def __init__(self):
        super().__init__()

    def get_examples_satisfying_query(self, clause_db_examples: Iterable[ClauseDBExampleWrapper], query) -> Tuple[Set[ExampleWrapper], Set[ExampleWrapper]]:
        examples_satisfying_query = set()
        examples_not_satifying_query = set()

        for clause_db_ex in clause_db_examples:  # type: ClauseDBExampleWrapper
            db_to_query = clause_db_ex.extend()  # type: ClauseDB
            if clause_db_ex.classification_term is not None:
                db_to_query += clause_db_ex.classification_term

            # db_to_query = example_db.extend()
            db_to_query += Term('query')(self.to_query)
            db_to_query += (self.to_query << query)
            query_result = problog.get_evaluatable().create_from(db_to_query, engine=self.engine).evaluate()
            # query_result = self._query(db_to_query)

            if query_result[self.to_query] > 0.5:
                examples_satisfying_query.add(clause_db_ex)
            else:
                examples_not_satifying_query.add(clause_db_ex)

        return examples_satisfying_query, examples_not_satifying_query


class PartitionerBuilder:

    # def __init__(self, internal_ex_format: InternalExampleFormat):
    #     self.internal_ex_format = internal_ex_format

    def build_partitioner(self, internal_ex_format: InternalExampleFormat, background_knowledge: Optional[LogicProgram]=None) -> ExamplePartitioner:
        if internal_ex_format is InternalExampleFormat.SIMPLEPROGRAM:
            return SimpleProgramExamplePartitioner(background_knowledge)
        elif internal_ex_format is InternalExampleFormat.CLAUSEDB:
            return ClauseDBExamplePartitioner()
        else:
            raise InternalExampleFormatException("Only the internal formats SimpleProgram and ClauseDB are supported, got: " + str(internal_ex_format))


# def get_examples_satisfying_query(examples: Iterable[ExampleWrapper], query, background_knowledge: SimpleProgram)
#                                    -> Set[ExampleWrapper]:
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

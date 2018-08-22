from typing import Iterable, Set, Optional, Tuple

import matplotlib.pyplot as plt
import problog
import time
from problog.engine import DefaultEngine, ClauseDB, GenericEngine, math
from problog.program import SimpleProgram, LogicProgram
from problog.program import Term

from mai_version.representation.example import InternalExampleFormat, InternalExampleFormatException, \
    ClauseDBExampleWrapper, SimpleProgramExampleWrapper, ExampleWrapper


class ExamplePartitioner:

    nb_of_times_statistics_printed = 0


    s_nb_partitions_calculated = []

    s_sum_get_evaluatable = []
    s_mean_get_evaluatable = []

    s_sum_structure_creation_duration = []
    s_min_structure_creation_duration = []
    s_max_structure_creation_duration = []
    s_mean_structure_creation_duration = []

    s_nb_structure_creation_zero = []

    s_sum_evaluation_duration = []
    s_min_evaluation_duration = []
    s_max_evaluation_duration = []
    s_mean_evaluation_duration = []
    s_nb_evaluation_zero = []
    
    def __init__(self, engine: GenericEngine=None):
        if engine is None:
            self.engine = DefaultEngine()
            self.engine.unknown = 1
        else:
            self.engine = engine
        self.to_query = Term('to_query')

        self.nb_partitions_calculated = 0

        self.sum_get_evaluatable = 0

        self.sum_structure_creation_duration = 0
        self.min_structure_creation_duration = math.inf
        self.max_structure_creation_duration = - math.inf
        self.nb_structure_creation_zero = 0

        self.sum_evaluation_duration = 0
        self.min_evaluation_duration = math.inf
        self.max_evaluation_duration = - math.inf
        self.nb_evaluation_zero = 0

    def get_examples_satisfying_query(self, examples: Iterable[ExampleWrapper], query) -> Tuple[Set[ExampleWrapper], Set[ExampleWrapper]]:
        raise NotImplementedError("abstract method")

    # def _query(self, db_to_query: ClauseDB) -> Dict[Term, float]:
    #     lf = self.engine.ground_all(db_to_query)  # type: LogicFormula
    #     dag = LogicDAG.create_from(lf)  # break cycles in the ground program
    #     cnf = CNF.create_from(dag)  # convert to CNF
    #     ddnnf = DDNNF.create_from(cnf)
    #     return ddnnf.evaluate()
    
    def print_statistics(self):
        print("nb of partitioning calls:", self.nb_partitions_calculated)
        print("-----")
        print("total get_evaluatable duration:", self.sum_get_evaluatable)
        print("mean get_evaluatable duration:", self.sum_get_evaluatable / self.nb_partitions_calculated)
        print("-----")
        print("total structure creation duration:", self.sum_structure_creation_duration)
        print("nb of structure creation duration == 0s:", self.nb_structure_creation_zero)
        print("% structure creation duration  == 0s:", self.nb_structure_creation_zero / self.nb_partitions_calculated)
        print("mean structure creation duration:", self.sum_structure_creation_duration / self.nb_partitions_calculated)
        print("min structure creation duration:", self.min_structure_creation_duration)
        print("max structure creation duration:", self.max_structure_creation_duration)
        print("-----")
        print("total evaluation duration:", self.sum_evaluation_duration)
        print("nb of times evaluation duration == 0s:", self.nb_evaluation_zero)
        print("% evaluation duration  == 0s:", self.nb_evaluation_zero / self.nb_partitions_calculated)
        print("mean evaluation duration:", self.sum_evaluation_duration / self.nb_partitions_calculated)
        print("min evaluation duration:", self.min_evaluation_duration)
        print("max evaluation duration:", self.max_evaluation_duration)
        print("-----")
        print()

        ExamplePartitioner.s_nb_partitions_calculated.append(self.nb_partitions_calculated)
        # ---
        ExamplePartitioner.s_sum_get_evaluatable.append(self.sum_get_evaluatable)
        ExamplePartitioner.s_mean_get_evaluatable.append(self.sum_get_evaluatable / self.nb_partitions_calculated)
        # ---
        ExamplePartitioner.s_sum_structure_creation_duration.append(self.sum_structure_creation_duration)
        ExamplePartitioner.s_mean_structure_creation_duration.append(self.sum_structure_creation_duration / self.nb_partitions_calculated)
        ExamplePartitioner.s_min_structure_creation_duration.append(self.min_structure_creation_duration)
        ExamplePartitioner.s_max_structure_creation_duration.append(self.max_structure_creation_duration)
        # ---
        ExamplePartitioner.s_sum_evaluation_duration.append(self.sum_evaluation_duration)
        ExamplePartitioner.s_mean_evaluation_duration.append(self.sum_evaluation_duration / self.nb_partitions_calculated)
        ExamplePartitioner.s_min_evaluation_duration.append(self.min_evaluation_duration)
        ExamplePartitioner.s_max_evaluation_duration.append(self.max_evaluation_duration)

        ExamplePartitioner.nb_of_times_statistics_printed += 1

    @staticmethod
    def print_statistic_lists():
        print("nb of partitioning calls:", ExamplePartitioner.s_nb_partitions_calculated)
        print("-----")
        print("total get_evaluatable duration:", ExamplePartitioner.s_sum_get_evaluatable)
        print("mean get_evaluatable duration:", ExamplePartitioner.s_mean_get_evaluatable)
        print("-----")

        plt.plot(ExamplePartitioner.s_sum_structure_creation_duration, 'ro')
        plt.ylabel('seconds')
        plt.xlabel('iteration')
        plt.title("structure_creation_duration")
        plt.savefig("structure_creation_duration.png")

        print("total structure creation duration:", ExamplePartitioner.s_sum_structure_creation_duration)
        print("mean structure creation duration:", ExamplePartitioner.s_mean_structure_creation_duration)
        print("min structure creation duration:", ExamplePartitioner.s_min_structure_creation_duration)
        print("max structure creation duration:", ExamplePartitioner.s_max_structure_creation_duration)
        print("-----")
        print("total evaluation duration:", ExamplePartitioner.s_sum_evaluation_duration)
        print("mean evaluation duration:", ExamplePartitioner.s_mean_evaluation_duration)
        print("min evaluation duration:", ExamplePartitioner.s_min_evaluation_duration)
        print("max evaluation duration:", ExamplePartitioner.s_max_evaluation_duration)
        print("-----")
        print()



class SimpleProgramExamplePartitioner(ExamplePartitioner):
    def __init__(self, background_knowledge: Optional[LogicProgram]=None, engine:GenericEngine = None):
        super().__init__(engine=engine)
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
    def __init__(self, engine:GenericEngine=None):
        super().__init__(engine=engine)

    def get_examples_satisfying_query(self, clause_db_examples: Iterable[ClauseDBExampleWrapper], query) -> Tuple[Set[ExampleWrapper], Set[ExampleWrapper]]:
        examples_satisfying_query = set()
        examples_not_satisfying_query = set()

        for clause_db_ex in clause_db_examples:  # type: ClauseDBExampleWrapper
            db_to_query = clause_db_ex.extend()  # type: ClauseDB
            if clause_db_ex.classification_term is not None:
                db_to_query += clause_db_ex.classification_term

            # db_to_query = example_db.extend()
            db_to_query += Term('query')(self.to_query)
            db_to_query += (self.to_query << query)

            start_time = time.time()
            evaluatable = problog.get_evaluatable()
            mid_time1 = time.time()
            something = evaluatable.create_from(db_to_query, engine=self.engine)
            mid_time2 = time.time()
            query_result = something.evaluate()
            end_time = time.time()

            self.nb_partitions_calculated += 1

            get_evaluatable_duration = mid_time1 - start_time
            self.sum_get_evaluatable += get_evaluatable_duration

            structure_creation_duration = mid_time2 - mid_time1
            self.sum_structure_creation_duration += structure_creation_duration
            if structure_creation_duration > self.max_structure_creation_duration:
                self.max_structure_creation_duration = structure_creation_duration
            if structure_creation_duration < self.min_structure_creation_duration:
                self.min_structure_creation_duration = structure_creation_duration
            if structure_creation_duration < 0.000001:
                self.nb_structure_creation_zero += 1

            evalutation_duration = end_time - mid_time2
            self.sum_evaluation_duration += evalutation_duration
            if evalutation_duration > self.max_evaluation_duration:
                self.max_evaluation_duration = evalutation_duration
            if evalutation_duration < self.min_evaluation_duration:
                self.min_evaluation_duration = evalutation_duration
            if evalutation_duration < 0.000001:
                self.nb_evaluation_zero += 1

            # query_result = problog.get_evaluatable().create_from(db_to_query, engine=self.engine).evaluate()

            if query_result[self.to_query] > 0.5:
                examples_satisfying_query.add(clause_db_ex)
            else:
                examples_not_satisfying_query.add(clause_db_ex)

        return examples_satisfying_query, examples_not_satisfying_query


class PartitionerBuilder:

    # def __init__(self, internal_ex_format: InternalExampleFormat):
    #     self.internal_ex_format = internal_ex_format

    def build_partitioner(self, internal_ex_format: InternalExampleFormat, background_knowledge: Optional[LogicProgram]=None, engine:GenericEngine=None) -> ExamplePartitioner:
        if internal_ex_format is InternalExampleFormat.SIMPLEPROGRAM:
            return SimpleProgramExamplePartitioner(background_knowledge, engine=engine)
        elif internal_ex_format is InternalExampleFormat.CLAUSEDB:
            return ClauseDBExamplePartitioner(engine=engine)
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

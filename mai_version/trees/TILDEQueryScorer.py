import math
from typing import Iterable, Set, List, Optional

import problog
import time
from problog.logic import And, Term

from mai_version.classification.example_partitioning import ExamplePartitioner
from mai_version.representation.TILDE_query import TILDEQuery
from mai_version.representation.example import ExampleWrapper
from mai_version.representation.example import Label
from mai_version.trees.scoring import entropy, information_gain2


class QueryScoreInfo:
    """Wrapper around the information about best scoring query"""

    def __init__(self, best_query: TILDEQuery, score_of_best_query: float,
                 examples_satisfying_best_query: Set[ExampleWrapper],
                 examples_not_satisfying_best_query: Set[ExampleWrapper]):
        self.best_query = best_query  # type: TILDEQuery
        self.score_of_best_query = score_of_best_query  # type: float
        self.examples_satisfying_best_query = examples_satisfying_best_query  # type: Set[ExampleWrapper]
        self.examples_not_satisfying_best_query = examples_not_satisfying_best_query  # type: Set[ExampleWrapper]


class TILDEQueryScorer:
    @staticmethod
    def get_best_refined_query(refined_queries: Iterable[TILDEQuery], examples: Set[ExampleWrapper],
                               example_partitioner: ExamplePartitioner, possible_targets: List[Label],
                               probabilistic: Optional[bool] = False) -> QueryScoreInfo:
        # Tuple[Optional[TILDEQuery], float, Optional[Set[ExampleWrapper]], Optional[Set[ExampleWrapper]]]:
        best_query = None  # type: Optional[TILDEQuery]
        score_best_query = - math.inf  # type: float
        examples_satisfying_best_query = None # type: Optional[Set[ExampleWrapper]]
        examples_not_satisfying_best_query = None  # type: Optional[Set[ExampleWrapper]]

        entropy_complete_set = entropy(examples, possible_targets)
        nb_of_examples_complete_set = len(examples)

        for q in refined_queries:  # type: TILDEQuery
            print(q)
            # compute the score of the queries
            conj_of_tilde_query = q.to_conjunction()  # type: And

            examples_satisfying_q, examples_not_satisfying_q = example_partitioner.get_examples_satisfying_query(
                examples, conj_of_tilde_query)  # type: Set[ExampleWrapper]
            # examples_not_satisfying_q = examples - examples_satisfying_q  # type: Set[ExampleWrapper]

            #TODO: no longer probabilistic!
            score = information_gain2(examples_satisfying_q, examples_not_satisfying_q, possible_targets, nb_of_examples_complete_set, entropy_complete_set)

            if score > score_best_query:
                best_query = q
                score_best_query = score
                examples_satisfying_best_query = examples_satisfying_q
                examples_not_satisfying_best_query = examples_not_satisfying_q

        return QueryScoreInfo(best_query, score_best_query, examples_satisfying_best_query,
                              examples_not_satisfying_best_query)


class TILDEQueryScorer2:
    @staticmethod
    def get_best_refined_query(refined_queries: Iterable[TILDEQuery], examples: Set[ExampleWrapper],
                               example_partitioner: ExamplePartitioner, possible_targets: List[Label],
                               probabilistic: Optional[bool] = False) -> QueryScoreInfo:
        # Tuple[Optional[TILDEQuery], float, Optional[Set[ExampleWrapper]], Optional[Set[ExampleWrapper]]]:
        best_query = None  # type: Optional[TILDEQuery]
        score_best_query = - math.inf  # type: float
        # examples_satisfying_best_query = None # type: Optional[Set[ExampleWrapper]]
        # examples_not_satisfying_best_query = None  # type: Optional[Set[ExampleWrapper]]

        entropy_complete_set = entropy(examples, possible_targets)
        nb_of_examples_complete_set = len(examples)


        # ided_queries = list(zip(range(0,len(refined_queries)), refined_queries))

        entropy_dict = {label: 0 for label in possible_targets}

        query_entropy_dicts = [(entropy_dict.copy(), entropy_dict.copy()) for q in refined_queries]

        for clause_db_ex in examples:
            db_to_query = clause_db_ex.extend()  # type: ClauseDB
            if clause_db_ex.classification_term is not None:
                db_to_query += clause_db_ex.classification_term

            for id, q in zip(range(0,len(refined_queries)), refined_queries):
                to_query = Term('q' + str(id))
                db_to_query += Term('query')(to_query)
                db_to_query += (to_query << q.to_conjunction())

            start_time = time.time()
            evaluatable = problog.get_evaluatable()
            mid_time1 = time.time()
            something = evaluatable.create_from(db_to_query, engine=example_partitioner.engine)
            mid_time2 = time.time()
            results = something.evaluate()
            end_time = time.time()

            example_partitioner.nb_partitions_calculated += 1

            get_evaluatable_duration = mid_time1 - start_time
            example_partitioner.sum_get_evaluatable += get_evaluatable_duration

            structure_creation_duration = mid_time2 - mid_time1
            example_partitioner.sum_structure_creation_duration += structure_creation_duration
            if structure_creation_duration > example_partitioner.max_structure_creation_duration:
                example_partitioner.max_structure_creation_duration = structure_creation_duration
            if structure_creation_duration < example_partitioner.min_structure_creation_duration:
                example_partitioner.min_structure_creation_duration = structure_creation_duration
            if structure_creation_duration < 0.000001:
                example_partitioner.nb_structure_creation_zero += 1

            evalutation_duration = end_time - mid_time2
            example_partitioner.sum_evaluation_duration += evalutation_duration
            if evalutation_duration > example_partitioner.max_evaluation_duration:
                example_partitioner.max_evaluation_duration = evalutation_duration
            if evalutation_duration < example_partitioner.min_evaluation_duration:
                example_partitioner.min_evaluation_duration = evalutation_duration
            if evalutation_duration < 0.000001:
                example_partitioner.nb_evaluation_zero += 1


            # results = problog.get_evaluatable().create_from(db_to_query, engine=example_partitioner.engine).evaluate()

            for to_query, prob in results.items():
                id = int(to_query.functor[1:])
                if prob > 0.5:
                    query_entropy_dicts[id][0][clause_db_ex.get_label()] = query_entropy_dicts[id][0][clause_db_ex.get_label()] + 1

                else:
                    query_entropy_dicts[id][1][clause_db_ex.get_label()] = query_entropy_dicts[id][1][
                                                                               clause_db_ex.get_label()] + 1

        for query, (left_dic, right_dic) in zip(refined_queries, query_entropy_dicts):

            # -- ig --
            ig = 0
            if nb_of_examples_complete_set != 0:
                ig = entropy_complete_set

                nb_examples_left = sum(left_dic.values())
                if nb_examples_left > 0:
                    entropy_left = 0
                    for label in left_dic.keys():
                        label_value = left_dic[label]
                        if label_value != 0:
                            entropy_left -= label_value / nb_examples_left \
                                * math.log2(label_value / nb_examples_left)
                    ig -= nb_examples_left / nb_of_examples_complete_set * entropy_left

                # ------
                nb_examples_right = sum(right_dic.values())
                if nb_examples_right > 0:
                    entropy_right = 0
                    for label in right_dic.keys():
                        label_value = right_dic[label]
                        if label_value != 0:
                            entropy_right -= label_value / nb_examples_right \
                                * math.log2(label_value / nb_examples_right)
                    ig -= nb_examples_right / nb_of_examples_complete_set * entropy_right

            if ig > score_best_query:
                best_query = query
                score_best_query = ig

        # --- we now know the best query, so create the partition again:
        examples_satisfying_best_query = set()  # type: Optional[Set[ExampleWrapper]]
        examples_not_satisfying_best_query = set()  # type: Optional[Set[ExampleWrapper]]

        to_query = Term('to_query')
        to_add1 = Term('query')(to_query)
        to_add2 = (to_query << best_query.to_conjunction())

        for clause_db_ex in examples:
            db_to_query = clause_db_ex.extend()  # type: ClauseDB
            if clause_db_ex.classification_term is not None:
                db_to_query += clause_db_ex.classification_term

                # db_to_query = example_db.extend()
                db_to_query += to_add1
                db_to_query += to_add2

                start_time = time.time()
                evaluatable = problog.get_evaluatable()
                mid_time1 = time.time()
                something = evaluatable.create_from(db_to_query, engine=example_partitioner.engine)
                mid_time2 = time.time()
                query_result = something.evaluate()
                end_time = time.time()

                example_partitioner.nb_partitions_calculated += 1

                get_evaluatable_duration = mid_time1 - start_time
                example_partitioner.sum_get_evaluatable += get_evaluatable_duration

                structure_creation_duration = mid_time2 - mid_time1
                example_partitioner.sum_structure_creation_duration += structure_creation_duration
                if structure_creation_duration > example_partitioner.max_structure_creation_duration:
                    example_partitioner.max_structure_creation_duration = structure_creation_duration
                if structure_creation_duration < example_partitioner.min_structure_creation_duration:
                    example_partitioner.min_structure_creation_duration = structure_creation_duration
                if structure_creation_duration < 0.000001:
                    example_partitioner.nb_structure_creation_zero += 1

                evalutation_duration = end_time - mid_time2
                example_partitioner.sum_evaluation_duration += evalutation_duration
                if evalutation_duration > example_partitioner.max_evaluation_duration:
                    example_partitioner.max_evaluation_duration = evalutation_duration
                if evalutation_duration < example_partitioner.min_evaluation_duration:
                    example_partitioner.min_evaluation_duration = evalutation_duration
                if evalutation_duration < 0.000001:
                    example_partitioner.nb_evaluation_zero += 1



                # query_result = problog.get_evaluatable().create_from(db_to_query,
                #                                                 engine=example_partitioner.engine).evaluate()
                if query_result[to_query] > 0.5:
                    examples_satisfying_best_query.add(clause_db_ex)
                else:
                    examples_not_satisfying_best_query.add(clause_db_ex)

        # for qid, q in enumerate(refined_queries):  # type: TILDEQuery
        #     # compute the score of the queries
        #     conj_of_tilde_query = q.to_conjunction()  # type: And
        #
        #     examples_satisfying_q, examples_not_satisfying_q = example_partitioner.get_examples_satisfying_query(
        #         examples, conj_of_tilde_query)  # type: Set[ExampleWrapper]
        #     # examples_not_satisfying_q = examples - examples_satisfying_q  # type: Set[ExampleWrapper]
        #
        #     #TODO: no longer probabilistic!
        #     score = information_gain2(examples_satisfying_q, examples_not_satisfying_q, possible_targets, nb_of_examples_complete_set, entropy_complete_set)
        #
        #     if score > score_best_query:
        #         best_query = q
        #         score_best_query = score
        #         examples_satisfying_best_query = examples_satisfying_q
        #         examples_not_satisfying_best_query = examples_not_satisfying_q

        return QueryScoreInfo(best_query, score_best_query, examples_satisfying_best_query,
                              examples_not_satisfying_best_query)
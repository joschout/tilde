from typing import Iterable, Set, List, Optional, Tuple

import math

from problog.logic import And
from trees.scoring import information_gain
from classification.classification_helper import Label
from classification.example_partitioning import ExamplePartitioner
from representation.TILDE_query import TILDEQuery
from representation.example import Example


class TILDEQueryScorer:
    @staticmethod
    def get_best_refined_query(refined_queries: Iterable[TILDEQuery], examples: Set[Example],
                               example_partitioner: ExamplePartitioner, possible_targets: List[Label],
                               probabilistic: Optional[bool]=False)\
                    -> Tuple[Optional[TILDEQuery], float, Optional[Set[Example]], Optional[Set[Example]]]:
        best_query = None  # type: Optional[TILDEQuery]
        score_best_query = - math.inf  # type: float
        examples_satisfying_best_query = set()  # type: Optional[Set[Example]]
        examples_not_satisfying_best_query = set()  # type: Optional[Set[Example]]

        for q in refined_queries:  # type: TILDEQuery
            # compute the score of the queries
            conj_of_tilde_query = q.to_conjunction()  # type: And

            examples_satisfying_q = example_partitioner.get_examples_satisfying_query(examples, conj_of_tilde_query)  # type: Set[Example]
            examples_not_satisfying_q = examples - examples_satisfying_q  # type: Set[Example]
            score = information_gain(examples, examples_satisfying_q,
                                                   examples_not_satisfying_q, possible_targets, probabilistic)

            if score > score_best_query:
                best_query = q
                score_best_query = score
                examples_satisfying_best_query = examples_satisfying_q
                examples_not_satisfying_best_query = examples_not_satisfying_q

        return best_query, score_best_query, examples_satisfying_best_query, examples_not_satisfying_best_query

import math
from typing import Iterable, Set, List, Optional

from problog.logic import And
from tilde.representation.example import Example

from tilde.classification.example_partitioning import ExamplePartitioner
from tilde.representation.example import Label
from tilde.representation.TILDE_query import TILDEQuery
from tilde.trees.scoring import information_gain


class QueryScoreInfo:
    """Wrapper around the information about best scoring query"""
    def __init__(self, best_query: TILDEQuery, score_of_best_query: float, examples_satisfying_best_query: Set[Example], examples_not_satisfying_best_query: Set[Example]):
        self.best_query = best_query  # type: TILDEQuery
        self.score_of_best_query = score_of_best_query  # type: float
        self.examples_satisfying_best_query = examples_satisfying_best_query  # type: Set[Example]
        self.examples_not_satisfying_best_query = examples_not_satisfying_best_query  # type: Set[Example]


class TILDEQueryScorer:
    @staticmethod
    def get_best_refined_query(refined_queries: Iterable[TILDEQuery], examples: Set[Example],
                               example_partitioner: ExamplePartitioner, possible_targets: List[Label],
                               probabilistic: Optional[bool]=False)-> QueryScoreInfo:
            # Tuple[Optional[TILDEQuery], float, Optional[Set[Example]], Optional[Set[Example]]]:
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

        return QueryScoreInfo(best_query, score_best_query, examples_satisfying_best_query, examples_not_satisfying_best_query)

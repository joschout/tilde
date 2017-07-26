from typing import Dict, List, Optional

from problog.logic import Term

from tilde.representation.example import Label


class QueryResultLabelExtractor:

    def extract_labels(self, query_results: Dict[Term, float]) -> List[Term]:
        raise NotImplementedError('abstract method')


class ModelsQueryResultLabelExtractor(QueryResultLabelExtractor):
    def extract_labels(self, query_results: Dict[Term, float]) -> List[Term]:
        return [label for label in query_results if query_results[label] > 0.0]  # type: List[Label]


class KeysQueryResultLabelExtractor(QueryResultLabelExtractor):

    def __init__(self):
        self.index_of_label_arg = None  # type: Optional[int]

    def set_index_of_label_arg(self, index_of_label_arg: int):
        self.index_of_label_arg = index_of_label_arg

    def extract_labels(self, query_results: Dict[Term, float]) -> List[Term]:
        labels = []  # type: List[Label]
        if len(query_results) == 0:
            raise Exception("Cannot extract labels since querying on the example gave no results")
        for result in query_results:
            if query_results[result] > 0:
                label = result.args[self.index_of_label_arg]
                labels.append(label)
        return labels

# TODO:
# class KeysLabelHandler:
#     def __init__(self, prediction_goal: Term, index_of_label_arg: int):
#         self.prediction_goal = prediction_goal  # type: Term
#         self.index_of_label_arg = index_of_label_arg  # type: int
#
#     def get_label_argument(self, keys_term: Term):
#         return keys_term[self.index_of_label_arg]


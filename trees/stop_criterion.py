class StopCriterionHandler:
    def is_stop_criterion_reached(self, score, examples_satisfying_best_query, examples_not_satisfying_best_query) -> bool:
        raise NotImplementedError('abstract method')


class StopCriterionMinimalCoverage(StopCriterionHandler):
    def __init__(self, minimum_nb_of_examples_in_node: int = 2):
        self.minimum_nb_of_examples_in_node = minimum_nb_of_examples_in_node

    def is_stop_criterion_reached(self,score,  examples_satisfying_best_query, examples_not_satisfying_best_query) -> bool:
        if score < 0.001:
            return True

        nb_of_examples_satisfying_best_query = len(examples_satisfying_best_query)
        nb_of_examples_not_satisfying_best_query = len(examples_not_satisfying_best_query)

        if min(nb_of_examples_satisfying_best_query,
               nb_of_examples_not_satisfying_best_query) < self.minimum_nb_of_examples_in_node:
            return True
        else:
            return False

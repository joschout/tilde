class StopCriterionHandler:
    def is_stop_criterion_reached(self, score, examples_satisfying_best_query, examples_not_satisfying_best_query) -> bool:
        raise NotImplementedError('abstract method')


class StopCriterionMinimalCoverage(StopCriterionHandler):
    def __init__(self, minimum_nb_of_examples_in_node: int = 2, cutoff_score:float=0.001):
        self.minimum_nb_of_examples_in_node = minimum_nb_of_examples_in_node
        self.cutoff_score = cutoff_score

    def is_stop_criterion_reached(self, score,  examples_satisfying_best_query, examples_not_satisfying_best_query) -> bool:
        if score < self.cutoff_score:
            return True

        nb_of_examples_satisfying_best_query = len(examples_satisfying_best_query)
        nb_of_examples_not_satisfying_best_query = len(examples_not_satisfying_best_query)

        # (De Raedt: a good heuristic:
        # stop expanding nodes
        #   WHEN the number of examples in the nodes falls below a certain (user-defined threshold)
        # NOTE:
        #   the nodes get split into two children
        #   --> possible case:
        #       only for 1 of the children, the nb of examples falls below the threshold
        #       --> we should only expand that child node
        #           BUT we still need to find queries for both children
        #
        #   SO: IF by splitting,
        #       BOTH nodes fall below a certain user-defined threshold
        #           (i.e. the max of their nbs < threshold)
        #       THEN we don't split this node
        #
        if max(nb_of_examples_satisfying_best_query,
               nb_of_examples_not_satisfying_best_query) < self.minimum_nb_of_examples_in_node:
            return True
        else:
            return False

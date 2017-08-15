from typing import Dict

from problog.logic import Term


class LeafStrategy:
    def to_string(self, node_indentation) -> str:
        raise NotImplementedError('abstract method')

    def to_string_compact(self) -> str:
        raise NotImplementedError('abstract method')

    def can_classify(self) -> object:
        raise NotImplementedError('abstract method')

    # def get_leaf_clause(self, previous_conjunction) -> Clause:
    #     raise NotImplementedError('abstract method')


class DeterministicLeafMergeException(Exception):
    pass


class DeterministicLeafStrategy(LeafStrategy):
    def __init__(self, classification: Term, nb_of_examples_with_label: int, nb_of_examples_in_this_node: int):
        self.classification = classification  # type: Term
        self.nb_of_examples_with_label = nb_of_examples_with_label  # type: int
        self.nb_of_examples_in_this_node = nb_of_examples_in_this_node  # type: int

    def can_classify(self) -> object:
        return isinstance(self.classification, Term)

    def to_string(self, node_indentation) -> str:
        result = node_indentation + "Leaf, class label: " + str(self.classification) + ", [" + str(
            self.nb_of_examples_with_label) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
        return result

    def to_string_compact(self) -> str:
        result = '[' + str(self.classification) + "] [" + str(
         self.nb_of_examples_with_label) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
        return result

    def merge(self, other: 'DeterministicLeafStrategy'):
        if other.classification != self.classification:
            raise DeterministicLeafMergeException('2 DeterministicLeafStrategy cannot be merged, one has '
                                                  'classification: ' + str(self.classification) + ", the other has "
                                                                                                 "classification: " +
                                                  str(other.classification))
        self.nb_of_examples_with_label += other.nb_of_examples_with_label
        self.nb_of_examples_in_this_node += other.nb_of_examples_in_this_node

    # def get_leaf_clause(self, previous_conjunction):
    #     return self.classification << previous_conjunction


class MLEDeterministicLeafStrategy(LeafStrategy):
    def __init__(self, label_frequencies: Dict[Term, float], label_absolute_counts: Dict[Term, float]):
        self.label_frequencies = label_frequencies  # type: Dict[Term, float]
        self.label_absolute_counts = label_absolute_counts  # type: Dict[Term, float]
        self.nb_of_examples_in_this_node = sum(self.label_absolute_counts.values())  # type: int

    def can_classify(self) -> bool:
        return isinstance(self.label_frequencies, dict)

    def to_string(self, node_indentation) -> str:
        result = node_indentation + "Leaf, class label frequencies: " + str(
            self.label_frequencies) + ", class label counts" + str(
            self.label_absolute_counts) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
        return result

    def to_string_compact(self) -> str:
        # result = "class label frequencies: " + str(
        #     self.label_frequencies) + ", class label counts" + str(
        #     self.label_absolute_counts) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
        result = str(
            self.label_absolute_counts) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
        return result

    # def get_leaf_clause(self,  previous_conjunction: Term):
    #     var = self.prediction_goal.args[self.index]  # type: Var
    #     label_frequencies = node.label_frequencies  # type: Optional[Dict[Label, float]]
    #
    #     goals_with_probabilities = []
    #
    #     for label in label_frequencies.keys():
    #         substitution = {var.name: label}  # type: Dict[str, Term]
    #         goal_with_label = apply_substitution_to_term(self.prediction_goal, substitution)  # type: Term
    #         probability_of_goal = Constant(label_frequencies[label])
    #         goal_with_label.probability = probability_of_goal
    #         goals_with_probabilities.append(goal_with_label)
    #
    #     return AnnotatedDisjunction(goals_with_probabilities, previous_conjunction)
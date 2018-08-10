import math


class SplitCriterion:
    """
    Abstract class for calculating a split criterion heuristic using the training examples in a node, split into the
    subsets of examples satisfying a test and those not satisfying that test.

    """

    def calculate(self, examples_satisfying_test, examples_not_satisfying_test):
        raise NotImplementedError('abstract method')

    def get_threshold(self):
        raise NotImplementedError('abstract method')

    def get_name(self):
        raise NotImplementedError('abstract method')


class InformationGain(SplitCriterion):
    """
    Calculates the information gain (for use as a split criterion)
    """
    threshold = 0.001

    def __init__(self, examples, possible_labels):
        self.n_examples = len(examples)
        self.labels = possible_labels
        self.entropy_all_examples = self._entropy(examples)

    def get_threshold(self):
        return InformationGain.threshold

    def calculate(self, examples_satisfying_test, examples_not_satisfying_test):
        score = self._information_gain(examples_satisfying_test, examples_not_satisfying_test)
        return score

    def _entropy(self, list_of_examples) -> float:
        """Calculates the entropy of a list of examples. Entropy is also known as information.

        An example is an object containing a label, e.g. an instance of representation.example
        It is necessary to provide the list of all possible labels.

        :param list_of_examples
                A list of examples
        """

        nb_of_examples = len(list_of_examples)

        if nb_of_examples == 0:
            return 0
        entropy_value = 0  # type: float

        for label in self.labels:
            probability_of_label = sum(
                [1.0 for example in list_of_examples if example.label == label])
            if probability_of_label != 0:
                entropy_value -= probability_of_label / nb_of_examples \
                                 * math.log2(probability_of_label / nb_of_examples)
        return entropy_value

    def _information_gain(self, sublist_left, sublist_right) -> float:
        """
        Calculates the information gain of splitting a set of examples into two subsets.
        """
        if self.n_examples == 0:
            return 0

        ig = self.entropy_all_examples  # type: float

        ig -= len(sublist_left) / self.n_examples * self._entropy(sublist_left)
        ig -= len(sublist_right) / self.n_examples * self._entropy(sublist_right)
        return ig

    def get_name(self):
        return 'entropy'


# class GiniIndex(SplitCriterion):
#     pass


class SplitCriterionBuilder:
    """
    Get a split criterion based on its name as a string.
    """
    @staticmethod
    def get_split_criterion(split_criterion_str: str, examples, node_labels):
        if split_criterion_str == 'entropy':
            return InformationGain(examples, node_labels)

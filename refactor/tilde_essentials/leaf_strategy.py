from refactor.tilde_essentials.example import calculate_label_frequencies_and_absolute_counts


class LeafStrategy:
    """
    Abstract LeafStrategy class used in a leaf node for making a prediction for an example
    """
    def to_string(self, node_indentation) -> str:
        raise NotImplementedError('abstract method')

    def to_string_compact(self):
        raise NotImplementedError('abstract method')

    def predict(self, example):
        raise NotImplementedError('abstract method')


class MajorityClassLSMergeException(Exception):
    pass


class MajorityClassLS(LeafStrategy):
    """
    Predict for an example the majority class of a leaf
    """
    def __init__(self, examples):
        self.label_frequencies, self.label_counts = calculate_label_frequencies_and_absolute_counts(examples)
        self.majority_label = max(self.label_counts.keys(), key=(lambda key: self.label_counts[key]))
        self.n_examples = len(examples)  # nb of examples in this leaf

    def to_string(self, node_indentation) -> str:
        return node_indentation + "Leaf, class label: " + str(self.majority_label) + ", [" + str(
            self.label_counts[self.majority_label]) + "/" + str(self.n_examples) + "]" + '\n'

    def to_string_compact(self):
        return '[' + str(self.majority_label) + "] [" + str(
         self.label_counts[self.majority_label]) + "/" + str(self.n_examples) + "]" + '\n'

    def predict(self, example):
        return self.majority_label

    def merge(self, other: 'MajorityClassLS'):
        if other.majority_label != self.majority_label:
            raise MajorityClassLSMergeException('2 MajorityClassLS objects could not be merged, as one has'
                                                'majority class' + str(self.majority_label) +
                                                ' while the other has majority class ' + str(other.majority_label))
        self.n_examples += other.n_examples

        for label in other.label_frequencies:
            self.label_frequencies[label] = self.label_frequencies.get(label, 0) + other.label_frequencies[label]
            self.label_counts[label] = self.label_counts.get(label, 0) + other.label_counts[label]


class LeafBuilder:
    """
    Create a leaf strategy based on the training examples (sorted into a leaf node)
    """

    def build(self, examples):
        return MajorityClassLS(examples)

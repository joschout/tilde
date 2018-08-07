from refactor.tilde_essentials.example import calculate_label_frequencies_and_absolute_counts


class LeafStrategy:
    def to_string(self, node_indentation) -> str:
        raise NotImplementedError('abstract method')

    def to_string_compact(self):
        raise NotImplementedError('abstract method')

    def predict(self, example):
        raise NotImplementedError('abstract method')


class MajorityClassLS(LeafStrategy):
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


class LeafBuilder:
    def build(self, examples):
        return MajorityClassLS(examples)

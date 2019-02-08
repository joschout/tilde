from typing import Iterable

from refactor.tilde_essentials.destuctable import Destructible


class Example(Destructible):
    """
    Container class for an example, storing its data and label (types undefined)

    """

    def __init__(self, data, label):
        self.data = data
        self.label = label

    def destruct(self):
        destruct_method = getattr(self.data, 'destruct', None)
        if callable(destruct_method):
            self.data.destruct()


def get_labels(examples: Iterable):
    labels = set()

    for current_example in examples:
        # for label in current_example.labels:
        labels.add(current_example.label)
    return labels


def calculate_majority_class(examples):
    """Calculate the majority class label in the given set of examples.
    """
    label_counts = calculate_label_counts(examples)
    label_with_max_count = max(label_counts, key=(lambda key: label_counts[key]))
    count = label_counts[label_with_max_count]  # type: int
    return label_with_max_count, count


def calculate_label_counts(examples):
    """Assumes that the examples each have ONE label, and not a distribution over labels"""
    label_counts = {}

    for example in examples:
        label = example.label
        label_counts[label] = label_counts.get(label, 0) + 1

    return label_counts


def calculate_label_frequencies(examples):
    """Assumes that the examples each have ONE label, and not a distribution over labels"""
    label_counts = calculate_label_counts(examples)

    for label in label_counts.keys():
        label_counts[label] = label_counts[label] / len(examples)

    return label_counts


def calculate_label_frequencies_and_absolute_counts(examples):
    """Assumes that the examples each have ONE label, and not a distribution over labels"""
    label_counts = calculate_label_counts(examples)

    label_frequencies = {}

    for label in label_counts.keys():
        label_frequencies[label] = label_counts[label] / len(examples)

    return label_frequencies, label_counts

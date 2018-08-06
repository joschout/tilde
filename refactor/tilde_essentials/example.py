from typing import Iterable


class Example:
    def __init__(self, data, labels):
        self.data = data,
        self.labels = labels


def get_labels(examples: Iterable):
    labels = set()

    for current_example in examples:
        for label in current_example.labels:
            labels.add(label)
    return labels

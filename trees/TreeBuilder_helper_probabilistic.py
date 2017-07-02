from typing import Dict, Iterable

from classification.classification_helper import Label
from representation.example import Probability, Example
from trees import TreeNode


class ProbabilisticTreeBuildingError(Exception):
    pass


def print_set_statistics_prob(example_set, possible_targets, indent: str = ""):
    nb_of_ex = len(example_set)

    if nb_of_ex != 0:

        mean_label_prob = {}
        nb_times_label_is_max = {}

        for label in possible_targets:  # type: Label
            mean_label_prob[label] = 0
            nb_times_label_is_max[label] = 0

        for example in example_set:
            true_example_labels = example.get_label_dict()  # type: Dict[Label, Probability]

            label_max_prob = None
            max_prob = 0

            for label in true_example_labels.keys():
                label_prob = true_example_labels[label].value

                mean_label_prob[label] = mean_label_prob[label] + label_prob

                if label_prob > max_prob:
                    label_max_prob = label
                    max_prob = label_prob
            nb_times_label_is_max[label_max_prob] = nb_times_label_is_max[label_max_prob] + 1

        for label in mean_label_prob.keys():
            mean_label_prob[label] = mean_label_prob[label] / nb_of_ex

        # printing the statistics
        print(indent + "nb of examples: " + str(nb_of_ex))
        print(indent + "nb of times a label has the highest probability:")
        for label in nb_times_label_is_max:
            print(indent + "\t" + str(label) + ": " + str(nb_times_label_is_max[label]) + "/" + str(nb_of_ex))

        print(indent + "mean probability for each label:")
        for label in mean_label_prob.keys():
            print(indent + "\t" + str(label) + ": " + str(mean_label_prob[label]))

    else:
        print(indent + "example set is empty")


def print_partition_statistics_prob(examples_satisfying_best_query, examples_not_satisfying_best_query, possible_targets, indentation):
    print("examples satisfying query")
    print_set_statistics_prob(examples_satisfying_best_query, possible_targets, indentation)
    print("examples not satisfying query")
    print_set_statistics_prob(examples_not_satisfying_best_query, possible_targets, indentation)




class MLELeafNodeConverter:

    def convert_to_MLE_leaf_node(self, node: TreeNode, examples_in_this_node: Iterable[Example], possible_targets):
        pass

    def _count_labels_of_examples(self, examples:Iterable[Example], possible_targets) -> Dict[Label, float]:
        label_counts = {}  # type: Dict[Label, float]

        for example in examples:  # type: Example
            label = example.get_label()  # type: Label
            label_counts[label] = label_counts.get(label, 0) + 1

        for label in label_counts.keys():
            label_counts[label] = label_counts[label] / len(examples)

        return label_counts


def create_probabilistic_leaf_node(node: TreeNode, examples: Iterable[Example], possible_targets):
    # TODO: this still uses deterministic labels
    nb_of_ex = len(examples)

    if nb_of_ex != 0:

        mean_label_prob = {}
        nb_times_label_is_max = {}

        for label in possible_targets:  # type: Label
            mean_label_prob[label] = 0
            nb_times_label_is_max[label] = 0

        for example in examples:
            true_example_labels = example.get_label_dict()  # type: Dict[Label, Probability]

            label_max_prob = None
            max_prob = 0

            for label in true_example_labels.keys():
                label_prob = true_example_labels[label].value

                mean_label_prob[label] = mean_label_prob[label] + label_prob

                if label_prob > max_prob:
                    label_max_prob = label
                    max_prob = label_prob
            nb_times_label_is_max[label_max_prob] = nb_times_label_is_max[label_max_prob] + 1

        for label in mean_label_prob.keys():
            mean_label_prob[label] = mean_label_prob[label] / nb_of_ex

        label_max_prob = None
        max_prob = 0

        for label in mean_label_prob.keys():
            mean_prob_of_this_label = mean_label_prob[label]
            if mean_prob_of_this_label > max_prob:
                max_prob = mean_prob_of_this_label
                label_max_prob = label

        # making a leaf node
        node.classification = label_max_prob

    else:
        raise ProbabilisticTreeBuildingError("there are no examples to make this node a leaf node")

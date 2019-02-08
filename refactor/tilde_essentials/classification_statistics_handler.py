import warnings
from typing import List, Dict, Tuple

from problog.logic import Term
from sklearn.metrics import classification_report, accuracy_score

from refactor.representation.example import Label


class ClassificationStatisticsHandler:
    def __init__(self, possible_labels: List[Label]):
        self.confusion_matrix = {}  # type: Dict[Tuple[Term, Term], int]
        self.possible_labels = possible_labels

        self.true_labels_str = []
        self.predicted_labels_str = []

        self.total_nb_of_examples = 0
        self.nb_ex_correctly_classified = 0
        self.nb_ex_incorrectly_classified = 0

    def update_statistics(self, actual_label, predicted_label):

        self.true_labels_str.append(str(actual_label))
        self.predicted_labels_str.append(str(predicted_label))

        is_correctly_classified = (actual_label == predicted_label)
        if is_correctly_classified:
            self.nb_ex_correctly_classified += 1
        else:
            self.nb_ex_incorrectly_classified += 1

        self.total_nb_of_examples += 1

        key = (actual_label, predicted_label)
        old_value = self.confusion_matrix.get(key, 0)
        new_value = old_value + 1
        self.confusion_matrix[key] = new_value

    def get_confusion_matrix_str(self) -> str:

        max_label_str_len = max([len(str(label)) for label in self.possible_labels])

        result = "--- confusion matrix: true/predicted --- :\n\n"

        result += ' ' * max_label_str_len + '|'

        column_sums = {}  # type: Dict[Term, int]

        # === create header row + initialize sum of columns ===
        for first_row_label in self.possible_labels:
            column_sums[first_row_label] = 0

            str_label = str(first_row_label)
            label_str_len = len(str_label)
            result += ' ' * (max_label_str_len - label_str_len) + str_label + '|'
        # --------------------
        result += '\n'
        # =========================

        nb_of_labels = len(self.possible_labels)
        horizontal_bar_str = '-' * ((nb_of_labels + 2) * max_label_str_len + nb_of_labels + 1)
        result += horizontal_bar_str + '\n'

        # == create table rows ===
        for first_column_label in self.possible_labels:
            # first column value of this row is a label
            first_column_label_str = str(first_column_label)
            first_column_label_str_len = len(first_column_label_str)
            result += first_column_label_str + ' ' * (max_label_str_len - first_column_label_str_len) + '|'

            # initialize sum of this row
            row_sum = 0

            # other column values of this table
            for row_label in self.possible_labels:
                key = (first_column_label, row_label)
                value = self.confusion_matrix.get(key, 0)
                value_str = str(value)
                value_str_len = len(value_str)

                # update column and row sums
                column_sums[row_label] = column_sums.get(row_label, 0) + value
                row_sum += value

                result += ' ' * (max_label_str_len - value_str_len) + value_str + '|'
            # --------------------
            # close this row with the row sum
            result += '\tactual: ' + str(row_sum) + '\n'
        # =========================

        # last row: print the column sums
        result += horizontal_bar_str + '\n'

        total_nb_of_examples = 0

        result += ' ' * max_label_str_len + '|'
        for column_label in self.possible_labels:
            column_sum = column_sums[column_label]
            column_sum_str = str(column_sum)
            column_sum_str_len = len(column_sum_str)

            total_nb_of_examples += column_sum

            result += ' ' * (max_label_str_len - column_sum_str_len) + column_sum_str + '|'

        result += '\ttotal: ' + str(self.total_nb_of_examples)

        return result

    def get_nb_of_examples_str_verbose(self) -> str:
        result = "total nb of examples: " + str(self.total_nb_of_examples) + '\n'
        result += "examples labeled correctly: " + str(self.nb_ex_correctly_classified) + "/" + str(
            self.total_nb_of_examples) + ", " + str(
            self.nb_ex_correctly_classified / self.total_nb_of_examples * 100) + "%\n"
        result += "examples labeled incorrectly: " + str(self.nb_ex_incorrectly_classified) + "/" + str(
            self.total_nb_of_examples) + ", " + str(
            self.nb_ex_incorrectly_classified / self.total_nb_of_examples * 100) + "%\n"
        return result

    def get_classification_report_str(self) -> str:
        if len(self.true_labels_str) == 0:
            warnings.warn("PROBLEM: len(self.true_labels_str) == 0:" +  str(self.true_labels_str))
        if len(self.predicted_labels_str) == 0:
            warnings.warn("PROBLEM: len(self.predicted_labels_str) == 0:" + str(self.predicted_labels_str))
        if len(self.true_labels_str) != len(self.predicted_labels_str):
            warnings.warn("PROBLEM: len(self.true_labels_str)  != len(self.predicted_labels_str):")
            warnings.warn("self.true_labels_str: " + str(self.true_labels_str))
            warnings.warn("self.predicted_labels_str: " + str(self.predicted_labels_str))
        classification_rep = classification_report(self.true_labels_str, self.predicted_labels_str)
        result = '--- Classification report (scikit-learn) ---\n\n'
        result += classification_rep
        return result

    def get_accuracy(self) -> Tuple[float, str]:
        accuracy = accuracy_score(self.true_labels_str, self.predicted_labels_str)
        accuracy_str = "accuracy: " + str(accuracy) + '\n'
        return accuracy, accuracy_str

    def write_out_statistics_to_file(self, fname: str):
        with open(fname, 'w') as f:
            f.write("===  MODEL VERIFICATION STATISTICS ===\n\n")
            f.write(self.get_accuracy()[1] + '\n')
            f.write(self.get_classification_report_str() + '\n')
            f.write(self.get_confusion_matrix_str())

# class ClassificationStatisticsHandler2:
#     def __init__(self, possible_labels: List[Label]):
#         self.true_labels = []
#         self.predicted_labels = []
#         self.possible_labels = possible_labels
#
#         self.total_nb_of_examples = 0
#         self.nb_ex_correctly_classified = 0
#         self.nb_ex_incorrectly_classified = 0
#
#         self.confusion_matrix = None
#
#     def update_statistics(self, actual_label, predicted_label):
#
#         is_correctly_classified = (actual_label == predicted_label)
#         if is_correctly_classified:
#             self.nb_ex_correctly_classified += 1
#         else:
#             self.nb_ex_incorrectly_classified += 1
#
#         self.total_nb_of_examples += 1
#
#     def confusion_matrix(self):
#         return metrics.confusion_matrix(self.true_labels, self.predicted_labels)

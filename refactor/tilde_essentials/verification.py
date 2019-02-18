from refactor.tilde_essentials.tree import DecisionTree
from refactor.tilde_essentials.classification_statistics_handler import ClassificationStatisticsHandler


def verify(decision_tree: DecisionTree, test_examples, debug_printing=False):
    possible_labels = decision_tree.tree.labels

    statistics_handler = ClassificationStatisticsHandler(possible_labels)

    # classifier.debug_printing = True

    actual_labels = []
    predicted_labels = []

    for test_ex in test_examples:
        actual_label = test_ex.label

        predicted_label = decision_tree.predict(test_ex)
        # found_labels = classifier.classify(example)
        # if len(found_labels) > 1:
        #     print('actual label: ', actual_label)
        #     print('found labels: ', found_labels)
        #
        # a_predicted_label = found_labels[0]

        # TEST
        actual_labels.append(str(actual_label))
        predicted_labels.append(str([predicted_label]))

        statistics_handler.update_statistics(actual_label, predicted_label)
    # -------------

    # conf_matrix = confusion_matrix(actual_labels, predicted_labels)
    # accuracy = accuracy_score(actual_labels, predicted_labels)
    #
    # possible_labels_str = [str(label) for label in possible_labels]

    if debug_printing:
        # print("sklearn confusion matrix:")
        # print(conf_matrix)
        # print("pretty print:")
        # print_cm(conf_matrix, labels=possible_labels_str)
        print("===  MODEL VERIFICATION STATISTICS ===")

        print(statistics_handler.get_accuracy()[1])

        # precision = precision_score(actual_labels, predicted_labels)
        # recall = recall_score(actual_labels, predicted_labels)
        # print('precision:')
        # print('\t' + str(precision))
        # print('recall:')
        # print('\t' + str(recall))

        print(statistics_handler.get_classification_report_str())
        print(statistics_handler.get_nb_of_examples_str_verbose() + '\n')
        print(statistics_handler.get_confusion_matrix_str())

        # nb_of_examples = len(examples)
        # nb_of_correcty_labeled_examples = statistics_handler.nb_ex_correctly_classified
        # nb_of_incorrecty_labeled_examples = statistics_handler.nb_ex_incorrectly_classified
        #
        # if debug_printing:
        #     print("total nb of examples: " + str(nb_of_examples))
        #     print(
        #         "examples labeled correctly: " + str(nb_of_correcty_labeled_examples) + "/" + str(
        #             nb_of_examples) + ", " + str(
        #             nb_of_correcty_labeled_examples / nb_of_examples * 100) + "%")
        #     print("examples labeled incorrectly: " + str(nb_of_incorrecty_labeled_examples) + "/" + str(
        #         nb_of_examples) + ", " + str(
        #         nb_of_incorrecty_labeled_examples / nb_of_examples * 100) + "%\n")
        #     print("--- confusion matrix: true/predicted --- :")
        #     print(statistics_handler.get_confusion_matrix_str())

    return statistics_handler

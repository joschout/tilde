from math import sqrt
from statistics import mean, variance
from typing import Set, List, Optional, Tuple

import time
from problog.logic import Constant
from problog.program import SimpleProgram

from tilde.IO.input_format import KnowledgeBaseFormat
from tilde.IO.parsing_settings.setting_parser import SettingsParserMapper
from tilde.classification.classification_helper import get_keys_classifier, do_labeled_examples_get_correctly_classified
from tilde.classification.classification_statistics_handler import ClassificationStatisticsHandler
from tilde.classification.confidence_intervals import mean_confidence_interval
from tilde.fold.fold_helper import write_out_tree, write_out_program, FoldData, get_fold_info_filenames, \
    get_keys_in_fold_file
from tilde.representation.example import InternalExampleFormat, ExampleWrapper, ClauseDBExampleWrapper, \
    SimpleProgramExampleWrapper
from tilde.representation.example_collection import ExampleCollection
from tilde.run.program_phase import preprocessing_examples_keys, build_tree, convert_tree_to_program, prune_tree
from tilde.trees.TreeBuilder import TreeBuilderType


# dir_logic_files = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ecml06 - met ace bestanden\\bongard4\\results\\t-0-0-0\\'
# fname_prefix_logic = 'bongard'
# 
# fname_examples = dir_logic_files + fname_prefix_logic + kb_suffix
# fname_settings = dir_logic_files + fname_prefix_logic + s_suffix
# fname_background = dir_logic_files + fname_prefix_logic + bg_suffix
# 
# dir_fold_files = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ecml06 - met ace bestanden\\bongard4\\foil\\folds\\'
# fname_prefix_fold = 'test'
# fold_start_index = 0
# nb_folds = 10
# fold_suffix = '.txt'
# 
# dir_output_files = 'D:\\KUL\\KUL MAI\\Masterproef\\TILDE\\tilde\\fold\\data\\'


def split_examples_into_training_and_test_sets(
        all_key_sets: List[Set[Constant]], test_key_set: Set[Constant],
        examples_collection_usable_for_training: ExampleCollection,
        examples_usable_for_testing: List[ClauseDBExampleWrapper]
) -> Tuple[ExampleCollection, List[ExampleWrapper]]:
    training_key_sets_list = [s for s in all_key_sets if s is not test_key_set]  # type: List[Set[Constant]]

    training_key_set = set.union(*training_key_sets_list)  # type: Set[Constant]

    training_example_collection = examples_collection_usable_for_training.filter_examples(
        training_key_set)  # type: ExampleCollection

    test_examples = [ex_wp for ex_wp in examples_usable_for_testing if
                     ex_wp.key in test_key_set]  # type: List[ExampleWrapper]

    return training_example_collection, test_examples


def do_one_fold(fold_index: int, test_key_set: Set[Constant], fd: FoldData
                ):
    print('\n===========================')
    print('=== start FOLD ' + str(fold_index + 1) + ' of ' + str(fd.nb_folds))
    print('===========================')

    training_example_collection, test_examples = split_examples_into_training_and_test_sets(
        fd.all_key_sets, test_key_set, fd.examples_collection_usable_for_training, fd.examples_usable_for_testing)
    print('\ttotal nb of labeled examples: ' + str(fd.total_nb_of_labeled_examples))
    nb_of_training_ex = len(training_example_collection.example_wrappers_sp)
    nb_of_test_ex = len(test_examples)
    print('\tnb of TRAINING ex: ' + str(nb_of_training_ex))
    print('\tnb of TEST ex: ' + str(nb_of_test_ex))

    # ===========================
    start_time = time.time()

    # ==============================================================================================================
    print('\t=== start building tree for fold ' + str(fold_index + 1))

    # TRAIN MODEL using training set
    tree = build_tree(fd.internal_ex_format, fd.treebuilder_type, fd.parsed_settings.language,
                      fd.possible_labels, training_example_collection, prediction_goal=fd.prediction_goal,
                      full_background_knowledge_sp=fd.full_background_knowledge_sp,
                      debug_printing_tree_building=fd.debug_printing_tree_building)

    tree = prune_tree(tree, debug_printing_tree_pruning=fd.debug_printing_tree_pruning)
    nb_of_nodes = tree.get_nb_of_nodes()
    nb_inner_nodes = tree.get_nb_of_inner_nodes()
    fd.total_nb_of_nodes_per_fold.append(nb_of_nodes)
    fd.nb_of_inner_node_per_fold.append(nb_inner_nodes)

    # write out tree
    tree_fname = fd.dir_output_files + fd.fname_prefix_fold + '_fold' + str(fold_index) + ".tree"
    write_out_tree(tree_fname, tree)

    print('\t=== end building tree for fold ' + str(fold_index + 1))

    # ==============================================================================================================

    print('\t=== start converting tree to program for fold ' + str(fold_index + 1))
    program = convert_tree_to_program(fd.kb_format, fd.treebuilder_type, tree, fd.parsed_settings.language,
                                      debug_printing=fd.debug_printing_program_conversion,
                                      prediction_goal=fd.prediction_goal,
                                      index_of_label_var=fd.index_of_label_var)
    program_fname = fd.dir_output_files + fd.fname_prefix_fold + '_fold' + str(fold_index) + ".program"
    write_out_program(program_fname, program)

    print('\t=== end converting tree to program for fold ' + str(fold_index + 1))

    # ==============================================================================================================

    print('\t=== start classifying test set' + str(fold_index + 1))
    # EVALUATE MODEL using test set
    classifier = get_keys_classifier(fd.internal_ex_format, program, fd.prediction_goal,
                                     fd.index_of_label_var, fd.stripped_background_knowledge,
                                     debug_printing=fd.debug_printing_get_classifier)

    statistics_handler = do_labeled_examples_get_correctly_classified(
        classifier, test_examples, fd.possible_labels,
        fd.debug_printing_classification)  # type: ClassificationStatisticsHandler

    # ===================
    end_time = time.time()
    # time in seconds: # time in seconds
    elapsed_time = end_time - start_time
    fd.execution_time_per_fold.append(elapsed_time)

    accuracy, _ = statistics_handler.get_accuracy()
    fd.accuracies_folds.append(accuracy)

    statistics_fname = fd.dir_output_files + fd.fname_prefix_fold + '_fold' + str(fold_index) + ".statistics"
    statistics_handler.write_out_statistics_to_file(statistics_fname)

    with open(statistics_fname, 'a') as f:
        f.write('\n\nnb of TRAINING ex: ' + str(nb_of_training_ex) + "\n")
        f.write('nb of TEST ex: ' + str(nb_of_test_ex) + "\n\n")

        f.write("total nb of nodes: " + str(nb_of_nodes) + "\n")
        f.write("nb of internal nodes: " + str(nb_inner_nodes) + "\n\n")
        f.write("execution time of fold: " + str(elapsed_time) + " seconds\n")
    print("total nb of nodes: " + str(nb_of_nodes))
    print("nb of internal nodes: " + str(nb_inner_nodes))
    print("execution time of fold: ", elapsed_time, "seconds")

    print('\t=== end classifying test set' + str(fold_index + 1))
    print('\t=== end FOLD ' + str(fold_index + 1) + ' of ' + str(fd.nb_folds) + '\n')


def do_all_examples(fd: FoldData):
    print('\n=======================================')
    print('=== FINALLY, learn tree on all examples')
    print('========================================')
    print('\ttotal nb of labeled examples: ' + str(fd.total_nb_of_labeled_examples))

    print('\t=== start building tree for ALL examples')

    # ===========================
    start_time = time.time()

    # TRAIN MODEL using training set
    tree = build_tree(fd.internal_ex_format, fd.treebuilder_type, fd.parsed_settings.language,
                      fd.possible_labels, fd.examples_collection_usable_for_training,
                      prediction_goal=fd.prediction_goal,
                      full_background_knowledge_sp=fd.full_background_knowledge_sp,
                      debug_printing_tree_building=fd.debug_printing_tree_building)

    tree = prune_tree(tree, debug_printing_tree_pruning=fd.debug_printing_tree_pruning)
    nb_of_nodes = tree.get_nb_of_nodes()
    nb_inner_nodes = tree.get_nb_of_inner_nodes()
    fd.total_nb_of_nodes_per_fold.append(nb_of_nodes)
    fd.nb_of_inner_node_per_fold.append(nb_inner_nodes)

    # write out tree
    tree_fname = fd.dir_output_files + fd.fname_prefix_fold + ".tree"
    write_out_tree(tree_fname, tree)

    print('=== end building tree for ALL examples')

    print('=== start converting tree to program for ALL examples')
    program = convert_tree_to_program(fd.kb_format, fd.treebuilder_type, tree, fd.parsed_settings.language,
                                      debug_printing=fd.debug_printing_program_conversion,
                                      prediction_goal=fd.prediction_goal,
                                      index_of_label_var=fd.index_of_label_var)
    program_fname = fd.dir_output_files + fd.fname_prefix_fold + ".program"
    write_out_program(program_fname, program)

    print('=== end converting tree to program for ALL examples')

    all_examples = fd.examples_collection_usable_for_training.get_labeled_examples()

    print('\t=== start classifying total set')
    # EVALUATE MODEL using test set
    classifier = get_keys_classifier(fd.internal_ex_format, program, fd.prediction_goal,
                                     fd.index_of_label_var, fd.stripped_background_knowledge,
                                     debug_printing=fd.debug_printing_get_classifier)

    statistics_handler = do_labeled_examples_get_correctly_classified(classifier, all_examples, fd.possible_labels,
                                                                      fd.debug_printing_classification)  # type: ClassificationStatisticsHandler
    end_time = time.time()
    # time in seconds: # time in seconds
    elapsed_time = end_time - start_time

    accuracy, _ = statistics_handler.get_accuracy()

    statistics_fname = fd.dir_output_files + fd.fname_prefix_fold + ".statistics"
    statistics_handler.write_out_statistics_to_file(statistics_fname)

    mean_accuracy_of_folds = mean(fd.accuracies_folds)
    var_accuracy_of_folds = variance(fd.accuracies_folds, mean_accuracy_of_folds)
    std_accuracy_of_folds = sqrt(var_accuracy_of_folds)

    confidence = 0.9
    mean_acc, conf_left, conf_right, diff_from_mean = mean_confidence_interval(fd.accuracies_folds, confidence)

    mean_total_nb_of_nodes = mean(fd.total_nb_of_nodes_per_fold)
    var_total_nb_of_nodes = variance(fd.total_nb_of_nodes_per_fold, mean_total_nb_of_nodes)
    std_total_nb_of_nodes = sqrt(var_total_nb_of_nodes)

    mean_nb_of_inner_nodes = mean(fd.nb_of_inner_node_per_fold)
    var_nb_of_inner_nodes = variance(fd.nb_of_inner_node_per_fold, mean_nb_of_inner_nodes)
    std_nb_of_inner_nodes = sqrt(var_nb_of_inner_nodes)

    total_execution_time_of_cross_validation = sum(fd.execution_time_per_fold)

    with open(statistics_fname, 'a') as f:
        f.write("\n\ntotal nb of examples (labeled + unlabeled): " + str(fd.total_nb_of_examples) + "\n")
        f.write("total nb of LABELED examples: " + str(fd.total_nb_of_labeled_examples) + "\n\n")

        f.write("list of accuracies per fold:\n")
        f.write("\t" + str(fd.accuracies_folds) + "\n")
        f.write("mean accuracy: " + str(mean_accuracy_of_folds) + "\n")
        f.write("var accuracy: " + str(var_accuracy_of_folds) + "\n")
        f.write("std accuracy: " + str(std_accuracy_of_folds) + "\n")
        f.write("accuracy of total tree: " + str(statistics_handler.get_accuracy()[0]) + "\n\n")
        f.write("accuracy " + str(confidence * 100) + "% confidence interval: ["
                + str(conf_left) + "," + str(conf_right) + "]\n")
        f.write("\taccuracy " + str(confidence * 100) + "% confidence interval around mean: "
                + str(mean_acc) + " +- " + str(diff_from_mean) + "\n\n")

        f.write("total nb of nodes in total tree: " + str(nb_of_nodes) + "\n")
        f.write("nb of internal nodes in total tree: " + str(nb_inner_nodes) + "\n\n")

        f.write("list of total nb of nodes per fold:\n")
        f.write("\t" + str(fd.total_nb_of_nodes_per_fold) + "\n")
        f.write("mean total nb of nodes: " + str(mean_total_nb_of_nodes) + "\n")
        f.write("var total nb of nodes: " + str(var_total_nb_of_nodes) + "\n")
        f.write("std total nb of nodes: " + str(std_total_nb_of_nodes) + "\n\n")

        f.write("list of nb of internal nodes per fold:\n")
        f.write("\t" + str(fd.nb_of_inner_node_per_fold) + "\n")
        f.write("mean nb of internal nodes: " + str(mean_nb_of_inner_nodes) + "\n")
        f.write("var nb of internal nodes: " + str(var_nb_of_inner_nodes) + "\n")
        f.write("std nb of internal nodes: " + str(std_nb_of_inner_nodes) + "\n\n")

        f.write("execution times of folds:\n")
        f.write("\t" + str(fd.execution_time_per_fold) + "\n")
        f.write("total time cross  (sum folds): " + str(total_execution_time_of_cross_validation) + " seconds\n")
        f.write("time total tree building + verifying: " + str(elapsed_time) + " seconds\n")

    print("total nb of nodes in total tree: " + str(nb_of_nodes))
    print("nb of internal nodes in total tree: " + str(nb_inner_nodes))
    print()
    print("list of accuracies per fold:")
    print("\t" + str(fd.accuracies_folds))
    print("mean accuracy: " + str(mean_accuracy_of_folds))
    print("var accuracy: " + str(var_accuracy_of_folds))
    print("std accuracy " + str(std_accuracy_of_folds))
    print("accuracy of total tree: " + str(statistics_handler.get_accuracy()))
    print()
    print("accuracy " + str(confidence * 100) + "% confidence interval: ["
            + str(conf_left) + "," + str(conf_right) + "]")
    print("\taccuracy " + str(confidence * 100) + "% confidence interval around mean: "
            + str(mean_acc) + " +- " + str(diff_from_mean))
    print()
    print("total nb of nodes in total tree: " + str(nb_of_nodes))
    print("nb of internal nodes in total tree: " + str(nb_inner_nodes))
    print()
    print("list of total nb of nodes per fold:")
    print("\t" + str(fd.total_nb_of_nodes_per_fold))
    print("mean total nb of nodes: " + str(mean_total_nb_of_nodes))
    print("var total nb of nodes: " + str(var_total_nb_of_nodes))
    print("std total nb of nodes: " + str(std_total_nb_of_nodes))
    print()
    print("list of nb of internal nodes per fold:")
    print("\t" + str(fd.nb_of_inner_node_per_fold))
    print("mean nb of internal nodes: " + str(mean_nb_of_inner_nodes))
    print("var nb of internal nodes: " + str(var_nb_of_inner_nodes))
    print("std nb of internal nodes: " + str(std_nb_of_inner_nodes))
    print()
    print("execution times of folds:")
    print("\t" + str(fd.execution_time_per_fold))
    print("total time cross  (sum folds):", total_execution_time_of_cross_validation, "seconds")
    print("time total tree building + verifying:", elapsed_time, "seconds")

    print('\t=== end classifying total set')


def main_cross_validation(fname_examples: str, fname_settings: str, fname_background: str,
                          dir_fold_files: str, fname_prefix_fold: str, fold_start_index: int, nb_folds: int,
                          fold_suffix: str, dir_output_files: str,
                          filter_out_unlabeled_examples=False,
                          debug_printing_example_parsing=False,
                          debug_printing_tree_building=False,
                          debug_printing_tree_pruning=False,
                          debug_printing_program_conversion=False,
                          debug_printing_get_classifier=False,
                          debug_printing_classification=False):
    fd = FoldData.build_fold_data(fname_examples, fname_settings, fname_background,
                                  dir_fold_files, fname_prefix_fold, fold_start_index, nb_folds, fold_suffix,
                                  dir_output_files,
                                  filter_out_unlabeled_examples,
                                  debug_printing_example_parsing,
                                  debug_printing_tree_building,
                                  debug_printing_tree_pruning,
                                  debug_printing_program_conversion,
                                  debug_printing_get_classifier,
                                  debug_printing_classification
                                  )

    # take one key set as test, the others as training
    for fold_index, test_key_set in enumerate(fd.all_key_sets):
        do_one_fold(fold_index, test_key_set, fd)

    do_all_examples(fd)


# def main_cross_validation_old(fname_examples: str, fname_settings: str, fname_background: str,
#                               dir_fold_files: str, fname_prefix_fold: str, fold_start_index: int, nb_folds: int, fold_suffix: str,
#                               dir_output_files: str,
#                               debug_printing_example_parsing=False,
#                               debug_printing_tree_building=False,
#                               debug_printing_tree_pruning=False,
#                               debug_printing_program_conversion=False,
#                               debug_printing_get_classifier=False,
#                               debug_printing_classification=False):
#     settings_file_parser = SettingsParserMapper.get_settings_parser(KnowledgeBaseFormat.KEYS)
#     parsed_settings = settings_file_parser.parse(fname_settings)
#
#     kb_format = KnowledgeBaseFormat.KEYS
#     internal_ex_format = InternalExampleFormat.CLAUSEDB
#
#     treebuilder_type = TreeBuilderType.DETERMINISTIC
#
#     print('=== start preprocessing examples ===')
#     examples_collection_usable_for_training, prediction_goal, index_of_label_var, possible_labels, background_knowledge_wrapper = \
#         preprocessing_examples_keys(fname_examples, parsed_settings, internal_ex_format,
#                                     fname_background, debug_printing_example_parsing,
#                                     filter_out_unlabeled_examples=False)
#
#     total_nb_of_examples = len(examples_collection_usable_for_training.example_wrappers_sp)
#
#     print('\tnb of examples: ' + str(total_nb_of_examples))
#     print('\tprediction goal: ' + str(prediction_goal))
#     print('\tpossible labels: ' + str(possible_labels))
#     print('=== end preprocessing examples ===\n')
#
#     full_background_knowledge_sp \
#         = background_knowledge_wrapper.get_full_background_knowledge_simple_program()  # type: Optional[SimpleProgram]
#
#     stripped_background_knowledge = background_knowledge_wrapper.get_stripped_background_knowledge()  # type: Optional[SimpleProgram]
#     stripped_examples_simple_program = examples_collection_usable_for_training.get_labeled_example_wrappers_sp()  # type: List[SimpleProgramExampleWrapper]
#     examples_usable_for_testing = stripped_examples_simple_program  # type: List[SimpleProgramExampleWrapper]
#
#     if internal_ex_format == InternalExampleFormat.CLAUSEDB:
#         stripped_examples_clausedb = ClauseDBExampleWrapper.get_clause_db_examples(stripped_examples_simple_program,
#                                                                                    background_knowledge=stripped_background_knowledge)
#         examples_usable_for_testing = stripped_examples_clausedb  # type: List[ClauseDBExampleWrapper]
#
#     fold_file_names = get_fold_info_filenames(fold_start_index, nb_folds, dir_fold_files, fname_prefix_fold,
#                                               fold_suffix)
#
#     accuracies_folds = []
#
#     # read in all the keysets
#     all_key_sets = []  # type: List[Set[Constant]]
#     for fname in fold_file_names:
#         all_key_sets.append(get_keys_in_fold_file(fname))
#
#     # take one key set as test, the others as training
#     for fold_index, test_key_set in enumerate(all_key_sets):
#         print('\n===========================')
#         print('=== start FOLD ' + str(fold_index + 1) + ' of ' + str(nb_folds))
#         print('===========================')
#
#         training_example_collection, test_examples = split_examples_into_training_and_test_sets(
#             all_key_sets, test_key_set, examples_collection_usable_for_training, examples_usable_for_testing)
#         print('\ttotal nb of examples: ' + str(total_nb_of_examples))
#         print('\tnb of TRAINING ex: ' + str(len(training_example_collection.example_wrappers_sp)))
#         print('\tnb of TEST ex: ' + str(len(test_examples)))
#
#         # ==============================================================================================================
#         print('\t=== start building tree for fold ' + str(fold_index + 1))
#
#         # TRAIN MODEL using training set
#         tree = build_tree(internal_ex_format, treebuilder_type, parsed_settings.language,
#                           possible_labels, training_example_collection, prediction_goal=prediction_goal,
#                           full_background_knowledge_sp=full_background_knowledge_sp,
#                           debug_printing_tree_building=debug_printing_tree_building)
#
#         tree = prune_tree(tree, debug_printing_tree_pruning=debug_printing_tree_pruning)
#
#         # write out tree
#         tree_fname = dir_output_files + fname_prefix_fold + '_fold' + str(fold_index) + ".tree"
#         write_out_tree(tree_fname, tree)
#
#         print('\t=== end building tree for fold ' + str(fold_index + 1))
#
#         # ==============================================================================================================
#
#         print('\t=== start converting tree to program for fold ' + str(fold_index + 1))
#         program = convert_tree_to_program(kb_format, treebuilder_type, tree, parsed_settings.language,
#                                           debug_printing=debug_printing_program_conversion,
#                                           prediction_goal=prediction_goal,
#                                           index_of_label_var=index_of_label_var)
#         program_fname = dir_output_files + fname_prefix_fold + '_fold' + str(fold_index) + ".program"
#         write_out_program(program_fname, program)
#
#         print('\t=== end converting tree to program for fold ' + str(fold_index + 1))
#
#         # ==============================================================================================================
#
#         print('\t=== start classifying test set' + str(fold_index + 1))
#         # EVALUATE MODEL using test set
#         classifier = get_keys_classifier(internal_ex_format, program, prediction_goal,
#                                          index_of_label_var, stripped_background_knowledge,
#                                          debug_printing=debug_printing_get_classifier)
#
#         statistics_handler = do_labeled_examples_get_correctly_classified(classifier, test_examples, possible_labels,
#                                                                           debug_printing_classification)  # type: ClassificationStatisticsHandler
#         accuracy, _ = statistics_handler.get_accuracy()
#         accuracies_folds.append(accuracy)
#
#         statistics_fname = dir_output_files + fname_prefix_fold + '_fold' + str(fold_index) + ".statistics"
#         statistics_handler.write_out_statistics_to_file(statistics_fname)
#
#         print('\t=== end classifying test set' + str(fold_index + 1))
#
#         print('\t=== end FOLD ' + str(fold_index + 1) + ' of ' + str(nb_folds) + '\n')
#
#     print('\n=======================================')
#     print('=== FINALLY, learn tree on all examples')
#     print('========================================')
#     print('\ttotal nb of examples: ' + str(total_nb_of_examples))
#
#     print('\t=== start building tree for ALL examples')
#
#     # TRAIN MODEL using training set
#     tree = build_tree(internal_ex_format, treebuilder_type, parsed_settings.language,
#                       possible_labels, examples_collection_usable_for_training, prediction_goal=prediction_goal,
#                       full_background_knowledge_sp=full_background_knowledge_sp,
#                       debug_printing_tree_building=debug_printing_tree_building)
#
#     tree = prune_tree(tree, debug_printing_tree_pruning=debug_printing_tree_pruning)
#
#     # write out tree
#     tree_fname = dir_output_files + fname_prefix_fold + ".tree"
#     write_out_tree(tree_fname, tree)
#
#     print('=== end building tree for ALL examples')
#
#     print('=== start converting tree to program for ALL examples')
#     program = convert_tree_to_program(kb_format, treebuilder_type, tree, parsed_settings.language,
#                                       debug_printing=debug_printing_program_conversion, prediction_goal=prediction_goal,
#                                       index_of_label_var=index_of_label_var)
#     program_fname = dir_output_files + fname_prefix_fold + ".program"
#     write_out_program(program_fname, program)
#
#     print('=== end converting tree to program for ALL examples')
#
#     all_examples = examples_collection_usable_for_training.get_labeled_examples()
#
#     print('\t=== start classifying total set')
#     # EVALUATE MODEL using test set
#     classifier = get_keys_classifier(internal_ex_format, program, prediction_goal,
#                                      index_of_label_var, stripped_background_knowledge,
#                                      debug_printing=debug_printing_get_classifier)
#
#     statistics_handler = do_labeled_examples_get_correctly_classified(classifier, all_examples, possible_labels,
#                                                                       debug_printing_classification)  # type: ClassificationStatisticsHandler
#     accuracy, _ = statistics_handler.get_accuracy()
#
#     statistics_fname = dir_output_files + fname_prefix_fold + ".statistics"
#     statistics_handler.write_out_statistics_to_file(statistics_fname)
#
#     mean_accuracy_of_folds = mean(accuracies_folds)
#     var_accuracy_of_folds = variance(accuracies_folds, mean_accuracy_of_folds)
#     std_accuracy_of_folds = sqrt(var_accuracy_of_folds)
#
#     with open(statistics_fname, 'a') as f:
#         f.write("list of accuracies:\n")
#         f.write("\t" + str(accuracies_folds))
#         f.write("mean accuracy: " + str(mean_accuracy_of_folds) + "\n")
#         f.write("var accuracy: " + str(var_accuracy_of_folds) + "\n")
#         f.write("std accuracy " + str(std_accuracy_of_folds) + "\n")
#         f.write("accuracy of total tree: " + str(statistics_handler.get_accuracy()) + "\n")
#
#     print("list of accuracies:")
#     print("\t" + str(accuracies_folds))
#     print("mean accuracy: " + str(mean_accuracy_of_folds))
#     print("var accuracy: " + str(var_accuracy_of_folds))
#     print("std accuracy " + str(std_accuracy_of_folds))
#     print("accuracy of total tree: " + str(statistics_handler.get_accuracy()))
#
#     print('\t=== end classifying total set')


def filter_examples(examples: List[ExampleWrapper], key_set: Set[ExampleWrapper]):
    return [ex for ex in examples if ex.key in key_set]


if __name__ == '__main__':
    main_cross_validation()

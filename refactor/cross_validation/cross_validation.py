import time
from typing import Set

from problog.logic import Constant

from mai_experiments.fold_file_parser import split_examples_into_training_and_test_sets
from refactor.tilde_essentials.tree import DecisionTree

class CrossValidationController:
    pass

class FoldController:
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
    tree_builder = get_default_decision_tree_builder(language, prediction_goal)  # type: TreeBuilder
    decision_tree = DecisionTree()
    decision_tree.fit(examples=training_examples_fold, tree_builder=tree_builder)
    # tree = build_tree(fd.internal_ex_format, fd.treebuilder_type, fd.parsed_settings.language,
    #                   fd.possible_labels, training_example_collection, prediction_goal=fd.prediction_goal,
    #                   full_background_knowledge_sp=fd.full_background_knowledge_sp,
    #                   debug_printing_tree_building=fd.debug_printing_tree_building, engine=fd.engine)

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
                                     debug_printing=fd.debug_printing_get_classifier, engine=fd.engine)

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
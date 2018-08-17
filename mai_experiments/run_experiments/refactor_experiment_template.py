import os
import statistics
import sys
import time
from typing import List

from mai_experiments.experiment_settings import FileNameData, DebugPrintingOptions
from mai_experiments.fold_control import FoldInfo
from mai_experiments.fold_control import FoldInfoController
from mai_experiments.fold_example_splitting import FoldExampleSplitter
from mai_experiments.run_experiments.example_preprocessing_refactor import Experiment
from refactor.default_interface import DefaultHandler
from refactor.tilde_essentials.tree import DecisionTree, write_out_tree
from refactor.tilde_essentials.tree_builder import TreeBuilder
from refactor.tilde_essentials.tree_pruning import prune_leaf_nodes_with_same_label
from tilde.representation.example import ExampleWrapper
from tilde.representation.example_collection import ExampleCollection


def run_experiment(file_name_data: FileNameData, fold_info_controller: FoldInfoController,
                   default_handler: DefaultHandler,
                   hide_printouts: bool = False,
                   filter_out_unlabeled_examples=False,
                   debug_printing_options=DebugPrintingOptions()):
    # -- create output directory
    if not os.path.exists(file_name_data.output_dir):
        os.makedirs(file_name_data.output_dir)

    print("start", file_name_data.test_name)
    save_stdout = sys.stdout
    if hide_printouts:
        sys.stdout = open(os.devnull, "w")

    experiment = Experiment()
    experiment.preprocess_examples_and_background_knowledge(file_name_data, filter_out_unlabeled_examples,
                                                            debug_printing_options)

    fold_example_splitter = FoldExampleSplitter(fold_info_controller)
    for fold_info, training_examples_collection, test_examples in fold_example_splitter.fold_split_generator(
            experiment):  # type: FoldInfo, ExampleCollection, List[ExampleWrapper]
        print("fold: ", fold_info.index)
        training_examples = default_handler.get_transformed_example_list(training_examples_collection)

        tree_builder = default_handler.get_default_decision_tree_builder(experiment.language,
                                                                         experiment.prediction_goal)  # type: TreeBuilder
        decision_tree = DecisionTree()
        start_build_time = time.time()
        decision_tree.fit(examples=training_examples, tree_builder=tree_builder)

        print("unpruned:")
        print(decision_tree)
        decision_tree.prune(prune_leaf_nodes_with_same_label)
        end_build_time = time.time()

        # run_time_sec = end_time - start_time
        run_time_sec = end_build_time - start_build_time
        run_time_ms = 1000.0 * run_time_sec
        fold_info.dt_build_time_ms = run_time_ms
        print("run time (ms):", run_time_ms)
        print("pruned")
        print(decision_tree)

        # write out tree
        tree_fname = os.path.join(file_name_data.output_dir,
                                  "refactor_" + fold_info_controller.fname_prefix_fold + '_fold' + str(fold_info.index) + ".tree")
        write_out_tree(tree_fname, decision_tree)

        # ------------------------------------------

        # --- DESTRUCTION (necessary for Django) ---
        decision_tree.destruct()

        for ex in training_examples:
            ex.destruct()

    dt_build_times = [fold_info.dt_build_time_ms for (_index, fold_info) in fold_info_controller.fold_infos.items()]
    average_build_time = statistics.mean(dt_build_times)
    print("average dt build time (ms):", average_build_time)

    if hide_printouts:
        sys.stdout = save_stdout
    print("finished", file_name_data.test_name)

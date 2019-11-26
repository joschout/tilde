from typing import Set, List, Tuple

from problog.logic import Constant

from mai_experiments.fold_control import FoldInfoController, FoldInfo
from mai_experiments.run_experiments_refactor.example_preprocessing_refactor import Experiment
from mai_version.representation.example import ClauseDBExampleWrapper, ExampleWrapper
from mai_version.representation.example_collection import ExampleCollection


class FoldExampleSplitter:
    def __init__(self, fold_info_controller: FoldInfoController):
        self.fold_info_controller = fold_info_controller  # type: FoldInfoController

    def fold_split_generator(self, experiment: Experiment)\
            -> Tuple[FoldInfo, ExampleCollection, List[ExampleWrapper]]:
        for fold_index, fold_info in self.fold_info_controller.fold_infos.items():  # type: int, FoldInfo
            training_examples, test_examples = self._split_examples_into_training_and_test_sets(
                self.fold_info_controller.all_keys,
                fold_info.key_set,
                experiment.training_examples_collection,
                experiment.examples_usable_for_testing
            )
            yield fold_info, training_examples, test_examples

    def _split_examples_into_training_and_test_sets(self,
                                                    all_keys_set: Set[Constant],
                                                    test_key_set: Set[Constant],
                                                    examples_collection_usable_for_training: ExampleCollection,
                                                    examples_usable_for_testing: List[ClauseDBExampleWrapper]
                                                    ) -> Tuple[ExampleCollection, List[ExampleWrapper]]:
        # for all keys
        # if key is not part of the current test set keys
        #   add key to training set keys
        # else

        training_key_set = [s for s in all_keys_set
                            if s not in test_key_set]  # type: Set[Constant]

        training_example_collection = examples_collection_usable_for_training.filter_examples(
            training_key_set)  # type: ExampleCollection

        test_examples = [ex_wp for ex_wp in examples_usable_for_testing
                         if ex_wp.key in test_key_set]  # type: List[ExampleWrapper]

        return training_example_collection, test_examples

import os
from typing import List, Set, Tuple, Dict

from problog.logic import Constant

from tilde.IO.parsing_settings.utils import ConstantBuilder
from tilde.main import kb_suffix, s_suffix, bg_suffix


class DebugPrintingOptions:
    def __init__(self,
                 example_parsing=False,
                 tree_building=False,
                 tree_pruning=False,
                 program_conversion=False,
                 get_classifier=False,
                 classification=False):
        self.example_parsing = example_parsing
        self.tree_building = tree_building
        self.tree_pruning = tree_pruning
        self.program_conversion = program_conversion
        self.get_classifier = get_classifier
        self.debug_printing_classification = classification


class FileNameData:
    def __init__(self, root_dir, logic_relative_dir, fold_relative_dir, output_relative_dir,
                 test_name, logic_name):
        self.fold_dir = os.path.join(root_dir, test_name, fold_relative_dir)
        self.output_dir = os.path.join(root_dir, test_name, output_relative_dir)

        logic_dir = os.path.join(root_dir, test_name, logic_relative_dir)
        self.fname_examples = os.path.join(logic_dir, logic_name + kb_suffix)
        self.fname_settings = os.path.join(logic_dir, logic_name + s_suffix)
        self.fname_background = os.path.join(logic_dir, logic_name + bg_suffix)


class FoldInfo:
    def __init__(self, index, file_name, key_set):
        self.index = index,
        self.file_name = file_name
        self.key_set = key_set  # type: Set[Constant]


class FoldController:
    def __init__(self,
                 fold_file_directory,
                 fold_fname_prefix='test',
                 fold_start_index=0,
                 nb_folds=10,
                 fold_suffix='.txt',
                 ):
        self.fold_file_directory = fold_file_directory
        self.fname_prefix_fold = fold_fname_prefix
        self.start_index = fold_start_index
        self.nb_folds = nb_folds
        self.fold_suffix = fold_suffix

        self.fold_infos = []  # type: Dict[int, FoldInfo]


    def _get_fold_info_filenames(self) -> List[Tuple[int, str]]:
        fnames = []
        for i in range(self.start_index, self.start_index + self.nb_folds):
            fname = os.path.join(self.fold_file_directory, self.fname_prefix_fold + str(i) + self.fold_suffix)
            fnames.append((i, fname))
        return fnames

    def get_key_sets_per_fold(self):
        fold_file_names = self._get_fold_info_filenames()
        for fold_index, fold_file_name in fold_file_names:
            self.fold_infos = FoldInfo(index=fold_index, file_name=fold_file_name, key_set=test_example_keyset)

        return self.fold_infos


    @staticmethod
    def _get_keys_in_fold_file( fname: str) -> Set[Constant]:
        key_set = set()

        with open(fname, 'r') as f:
            for line in f:
                split_line = line.split(':')
                key = split_line[0]
                key_set.add(ConstantBuilder.parse_constant_str(key))
        return key_set

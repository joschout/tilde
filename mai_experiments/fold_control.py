import os
from typing import List, Tuple, Set, Dict, Optional

from problog.logic import Constant

from tilde.IO.parsing_settings.utils import ConstantBuilder


class FoldInfoController:
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

        self.all_keys = set()  # type: Set[Constant]

        self.fold_infos = {}  # type: Dict[int, FoldInfo]

        self._get_key_sets_per_fold()

    def _get_fold_info_filenames(self) -> List[Tuple[int, str]]:
        fnames = []
        for i in range(self.start_index, self.start_index + self.nb_folds):
            fname = os.path.join(self.fold_file_directory, self.fname_prefix_fold + str(i) + self.fold_suffix)
            fnames.append((i, fname))
        return fnames

    def _get_key_sets_per_fold(self):
        fold_file_names = self._get_fold_info_filenames()
        for fold_index, fold_file_name in fold_file_names:
            test_example_key_set = self._get_keys_in_fold_file(fold_file_name)
            self.all_keys.update(test_example_key_set)
            self.fold_infos[fold_index] = FoldInfo(index=fold_index, file_name=fold_file_name, key_set=test_example_key_set)

    @staticmethod
    def _get_keys_in_fold_file( fname: str) -> Set[Constant]:
        key_set = set()

        with open(fname, 'r') as f:
            for line in f:
                split_line = line.split(':')
                key = split_line[0]
                key_set.add(ConstantBuilder.parse_constant_str(key))
        return key_set


class FoldInfo:
    def __init__(self, index, file_name, key_set):
        self.index = index
        self.file_name = file_name
        self.key_set = key_set  # type: Set[Constant]

        self.dt_build_time_ms = None  # type: Optional[int]

import os
from typing import TYPE_CHECKING, Optional, List, Set

from problog.engine import GenericEngine

from mai_version.IO.parsing_settings.setting_parser import SettingsParserMapper
from mai_version.run.program_phase import preprocessing_examples_keys

from problog.engine import DefaultEngine

from problog.program import SimpleProgram
from mai_version.trees import TreeNode
from mai_version.IO.input_format import KnowledgeBaseFormat
from mai_version.IO.parsing_settings.utils import FileSettings, ConstantBuilder
from mai_version.representation.example import InternalExampleFormat, Label, ClauseDBExampleWrapper, \
    SimpleProgramExampleWrapper
from mai_version.trees.TreeBuilder import TreeBuilderType
from problog.logic import Term, Constant

from mai_version.representation.background_knowledge import BackgroundKnowledgeWrapper
from mai_version.representation.example_collection import ExampleCollection


def write_out_tree(fname: str, tree: TreeNode):
    # write out tree
    print('\t--- writing out tree to: ' + fname)
    with open(fname, 'w') as f:
        f.write(str(tree))


def write_out_program(fname: str, program: SimpleProgram):
    print('--- writing out program to: ' + fname)
    with open(fname, 'w') as f:
        for program_statement in program:
            f.write(str(program_statement) + '.\n')


class FoldData:
    all_key_sets = []  # type: List[Set[Constant]]
    accuracies_folds = []
    total_nb_of_nodes_per_fold = []  # type: List[int]
    nb_of_inner_node_per_fold = []  # type: List[int]

    execution_time_per_fold = []  # type: List[float]

    examples_collection_usable_for_training = None  # type: Optional[ExampleCollection]
    examples_usable_for_testing = None

    total_nb_of_examples = None  # Optional[int]
    total_nb_of_labeled_examples = None  # Optional[int]

    kb_format = None  # type: Optional[KnowledgeBaseFormat]
    internal_ex_format = None  # type: Optional[InternalExampleFormat]
    treebuilder_type = None  # type: Optional[TreeBuilderType]
    parsed_settings = None  # type: Optional[FileSettings]
    prediction_goal = None  # type: Optional[Term]
    possible_labels = None  # type: Optional[List[Label]]
    index_of_label_var = None  # type: Optional[int]
    full_background_knowledge_sp = None  # type: Optional[BackgroundKnowledgeWrapper]
    stripped_background_knowledge = None

    def __init__(self,
                 fname_prefix_fold,
                 nb_folds,
                 dir_output_files,
                 debug_printing_example_parsing=False,
                 debug_printing_tree_building=False,
                 debug_printing_tree_pruning=False,
                 debug_printing_program_conversion=False,
                 debug_printing_get_classifier=False,
                 debug_printing_classification=False,
                 engine: GenericEngine=None
                 ):

        self.fname_prefix_fold = fname_prefix_fold
        self.nb_folds = nb_folds
        self.dir_output_files = dir_output_files
        self.dir_output_files = dir_output_files

        self.debug_printing_example_parsing = debug_printing_example_parsing
        self.debug_printing_tree_building = debug_printing_tree_building
        self.debug_printing_tree_pruning = debug_printing_tree_pruning
        self.debug_printing_program_conversion = debug_printing_program_conversion
        self.debug_printing_get_classifier = debug_printing_get_classifier
        self.debug_printing_classification = debug_printing_classification

        if engine is None:
            self.engine = DefaultEngine()
            self.engine.unknown = 1
        else:
            self.engine = engine

    @staticmethod
    def build_fold_data(fname_examples: str,
                        fname_settings: str,
                        fname_background: str,
                        dir_fold_files: str,
                        fname_prefix_fold: str,
                        fold_start_index: int,
                        nb_folds: int,
                        fold_suffix: str,
                        dir_output_files: str,
                        filter_out_unlabeled_examples=False,
                        debug_printing_example_parsing=False,
                        debug_printing_tree_building=False,
                        debug_printing_tree_pruning=False,
                        debug_printing_program_conversion=False,
                        debug_printing_get_classifier=False,
                        debug_printing_classification=False,
                        engine: GenericEngine=None):

        fd = FoldData(fname_prefix_fold,
                      nb_folds,
                      dir_output_files,
                      debug_printing_example_parsing,
                      debug_printing_tree_building,
                      debug_printing_tree_pruning,
                      debug_printing_program_conversion,
                      debug_printing_get_classifier,
                      debug_printing_classification,
                      engine=engine)

        settings_file_parser = SettingsParserMapper.get_settings_parser(KnowledgeBaseFormat.KEYS)
        fd.parsed_settings = settings_file_parser.parse(fname_settings)

        fd.kb_format = KnowledgeBaseFormat.KEYS
        fd.internal_ex_format = InternalExampleFormat.CLAUSEDB

        fd.treebuilder_type = TreeBuilderType.DETERMINISTIC

        print('=== start preprocessing examples ===')
        fd.examples_collection_usable_for_training, fd.prediction_goal, fd.index_of_label_var, fd.possible_labels, background_knowledge_wrapper = \
            preprocessing_examples_keys(fname_examples, fd.parsed_settings, fd.internal_ex_format,
                                        fname_background, debug_printing_example_parsing,
                                        filter_out_unlabeled_examples=filter_out_unlabeled_examples,
                                        fold_data=fd,
                                        engine=fd.engine)

        fd.total_nb_of_labeled_examples = len(fd.examples_collection_usable_for_training.example_wrappers_sp)

        print('\tnb of labeled examples: ' + str(fd.total_nb_of_labeled_examples))
        print('\tprediction goal: ' + str(fd.prediction_goal))
        print('\tpossible labels: ' + str(fd.possible_labels))
        print('=== end preprocessing examples ===\n')

        fd.full_background_knowledge_sp \
            = background_knowledge_wrapper.get_full_background_knowledge_simple_program()  # type: Optional[SimpleProgram]

        fd.stripped_background_knowledge = background_knowledge_wrapper.get_stripped_background_knowledge()  # type: Optional[SimpleProgram]
        stripped_examples_simple_program = fd.examples_collection_usable_for_training.get_labeled_example_wrappers_sp()  # type: List[SimpleProgramExampleWrapper]
        fd.examples_usable_for_testing = stripped_examples_simple_program  # type: List[SimpleProgramExampleWrapper]

        if fd.internal_ex_format == InternalExampleFormat.CLAUSEDB:
            stripped_examples_clausedb = ClauseDBExampleWrapper.get_clause_db_examples(stripped_examples_simple_program,
                                                                                       background_knowledge=fd.stripped_background_knowledge)
            fd.examples_usable_for_testing = stripped_examples_clausedb  # type: List[ClauseDBExampleWrapper]

        fold_file_names = get_fold_info_filenames(fold_start_index, nb_folds, dir_fold_files, fname_prefix_fold,
                                                  fold_suffix)

        fd.accuracies_folds = []

        # read in all the keysets
        for fname in fold_file_names:
            fd.all_key_sets.append(get_keys_in_fold_file(fname))

        return fd


def get_fold_info_filenames(fold_start_index: int, nb_folds: int, dir_fold_files: str, fname_prefix_fold: str,
                            fold_suffix: str) -> List[str]:
    fnames = []
    for i in range(fold_start_index, fold_start_index + nb_folds):
        fname = os.path.join(dir_fold_files, fname_prefix_fold + str(i) + fold_suffix)
        fnames.append(fname)
    return fnames


def get_keys_in_fold_file(fname: str) -> Set[Constant]:
    key_set = set()

    with open(fname, 'r') as f:
        for line in f:
            split_line = line.split(':')
            key = split_line[0]
            key_set.add(ConstantBuilder.parse_constant_str(key))
    return key_set
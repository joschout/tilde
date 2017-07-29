from typing import Set, List, Optional

from problog.logic import Constant
from problog.program import SimpleProgram

from tilde.IO.input_format import KnowledgeBaseFormat
from tilde.IO.parsing_settings.setting_parser import SettingsParserMapper
from tilde.IO.parsing_settings.utils import ConstantBuilder
from tilde.classification.classification_helper import get_keys_classifier, do_labeled_examples_get_correctly_classified
from tilde.representation.example import InternalExampleFormat, ExampleWrapper, ClauseDBExampleWrapper, \
    SimpleProgramExampleWrapper
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


def get_fold_info_filenames(fold_start_index: int, nb_folds: int, dir_fold_files: str, fname_prefix_fold: str,
                            fold_suffix: str) -> List[str]:
    fnames = []
    for i in range(fold_start_index, fold_start_index + nb_folds):
        fname = dir_fold_files + fname_prefix_fold + str(i) + fold_suffix
        fnames.append(fname)
    return fnames


def main_cross_validation(fname_examples: str,
                          fname_settings: str,
                          fname_background: str,
                          dir_fold_files: str,
                          fname_prefix_fold: str,
                          fold_start_index: int,
                          nb_folds: int,
                          fold_suffix: str,
                          dir_output_files: str,
                          debug_printing_example_parsing=False,
                          debug_printing_tree_building=False,
                          debug_printing_tree_pruning=False,
                          debug_printing_program_conversion=False,
                          debug_printing_get_classifier=False,
                          debug_printing_classification=False ):

    settings_file_parser = SettingsParserMapper.get_settings_parser(KnowledgeBaseFormat.KEYS)
    parsed_settings = settings_file_parser.parse(fname_settings)

    kb_format = KnowledgeBaseFormat.KEYS
    internal_ex_format = InternalExampleFormat.CLAUSEDB

    treebuilder_type = TreeBuilderType.DETERMINISTIC

    print('=== start preprocessing examples ===')
    examples_collection_usable_for_training, prediction_goal, index_of_label_var, possible_labels, background_knowledge_wrapper = \
        preprocessing_examples_keys(fname_examples, parsed_settings, internal_ex_format,
                                    fname_background, debug_printing_example_parsing)

    total_nb_of_examples = len(examples_collection_usable_for_training.example_wrappers_sp)

    print('\tnb of examples: ' + str(total_nb_of_examples))
    print('\tprediction goal: ' + str(prediction_goal))
    print('\tpossible labels: ' + str(possible_labels))
    print('=== end preprocessing examples ===\n')

    full_background_knowledge_sp \
        = background_knowledge_wrapper.get_full_background_knowledge_simple_program()  # type: Optional[SimpleProgram]

    stripped_background_knowledge = background_knowledge_wrapper.get_stripped_background_knowledge()  # type: Optional[SimpleProgram]
    stripped_examples_simple_program = examples_collection_usable_for_training.get_labeled_example_wrappers_sp()  # type: List[SimpleProgramExampleWrapper]
    examples_usable_for_testing = stripped_examples_simple_program  # type: List[SimpleProgramExampleWrapper]

    if internal_ex_format == InternalExampleFormat.CLAUSEDB:
        stripped_examples_clausedb = ClauseDBExampleWrapper.get_clause_db_examples(stripped_examples_simple_program,
                                                                                   background_knowledge=stripped_background_knowledge)
        examples_usable_for_testing = stripped_examples_clausedb  # type: List[ClauseDBExampleWrapper]

    fold_file_names = get_fold_info_filenames(fold_start_index, nb_folds, dir_fold_files, fname_prefix_fold,
                                              fold_suffix)

    # read in all the keysets
    key_sets = []  # type: List[Set[Constant]]
    for fname in fold_file_names:
        key_sets.append(get_keys_in_fold_file(fname))

    # take one key set as test, the others as training
    for fold_index, test_set_keys in enumerate(key_sets):
        print('\n===========================')
        print('=== start FOLD ' + str(fold_index + 1) + ' of ' + str(nb_folds))
        print('===========================')
        sets = [s for s in key_sets if s is not test_set_keys]

        training_set_keys = set.union(*sets)

        training_example_collection = examples_collection_usable_for_training.filter_examples(training_set_keys)

        test_examples = [ex_wp for ex_wp in examples_usable_for_testing if ex_wp.key in test_set_keys]
        # training_examples = filter_examples(examples, training_set_keys)
        # test_examples = filter_examples(examples, test_set_keys)

        print('\ttotal nb of examples: ' + str(total_nb_of_examples))
        print('\tnb of TRAINING ex: ' + str(len(training_example_collection.example_wrappers_sp)))
        print('\tnb of TEST ex: ' + str(len(test_examples)))

        print('\t=== start building tree for fold ' + str(fold_index + 1))

        # TRAIN MODEL using training set
        tree = build_tree(internal_ex_format, treebuilder_type, parsed_settings.language,
                          possible_labels, training_example_collection, prediction_goal=prediction_goal,
                          full_background_knowledge_sp=full_background_knowledge_sp,
                          debug_printing_tree_building=debug_printing_tree_building)

        tree = prune_tree(tree, debug_printing_tree_pruning=debug_printing_tree_pruning)

        # write out tree
        tree_fname = dir_output_files + fname_prefix_fold + '_fold' + str(fold_index) + ".tree"
        print('\t--- writing out tree to: ' + tree_fname)
        with open(tree_fname, 'w') as f:
            f.write(str(tree))

        print('\t=== end building tree for fold ' + str(fold_index + 1))

        print('\t=== start converting tree to program for fold ' + str(fold_index + 1))
        program = convert_tree_to_program(kb_format, treebuilder_type, tree, parsed_settings.language,
                                          debug_printing=debug_printing_program_conversion,
                                          prediction_goal=prediction_goal,
                                          index_of_label_var=index_of_label_var)
        program_fname = dir_output_files + fname_prefix_fold + '_fold' + str(fold_index) + ".program"
        print('\t--- writing out program to: ' + program_fname)
        with open(program_fname, 'w') as f:
            for program_statement in program:
                f.write(str(program_statement) + '.\n')

        print('\t=== end converting tree to program for fold ' + str(fold_index + 1))

        print('\t=== start classifying test set' + str(fold_index + 1))
        # EVALUATE MODEL using test set
        classifier = get_keys_classifier(internal_ex_format, program, prediction_goal,
                                         index_of_label_var, stripped_background_knowledge,
                                         debug_printing=debug_printing_get_classifier)

        statistics_handler = do_labeled_examples_get_correctly_classified(classifier, test_examples, possible_labels,
                                                                          debug_printing_classification)

        statistics_fname = dir_output_files + fname_prefix_fold + '_fold' + str(fold_index) + ".statistics"
        statistics_handler.write_out_statistics_to_file(statistics_fname)

        print('\t=== end classifying test set' + str(fold_index + 1))

        print('\t=== end FOLD ' + str(fold_index + 1) + ' of ' + str(nb_folds) + '\n')

    print('\n=======================================')
    print('=== FINALLY, learn tree on all examples')
    print('========================================')
    print('\ttotal nb of examples: ' + str(total_nb_of_examples))

    print('\t=== start building tree for ALL examples')

    # TRAIN MODEL using training set
    tree = build_tree(internal_ex_format, treebuilder_type, parsed_settings.language,
                      possible_labels, examples_collection_usable_for_training, prediction_goal=prediction_goal,
                      full_background_knowledge_sp=full_background_knowledge_sp,
                      debug_printing_tree_building=debug_printing_tree_building)

    tree = prune_tree(tree, debug_printing_tree_pruning=debug_printing_tree_pruning)

    # write out tree
    tree_fname = dir_output_files + fname_prefix_fold + ".tree"
    print('--- writing out tree to: ' + tree_fname)
    with open(tree_fname, 'w') as f:
        f.write(str(tree))

    print('=== end building tree for ALL examples')

    print('=== start converting tree to program for ALL examples')
    program = convert_tree_to_program(kb_format, treebuilder_type, tree, parsed_settings.language,
                                      debug_printing=debug_printing_program_conversion, prediction_goal=prediction_goal,
                                      index_of_label_var=index_of_label_var)
    program_fname = dir_output_files + fname_prefix_fold + ".program"
    print('--- writing out program to: ' + program_fname)
    with open(program_fname, 'w') as f:
        for program_statement in program:
            f.write(str(program_statement) + '.\n')

    print('=== end converting tree to program for ALL examples')


def filter_examples(examples: List[ExampleWrapper], key_set: Set[ExampleWrapper]):
    return [ex for ex in examples if ex.key in key_set]


def get_keys_in_fold_file(fname: str) -> Set[Constant]:
    key_set = set()

    with open(fname, 'r') as f:
        for line in f:
            split_line = line.split(':')
            key = split_line[0]
            key_set.add(ConstantBuilder.parse_constant_str(key))
    return key_set


if __name__ == '__main__':
    main_cross_validation()

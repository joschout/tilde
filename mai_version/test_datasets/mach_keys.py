import cProfile
import os

from mai_version.IO.parsing_settings.setting_parser import KeysSettingsParser
from mai_version.representation.example import InternalExampleFormat
from mai_version.run.run_keys import run_keys
from mai_version.trees.TreeBuilder import TreeBuilderType


def main():
    project_dir = '/home/joschout/Repos/tilde'

    dataset_name = 'mach'
    data_dir = os.path.join(project_dir, 'ACE-examples-data', dataset_name)

    keys_or_examples = 'keys'

    file_name_settings = os.path.join(data_dir, keys_or_examples, dataset_name + '.s')
    file_name_background = os.path.join(data_dir, keys_or_examples, dataset_name + '.bg')
    file_name_labeled_examples = os.path.join(data_dir, keys_or_examples, dataset_name + '.kb')

    use_clausedb = True
    use_mle = False

    debug_printing_example_parsing = False
    debug_printing_tree_building = False
    debug_printing_tree_pruning = False
    debug_printing_program_conversion = False
    debug_printing_get_classifier = False
    debug_printing_classification = True

    parsed_settings = KeysSettingsParser().parse(file_name_settings)

    treebuilder_type = TreeBuilderType.DETERMINISTIC

    # background_knowledge = parse_background_knowledge(file_name_background)

    if use_clausedb:
        internal_ex_format = InternalExampleFormat.CLAUSEDB
    else:
        internal_ex_format = InternalExampleFormat.SIMPLEPROGRAM

    run_keys(file_name_labeled_examples, parsed_settings, internal_ex_format, treebuilder_type,
             fname_background_knowledge=file_name_background,
             debug_printing_example_parsing=debug_printing_example_parsing,
             debug_printing_tree_building=debug_printing_tree_building,
             debug_printing_tree_pruning=debug_printing_tree_pruning,
             debug_printing_program_conversion=debug_printing_program_conversion,
             debug_printing_get_classifier=debug_printing_get_classifier,
             debug_printing_classification=debug_printing_classification
             )

if __name__ == '__main__':
    # cProfile.run('main()', 'mach_keys.cprofilestats')
    main()

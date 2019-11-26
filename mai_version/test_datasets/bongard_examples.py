import os

from mai_version.IO.parsing_settings.setting_parser import ModelsSettingsParser
from mai_version.representation.example import InternalExampleFormat
from mai_version.run.run_models import run_models
from mai_version.trees.TreeBuilder import TreeBuilderType


project_dir = '/home/joschout/Repos/tilde'

dataset_name = 'bongard'
data_dir = os.path.join(project_dir, 'ACE-examples-data', dataset_name)

file_name_settings = os.path.join(data_dir, 'examples', dataset_name + '.s')
file_name_labeled_examples = os.path.join(data_dir, 'examples', dataset_name + '.kb')

use_clausedb = True
debug_printing = True

debug_printing_example_parsing=False
debug_printing_tree_building = False
debug_printing_tree_pruning = False
debug_printing_program_conversion = False
debug_printing_get_classifier = False
debug_printing_classification = True

parsed_settings = ModelsSettingsParser().parse(file_name_settings)

treebuilder_type = TreeBuilderType.DETERMINISTIC


if use_clausedb:
    internal_ex_format = InternalExampleFormat.CLAUSEDB
else:
    internal_ex_format = InternalExampleFormat.SIMPLEPROGRAM

run_models(file_name_labeled_examples, parsed_settings, internal_ex_format, treebuilder_type,
           debug_printing_example_parsing=debug_printing_example_parsing,
           debug_printing_tree_building=debug_printing_tree_building,
           debug_printing_tree_pruning=debug_printing_tree_pruning,
           debug_printing_program_conversion=debug_printing_program_conversion,
           debug_printing_get_classifier=debug_printing_get_classifier,
           debug_printing_classification=debug_printing_classification
           )

import os

from mai_version.IO.parsing_settings.setting_parser import KeysSettingsParser

from mai_version.representation.example import InternalExampleFormat
from mai_version.run.run_keys import run_keys
from mai_version.trees.TreeBuilder import TreeBuilderType
from mai_version.trees.stop_criterion import StopCriterionMinimalCoverage

project_dir = '/home/joschout/Repos/tilde'

data_dir = os.path.join(project_dir, 'ACE-examples-data/muta')
dataset_name = 'muta'

file_name_labeled_examples = os.path.join(data_dir, dataset_name + ".kb")
file_name_settings = os.path.join(data_dir, dataset_name + ".s")
file_name_background = os.path.join(data_dir, dataset_name + ".bg")

debug_printing_example_parsing = True
debug_printing_tree_building = True
debug_printing_tree_pruning = True
debug_printing_program_conversion = True
debug_printing_get_classifier = True
debug_printing_classification = True

parsed_settings = KeysSettingsParser().parse(file_name_settings)

treebuilder_type = TreeBuilderType.MLEDETERMINISTIC

internal_ex_format = InternalExampleFormat.CLAUSEDB

run_keys(file_name_labeled_examples, parsed_settings, internal_ex_format, treebuilder_type,
         fname_background_knowledge=file_name_background,
         stop_criterion_handler=StopCriterionMinimalCoverage(4),
         debug_printing_example_parsing=debug_printing_example_parsing,
         debug_printing_tree_building=debug_printing_tree_building,
         debug_printing_tree_pruning=debug_printing_tree_pruning,
         debug_printing_program_conversion=debug_printing_program_conversion,
         debug_printing_get_classifier=debug_printing_get_classifier,
         debug_printing_classification=debug_printing_classification
         )

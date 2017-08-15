from tilde.IO.parsing_settings.setting_parser import KeysSettingsParser

from tilde.representation.example import InternalExampleFormat
from tilde.run.run_keys import run_keys
from tilde.trees.TreeBuilder import TreeBuilderType
from tilde.trees.stop_criterion import StopCriterionMinimalCoverage

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\muta\\muta.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\muta\\muta.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\muta\\muta.bg'


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

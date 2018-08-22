from mai_version.IO.parsing_settings.setting_parser import ModelsSettingsParser
from mai_version.representation.example import InternalExampleFormat
from mai_version.run.run_models import run_models
from mai_version.trees.TreeBuilder import TreeBuilderType

file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.bg'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.kb'


use_clausedb = True
use_mle = True

debug_printing_example_parsing = False
debug_printing_tree_building = False
debug_printing_tree_pruning = False
debug_printing_program_conversion = False
debug_printing_get_classifier = False
debug_printing_classification = True

parsed_settings = ModelsSettingsParser().parse(file_name_settings)

if use_mle:
    treebuilder_type = TreeBuilderType.MLEDETERMINISTIC
else:
    treebuilder_type = TreeBuilderType.DETERMINISTIC

if use_clausedb:
    internal_ex_format = InternalExampleFormat.CLAUSEDB
else:
    internal_ex_format = InternalExampleFormat.SIMPLEPROGRAM

run_models(file_name_labeled_examples, parsed_settings, internal_ex_format, treebuilder_type,
           fname_background_knowledge=file_name_background,
           debug_printing_example_parsing=debug_printing_example_parsing,
           debug_printing_tree_building=debug_printing_tree_building,
           debug_printing_tree_pruning=debug_printing_tree_pruning,
           debug_printing_program_conversion=debug_printing_program_conversion,
           debug_printing_get_classifier=debug_printing_get_classifier,
           debug_printing_classification=debug_printing_classification
           )

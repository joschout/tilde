from tilde.IO.parsing_settings.setting_parser import ModelsSettingsParser
from tilde.representation.example import InternalExampleFormat
from tilde.run.run_models import run_models
from tilde.trees.TreeBuilder import TreeBuilderType

file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\bongard\\examples\\bongard.s'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\bongard\\examples\\bongard.kb'


use_clausedb = True
debug_printing = True

parsed_settings = ModelsSettingsParser().parse(file_name_settings)

treebuilder_type = TreeBuilderType.DETERMINISTIC


if use_clausedb:
    internal_ex_format = InternalExampleFormat.CLAUSEDB
else:
    internal_ex_format = InternalExampleFormat.SIMPLEPROGRAM

run_models(file_name_labeled_examples, parsed_settings, internal_ex_format, treebuilder_type, debug_printing=debug_printing)

from tilde.IO.parsing_settings.setting_parser import KeysSettingsParser

from tilde.representation.example import InternalExampleFormat
from tilde.run.run_keys import run_keys
from tilde.trees.TreeBuilder import TreeBuilderType

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\muta\\muta.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\muta\\muta.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\muta\\muta.bg'


debug_printing = True
use_mle = True

parsed_settings = KeysSettingsParser().parse(file_name_settings)

treebuilder_type = TreeBuilderType.DETERMINISTIC

internal_ex_format = InternalExampleFormat.CLAUSEDB

run_keys(file_name_labeled_examples, parsed_settings, internal_ex_format, treebuilder_type, fname_background_knowledge=file_name_background, debug_printing=debug_printing)


from tilde.IO.parsing_settings import ModelsSettingsParser
from tilde.representation.example import InternalExampleFormat
from tilde.run.run_models import run_models
from tilde.trees.TreeBuilder import TreeBuilderType

file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.bg'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.kb'


use_clausedb = False
debug_printing = True
use_mle = True

parsed_settings = ModelsSettingsParser().parse(file_name_settings)

if use_mle:
    treebuilder_type = TreeBuilderType.MLEDETERMINISTIC
else:
    treebuilder_type = TreeBuilderType.DETERMINISTIC

if use_clausedb:
    internal_ex_format = InternalExampleFormat.CLAUSEDB
else:
    internal_ex_format = InternalExampleFormat.SIMPLEPROGRAM

run_models(file_name_labeled_examples, parsed_settings, internal_ex_format, treebuilder_type, file_name_background, debug_printing=debug_printing)

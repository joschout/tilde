from problog.program import SimpleProgram

from IO.parsing_examples import parse_examples_model_format
from IO.parsing_settings import SettingParser
from classification.classification_helper import do_labeled_examples_get_correctly_classified_models
from trees.TreeBuilder import TreeBuilder
from trees.tree_converter import convert_tree_to_simple_program

settings_file_path = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\bongard\\examples\\bongard.s'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\bongard\\examples\\bongard.kb'

# === DEFINING TEST ====
setting_parser = SettingParser.get_models_settings_parser()
setting_parser.parse(settings_file_path)
settings = setting_parser.settings
language = settings.language
possible_targets = settings.possible_labels

background_knw = SimpleProgram()
test_examples = parse_examples_model_format(file_name_labeled_examples, possible_targets)

tree_builder = TreeBuilder(language, background_knw, possible_targets)

tree_builder.debug_printing(True)
tree_builder.build_tree(test_examples)
tree = tree_builder.get_tree()
print(tree)


program = convert_tree_to_simple_program(tree, language, debug_printing=True)
print(program)

do_labeled_examples_get_correctly_classified_models(test_examples, program, possible_targets, background_knw)

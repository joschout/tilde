from classification.classification_helper import do_labeled_examples_get_correctly_classified_models
from trees.TreeBuilder import TreeBuilder
from IO.parsing_background_knowledge import parse_background_knowledge
from IO.parsing_examples import parse_examples_model_format
from IO.parsing_settings import SettingParser
from trees.tree_converter import convert_tree_to_simple_program

import cProfile, pstats, io


settings_file_path = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.bg'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.kb'

# === DEFINING TEST ====
setting_parser = SettingParser.get_models_settings_parser()
setting_parser.parse(settings_file_path)
settings = setting_parser.settings
language = settings.language
possible_targets = settings.possible_labels

# background_knw = background_knowledge
background_knw = parse_background_knowledge(file_name_background)

test_examples = parse_examples_model_format(file_name_labeled_examples, possible_targets)

# ======================

# tree_builder = TreeBuilder(language_machines, background_knw, possible_targets)
tree_builder = TreeBuilder(language, background_knw, possible_targets)

tree_builder.debug_printing(True)

pr = cProfile.Profile()
pr.enable()
# ... do something ...
tree_builder.build_tree(test_examples)
pr.disable()
tree = tree_builder.get_tree()
print(tree)


program = convert_tree_to_simple_program(tree, language, debug_printing=True)
print(program)

do_labeled_examples_get_correctly_classified_models(test_examples, program, possible_targets, background_knw)



s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
from classification import get_label_single_example
from mach_tests.mach_definitions_TILDE_paper import language_machines,  possible_targets, labeled_examples, background_knowledge
from trees.TreeBuilder import TreeBuilder
from IO.parsing_background_knowledge import parse_background_knowledge
from IO.parsing_examples import parse_examples_model_format
from IO.parsing_settings import SettingParser
from trees.tree_converter import convert_tree_to_simple_program


settings_file_path = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.bg'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.kb'

# === DEFINING TEST ====
setting_parser = SettingParser()
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
tree_builder.build_tree(test_examples)
tree = tree_builder.get_tree()
print(tree)


program = convert_tree_to_simple_program(tree, language, debug_printing=True)
print(program)
for example in test_examples:
    true_label = example.label
    found_label = get_label_single_example(example, program, possible_targets, background_knw)[0]
    label_is_correct = ( true_label == found_label)
    if label_is_correct:
        pass
        # output = 'correct\treal label: ' + str(true_label) + '\tfound label: ' + str(found_label)
        # print(output)
    else:
        output = 'incorrect\n\treal label: ' + str(true_label) + '\n\tfound label: ' + str(found_label)
        print(output)
        print('\tincorrectly labeled example:')
        for statement in example:
            print('\t\t'+str(statement))
        get_label_single_example(example, program, possible_targets, background_knw, debug_printing=True)
        print('----------------')

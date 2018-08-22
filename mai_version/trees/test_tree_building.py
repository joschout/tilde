from mai_version.probeersel.mach_tests.mach_definitions_TILDE_paper import labeled_examples, background_knowledge, possible_targets, \
    language_machines
from mai_version.probeersel.mach_tests.mach_definitions_examples_ACE import ex1
from mai_version.trees.tree_converter import convert_tree_to_simple_program

from mai_version.classification.classification import get_labels_single_example_models
from mai_version.probeersel.mach_tests.mach_definitions_logic import sendback, fix, ok
from mai_version.trees.TreeBuilder import TreeBuilder

PRINTOUT = False


tree_builder = TreeBuilder(language_machines, background_knowledge, possible_targets)
tree_builder.debug_printing(True)

tree_builder.build_tree(labeled_examples)
tree = tree_builder.get_tree()
print(str(tree))


program = convert_tree_to_simple_program(tree, language_machines, debug_printing=True)

labels_ex1 = get_labels_single_example_models(ex1, program, [sendback, fix, ok], debug_printing=True)
print(labels_ex1)

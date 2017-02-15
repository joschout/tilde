from problog.program import SimpleProgram

from mach_tests.mach_definitions_logic import sendback, fix, ok
from mach_tests.mach_definitions_TILDE_paper import examples, background_knowledge, possible_targets, language_machines
from trees.TreeNode import PredicateGenerator, decision_tree_to_simple_program2
from trees.tree_building import TreeBuilder

tree_builder = TreeBuilder(language_machines, background_knowledge, possible_targets)

tree_builder.build_tree(examples)
tree = tree_builder.get_tree()
print(tree)

predicate_generator = PredicateGenerator(language_machines)
predicate_gen = predicate_generator.get_new_predicate_name()


program = SimpleProgram()
decision_tree_to_simple_program2(tree, program, predicate_gen)


from mach_tests.mach_definitions_examples_ACE import ex1

from classification import get_label_single_example

labels_ex1 = get_label_single_example(ex1, program, [sendback, fix, ok])
print(labels_ex1)

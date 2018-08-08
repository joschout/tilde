import time

from problog.engine import DefaultEngine

from refactor.tilde_essentials.example import Example
from refactor.tilde_essentials.leaf_strategy import LeafBuilder
from refactor.tilde_essentials.stop_criterion import StopCriterion
from refactor.tilde_essentials.tree import DecisionTree
from refactor.tilde_essentials.tree_builder import TreeBuilder
from refactor.tilde_on_django.clause_handling import build_clause, destruct_tree_tests
from refactor.tilde_on_django.evaluation import DjangoQueryEvaluator
from refactor.tilde_on_django.splitter import DjangoSplitter
from refactor.tilde_on_django.test_generation import DjangoTestGeneratorBuilder
from tilde.IO.label_collector import LabelCollectorMapper
from tilde.IO.parsing_background_knowledge import parse_background_knowledge_keys
from tilde.IO.parsing_examples import KeysExampleBuilder
from tilde.IO.parsing_settings.setting_parser import KeysSettingsParser
from tilde.representation.example import InternalExampleFormat

file_name_labeled_examples = '/home/joschout/Documents/tilde_data/ACE-examples-data/ace/bongard/keys/bongard.kb'
file_name_settings = '/home/joschout/Documents/tilde_data/ACE-examples-data/ace/bongard/keys/bongard.s'

parsed_settings = KeysSettingsParser().parse(file_name_settings)

debug_printing_example_parsing = False
debug_printing_tree_building = False
debug_printing_tree_pruning = False
debug_printing_program_conversion = True
debug_printing_get_classifier = False
debug_printing_classification = False
fname_background_knowledge = None

internal_ex_format = InternalExampleFormat.CLAUSEDB


engine = DefaultEngine()
engine.unknown = 1

language = parsed_settings.language  # type: TypeModeLanguage

# TODO: unify this with models --> let models use a prediction goal predicate label()
prediction_goal_handler = parsed_settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

print('=== START parsing background ===')
background_knowledge_wrapper \
    = parse_background_knowledge_keys(fname_background_knowledge,
                                      prediction_goal)  # type: BackgroundKnowledgeWrapper

full_background_knowledge_sp \
    = background_knowledge_wrapper.get_full_background_knowledge_simple_program()  # type: Optional[SimpleProgram]
print('=== END parsing background ===\n')
# =================================================================================================================
print('=== START parsing examples ===')
# EXAMPLES
example_builder = KeysExampleBuilder(prediction_goal, debug_printing_example_parsing)
training_examples_collection = example_builder.parse(internal_ex_format, file_name_labeled_examples,
                                                     full_background_knowledge_sp)  # type: ExampleCollection

# =================================================================================================================

print('=== START collecting labels ===')
# LABELS
index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
label_collector = LabelCollectorMapper.get_label_collector(internal_ex_format, prediction_goal, index_of_label_var,
                                                           engine=engine)
label_collector.extract_labels(training_examples_collection)

possible_labels = label_collector.get_labels()  # type: Set[Label]
possible_labels = list(possible_labels)
print('=== END collecting labels ===\n')

# =================================================================================================================

examples = []
for ex_wr_sp in training_examples_collection.get_example_wrappers_sp():
    example_clause = build_clause(ex_wr_sp)
    example = Example(data=example_clause, label=ex_wr_sp.label)
    example.classification_term = ex_wr_sp.classification_term
    examples.append(example)

# =================================================================================================================


print('=== START tree building ===')

# test_evaluator = SimpleProgramQueryEvaluator(engine=engine)
# splitter = ProblogSplitter(language=language,split_criterion_str='entropy', test_evaluator=test_evaluator,
#                            query_head_if_keys_format=prediction_goal)
test_evaluator = DjangoQueryEvaluator()
test_generator_builder = DjangoTestGeneratorBuilder(language=language,
                                                    query_head_if_keys_format=prediction_goal)

splitter = DjangoSplitter(split_criterion_str='entropy', test_evaluator=test_evaluator,
                          test_generator_builder=test_generator_builder)
leaf_builder = LeafBuilder()
stop_criterion = StopCriterion()
tree_builder = TreeBuilder(splitter=splitter, leaf_builder=leaf_builder, stop_criterion=stop_criterion)
decision_tree = DecisionTree()

start_time = time.time()
decision_tree.fit(examples=examples, tree_builder=tree_builder)
end_time = time.time()
run_time_sec = end_time - start_time
run_time_ms = 1000.0 * run_time_sec
print("run time (ms):", run_time_ms)

print('=== END tree building ===\n')

print(decision_tree)


print("=== start destructing examples ===")
for instance in examples:
    instance.data.destruct()
print("=== end destructing examples ===")

print("=== start destructing tree queries ===")
destruct_tree_tests(decision_tree.tree)
print("=== start destructing tree queries ===")

# =================================================================================================================
#
# if debug_printing_tree_pruning:
#     print("UNPRUNED tree:")
#     print("--------------")
#     print(tree)
#     nb_of_nodes = tree.get_nb_of_nodes()
#     nb_inner_nodes = tree.get_nb_of_inner_nodes()
#     print("nb of nodes in unpruned tree: " + str(nb_of_nodes))
#     print("\tinner nodes: " + str(nb_inner_nodes))
#     print("\tleaf nodes: " + str(nb_of_nodes - nb_inner_nodes))
#
# prune_leaf_nodes_with_same_label(tree)
# if debug_printing_tree_pruning:
#     print("PRUNED tree:")
#     print("------------")
# print(tree)
# nb_of_nodes = tree.get_nb_of_nodes()
# nb_inner_nodes = tree.get_nb_of_inner_nodes()
# print("nb of nodes in unpruned tree: " + str(nb_of_nodes))
# print("\tinner nodes: " + str(nb_inner_nodes))
# print("\tleaf nodes: " + str(nb_of_nodes - nb_inner_nodes))
# # =================================================================================================================
#
# tree_to_program_converter = TreeToProgramConverterMapper.get_converter(treebuilder_type, kb_format,
#                                                                        debug_printing=debug_printing_program_conversion,
#                                                                        prediction_goal=prediction_goal,
#                                                                        index=index_of_label_var)
# program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)
#
# print("%resulting program:")
# print("%------------------")
# for statement in program:
#     print(str(statement) + ".")


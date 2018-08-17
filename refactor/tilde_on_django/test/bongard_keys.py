import statistics
import time

from problog.engine import DefaultEngine

from refactor.back_end_picking import get_back_end_default, QueryBackEnd
from refactor.tilde_essentials.tree import DecisionTree
from refactor.tilde_essentials.tree_builder import TreeBuilder
from refactor.tilde_on_django.clause_handling import destruct_tree_tests
from tilde.IO.label_collector import LabelCollectorMapper
from tilde.IO.parsing_background_knowledge import parse_background_knowledge_keys
from tilde.IO.parsing_examples import KeysExampleBuilder
from tilde.IO.parsing_settings.setting_parser import KeysSettingsParser
from tilde.representation.example import InternalExampleFormat
from tilde_config import kb_file, s_file

default_handler = get_back_end_default(QueryBackEnd.DJANGO)

file_name_labeled_examples = kb_file()
file_name_settings = s_file()

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

examples = default_handler.get_transformed_example_list(training_examples_collection)

# =================================================================================================================

run_time_list = []

for i in range(0, 10):
    print('=== START tree building ===')

    # test_evaluator = SimpleProgramQueryEvaluator(engine=engine)
    # splitter = ProblogSplitter(language=language,split_criterion_str='entropy', test_evaluator=test_evaluator,
    #                            query_head_if_keys_format=prediction_goal)
    tree_builder = default_handler.get_default_decision_tree_builder(language, prediction_goal)  # type: TreeBuilder
    decision_tree = DecisionTree()
    start_time = time.time()
    decision_tree.fit(examples=examples, tree_builder=tree_builder)
    end_time = time.time()
    run_time_sec = end_time - start_time
    run_time_ms = 1000.0 * run_time_sec
    run_time_list.append(run_time_ms)
    print("run time (ms):", run_time_ms)

    print('=== END tree building ===\n')

average_run_time_ms = statistics.mean(run_time_list)
print("average tree build time (ms):", average_run_time_ms)
print(decision_tree)


print("=== start destructing examples ===")
for instance in examples:
    instance.data.destruct()
print("=== end destructing examples ===")

print("=== start destructing tree queries ===")
destruct_tree_tests(decision_tree.tree)
print("=== start destructing tree queries ===")

import time

from refactor.tilde_essentials.example import Example
from refactor.tilde_essentials.tree import DecisionTree
from refactor.query_testing_back_end.problog.defaults import get_default_decision_tree_builder
from mai_version.IO.label_collector import LabelCollectorMapper
from mai_version.IO.parsing_background_knowledge import parse_background_knowledge_keys
from mai_version.IO.parsing_examples import KeysExampleBuilder
from mai_version.IO.parsing_settings.setting_parser import KeysSettingsParser
from mai_version.representation.example import InternalExampleFormat
from tilde_config import kb_file, s_file

from problog.engine import DefaultEngine

file_name_labeled_examples = kb_file()
file_name_settings = s_file()

engine = DefaultEngine
engine.unknown = 1

parsed_settings = KeysSettingsParser().parse(file_name_settings)

debug_printing_example_parsing = False
debug_printing_tree_building = False
debug_printing_tree_pruning = False
debug_printing_program_conversion = True
debug_printing_get_classifier = False
debug_printing_classification = False
fname_background_knowledge = None

internal_ex_format = InternalExampleFormat.CLAUSEDB

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
    example = Example(data=ex_wr_sp.logic_program, label=ex_wr_sp.label)
    example.classification_term = ex_wr_sp.classification_term
    examples.append(example)

# =================================================================================================================


print('=== START tree building ===')

tree_builder = get_default_decision_tree_builder(language, prediction_goal)
decision_tree = DecisionTree()


start_time = time.time()
decision_tree.fit(examples=examples, tree_builder=tree_builder)
end_time = time.time()
run_time_sec = end_time - start_time
run_time_ms = 1000.0 * run_time_sec
print("run time (ms):", run_time_ms)


print('=== END tree building ===\n')


print(decision_tree)

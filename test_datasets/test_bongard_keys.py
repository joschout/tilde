from problog.program import SimpleProgram

from IO.label_collector import LabelCollector, SimpleProgramLabelCollector
from IO.parsing_examples import parse_examples_key_format_with_key
from IO.parsing_settings import Settings, SettingParser, KeysPredictionGoalHandler

from problog.logic import *

from classification.classification_helper import do_labeled_examples_get_correctly_classified_keys
from classification.example_partitioning import SimpleProgramExamplePartitioner
from representation.example import SimpleProgramExample
from representation.language import TypeModeLanguage
from trees.TreeBuilder import TreeBuilder
from trees.tree_converter import KeyTreeToProgramConverter

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\bongard\\keys\\bongard.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\bongard\\keys\\bongard.s'

setting_parser = SettingParser.get_key_settings_parser()  # type: SettingParser
setting_parser.parse(file_name_settings)
settings = setting_parser.settings  # type: Settings
prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

language = settings.language  # type: TypeModeLanguage


examples = parse_examples_key_format_with_key(file_name_labeled_examples)  # type: List[SimpleProgramExample]

# === getting the labels ===
index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
label_collector = SimpleProgramLabelCollector(prediction_goal, index_of_label_var)
label_collector.extract_labels(examples)
possible_labels = label_collector.get_labels()
# =================================

tree_builder = TreeBuilder(language, possible_labels, SimpleProgramExamplePartitioner())
tree_builder.debug_printing(True)
tree_builder.build_tree(examples, prediction_goal)

tree = tree_builder.get_tree()
print(tree)


treeToProgramConverter = KeyTreeToProgramConverter(prediction_goal, index_of_label_var, debug_printing=True)
program = treeToProgramConverter.convert_tree_to_simple_program(tree, language)
print(program)
#do_labeled_examples_get_correctly_classified_keys(examples, program, prediction_goal, index_of_label_var, possible_labels, background_knw)

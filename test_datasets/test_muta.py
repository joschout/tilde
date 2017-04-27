from problog.logic import Term

from IO.label_collector import LabelCollector
from IO.parsing_background_knowledge import parse_background_knowledge
from IO.parsing_examples import parse_examples_key_format_with_key
from IO.parsing_settings import Settings, SettingParser, KeysPredictionGoalHandler
from classification.classification_helper import do_labeled_examples_get_correctly_classified_keys, get_example_databases
from representation.language import TypeModeLanguage
from trees.TreeBuilder import TreeBuilder
from trees.pruning import prune_leaf_nodes_with_same_label
from trees.stop_criterion import StopCriterionMinimalCoverage
from trees.tree_converter import KeyTreeToProgramConverter

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\muta\\muta.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\muta\\muta.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\muta\\muta.bg'

# def test():
#     test_str = 'predict(machine(+machine,-action)).'
#     test = PrologString(test_str)
#     engine = DefaultEngine()
#     db = engine.prepare(test)
#     goals_to_predict = engine.query(db, Term('predict', None))
#     print(goals_to_predict)
#     print(test)
#
#
# def test_keys_settings_parser():
#     setting_parser = SettingParser.get_key_settings_parser()
#     setting_parser.parse(file_name_settings)
#     print(setting_parser)
#
#
# def test_background_knowledge():
#     background_knowledge = PrologFile(file_name_background)
#     for statement in background_knowledge:
#         print(statement)
#
#
# def test_get_all_class_labels():
#     setting_parser = SettingParser.get_key_settings_parser()
#     setting_parser.parse(file_name_settings)
#
#     examples = parse_examples_key_format_with_key(file_name_labeled_examples)
#     print(examples)
#
#
# if __name__ == "__main__":
#     test_get_all_class_labels()


setting_parser = SettingParser.get_key_settings_parser()  # type: SettingParser
setting_parser.parse(file_name_settings)
settings = setting_parser.settings  # type: Settings
prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

language = settings.language  # type: TypeModeLanguage

background_knw = parse_background_knowledge(file_name_background)

examples = parse_examples_key_format_with_key(file_name_labeled_examples)

example_dbs = get_example_databases(examples, background_knw)

# === getting the labels ===
index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
label_collector = LabelCollector(prediction_goal, index_of_label_var, background_knw)
label_collector.extract_labels_dbs(example_dbs)
possible_labels = label_collector.get_labels()
# =================================

tree_builder = TreeBuilder(language, background_knw, possible_labels, StopCriterionMinimalCoverage(4))
tree_builder.debug_printing(True)
tree_builder.build_tree(example_dbs, prediction_goal)

tree = tree_builder.get_tree()
print(tree.to_string2())

prune_leaf_nodes_with_same_label(tree)
print(tree.to_string2())

treeToProgramConverter = KeyTreeToProgramConverter(prediction_goal, index_of_label_var, debug_printing=True)
program = treeToProgramConverter.convert_tree_to_simple_program(tree, language)
print(program)

# do_labeled_examples_get_correctly_classified_keys(examples, program, prediction_goal, index_of_label_var, possible_labels, background_knw)


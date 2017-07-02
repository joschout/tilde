from problog.logic import Term

from IO.label_collector import LabelCollector
from IO.parsing_background_knowledge import parse_background_knowledge
from IO.parsing_examples import parse_examples_key_format_with_key
from IO.parsing_settings import Settings, SettingParser, KeysPredictionGoalHandler
from IO.utils import KnowledgeBaseFormat
from classification.classification_helper import get_example_databases
from representation.language import TypeModeLanguage
from trees.TreeBuilder import TreeBuilder, DeterministicTreeBuilder
from trees.pruning import prune_leaf_nodes_with_same_label
from trees.stop_criterion import StopCriterionMinimalCoverage
from trees.tree_converter import KeyTreeToProgramConverter, DeterministicTreeToProgramConverter


def run_keys(file_name_labeled_examples, file_name_settings, file_name_background, use_SimpleProgram=False):

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

    tree_builder = DeterministicTreeBuilder(language, background_knw, possible_labels, StopCriterionMinimalCoverage(4))
    tree_builder.debug_printing(True)
    tree_builder.build_tree(example_dbs, prediction_goal)

    tree = tree_builder.get_tree()
    print(tree.to_string())

    prune_leaf_nodes_with_same_label(tree)
    print(tree.to_string())

    treeToProgramConverter = DeterministicTreeToProgramConverter(KnowledgeBaseFormat.KEYS, prediction_goal, index_of_label_var, debug_printing=True)
    program = treeToProgramConverter.convert_tree_to_simple_program(tree, language)
    print(program)
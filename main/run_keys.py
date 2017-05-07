from typing import List, Set, Optional

from problog.logic import Term
from problog.program import PrologFile

from IO.label_collector import ClauseDBLabelCollector, SimpleProgramLabelCollector
from IO.parsing_background_knowledge import parse_background_knowledge
from IO.parsing_examples import parse_examples_key_format_with_key
from IO.parsing_settings import Settings, SettingParser, KeysPredictionGoalHandler
from classification.classification_helper import do_labeled_examples_get_correctly_classified_keys, \
    get_example_databases, Label
from classification.example_partitioning import ClauseDBExamplePartitioner, SimpleProgramExamplePartitioner
from representation.example import SimpleProgramExample, ClauseDBExample
from representation.language import TypeModeLanguage
from trees.TreeBuilder import TreeBuilder
from trees.pruning import prune_leaf_nodes_with_same_label
from trees.stop_criterion import StopCriterionMinimalCoverage
from trees.tree_converter import KeyTreeToProgramConverter


def run_keys_clausedb(fname_labeled_examples: str, fname_settings: str, fname_background_knowledge:Optional[str]=None):

    # SETTINGS for KEYS formatted examples
    settings = SettingParser.get_settings_keys_format(fname_settings)  # type: Settings
    prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
    prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

    language = settings.language  # type: TypeModeLanguage

    # BACKGROUND KNOWLEDGE
    if fname_background_knowledge is not None:
        background_knw = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
    else:
        background_knw = None

    # EXAMPLES
    examples = parse_examples_key_format_with_key(fname_labeled_examples)  # type: List[SimpleProgramExample]
    example_dbs = get_example_databases(examples, background_knw)  # type: List[ClauseDBExample]

    # LABELS
    index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
    label_collector = ClauseDBLabelCollector(prediction_goal, index_of_label_var, background_knw)
    label_collector.extract_labels(example_dbs)
    possible_labels = label_collector.get_labels()  # type: Set[Label]
    # =================================

    tree_builder = TreeBuilder(language, list(possible_labels), ClauseDBExamplePartitioner(),
                               StopCriterionMinimalCoverage(4))
    tree_builder.debug_printing(True)
    tree_builder.build_tree(example_dbs, prediction_goal)

    tree = tree_builder.get_tree()
    print(tree.to_string2())

    prune_leaf_nodes_with_same_label(tree)
    print(tree.to_string2())

    tree_to_program_converter = KeyTreeToProgramConverter(prediction_goal, index_of_label_var, debug_printing=True)
    program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)
    print(program)

    # do_labeled_examples_get_correctly_classified_keys(examples, program, prediction_goal, index_of_label_var, possible_labels, background_knw)


def run_keys_simpleprogram(fname_labeled_examples: str, fname_settings: str, fname_background_knowledge:Optional[str]=None):

    # SETTINGS
    settings = SettingParser.get_settings_keys_format(fname_settings)  # type: Settings
    prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
    prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

    language = settings.language  # type: TypeModeLanguage

    # BACKGROUND KNOWLEDGE
    if fname_background_knowledge is not None:
        background_knw = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
    else:
        background_knw = None

    # EXAMPLES
    examples = parse_examples_key_format_with_key(fname_labeled_examples)  # type: List[SimpleProgramExample]

    # LABELS
    index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
    label_collector = SimpleProgramLabelCollector(prediction_goal, index_of_label_var)
    label_collector.extract_labels(examples)
    possible_labels = label_collector.get_labels()
    # =================================

    tree_builder = TreeBuilder(language, possible_labels, SimpleProgramExamplePartitioner(background_knw))
    tree_builder.debug_printing(True)
    tree_builder.build_tree(examples, prediction_goal)

    tree = tree_builder.get_tree()
    print(tree.to_string2())

    tree_to_program_converter = KeyTreeToProgramConverter(prediction_goal, index_of_label_var, debug_printing=True)
    program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)
    print(program)

    do_labeled_examples_get_correctly_classified_keys(examples, program, prediction_goal, index_of_label_var,
                                                      possible_labels, background_knw)
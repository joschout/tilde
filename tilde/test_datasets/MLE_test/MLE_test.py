from typing import Optional

from tilde.trees.tree_converter import MLETreeToProgramConverter

from tilde.IO.input_format import KnowledgeBaseFormat
from tilde.IO.parsing_settings.setting_parser import SettingParser
from tilde.IO.label_collector import SimpleProgramLabelCollector
from tilde.IO.parsing_background_knowledge import parse_background_knowledge
from tilde.IO.parsing_examples_keys_format import parse_examples_key_format_with_key
from tilde.classification.example_partitioning import SimpleProgramExamplePartitioner
from tilde.run.run_keys import run_keys_clausedb
from tilde.trees.TreeBuilder import MLEDeterministicTreeBuilder

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\MLE test\\mle_test_3preds.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\MLE test\\mle_test_3preds.s'


use_clausedb = False


def run_keys_simpleprogram_MLE(fname_labeled_examples: str, fname_settings: str, fname_background_knowledge:Optional[str]=None):

    # SETTINGS
    settings = SettingParser.get_settings_keys_format(fname_settings)  # type: Settings
    prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
    prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

    language = settings.language  # type: TypeModeLanguage

    # BACKGROUND KNOWLEDGE
    if fname_background_knowledge is not None:
        background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
    else:
        background_knowledge = None

    # EXAMPLES
    examples = parse_examples_key_format_with_key(fname_labeled_examples)  # type: List[SimpleProgramExample]

    # LABELS
    index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
    label_collector = SimpleProgramLabelCollector(prediction_goal, index_of_label_var)
    label_collector.extract_labels(examples)
    possible_labels = label_collector.get_labels()
    # =================================

    tree_builder = MLEDeterministicTreeBuilder(language, possible_labels, SimpleProgramExamplePartitioner(background_knowledge))
    tree_builder.debug_printing(True)
    tree_builder.build_tree(examples, prediction_goal)

    tree = tree_builder.get_tree()
    print(tree.to_string())

    tree_to_program_converter = MLETreeToProgramConverter(KnowledgeBaseFormat.KEYS, debug_printing=True, prediction_goal=prediction_goal, index = index_of_label_var)
    program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)

    # do_labeled_examples_get_correctly_classified_keys(examples, program, prediction_goal, index_of_label_var,
    #                                                   possible_labels, background_knowledge)


if use_clausedb:
    run_keys_clausedb(file_name_labeled_examples, file_name_settings)
else:
    run_keys_simpleprogram_MLE(file_name_labeled_examples, file_name_settings)


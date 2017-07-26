from typing import Optional, List, Set

from problog.logic import Term
from problog.program import PrologFile

from tilde.IO.input_format import KnowledgeBaseFormat
from tilde.IO.label_collector import LabelCollectorMapper
from tilde.IO.parsing_examples import ExampleFormatHandlerMapper
from tilde.IO.parsing_settings.utils import FileSettings, KeysPredictionGoalHandler
from tilde.classification.example_partitioning import PartitionerBuilder
from tilde.representation.example import InternalExampleFormat, Example, Label
from tilde.representation.language import TypeModeLanguage
from tilde.trees import TreeNode
from tilde.trees.TreeBuilder import TreeBuilderBuilder, \
    TreeBuilderType
from tilde.trees.pruning import prune_leaf_nodes_with_same_label
from tilde.trees.stop_criterion import StopCriterionMinimalCoverage
from tilde.trees.tree_converter import TreeToProgramConverterMapper


def preprocessing_examples_keys(
        fname_labeled_examples: str, settings: FileSettings, internal_ex_format: InternalExampleFormat,
        background_knowledge: Optional[PrologFile] = None,
        kb_format=KnowledgeBaseFormat.KEYS):
    prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
    prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

    # EXAMPLES
    examples_format_handler = ExampleFormatHandlerMapper().get_example_format_handler(kb_format)
    examples = examples_format_handler.parse(internal_ex_format, fname_labeled_examples,
                                             background_knowledge=background_knowledge)  # type: List[Example]

    # LABELS
    index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
    label_collector = LabelCollectorMapper.get_label_collector(internal_ex_format, prediction_goal, index_of_label_var)
    label_collector.extract_labels(examples)
    possible_labels = label_collector.get_labels()  # type: Set[Label]
    possible_labels = list(possible_labels)

    return examples, prediction_goal, index_of_label_var, possible_labels


def preprocessing_examples_models(
        fname_labeled_examples: str, settings: FileSettings, internal_ex_format: InternalExampleFormat,
        background_knowledge: Optional[PrologFile] = None,
        kb_format=KnowledgeBaseFormat.MODELS):
    # LABELS
    possible_labels = settings.possible_labels  # type: List[Label]

    # EXAMPLES
    examples_format_handler = ExampleFormatHandlerMapper().get_example_format_handler(kb_format)
    examples = examples_format_handler.parse(internal_ex_format, fname_labeled_examples, possible_labels,
                                             background_knowledge)  # type: List[Example]
    return examples


def build_tree(internal_ex_format: InternalExampleFormat,
               treebuilder_type: TreeBuilderType,
               language: TypeModeLanguage, possible_labels, examples,
               prediction_goal=None,
               background_knowledge: Optional[PrologFile] = None,
               debug_printing=False,
               ) -> TreeNode:
    example_partitioner = PartitionerBuilder().build_partitioner(internal_ex_format, background_knowledge)

    tree_builder = TreeBuilderBuilder().build_treebuilder(treebuilder_type, language, possible_labels,
                                                          example_partitioner, StopCriterionMinimalCoverage())

    tree_builder.debug_printing(debug_printing)
    tree_builder.build_tree(examples, prediction_goal)
    tree = tree_builder.get_tree()

    if debug_printing:
        print("UNPRUNED tree:")
        print(tree)

    prune_leaf_nodes_with_same_label(tree)
    if debug_printing:
        print("PRUNED tree:")
    print(tree)

    return tree


def convert_tree_to_program(kb_format: KnowledgeBaseFormat,
                            treebuilder_type: TreeBuilderType,
                            tree: TreeNode,
                            language: TypeModeLanguage,
                            debug_printing=False,
                            prediction_goal=None,
                            index_of_label_var=None):
    tree_to_program_converter = TreeToProgramConverterMapper.get_converter(treebuilder_type, kb_format,
                                                                           debug_printing=debug_printing,
                                                                           prediction_goal=prediction_goal,
                                                                           index=index_of_label_var)
    program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)

    print("%resulting program:")
    print("%------------------")
    for statement in program:
        print(str(statement) + ".")

    return program

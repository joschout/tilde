from typing import Set, Optional, List

from problog.logic import Term
from problog.program import PrologFile

from tilde.IO.input_format import KnowledgeBaseFormat
from tilde.IO.label_collector import LabelCollectorMapper
from tilde.IO.parsing_background_knowledge import parse_background_knowledge
from tilde.IO.parsing_examples import KeysExampleFormatHandler
from tilde.IO.parsing_settings import Settings, KeysPredictionGoalHandler
from tilde.classification.classification_helper import Label
from tilde.classification.example_partitioning import PartitionerBuilder
from tilde.representation.example import InternalExampleFormat, Example
from tilde.representation.language import TypeModeLanguage
from tilde.trees.TreeBuilder import TreeBuilderBuilder, \
    TreeBuilderType
from tilde.trees.pruning import prune_leaf_nodes_with_same_label
from tilde.trees.stop_criterion import StopCriterionMinimalCoverage
from tilde.trees.tree_converter import TreeToProgramConverterMapper


def run_keys(fname_labeled_examples: str, settings: Settings, internal_ex_format: InternalExampleFormat,
             treebuilder_type: TreeBuilderType,
             fname_background_knowledge:Optional[str]=None,
             debug_printing=False):

    prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
    prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

    language = settings.language  # type: TypeModeLanguage

    # BACKGROUND KNOWLEDGE
    if fname_background_knowledge is not None:
        background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
    else:
        background_knowledge = None

    # EXAMPLES
    examples_format_handler = KeysExampleFormatHandler()
    examples = examples_format_handler.parse(internal_ex_format, fname_labeled_examples,
                                             background_knowledge=background_knowledge)  # type: List[Example]

    # LABELS
    index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
    label_collector = LabelCollectorMapper.get_label_collector(internal_ex_format, prediction_goal, index_of_label_var)
    label_collector.extract_labels(examples)
    possible_labels = label_collector.get_labels()  # type: Set[Label]
    # =================================

    example_partitioner = PartitionerBuilder().build_partitioner(internal_ex_format, background_knowledge)

    tree_builder = TreeBuilderBuilder().build_treebuilder(treebuilder_type, language, list(possible_labels),
                                                          example_partitioner, StopCriterionMinimalCoverage(4))

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

    tree_to_program_converter = TreeToProgramConverterMapper.get_converter(treebuilder_type, KnowledgeBaseFormat.KEYS,
                                                                           debug_printing=debug_printing,
                                                                           prediction_goal=prediction_goal,
                                                                           index=index_of_label_var)
    program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)

    print("%resulting program:")
    print("%------------------")
    for statement in program:
        print(str(statement) + ".")

    # do_labeled_examples_get_correctly_classified_keys(examples, program, prediction_goal, index_of_label_var, possible_labels, background_knw)



# def run_keys_clausedb(fname_labeled_examples: str, settings: Settings, fname_background_knowledge:Optional[str]=None,
#                       debug_printing=False, use_mle=False):
#
#     prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
#     prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term
#
#     language = settings.language  # type: TypeModeLanguage
#
#     # BACKGROUND KNOWLEDGE
#     if fname_background_knowledge is not None:
#         background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
#     else:
#         background_knowledge = None
#
#     # EXAMPLES
#     examples = parse_examples_key_format_with_key(fname_labeled_examples)  # type: List[SimpleProgramExample]
#     example_dbs = get_example_databases(examples, background_knowledge)  # type: List[ClauseDBExample]
#
#     # LABELS
#     index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
#     label_collector = ClauseDBLabelCollector(prediction_goal, index_of_label_var, background_knowledge)
#     label_collector.extract_labels(example_dbs)
#     possible_labels = label_collector.get_labels()  # type: Set[Label]
#     # =================================
#
#     example_partitioner = PartitionerBuilder().build_partitioner(InternalExampleFormat.CLAUSEDB,
#                                                                  background_knowledge)
#
#     if use_mle:
#         tree_builder = MLEDeterministicTreeBuilder(language, list(possible_labels), example_partitioner,
#                                                 StopCriterionMinimalCoverage(4))
#     else:
#         tree_builder = DeterministicTreeBuilder(language, list(possible_labels), example_partitioner,
#                                StopCriterionMinimalCoverage(4))
#     tree_builder.debug_printing(debug_printing)
#     tree_builder.build_tree(example_dbs, prediction_goal)
#
#     tree = tree_builder.get_tree()
#
#     if debug_printing:
#         print("UNPRUNED tree:")
#         print(tree.to_string())
#
#     prune_leaf_nodes_with_same_label(tree)
#
#     if debug_printing:
#         print("PRUNED tree:")
#     print(tree.to_string())
#
#     if use_mle:
#         tree_to_program_converter = MLETreeToProgramConverter(KnowledgeBaseFormat.KEYS, debug_printing=debug_printing,
#                                                               prediction_goal=prediction_goal, index=index_of_label_var)
#     else:
#         tree_to_program_converter = DeterministicTreeToProgramConverter(KnowledgeBaseFormat.KEYS, debug_printing=debug_printing,
#                                                                         prediction_goal=prediction_goal,
#                                                                         index=index_of_label_var)
#
#     program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)
#     print("%resulting program:")
#     print("%------------------")
#     for statement in program:
#         print(str(statement) + ".")
#
#
#     # do_labeled_examples_get_correctly_classified_keys(examples, program, prediction_goal, index_of_label_var, possible_labels, background_knw)
#
#
# def run_keys_simpleprogram(fname_labeled_examples: str, settings: Settings, fname_background_knowledge:Optional[str]=None,
#                            debug_printing=False,use_mle=False):
#
#     prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
#     prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term
#
#     language = settings.language  # type: TypeModeLanguage
#
#     # BACKGROUND KNOWLEDGE
#     if fname_background_knowledge is not None:
#         background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
#     else:
#         background_knowledge = None
#
#     # EXAMPLES
#     examples = parse_examples_key_format_with_key(fname_labeled_examples)  # type: List[SimpleProgramExample]
#
#     # LABELS
#     index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
#     label_collector = SimpleProgramLabelCollector(prediction_goal, index_of_label_var)
#     label_collector.extract_labels(examples)
#     possible_labels = label_collector.get_labels()
#     # =================================
#
#     example_partitioner = PartitionerBuilder().build_partitioner(InternalExampleFormat.SIMPLEPROGRAM,
#                                                                  background_knowledge)
#
#     if use_mle:
#         tree_builder = TreeBuilderBuilder().build_treebuilder(TreeBuilderType.MLEDETERMINISTIC, language, possible_labels,
#                                                               example_partitioner)
#     else:
#         tree_builder = TreeBuilderBuilder().build_treebuilder(TreeBuilderType.DETERMINISTIC, language, possible_labels,
#                                                               example_partitioner)
#     tree_builder.debug_printing(debug_printing)
#     tree_builder.build_tree(examples, prediction_goal)
#
#     tree = tree_builder.get_tree()
#     print(tree.to_string())
#
#     if use_mle:
#         tree_to_program_converter = MLETreeToProgramConverter(KnowledgeBaseFormat.KEYS, debug_printing=debug_printing,
#                                                               prediction_goal=prediction_goal, index=index_of_label_var)
#     else:
#         tree_to_program_converter = DeterministicTreeToProgramConverter(KnowledgeBaseFormat.KEYS, debug_printing=debug_printing,
#                                                                         prediction_goal=prediction_goal,
#                                                                         index=index_of_label_var)
#     program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)
#
#     print("%resulting program:")
#     print("%------------------")
#     for statement in program:
#         print(str(statement)+ ".")
#
#     do_labeled_examples_get_correctly_classified_keys(examples, program, prediction_goal, index_of_label_var,
#                                                       possible_labels, background_knowledge)
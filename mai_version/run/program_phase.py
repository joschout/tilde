from typing import Optional, List, Set, Tuple

from problog.engine import GenericEngine
from problog.logic import Term
from problog.program import PrologFile, SimpleProgram

from mai_version.IO.input_format import KnowledgeBaseFormat
from mai_version.IO.label_collector import LabelCollectorMapper
from mai_version.IO.parsing_background_knowledge import parse_background_knowledge_keys, parse_background_knowledge_models
from mai_version.IO.parsing_examples import KeysExampleBuilder, ModelsExampleBuilder
from mai_version.IO.parsing_settings.utils import FileSettings, KeysPredictionGoalHandler
from mai_version.classification.example_partitioning import PartitionerBuilder
from mai_version.representation.background_knowledge import BackgroundKnowledgeWrapper
from mai_version.representation.example import InternalExampleFormat, Label, ExampleWrapper
from mai_version.representation.example_collection import ExampleCollection
from mai_version.representation.language import TypeModeLanguage
from mai_version.trees import TreeNode
from mai_version.trees.TreeBuilder import TreeBuilderBuilder, \
    TreeBuilderType
from mai_version.trees.pruning import prune_leaf_nodes_with_same_label
from mai_version.trees.stop_criterion import StopCriterionMinimalCoverage
from mai_version.trees.tree_converter import TreeToProgramConverterMapper


def preprocessing_examples_keys(
        fname_examples: str, settings: FileSettings, internal_ex_format: InternalExampleFormat,
        fname_background_knowledge: Optional[str] = None,
        debug_printing_example_parsing=False,
        filter_out_unlabeled_examples = False, fold_data: Optional['FoldData'] = None) \
        -> Tuple[ExampleCollection, Term, int, List[Label], BackgroundKnowledgeWrapper]:
    prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
    prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

    background_knowledge_wrapper \
        = parse_background_knowledge_keys(fname_background_knowledge,
                                          prediction_goal)  # type: BackgroundKnowledgeWrapper

    full_background_knowledge_sp \
        = background_knowledge_wrapper.get_full_background_knowledge_simple_program()  # type: Optional[SimpleProgram]

    # EXAMPLES
    example_builder = KeysExampleBuilder(prediction_goal, debug_printing_example_parsing)
    training_examples_collection = example_builder.parse(internal_ex_format, fname_examples,
                                                         full_background_knowledge_sp)  # type: ExampleCollection

    # LABELS
    index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
    label_collector = LabelCollectorMapper.get_label_collector(internal_ex_format, prediction_goal, index_of_label_var,engine=engine)

    keys_of_unlabeled_examples = label_collector.extract_labels(training_examples_collection)

    nb_of_unlabeled_examples = len(keys_of_unlabeled_examples)
    # TODO: change this back if necessary
    if filter_out_unlabeled_examples and nb_of_unlabeled_examples > 0:
        if fold_data is not None:
            fold_data.total_nb_of_examples = len(training_examples_collection.example_wrappers_sp)
        training_examples_collection = training_examples_collection.filter_examples_not_in_key_set(keys_of_unlabeled_examples)
        print("DANGEROUS: FILTERED OUT UNLABELED EXAMPLES")

    possible_labels = label_collector.get_labels()  # type: Set[Label]
    possible_labels = list(possible_labels)  # type: List[Label]

    return training_examples_collection, prediction_goal, index_of_label_var, possible_labels, background_knowledge_wrapper


def preprocessing_examples_models(
        fname_examples: str, settings: FileSettings, internal_ex_format: InternalExampleFormat,
        fname_background_knowledge: Optional[str] = None,
        debug_printing_example_parsing=False
        # background_knowledge: Optional[PrologFile] = None,
        # kb_format=KnowledgeBaseFormat.MODELS
) -> Tuple[ExampleCollection, BackgroundKnowledgeWrapper]:
    # LABELS
    possible_labels = settings.possible_labels  # type: List[Label]

    background_knowledge_wrapper \
        = parse_background_knowledge_models(fname_background_knowledge,
                                            possible_labels)  # type: BackgroundKnowledgeWrapper
    full_background_knowledge_sp \
        = background_knowledge_wrapper.get_full_background_knowledge_simple_program()  # type: Optional[SimpleProgram]

    # EXAMPLES
    example_builder = ModelsExampleBuilder(possible_labels, debug_printing_example_parsing)
    training_examples_collection = example_builder.parse(internal_ex_format, fname_examples,
                                                         full_background_knowledge_sp)  # type: ExampleCollection

    return training_examples_collection, background_knowledge_wrapper


def build_tree(internal_ex_format: InternalExampleFormat,
               treebuilder_type: TreeBuilderType,
               language: TypeModeLanguage, possible_labels,
               training_examples_collection: ExampleCollection,
               prediction_goal=None,
               full_background_knowledge_sp: Optional[PrologFile] = None,
               debug_printing_tree_building=False,
               stop_criterion_handler: Optional = StopCriterionMinimalCoverage(),
               engine:GenericEngine=None
               ) -> TreeNode:
    example_partitioner = PartitionerBuilder().build_partitioner(internal_ex_format, full_background_knowledge_sp, engine=engine)

    tree_builder = TreeBuilderBuilder().build_treebuilder(treebuilder_type, language, possible_labels,
                                                          example_partitioner, stop_criterion_handler)

    tree_builder.debug_printing(debug_printing_tree_building)
    tree_builder.build_tree(training_examples_collection.get_labeled_examples(), prediction_goal)
    tree = tree_builder.get_tree()  # type: TreeNode
    return tree


def prune_tree(tree: TreeNode, debug_printing_tree_pruning=False) -> TreeNode:
    if debug_printing_tree_pruning:
        print("UNPRUNED tree:")
        print("--------------")
        print(tree)
        nb_of_nodes = tree.get_nb_of_nodes()
        nb_inner_nodes = tree.get_nb_of_inner_nodes()
        print("nb of nodes in unpruned tree: " + str(nb_of_nodes))
        print("\tinner nodes: " + str(nb_inner_nodes))
        print("\tleaf nodes: " + str(nb_of_nodes - nb_inner_nodes))

    prune_leaf_nodes_with_same_label(tree)
    if debug_printing_tree_pruning:
        print("PRUNED tree:")
        print("-------------")
    print(tree)
    if debug_printing_tree_pruning:
        nb_of_nodes = tree.get_nb_of_nodes()
        nb_inner_nodes = tree.get_nb_of_inner_nodes()
        print("nb of nodes in unpruned tree: " + str(nb_of_nodes))
        print("\tinner nodes: " + str(nb_inner_nodes))
        print("\tleaf nodes: " + str(nb_of_nodes - nb_inner_nodes))

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

    if debug_printing:
        print("%resulting program:")
        print("%------------------")
        for statement in program:
            print(str(statement) + ".")

    return program

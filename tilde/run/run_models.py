from typing import List, Optional

from problog.program import PrologFile, SimpleProgram

from tilde.IO.input_format import KnowledgeBaseFormat
from tilde.IO.parsing_examples import ExampleFormatHandlerMapper
from tilde.IO.parsing_settings.utils import FileSettings
from tilde.classification.classification_helper import get_models_classifier, \
    do_labeled_examples_get_correctly_classified

from tilde.classification.example_partitioning import PartitionerBuilder
from tilde.representation.example import Example, Label, InternalExampleFormat
from tilde.representation.language import TypeModeLanguage
from tilde.trees.TreeBuilder import TreeBuilderBuilder, TreeBuilderType
from tilde.trees.pruning import prune_leaf_nodes_with_same_label
from tilde.trees.stop_criterion import StopCriterionMinimalCoverage
from tilde.trees.tree_converter import TreeToProgramConverterMapper


def run_models(fname_labeled_examples: str, settings: FileSettings, internal_ex_format: InternalExampleFormat,
               treebuilder_type: TreeBuilderType,
               background_knowledge: Optional[PrologFile] = None,
               debug_printing=False,
               kb_format=KnowledgeBaseFormat.MODELS,
               stop_criterion_handler: Optional=StopCriterionMinimalCoverage()
               ) -> SimpleProgram:
    language = settings.language  # type: TypeModeLanguage

    # LABELS
    possible_labels = settings.possible_labels  # type: List[Label]

    # EXAMPLES
    examples_format_handler = ExampleFormatHandlerMapper().get_example_format_handler(kb_format)
    examples = examples_format_handler.parse(internal_ex_format, fname_labeled_examples, possible_labels,
                                             background_knowledge)  # type: List[Example]
    # =======================

    example_partitioner = PartitionerBuilder().build_partitioner(internal_ex_format, background_knowledge)

    tree_builder = TreeBuilderBuilder().build_treebuilder(treebuilder_type, language, possible_labels,
                                                          example_partitioner, stop_criterion_handler)

    tree_builder.debug_printing(debug_printing)
    tree_builder.build_tree(examples)
    tree = tree_builder.get_tree()

    if debug_printing:
        print("UNPRUNED tree:")
        print("--------------")
        print(tree)
        nb_of_nodes = tree.get_nb_of_nodes()
        nb_inner_nodes = tree.get_nb_of_inner_nodes()
        print("nb of nodes in unpruned tree: " + str(nb_of_nodes))
        print("\tinner nodes: " + str(nb_inner_nodes))
        print("\tleaf nodes: " + str(nb_of_nodes - nb_inner_nodes))

    prune_leaf_nodes_with_same_label(tree)
    if debug_printing:
        print("PRUNED tree:")
        print("------------")
    print(tree)
    nb_of_nodes = tree.get_nb_of_nodes()
    nb_inner_nodes = tree.get_nb_of_inner_nodes()
    print("nb of nodes in unpruned tree: " + str(nb_of_nodes))
    print("\tinner nodes: " + str(nb_inner_nodes))
    print("\tleaf nodes: " + str(nb_of_nodes - nb_inner_nodes))

    tree_to_program_converter = TreeToProgramConverterMapper.get_converter(treebuilder_type, kb_format,
                                                                           debug_printing=debug_printing,
                                                                           prediction_goal=None,
                                                                           index=None)
    program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)

    print("%resulting program:")
    print("%------------------")
    for statement in program:
        print(str(statement) + ".")

    classifier = get_models_classifier(internal_ex_format, program, possible_labels, background_knowledge, debug_printing=False)

    # TODO: THIS CAN GIVE ERRORS WHEN USING MLE

    do_labeled_examples_get_correctly_classified(classifier, examples, possible_labels, debug_printing)
    return program

from typing import List, Optional

from problog.program import PrologFile

from tilde.IO.input_format import KnowledgeBaseFormat
from tilde.IO.parsing_background_knowledge import parse_background_knowledge
from tilde.IO.parsing_examples import ModelsExampleFormatHandler
from tilde.IO.parsing_settings import Settings
from tilde.classification.classification_helper import Label, do_labeled_examples_get_correctly_classified_models
from tilde.classification.example_partitioning import PartitionerBuilder
from tilde.representation.example import Example, InternalExampleFormat
from tilde.representation.language import TypeModeLanguage
from tilde.trees.TreeBuilder import TreeBuilderBuilder, TreeBuilderType
from tilde.trees.pruning import prune_leaf_nodes_with_same_label
from tilde.trees.tree_converter import convert_tree_to_simple_program, TreeToProgramConverterMapper


def run_models(fname_labeled_examples: str, settings: Settings, internal_ex_format: InternalExampleFormat,
               treebuilder_type: TreeBuilderType,
               fname_background_knowledge: Optional[str] = None,
               debug_printing=False):
    language = settings.language  # type: TypeModeLanguage

    # LABELS
    possible_targets = settings.possible_labels  # type: List[Label]

    # BACKGROUND KNOWLEDGE
    if fname_background_knowledge is not None:
        background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
    else:
        background_knowledge = None

        # EXAMPLES
    examples_format_handler = ModelsExampleFormatHandler()
    examples = examples_format_handler.parse(internal_ex_format, fname_labeled_examples, possible_targets,
                                             background_knowledge)  # type: List[Example]
    # =======================

    example_partitioner = PartitionerBuilder().build_partitioner(internal_ex_format,
                                                                 background_knowledge)

    tree_builder = TreeBuilderBuilder().build_treebuilder(treebuilder_type, language, possible_targets,
                                                          example_partitioner)

    tree_builder.debug_printing(debug_printing)
    tree_builder.build_tree(examples)
    tree = tree_builder.get_tree()

    if debug_printing:
        print("UNPRUNED tree:")
        print(tree.to_string())

    prune_leaf_nodes_with_same_label(tree)
    if debug_printing:
        print("PRUNED tree:")
    print(tree.to_string())

    tree_to_program_converter = TreeToProgramConverterMapper.get_converter(treebuilder_type, KnowledgeBaseFormat.MODELS,
                                                                           debug_printing)
    program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)

    print("%resulting program:")
    print("%------------------")
    for statement in program:
        print(str(statement) + ".")

    #TODO: THIS CAN GIVE ERRORS
    do_labeled_examples_get_correctly_classified_models(examples_format_handler.examples, program, possible_targets,
                                                        background_knowledge)


# def run_models_simpleprogram(fname_labeled_examples: str, settings: Settings,
#                              fname_background_knowledge: Optional[str] = None,
#                              debug_printing=False, use_mle=False):
#     language = settings.language  # type: TypeModeLanguage
#
#     # LABELS
#     possible_targets = settings.possible_labels  # type: List[Label]
#
#     # BACKGROUND KNOWLEDGE
#     if fname_background_knowledge is not None:
#         background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
#     else:
#         background_knowledge = None
#
#     # EXAMPLES
#     examples_format_handler = ModelsExampleFormatHandler()
#     examples = examples_format_handler.parse(InternalExampleFormat.SIMPLEPROGRAM, fname_labeled_examples,
#                                              possible_targets, background_knowledge)  # type: List[Example]
#
#     # =======================
#
#     example_partitioner = PartitionerBuilder().build_partitioner(InternalExampleFormat.SIMPLEPROGRAM,
#                                                                  background_knowledge)
#
#     tree_builder = TreeBuilderBuilder().build_treebuilder(TreeBuilderType.DETERMINISTIC, language, possible_targets,
#                                                           example_partitioner)
#
#     tree_builder.debug_printing(debug_printing)
#     tree_builder.build_tree(examples)
#     tree = tree_builder.get_tree()
#     print(tree.to_string())
#
#     program = convert_tree_to_simple_program(tree, language, debug_printing=debug_printing)
#
#     print("%resulting program:")
#     print("%------------------")
#     for statement in program:
#         print(str(statement) + ".")
#
#     do_labeled_examples_get_correctly_classified_models(examples, program, possible_targets, background_knowledge)
#
#
# def run_models_clausedb(fname_labeled_examples: str, settings: Settings,
#                         fname_background_knowledge: Optional[str] = None,
#                         debug_printing=False, use_mle=False):
#     language = settings.language  # type: TypeModeLanguage
#
#     # LABELS
#     possible_targets = settings.possible_labels  # type: List[Label]
#
#     # BACKGROUND KNOWLEDGE
#     if fname_background_knowledge is not None:
#         background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
#     else:
#         background_knowledge = None
#
#     # EXAMPLES
#     examples_format_handler = ModelsExampleFormatHandler()
#     examples = examples_format_handler.parse(InternalExampleFormat.CLAUSEDB, fname_labeled_examples,
#                                              possible_targets, background_knowledge)  # type: List[Example]
#     # =======================
#
#     example_partitioner = PartitionerBuilder().build_partitioner(InternalExampleFormat.CLAUSEDB,
#                                                                  background_knowledge)
#
#     tree_builder = TreeBuilderBuilder().build_treebuilder(TreeBuilderType.DETERMINISTIC, language, possible_targets,
#                                                           example_partitioner)
#
#     tree_builder.debug_printing(debug_printing)
#     tree_builder.build_tree(examples)
#     tree = tree_builder.get_tree()
#
#     if debug_printing:
#         print("UNPRUNED tree:")
#         print(tree.to_string())
#
#     prune_leaf_nodes_with_same_label(tree)
#     if debug_printing:
#         print("PRUNED tree:")
#     print(tree.to_string())
#
#     program = convert_tree_to_simple_program(tree, language, debug_printing=debug_printing)
#
#     print("%resulting program:")
#     print("%------------------")
#     for statement in program:
#         print(str(statement) + ".")
#
#     do_labeled_examples_get_correctly_classified_models(examples_format_handler.examples, program, possible_targets,
#                                                         background_knowledge)

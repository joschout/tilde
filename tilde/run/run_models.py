from typing import List, Optional

from problog.program import SimpleProgram

from tilde.IO.input_format import KnowledgeBaseFormat
from tilde.IO.parsing_background_knowledge import parse_background_knowledge_models
from tilde.IO.parsing_examples import ModelsExampleBuilder
from tilde.IO.parsing_settings.utils import FileSettings
from tilde.classification.classification_helper import get_models_classifier, \
    do_labeled_examples_get_correctly_classified
from tilde.classification.example_partitioning import PartitionerBuilder
from tilde.representation.background_knowledge import BackgroundKnowledgeWrapper
from tilde.representation.example import Label, InternalExampleFormat, SimpleProgramExampleWrapper, \
    ClauseDBExampleWrapper
from tilde.representation.example_collection import ExampleCollection
from tilde.representation.language import TypeModeLanguage
from tilde.trees import TreeNode
from tilde.trees.TreeBuilder import TreeBuilderBuilder, TreeBuilderType
from tilde.trees.pruning import prune_leaf_nodes_with_same_label
from tilde.trees.stop_criterion import StopCriterionMinimalCoverage
from tilde.trees.tree_converter import TreeToProgramConverterMapper


def run_models(fname_examples: str, settings: FileSettings, internal_ex_format: InternalExampleFormat,
               treebuilder_type: TreeBuilderType,
               fname_background_knowledge: Optional[str] = None,
               kb_format=KnowledgeBaseFormat.MODELS,
               stop_criterion_handler: Optional = StopCriterionMinimalCoverage(),
               debug_printing_example_parsing=False,
               debug_printing_tree_building=False,
               debug_printing_tree_pruning=False,
               debug_printing_program_conversion=False,
               debug_printing_get_classifier=False,
               debug_printing_classification=False
               ) -> SimpleProgram:
    language = settings.language  # type: TypeModeLanguage

    # LABELS
    possible_labels = settings.possible_labels  # type: List[Label]

    print('=== START parsing background ===')
    background_knowledge_wrapper \
        = parse_background_knowledge_models(fname_background_knowledge,
                                            possible_labels)  # type: BackgroundKnowledgeWrapper
    full_background_knowledge_sp \
        = background_knowledge_wrapper.get_full_background_knowledge_simple_program()  # type: Optional[SimpleProgram]
    print('=== END parsing background ===\n')
    # =================================================================================================================
    print('=== START parsing examples ===')
    # EXAMPLES
    example_builder = ModelsExampleBuilder(possible_labels, debug_printing_example_parsing)
    training_examples_collection = example_builder.parse(internal_ex_format, fname_examples,
                                                         full_background_knowledge_sp)  # type: ExampleCollection

    print('=== END parsing examples ===\n')
    # =================================================================================================================

    print('=== START tree building ===')
    example_partitioner = PartitionerBuilder().build_partitioner(internal_ex_format, full_background_knowledge_sp)

    tree_builder = TreeBuilderBuilder().build_treebuilder(treebuilder_type, language, possible_labels,
                                                          example_partitioner, stop_criterion_handler)

    tree_builder.debug_printing(debug_printing_tree_building)
    tree_builder.build_tree(training_examples_collection.get_labeled_examples())
    tree = tree_builder.get_tree()  # type: TreeNode
    print('=== END tree building ===\n')

    # =================================================================================================================

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
        print("------------")
    print(tree)
    nb_of_nodes = tree.get_nb_of_nodes()
    nb_inner_nodes = tree.get_nb_of_inner_nodes()
    print("nb of nodes in unpruned tree: " + str(nb_of_nodes))
    print("\tinner nodes: " + str(nb_inner_nodes))
    print("\tleaf nodes: " + str(nb_of_nodes - nb_inner_nodes))
    # =================================================================================================================

    tree_to_program_converter = TreeToProgramConverterMapper.get_converter(treebuilder_type, kb_format,
                                                                           debug_printing=debug_printing_program_conversion,
                                                                           prediction_goal=None,
                                                                           index=None)
    program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)

    print("%resulting program:")
    print("%------------------")
    for statement in program:
        print(str(statement) + ".")

    # =================================================================================================================
    # TODO: THIS CAN GIVE ERRORS WHEN USING MLE
    stripped_background_knowledge = background_knowledge_wrapper.get_stripped_background_knowledge()  # type: Optional[SimpleProgram]
    print('\nbackground knowledge used in classification:\n')
    if stripped_background_knowledge is not None:
        for statement in stripped_background_knowledge:
            print(statement)
    print()

    stripped_examples_simple_program = training_examples_collection.get_labeled_example_wrappers_sp()  # type: List[SimpleProgramExampleWrapper]
    test_examples = stripped_examples_simple_program

    if internal_ex_format.CLAUSEDB:
        stripped_examples_clausedb = ClauseDBExampleWrapper.get_clause_db_examples(stripped_examples_simple_program,
                                                                                   background_knowledge=stripped_background_knowledge)
        test_examples = stripped_examples_clausedb

    classifier = get_models_classifier(internal_ex_format, program, possible_labels, stripped_background_knowledge,
                                       debug_printing=debug_printing_get_classifier)

    do_labeled_examples_get_correctly_classified(classifier, test_examples, possible_labels,
                                                 debug_printing_classification)
    return program

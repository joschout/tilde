from typing import Set, Optional, List

from problog.logic import Term
from problog.program import SimpleProgram

from tilde.IO.input_format import KnowledgeBaseFormat
from tilde.IO.label_collector import LabelCollectorMapper
from tilde.IO.parsing_background_knowledge import parse_background_knowledge_keys
from tilde.IO.parsing_examples import KeysExampleBuilder
from tilde.IO.parsing_settings.utils import FileSettings, KeysPredictionGoalHandler
from tilde.classification.classification_helper import get_keys_classifier, do_labeled_examples_get_correctly_classified
from tilde.classification.example_partitioning import PartitionerBuilder
from tilde.representation.background_knowledge import BackgroundKnowledgeWrapper
from tilde.representation.example import InternalExampleFormat, Label, ClauseDBExampleWrapper, \
    SimpleProgramExampleWrapper
from tilde.representation.example_collection import ExampleCollection
from tilde.representation.language import TypeModeLanguage
from tilde.trees import TreeNode
from tilde.trees.TreeBuilder import TreeBuilderBuilder, \
    TreeBuilderType
from tilde.trees.pruning import prune_leaf_nodes_with_same_label
from tilde.trees.stop_criterion import StopCriterionMinimalCoverage
from tilde.trees.tree_converter import TreeToProgramConverterMapper


def run_keys(fname_examples: str, settings: FileSettings, internal_ex_format: InternalExampleFormat,
             treebuilder_type: TreeBuilderType,
             fname_background_knowledge: Optional[str] = None,
             kb_format=KnowledgeBaseFormat.KEYS,
             stop_criterion_handler: Optional = StopCriterionMinimalCoverage(),
             debug_printing_example_parsing=False,
             debug_printing_tree_building=False,
             debug_printing_tree_pruning=False,
             debug_printing_program_conversion=False,
             debug_printing_get_classifier=False,
             debug_printing_classification=False
             ) -> SimpleProgram:
    language = settings.language  # type: TypeModeLanguage

    # TODO: unify this with models --> let models use a prediction goal predicate label()
    prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
    prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

    print('=== START parsing background ===')
    background_knowledge_wrapper \
        = parse_background_knowledge_keys(fname_background_knowledge,
                                          prediction_goal)  # type: BackgroundKnowledgeWrapper

    full_background_knowledge_sp \
        = background_knowledge_wrapper.get_full_background_knowledge_simple_program()  # type: Optional[SimpleProgram]
    print('=== END parsing background ===\n')
    # =================================================================================================================
    print('=== START parsing examples ===')
    # EXAMPLES
    example_builder = KeysExampleBuilder(prediction_goal, debug_printing_example_parsing)
    training_examples_collection = example_builder.parse(internal_ex_format, fname_examples,
                                                         full_background_knowledge_sp)  # type: ExampleCollection

    print('=== END parsing examples ===\n')
    # =================================================================================================================

    print('=== START collecting labels ===')
    # LABELS
    index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
    label_collector = LabelCollectorMapper.get_label_collector(internal_ex_format, prediction_goal, index_of_label_var)
    label_collector.extract_labels(training_examples_collection)

    possible_labels = label_collector.get_labels()  # type: Set[Label]
    possible_labels = list(possible_labels)
    print('=== END collecting labels ===\n')

    # =================================================================================================================

    print('=== START tree building ===')
    example_partitioner = PartitionerBuilder().build_partitioner(internal_ex_format, full_background_knowledge_sp)

    tree_builder = TreeBuilderBuilder().build_treebuilder(treebuilder_type, language, possible_labels,
                                                          example_partitioner, stop_criterion_handler)

    tree_builder.debug_printing(debug_printing_tree_building)
    tree_builder.build_tree(training_examples_collection.get_labeled_examples(), prediction_goal)
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
                                                                           prediction_goal=prediction_goal,
                                                                           index=index_of_label_var)
    program = tree_to_program_converter.convert_tree_to_simple_program(tree, language)

    print("%resulting program:")
    print("%------------------")
    for statement in program:
        print(str(statement) + ".")

    # =================================================================================================================
    # model verification
    stripped_background_knowledge = background_knowledge_wrapper.get_stripped_background_knowledge()  # type: Optional[SimpleProgram]
    print('\nbackground knowledge used in classification:\n')
    if stripped_background_knowledge is not None:
        for statement in stripped_background_knowledge:
            print(statement)
    print()

    stripped_examples_simple_program = training_examples_collection.get_labeled_example_wrappers_sp()  # type: List[SimpleProgramExampleWrapper]
    test_examples = stripped_examples_simple_program

    if internal_ex_format == InternalExampleFormat.CLAUSEDB:
        stripped_examples_clausedb = ClauseDBExampleWrapper.get_clause_db_examples(stripped_examples_simple_program,
                                                                                   background_knowledge=stripped_background_knowledge)
        test_examples = stripped_examples_clausedb

    # for the KEYS case:
    #   IF SimpleProgram:
    #               - examples_format_handler.example_wrappers_sp: Labeled
    #               - examples_format_handler.example_wrappers_sp_db == None
    #   IF ClauseDB:
    #               - examples_format_handler.example_wrappers_sp: UNLabeled
    #               - examples_format_handler.example_wrappers_sp_db == Labeled BUT CONTAIN POSSIBLY FULL BACKGROUND KNOWLEDGE
    #                   -> IF NOT bgkw contains prediction_clauses: reuse examples_db
    #                       IF DOES:
    classifier = get_keys_classifier(internal_ex_format, program, prediction_goal,
                                     index_of_label_var, stripped_background_knowledge,
                                     debug_printing=debug_printing_get_classifier)
    do_labeled_examples_get_correctly_classified(classifier, test_examples, possible_labels,
                                                 debug_printing_classification)

    return program

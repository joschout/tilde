from typing import List, Optional

from tilde.classification.classification_helper import Label, do_labeled_examples_get_correctly_classified_models, \
    get_example_databases
from problog.program import PrologFile
from tilde.representation.example import ClauseDBExample, SimpleProgramExample, Example, InternalExampleFormat
from tilde.representation.language import TypeModeLanguage
from tilde.trees.TreeBuilder import DeterministicTreeBuilder, TreeBuilderBuilder, TreeBuilderType
from tilde.trees.tree_converter import convert_tree_to_simple_program

from tilde.IO.parsing_examples_models_format import ModelsExampleParser
from tilde.IO.parsing_settings import SettingParser, Settings
from tilde.IO.parsing_background_knowledge import parse_background_knowledge
from tilde.classification.example_partitioning import SimpleProgramExamplePartitioner, ClauseDBExamplePartitioner, \
    PartitionerBuilder
from tilde.trees.pruning import prune_leaf_nodes_with_same_label


def run_models_simpleprogram(fname_labeled_examples: str, settings: Settings,
                             fname_background_knowledge: Optional[str] = None,
                             debug_printing=False, use_mle=False):
    language = settings.language  # type: TypeModeLanguage

    # LABELS
    possible_targets = settings.possible_labels  # type: List[Label]

    # BACKGROUND KNOWLEDGE
    if fname_background_knowledge is not None:
        background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
    else:
        background_knowledge = None

    # EXAMPLES
    examples = ModelsExampleParser.parse(fname_labeled_examples, possible_targets)  # type: List[Example]
    # =======================

    example_partitioner = PartitionerBuilder().build_partitioner(InternalExampleFormat.SIMPLEPROGRAM,
                                                                 background_knowledge)

    tree_builder = TreeBuilderBuilder().build_treebuilder(TreeBuilderType.DETERMINISTIC, language, possible_targets,
                                                          example_partitioner)

    tree_builder.debug_printing(debug_printing)
    tree_builder.build_tree(examples)
    tree = tree_builder.get_tree()
    print(tree.to_string())

    program = convert_tree_to_simple_program(tree, language, debug_printing=debug_printing)

    print("%resulting program:")
    print("%------------------")
    for statement in program:
        print(str(statement) + ".")

    do_labeled_examples_get_correctly_classified_models(examples, program, possible_targets, background_knowledge)


def run_models_clausedb(fname_labeled_examples: str, settings: Settings,
                        fname_background_knowledge: Optional[str] = None,
                        debug_printing=False, use_mle=False):
    language = settings.language  # type: TypeModeLanguage

    # LABELS
    possible_targets = settings.possible_labels  # type: List[Label]

    # BACKGROUND KNOWLEDGE
    if fname_background_knowledge is not None:
        background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
    else:
        background_knowledge = None

    # EXAMPLES
    examples = ModelsExampleParser.parse(fname_labeled_examples, possible_targets)  # type: List[SimpleProgramExample]
    example_dbs = get_example_databases(examples, background_knowledge, models=True)  # type: List[ClauseDBExample]

    # =======================

    example_partitioner = PartitionerBuilder().build_partitioner(InternalExampleFormat.SIMPLEPROGRAM,
                                                                 background_knowledge)

    tree_builder = TreeBuilderBuilder().build_treebuilder(TreeBuilderType.DETERMINISTIC, language, possible_targets, example_partitioner)

    tree_builder.debug_printing(debug_printing)
    tree_builder.build_tree(example_dbs)
    tree = tree_builder.get_tree()
    print(tree.to_string())
    prune_leaf_nodes_with_same_label(tree)
    print(tree.to_string())

    program = convert_tree_to_simple_program(tree, language, debug_printing=debug_printing)

    print("%resulting program:")
    print("%------------------")
    for statement in program:
        print(str(statement) + ".")

    do_labeled_examples_get_correctly_classified_models(examples, program, possible_targets, background_knowledge)

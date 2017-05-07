from typing import List, Optional

from IO.parsing_background_knowledge import parse_background_knowledge
from IO.parsing_examples import parse_examples_model_format
from IO.parsing_settings import SettingParser, Settings
from classification.classification_helper import Label, do_labeled_examples_get_correctly_classified_models
from classification.example_partitioning import SimpleProgramExamplePartitioner
from representation.language import TypeModeLanguage
from trees.TreeBuilder import TreeBuilder
from trees.tree_converter import convert_tree_to_simple_program


def run_models_simpleprogram(fname_labeled_examples: str, fname_settings: str, fname_background_knowledge: Optional[str]=None):

    # SETINGS for MODELS format
    settings = SettingParser.get_settings_models_format(fname_settings)  # type: Settings
    language = settings.language  # type: TypeModeLanguage

    # LABELS
    possible_targets = settings.possible_labels  # type: List[Label]

    # BACKGROUND KNOWLEDGE
    if fname_background_knowledge is not None:
        background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
    else:
        background_knowledge = None

    # EXAMPLES
    test_examples = parse_examples_model_format(fname_labeled_examples, possible_targets)
    # =======================

    tree_builder = TreeBuilder(language, possible_targets, SimpleProgramExamplePartitioner(background_knowledge))

    tree_builder.debug_printing(True)
    tree_builder.build_tree(test_examples)
    tree = tree_builder.get_tree()
    print(tree.to_string2())

    program = convert_tree_to_simple_program(tree, language, debug_printing=True)
    print(program)

    do_labeled_examples_get_correctly_classified_models(test_examples, program, possible_targets, background_knowledge)
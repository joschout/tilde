from problog.program import PrologFile

from IO.parsing_background_knowledge import parse_background_knowledge
from IO.parsing_examples_models_format import ModelsExampleParser
from IO.parsing_settings import SettingParser, Settings
from classification.classification_helper import Label, do_labeled_examples_get_correctly_classified_models
from classification.example_partitioning import SimpleProgramExamplePartitioner

from representation.language import TypeModeLanguage
from trees.TreeBuilder import TreeBuilder

from trees.tree_converter import convert_tree_to_simple_program
from main.run_models import run_models_simpleprogram
from typing import List, Optional

fname_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples-experimental\\mach.s'
fname_background_knowledge = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples-experimental\\mach.bg'
fname_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples-experimental\\mach.kb'

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
examples = ModelsExampleParser.parse(fname_labeled_examples, possible_targets)
# =======================

tree_builder = TreeBuilder(language, possible_targets, SimpleProgramExamplePartitioner(background_knowledge))

tree_builder.debug_printing(True)
tree_builder.build_tree(examples)
tree = tree_builder.get_tree()
print(tree.to_string2())

program = convert_tree_to_simple_program(tree, language, debug_printing=True)

do_labeled_examples_get_correctly_classified_models(examples, program, possible_targets, background_knowledge)
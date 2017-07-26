from typing import List

from problog.program import PrologFile

from tilde.IO.parsing_background_knowledge import parse_background_knowledge
from tilde.IO.parsing_examples_models_format import ModelsExampleParser
from tilde.IO.parsing_settings.setting_parser import ModelsSettingsParser
from tilde.IO.parsing_settings.utils import FileSettings
from tilde.classification.classification_helper import do_labeled_examples_get_correctly_classified_models
from tilde.classification.example_partitioning import SimpleProgramExamplePartitioner
from tilde.representation.example import Label
from tilde.representation.language import TypeModeLanguage
from tilde.trees.TreeBuilder import ProbabilisticTreeBuilder
from tilde.trees.tree_converter import convert_tree_to_simple_program

fname_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples-experimental\\mach.s'
fname_background_knowledge = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples-experimental\\mach.bg'
fname_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples-experimental\\mach.kb'

# SETINGS for MODELS format
settings = ModelsSettingsParser().parse(fname_settings)  # type: FileSettings
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

tree_builder = ProbabilisticTreeBuilder(language, possible_targets, SimpleProgramExamplePartitioner(background_knowledge))

tree_builder.debug_printing(True)
tree_builder.build_tree(examples)
tree = tree_builder.get_tree()
print(tree.to_string())

program = convert_tree_to_simple_program(tree, language, debug_printing=True)

do_labeled_examples_get_correctly_classified_models(examples, program, possible_targets, background_knowledge)
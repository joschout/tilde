import os
from typing import List

from problog.program import PrologFile

from mai_version.IO.parsing_background_knowledge import parse_background_knowledge
from mai_version.IO.parsing_examples_models_format import ModelsExampleParser
from mai_version.IO.parsing_settings.setting_parser import ModelsSettingsParser
from mai_version.IO.parsing_settings.utils import FileSettings
from mai_version.classification.classification_helper import do_labeled_examples_get_correctly_classified_models
from mai_version.classification.example_partitioning import SimpleProgramExamplePartitioner
from mai_version.representation.example import Label
from mai_version.representation.language import TypeModeLanguage
from mai_version.trees.TreeBuilder import ProbabilisticTreeBuilder
from mai_version.trees.tree_converter import convert_tree_to_simple_program


project_dir = '/home/joschout/Repos/tilde'

dataset_name = 'mach'
data_dir = os.path.join(project_dir, 'ACE-examples-data', dataset_name)

keys_or_examples = 'examples-experimental'

fname_settings = os.path.join(data_dir, keys_or_examples, dataset_name + '.s')
fname_background_knowledge = os.path.join(data_dir, keys_or_examples, dataset_name + '.bg')
fname_labeled_examples = os.path.join(data_dir, keys_or_examples, dataset_name + '.kb')


# fname_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples-experimental\\mach.s'
# fname_background_knowledge = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples-experimental\\mach.bg'
# fname_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples-experimental\\mach.kb'

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
print(str(tree))

program = convert_tree_to_simple_program(tree, language, debug_printing=True)

do_labeled_examples_get_correctly_classified_models(examples, program, possible_targets, background_knowledge)
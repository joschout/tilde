import unittest
from typing import Optional, List

from tilde.classification.classification_helper import Label, get_example_databases
from problog.program import PrologFile, SimpleProgram
from tilde.representation.example import PrologStringExample, ClauseDBExample
from tilde.representation.language import TypeModeLanguage
from tilde.trees.TreeBuilder import DeterministicTreeBuilder
from tilde.trees.tree_converter import convert_tree_to_simple_program

from tilde.IO.parsing_examples_models_format import ModelsExampleParser
from tilde.IO.parsing_settings.setting_parser import SettingParser
from tilde.IO.parsing_settings.utils import Settings
from tilde.IO.parsing_background_knowledge import parse_background_knowledge
from tilde.classification.example_partitioning import SimpleProgramExamplePartitioner, ClauseDBExamplePartitioner
from tilde.trees.pruning import prune_leaf_nodes_with_same_label

debug_printing = False


class ModelsTestBase(unittest.TestCase):
    def general_setup(self, fname_labeled_examples: str, fname_settings: str, fname_background_knowledge: Optional[str] = None):

        # SETINGS for MODELS format
        settings = SettingParser.get_settings_models_format(fname_settings)  # type: Settings
        self.language = settings.language  # type: TypeModeLanguage

        # LABELS
        self.possible_targets = settings.possible_labels  # type: List[Label]

        # BACKGROUND KNOWLEDGE
        if fname_background_knowledge is not None:
            self.background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
        else:
            self.background_knowledge = None

        # EXAMPLES
        self.examples = ModelsExampleParser.parse(fname_labeled_examples,
                                                  self.possible_targets)  # type: List[PrologStringExample]

    def simple_program_setup(self) -> SimpleProgram:
        tree_builder = DeterministicTreeBuilder(self.language, self.possible_targets,
                                                SimpleProgramExamplePartitioner(self.background_knowledge))
        tree_builder.build_tree(self.examples)
        tree = tree_builder.get_tree()

        program = convert_tree_to_simple_program(tree, self.language, debug_printing=debug_printing)
        return program

    def clausedb_setup(self) -> SimpleProgram:
        example_dbs = get_example_databases(self.examples, self.background_knowledge,
                                            models=True)  # type: List[ClauseDBExample]

        tree_builder = DeterministicTreeBuilder(self.language, self.possible_targets, ClauseDBExamplePartitioner())

        tree_builder.build_tree(example_dbs)
        tree = tree_builder.get_tree()
        prune_leaf_nodes_with_same_label(tree)

        program = convert_tree_to_simple_program(tree, self.language, debug_printing=debug_printing)
        return program
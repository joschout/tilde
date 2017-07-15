# import unittest
# from typing import Optional, List
#
# from problog.program import PrologFile, SimpleProgram
#
# from IO.label_collector import ClauseDBLabelCollector, SimpleProgramLabelCollector
# from IO.parsing_background_knowledge import parse_background_knowledge
# from IO.parsing_examples_keys_format import parse_examples_key_format_with_key
# from IO.parsing_settings import SettingParser, Settings
# from IO.utils import KnowledgeBaseFormat
# from classification.classification_helper import Label, get_example_databases
# from classification.example_partitioning import SimpleProgramExamplePartitioner, ClauseDBExamplePartitioner
# from representation.example import  ClauseDBExample
# from representation.language import TypeModeLanguage
# from trees.TreeBuilder import DeterministicTreeBuilder
# from trees.pruning import prune_leaf_nodes_with_same_label
# from trees.stop_criterion import StopCriterionMinimalCoverage
# from trees.tree_converter import DeterministicTreeToProgramConverter
#
# debug_printing = False
#
#
# class KeyTestBase(unittest.TestCase):
#     def general_setup(self, fname_labeled_examples: str, fname_settings: str, fname_background_knowledge: Optional[str] = None):
#
#         # SETTINGS for KEYS formatted examples
#         settings = SettingParser.get_settings_keys_format(fname_settings)  # type: Settings
#         self.prediction_goal_handler = settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
#         self.prediction_goal = self.prediction_goal_handler.get_prediction_goal()  # type: Term
#
#         self.language = settings.language  # type: TypeModeLanguage
#
#         # BACKGROUND KNOWLEDGE
#         if fname_background_knowledge is not None:
#             self.background_knowledge = parse_background_knowledge(fname_background_knowledge)  # type: PrologFile
#         else:
#             self.background_knowledge = None
#
#         # EXAMPLES
#         self.examples = parse_examples_key_format_with_key(fname_labeled_examples)  # type: List[SimpleProgramExample]
#
#
#     def simple_program_setup(self) -> SimpleProgram:
#         # LABELS
#         index_of_label_var = self.prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
#         label_collector = SimpleProgramLabelCollector(self.prediction_goal, index_of_label_var)
#         label_collector.extract_labels(self.examples)
#         possible_labels = label_collector.get_labels()
#         # =================================
#
#
#         tree_builder = DeterministicTreeBuilder(self.language, possible_labels,
#                                                 SimpleProgramExamplePartitioner(self.background_knowledge))
#         tree_builder.debug_printing(debug_printing)
#         tree_builder.build_tree(self.examples, self.prediction_goal)
#
#         tree = tree_builder.get_tree()
#         print(tree.to_string())
#
#         tree_to_program_converter = DeterministicTreeToProgramConverter(KnowledgeBaseFormat.KEYS,
#                                                                         debug_printing=debug_printing,
#                                                                         prediction_goal=self.prediction_goal,
#                                                                         index=index_of_label_var)
#         program = tree_to_program_converter.convert_tree_to_simple_program(tree, self.language)
#         return program
#
#     def clausedb_setup(self) -> SimpleProgram:
#
#         example_dbs = get_example_databases(self.examples, self.background_knowledge)  # type: List[ClauseDBExample]
#
#         # LABELS
#         index_of_label_var = self.prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
#         label_collector = ClauseDBLabelCollector(self.prediction_goal, index_of_label_var, self.background_knowledge)
#         label_collector.extract_labels(example_dbs)
#         possible_labels = label_collector.get_labels()  # type: Set[Label]
#         # =================================
#
#         tree_builder = DeterministicTreeBuilder(self.language, list(possible_labels), ClauseDBExamplePartitioner(),
#                                                 StopCriterionMinimalCoverage(4))
#         tree_builder.debug_printing(debug_printing)
#         tree_builder.build_tree(example_dbs, self.prediction_goal)
#
#         tree = tree_builder.get_tree()
#         prune_leaf_nodes_with_same_label(tree)
#
#         tree_to_program_converter = DeterministicTreeToProgramConverter(KnowledgeBaseFormat.KEYS,
#                                                                         debug_printing=debug_printing,
#                                                                         prediction_goal=self.prediction_goal,
#                                                                         index=index_of_label_var)
#
#         program = tree_to_program_converter.convert_tree_to_simple_program(tree, self.language)
#         return program
import os

from tilde.main import kb_suffix, s_suffix, bg_suffix


class DebugPrintingOptions:
    def __init__(self,
                 example_parsing=False,
                 tree_building=False,
                 tree_pruning=False,
                 program_conversion=False,
                 get_classifier=False,
                 classification=False):
        self.example_parsing = example_parsing
        self.tree_building = tree_building
        self.tree_pruning = tree_pruning
        self.program_conversion = program_conversion
        self.get_classifier = get_classifier
        self.debug_printing_classification = classification


class FileNameData:
    def __init__(self, root_dir, logic_relative_dir, fold_relative_dir, output_relative_dir,
                 test_name, logic_name):
        self.test_name = test_name
        self.logic_name = logic_name

        self.fold_dir = os.path.join(root_dir, test_name, fold_relative_dir)
        self.output_dir = os.path.join(root_dir, test_name, output_relative_dir)

        logic_dir = os.path.join(root_dir, test_name, logic_relative_dir)
        self.fname_examples = os.path.join(logic_dir, logic_name + kb_suffix)
        self.fname_settings = os.path.join(logic_dir, logic_name + s_suffix)
        self.fname_background = os.path.join(logic_dir, logic_name + bg_suffix)



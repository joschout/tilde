from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from problog.program import SimpleProgram
    from tilde.trees import TreeNode


def write_out_tree(fname: str, tree: TreeNode):
    # write out tree
    print('\t--- writing out tree to: ' + fname)
    with open(fname, 'w') as f:
        f.write(str(tree))


def write_out_program(fname: str, program: SimpleProgram):
    print('--- writing out program to: ' + fname)
    with open(fname, 'w') as f:
        for program_statement in program:
            f.write(str(program_statement) + '.\n')


class FoldData:
    nb_folds = None  # type: int
    dir_output_files = None
    fname_prefix_fold = None
    all_key_sets = None

    examples_collection_usable_for_training = None
    examples_usable_for_testing = None

    total_nb_of_examples = None

    kb_format = None  # Optional[KnowledgeBaseFormat]
    internal_ex_format = None  # Optional[InternalExampleFormat]
    treebuilder_type = None  # Optional[TreeBuilderType]
    parsed_settings = None  # Optional[FileSettings]
    prediction_goal = None
    possible_labels = None
    index_of_label_var = None
    full_background_knowledge_sp = None
    stripped_background_knowledge = None

    debug_printing_example_parsing = False
    debug_printing_tree_building = False
    debug_printing_tree_pruning = False
    debug_printing_program_conversion = False
    debug_printing_get_classifier = False
    debug_printing_classification = False

    def __init__(self,
                 debug_printing_example_parsing=False,
                 debug_printing_tree_building=False,
                 debug_printing_tree_pruning=False,
                 debug_printing_program_conversion=False,
                 debug_printing_get_classifier=False,
                 debug_printing_classification=False):
        self.debug_printing_example_parsing = debug_printing_example_parsing
        self.debug_printing_tree_building = debug_printing_tree_building
        self.debug_printing_tree_pruning = debug_printing_tree_pruning
        self.debug_printing_program_conversion = debug_printing_program_conversion
        self.debug_printing_get_classifier = debug_printing_get_classifier
        self.debug_printing_classification = debug_printing_classification
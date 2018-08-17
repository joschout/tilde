import os
import sys

from problog.engine import DefaultEngine

from mai_experiments.experiment_settings import DebugPrintingOptions, FileNameData
from mai_experiments.fold_control import FoldInfoController

# CHANGE THESE TWO FOR EACH TEST
from tilde.IO.label_collector import LabelCollectorMapper
from tilde.IO.parsing_background_knowledge import parse_background_knowledge_keys
from tilde.IO.parsing_examples import KeysExampleBuilder
from tilde.IO.parsing_settings.setting_parser import KeysSettingsParser
from tilde.representation.example import InternalExampleFormat

test_name = 'bongard4'
logic_name = 'bongard'

# --- command-line printing settings ---
debug_printing_options = DebugPrintingOptions()
internal_ex_format = InternalExampleFormat.CLAUSEDB

engine = DefaultEngine()
engine.unknown = 1

filter_out_unlabeled_examples = False
hide_printouts = True

# --- directories ---
droot = '/home/joschout/Repos/tilde/mai_experiments/data'
dlogic_relative = 't-0-0-0'
dfold_relative = 'folds'
dout_relative = 'output'

file_name_data = FileNameData(root_dir=droot,
                              logic_relative_dir=dlogic_relative,
                              fold_relative_dir=dfold_relative,
                              output_relative_dir=dout_relative,
                              test_name=test_name,
                              logic_name=logic_name)


# --- fold settings ---
fname_prefix_fold = 'test'
fold_start_index = 0
nb_folds = 10
fold_suffix = '.txt'

fold_settings = FoldInfoController(fold_fname_prefix=fname_prefix_fold,
                                   fold_start_index=fold_start_index,
                                   nb_folds=nb_folds,
                                   fold_suffix=fold_suffix)

# -- create output directory
if not os.path.exists(file_name_data.output_dir):
    os.makedirs(file_name_data.output_dir)

print("start bongard4")
save_stdout = sys.stdout
if hide_printouts:
    sys.stdout = open(os.devnull, "w")

    # read in the fold information
    # read in the examples

    parsed_settings = KeysSettingsParser().parse(file_name_data.fname_settings)

    language = parsed_settings.language  # type: TypeModeLanguage

    # TODO: unify this with models --> let models use a prediction goal predicate label()
    prediction_goal_handler = parsed_settings.get_prediction_goal_handler()  # type: KeysPredictionGoalHandler
    prediction_goal = prediction_goal_handler.get_prediction_goal()  # type: Term

    print('=== START parsing background ===')
    background_knowledge_wrapper \
        = parse_background_knowledge_keys(file_name_data.fname_background,
                                          prediction_goal)  # type: BackgroundKnowledgeWrapper

    full_background_knowledge_sp \
        = background_knowledge_wrapper.get_full_background_knowledge_simple_program()  # type: Optional[SimpleProgram]
    print('=== END parsing background ===\n')
    # =================================================================================================================
    print('=== START parsing examples ===')
    # EXAMPLES
    example_builder = KeysExampleBuilder(prediction_goal, debug_printing_options.example_parsing)
    training_examples_collection = example_builder.parse(internal_ex_format, file_name_data.fname_examples,
                                                         full_background_knowledge_sp)  # type: ExampleCollection

    # =================================================================================================================

    print('=== START collecting labels ===')
    # LABELS
    index_of_label_var = prediction_goal_handler.get_predicate_goal_index_of_label_var()  # type: int
    label_collector = LabelCollectorMapper.get_label_collector(internal_ex_format, prediction_goal, index_of_label_var,
                                                               engine=engine)
    keys_of_unlabeled_examples = label_collector.extract_labels(training_examples_collection)

    possible_labels = label_collector.get_labels()  # type: Set[Label]
    possible_labels = list(possible_labels)
    print('=== END collecting labels ===\n')

    nb_of_unlabeled_examples = len(keys_of_unlabeled_examples)
    # TODO: change this back if necessary
    if filter_out_unlabeled_examples and nb_of_unlabeled_examples > 0:
        if fold_data is not None:
            fold_data.total_nb_of_examples = len(training_examples_collection.example_wrappers_sp)
        training_examples_collection = training_examples_collection.filter_examples_not_in_key_set(keys_of_unlabeled_examples)
        print("DANGEROUS: FILTERED OUT UNLABELED EXAMPLES")

    possible_labels = label_collector.get_labels()  # type: Set[Label]
    possible_labels = list(possible_labels)  # type: List[Label]

    # for each fold,
    #




if hide_printouts:
    sys.stdout = save_stdout
print("finished bongard4")

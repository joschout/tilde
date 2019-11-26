import sys

sys.path.append("/home/joschout/Repos/Django-subsumption")

from mai_experiments.experiment_settings import DebugPrintingOptions, FileNameData
from mai_experiments.fold_control import FoldInfoController

from mai_experiments.run_experiments_refactor.refactor_experiment_template import run_experiment
from refactor.back_end_picking import get_back_end_default, QueryBackEnd

# --- command-line printing settings ---
debug_printing_options = DebugPrintingOptions()

filter_out_unlabeled_examples = False
hide_printouts = False

# --- directories ---
droot = '/home/joschout/Repos/tilde/data-mai-experiments'
dlogic_relative = 't-0-0-0'
dfold_relative = 'folds'
dout_relative = 'output'

test_and_logic_names = [
    ('mutab0', 'muta-d'),
    ('mutaace1', 'muta-d'),
    ('financial', 'financial-d-mod'),
    ('canc', 'canc-d'),
    ('bongard4', 'bongard'),
]

default_handlers = [
    get_back_end_default(QueryBackEnd.SUBTLE),
    # get_back_end_default(QueryBackEnd.FLGG),
    # get_back_end_default(QueryBackEnd.DJANGO)
]

# --- fold settings ---
fname_prefix_fold = 'test'
fold_start_index = 0
nb_folds = 10
fold_suffix = '.txt'

for test_name, logic_name in test_and_logic_names:

    print('starting experiment', test_name)

    file_name_data = FileNameData(root_dir=droot,
                                  logic_relative_dir=dlogic_relative,
                                  fold_relative_dir=dfold_relative,
                                  output_relative_dir=dout_relative,
                                  test_name=test_name,
                                  logic_name=logic_name)

    for default_handler in default_handlers:

        fold_info_controller = FoldInfoController(
            fold_file_directory=file_name_data.fold_dir,
            fold_fname_prefix=fname_prefix_fold,
            fold_start_index=fold_start_index,
            nb_folds=nb_folds,
            fold_suffix=fold_suffix)

        run_experiment(file_name_data, fold_info_controller, default_handler,
                       hide_printouts, filter_out_unlabeled_examples, debug_printing_options)

    print('finishing experiment', test_name)

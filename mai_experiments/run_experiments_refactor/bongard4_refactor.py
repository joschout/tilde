from mai_experiments.experiment_settings import DebugPrintingOptions, FileNameData
from mai_experiments.fold_control import FoldInfoController

from mai_experiments.run_experiments.refactor_experiment_template import run_experiment
from refactor.back_end_picking import get_back_end_default, QueryBackEnd

# CHANGE THESE TWO FOR EACH TEST
test_name = 'bongard4'
logic_name = 'bongard'

import sys

# sys.path.append("/home/joschout/Repos/Django-subsumption")



# --- command-line printing settings ---
debug_printing_options = DebugPrintingOptions()

filter_out_unlabeled_examples = False
hide_printouts = False

# # --- directories ---
# droot = 'D:\\KUL\\KUL MAI\\Masterproef\\TILDE\\tilde\\fold\\data\\'
# dlogic_relative = 't-0-0-0\\'
# dfold_relative = 'folds\\'
# dout_relative = 'output\\'
#
# dlogic = droot + test_name + '\\' + dlogic_relative
# dfold = droot + test_name + '\\' + dfold_relative
# doutput = droot + test_name + '\\' + dout_relative
#
# # --- file names ---
# fname_examples = dlogic + logic_name + kb_suffix
# fname_settings = dlogic + logic_name + s_suffix
# fname_background = dlogic + logic_name + bg_suffix

# --- directories ---
droot = '/home/joschout/Repos/tilde/data'
dlogic_relative = 't-0-0-0'
dfold_relative = 'folds'
dout_relative = 'output'


file_name_data = FileNameData(root_dir=droot,
                              logic_relative_dir=dlogic_relative,
                              fold_relative_dir=dfold_relative,
                              output_relative_dir=dout_relative,
                              test_name=test_name,
                              logic_name=logic_name)

default_handler = get_back_end_default(QueryBackEnd.SUBTLE)

# --- fold settings ---
fname_prefix_fold = 'test'
fold_start_index = 0
nb_folds = 10
fold_suffix = '.txt'


fold_info_controller = FoldInfoController(
    fold_file_directory=file_name_data.fold_dir,
    fold_fname_prefix=fname_prefix_fold,
    fold_start_index=fold_start_index,
    nb_folds=nb_folds,
    fold_suffix=fold_suffix)

run_experiment(file_name_data, fold_info_controller, default_handler,
               hide_printouts, filter_out_unlabeled_examples, debug_printing_options)

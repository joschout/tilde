import os

import sys

from mai_experiments.experiment_settings import DebugPrintingOptions, FileNameData, FoldController
from mai_experiments.fold_file_parser import main_cross_validation

# CHANGE THESE TWO FOR EACH TEST
test_name = 'bongard4'
logic_name = 'bongard'

# --- command-line printing settings ---
debug_printing_options = DebugPrintingOptions()

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

fold_settings = FoldController(
    fold_file_directory=file_name_data.fold_dir,
    fold_fname_prefix=fname_prefix_fold,
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

main_cross_validation(file_name_data,
                      fold_settings,
                      filter_out_unlabeled_examples,
                      debug_printing_options)
if hide_printouts:
    sys.stdout = save_stdout
print("finished bongard4")

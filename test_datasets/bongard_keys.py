from run.run_keys import run_keys_simpleprogram, run_keys_clausedb

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\bongard\\keys\\bongard.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\bongard\\keys\\bongard.s'

use_clausedb = True
debug_printing = True
use_mle = True

if use_clausedb:
    run_keys_clausedb(file_name_labeled_examples, file_name_settings, debug_printing=debug_printing, use_mle=use_mle)
else:
    run_keys_simpleprogram(file_name_labeled_examples, file_name_settings, debug_printing=debug_printing, use_mle=use_mle)


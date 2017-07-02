from main.run_keys import run_keys_simpleprogram, run_keys_clausedb

file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\keys-experimental\\mach.kb'
file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\keys-experimental\\mach.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\keys-experimental\\mach.bg'


use_clausedb = False

if use_clausedb:
    run_keys_clausedb(file_name_labeled_examples, file_name_settings, file_name_background)
else:
    run_keys_simpleprogram(file_name_labeled_examples, file_name_settings, file_name_background)

from main.run_models import run_models_simpleprogram, run_models_clausedb

file_name_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\bongard\\examples\\bongard.s'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\bongard\\examples\\bongard.kb'


use_clausedb = True

if use_clausedb:
    run_models_clausedb(file_name_labeled_examples, file_name_settings)
else:
    run_models_simpleprogram(file_name_labeled_examples, file_name_settings)

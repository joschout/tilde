from main.run_models import run_models_simpleprogram, run_models_clausedb

settings_file_path = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\bongard\\examples\\bongard.s'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\bongard\\examples\\bongard.kb'

run_models_clausedb(file_name_labeled_examples, settings_file_path)

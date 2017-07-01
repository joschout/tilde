from main.run_models import run_models_simpleprogram, run_models_clausedb

settings_file_path = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.s'
file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.bg'
file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.kb'

run_models_clausedb(file_name_labeled_examples, settings_file_path, file_name_background)

from problog.program import PrologFile


file_name_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.kb'

examples_string = PrologFile(file_name_labeled_examples)

for line in examples_string:
    print(line)
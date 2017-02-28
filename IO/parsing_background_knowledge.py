from problog.program import PrologFile

file_name_background = 'D:\\KUL\\KUL MAI\\Masterproef\\ACE\\ace\\mach\\examples\\mach.bg'


def parse_background_knowledge():
    return PrologFile(file_name_background)

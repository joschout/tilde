from problog.program import PrologFile


def parse_background_knowledge(file_name: str)-> PrologFile:
    return PrologFile(file_name)

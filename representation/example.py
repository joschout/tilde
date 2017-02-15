from problog.program import SimpleProgram


class Example(SimpleProgram):
    """Wrapper class for an example.
    An example  consists of a prolog program (e.g. facts and/or clauses)
    and MIGHT have a label.
    """

    def __init__(self, label=None):
        SimpleProgram.__init__(self)
        self.label = label

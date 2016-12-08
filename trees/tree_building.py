from problog.logic import Term

class TreeBuilder:

    def __init__(self, language):
        self.language = language

    def build_tree(self, examples):
        self.build_tree_recursive(self, examples)

    #def build_tree_recursive(self, examples, conjunction=Term('true')):


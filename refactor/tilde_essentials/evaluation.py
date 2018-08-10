class TestEvaluator:
    """
    Abstract TestEvaluator class: used for evaluating a test on an example
    """
    def evaluate(self, example, test) -> bool:
        raise NotImplementedError('abstract method')
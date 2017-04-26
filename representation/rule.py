
class Rule(object):
    """Generic class for rules."""

    def __init__(self):
        pass

    def get_literals(self):
        """Returns all literals in the rule."""
        raise NotImplementedError('abstract method')

    def get_literal(self):
        """Returns the last added literal."""
        raise NotImplementedError('abstract method')

    def get_variables(self):
        """Return the set of variables in the rule.

        :return: all variables in that occur in the rule
        :rtype: set[Var]
        """
        variables = set()
        for lit in self.get_literals():
            if lit is not None:
                variables |= lit.variables()
        return variables

    def to_clauses(self, functor=None):
        """Transform rule into ProbLog clauses

        :param functor: override rule functor (set to None to keep original)
        :type functor: str | None
        :return: clause representation
        :rtype: list[Clause]
        """
        raise NotImplementedError('abstract method')

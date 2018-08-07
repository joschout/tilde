from typing import Optional, List

from problog.logic import Term, Clause, And
from problog.util import OrderedSet

from tilde.representation.rule import Rule


class TILDEQuery(Rule):
    """Represents a query as used in tilde.
    """

    def __init__(self, parent_query: Optional['TILDEQuery'], new_literal: Optional[Term]):
        Rule.__init__(self)
        self.parent = parent_query  # type: Optional['TILDEQuery']
        self.literal = new_literal  # type: Optional[Term]

    def get_literals(self) -> List[Term]:
        """Get literals in the rule.

        :return: list of literals including target
        :rtype: list[Term]
        """
        if self.parent is None:
            if self.literal is None:
                return []
            return [self.literal]
        else:
            return self.parent.get_literals() + [self.literal]

    def get_literal(self) -> Term:
        """Get most recently added body literal.

        :return: None (the body is empty for this type of rule)
        :rtype: Term
        """
        return self.literal

    def __and__(self, literal: Term) -> 'TILDEQuery':
        """Add a literal to the body of the rule.

        :param literal: literal to add
        :type literal: Term
        :return: new rule
        :rtype: TILDEQuery
        """
        return TILDEQuery(self, literal)

    def to_conjunction(self, functor=None) -> And:
        """Transform query into ProbLog conjunction

        :param functor: override rule functor (set to None to keep original)
        :type functor: str | None
        :return: clause representation
        :rtype: list[Clause]
        """
        literals = self.get_literals()

        def rename_recursive(lit, new_functor_of_recursive):
            if lit.functor == '_recursive':
                return Term(new_functor_of_recursive, *lit.args)
            else:
                return lit

        literals = [rename_recursive(lit, functor) for lit in literals]
        return And.from_list(literals)

    def has_new_variables(self) -> OrderedSet:
        # if I am the first query literal
        if self.parent is None:
            return self.get_literal().variables()
        else:
            return self.get_literal().variables() - self.parent.get_variables()

    def __str__(self) -> str:
        literals = self.get_literals()

        root = self._get_root()


        if len(literals) > 0 and isinstance(root, TILDEQueryHiddenLiteral):
        # if len(literals) > 0 and isinstance(literals[0], TILDEQueryHiddenLiteral):
            head = literals[0]
            if len(literals) == 1:
                return '%s :- true.' % (head,)
            else:
                return '%s :- %s' % (head, ', '.join(map(str, literals[1:])))
        else:
            head = Term('false')
            if len(literals) == 0:
                return '%s :- true.' % (head,)
            else:
                return '%s :- %s' % (head, ', '.join(map(str, literals)))

    def __len__(self) -> int:
        if self.parent is not None:
            return len(self.parent) + 1
        else:
            return 1

    def _get_root(self):

        current_node = self
        root = self
        while current_node is not None:
            if current_node.parent is not None:
                root = current_node.parent
            current_node = current_node.parent
        return root


class TILDEQueryHiddenLiteral(TILDEQuery):
    def __init__(self, literal: Optional[Term] = None):
        TILDEQuery.__init__(self, None, literal)

    def get_literals(self) -> List[Term]:
        """Get literals in the rule.

        :return: list of literals including target
        :rtype: list[Term]
        """
        return [self.literal]

    def get_literal(self):
        """Get most recently added body literal.

        :return: None (the body is empty for this type of rule)
        :rtype: Term
        """
        return None

    def __str__(self):
        return '%s :- true' % self.literal



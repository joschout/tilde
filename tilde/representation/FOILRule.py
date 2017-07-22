from typing import Optional, List

from problog.engine_builtin import StructSort
from problog.logic import Term, And, Constant, Clause

from tilde.representation.rule import Rule


class FOILRuleB(Rule):
    """A FOIL rule is a rule with a specified target literal.
    These rules are represented as a (reversed) linked list.

    :param parent: parent rule which corresponds to the rule obtained by removing the last literal
    :type parent: FOILRuleB | None
    :param literal: last literal of the body
    :type literal: Term | None
    """

    def __init__(self, parent: Optional['FOILRuleB'], literal: Optional[Term], target, previous, correct):
        Rule.__init__(self)
        self.parent: Optional['FOILRuleB'] = parent
        self.literal: Optional[Term] = literal
        self.target = target
        self.previous = previous
        self.correct = correct
        self.rule_prob = None
        self.score = None

    def get_literals(self) -> List[Term]:
        """Get literals in the rule.

        :return: list of literals including target
        :rtype: list[Term]
        """
        return self.parent.get_literals() + [self.literal]

    def get_literal(self) -> Term:
        """Get most recently added body literal.

        :return: None (the body is empty for this type of rule)
        :rtype: Term
        """
        return self.literal

    def __and__(self, literal: Term) -> 'FOILRuleB':
        """Add a literal to the body of the rule.

        :param literal: literal to add
        :type literal: Term
        :return: new rule
        :rtype: FOILRuleB
        """
        return FOILRuleB(self, literal, self.target, self.previous, self.correct)

    def to_clauses(self, functor: Optional[str]=None) -> List[Clause]:
        """Transform rule into ProbLog clauses

        :param functor: override rule functor (set to None to keep original)
        :type functor: str | None
        :return: clause representation
        :rtype: list[Clause]
        """
        if self.previous is not None:
            previous = self.previous.to_clauses(functor)  # type: List[Clause]
        else:
            previous = []  # type: List[Clause]

        inequalities = []

        object_identity = False
        if object_identity:
            variables = list(self.get_variables())
            for i, v1 in enumerate(variables):
                for v2 in variables[i + 1:]:
                    inequalities.append(Term('\=', v1, v2))

        literals = self.get_literals()

        def rename_recursive(lit, functor_to_rename_to):
            """"
            Checks whether the functor_to_rename_to of given 'lit' equals '_recursive'.
            If it does, it returns a new Term with the same arguments as 'lit' but with a new functor,
            namely the given 'functor_to_rename_to'. 
            Else, it returns the given 'lit'
            """
            if lit.functor == '_recursive':
                return Term(functor_to_rename_to, *lit.args)
            else:
                return lit

        literals = [rename_recursive(lit, functor) for lit in literals]

        prob = self.get_rule_probability()
        if prob is not None:
            prob = Constant(prob)
        head = literals[0].with_probability(prob)
        body = And.from_list(literals[1:] + inequalities)

        if functor is not None:
            head = Term(functor, *head.args, p=prob)
        return previous + [Clause(head, body)]

    def set_rule_probability(self, probability=None):
        rule = self
        while rule.parent:
            rule = rule.parent
        rule.rule_prob = probability

    def get_rule_probability(self):
        rule = self
        while rule.parent:
            rule = rule.parent
        return rule.rule_prob

    def has_new_variables(self):
        if not self.parent:
            return self.target.variables() - self.parent.get_variables()
        else:
            return self.get_literal().variables() - self.parent.get_variables()

    def __str__(self) -> str:
        literals = self.get_literals()
        head = literals[0].with_probability(self.get_rule_probability())
        if len(literals) == 1:
            return '%s :- true.' % (head,)
        else:
            return '%s :- %s' % (head, ', '.join(map(str, literals[1:])))

    def is_equivalent(self, other) -> bool:
        if abs(self.score - other.score) > 1e-8:
            return False
        literals1 = sorted(self.get_literals(), key=StructSort)
        literals2 = sorted(other.get_literals(), key=StructSort)

        result = literals1 == literals2
        return result

    def __len__(self) -> int:
        if self.parent:
            return len(self.parent) + 1
        else:
            return 1


class FOILRule(FOILRuleB):
    """Represents the head of a FOILRule.

    :param target: literal in the head of the rule
    :type target: Term
    :param previous: previous rule (if part of set)
    :type previous: FOILRuleB
    """

    def __init__(self, target=None, previous=None, correct=None):
        if target is None and previous is not None:
            target = previous.target
        FOILRuleB.__init__(self, None, None, target, previous, correct)

    def get_literals(self) -> List[Term]:
        """Get literals in the rule.

        :return: list of literals including target
        :rtype: list[Term]
        """
        return [self.target]

    def get_literal(self) -> Optional[Term]:
        """Get most recently added body literal.

        :return: None (the body is empty for this type of rule)
        :rtype: Term
        """
        return None

    def __str__(self) -> str:
        return '%s :- true' % self.target

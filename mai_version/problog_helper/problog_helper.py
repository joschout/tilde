from typing import Dict

from problog.logic import Term, Var


def apply_substitution_to_term(term: Term, substitution: Dict[str, Term]) -> Term:
    complete_substitution = {}

    # NOTE: all variables in the term need to be defined in the substitution
    for var in term.variables():
        complete_substitution[var.name] = Var(var.name)

    complete_substitution.update(substitution)

    term_substitution = term.apply(complete_substitution)
    return term_substitution


def get_probability(term: Term) -> float:
    if term.probability is None:
        return 1.0
    else:
        return term.probability

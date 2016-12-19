from collections import defaultdict
from itertools import product

from problog.logic import Term, is_variable, Var, Clause, And


class BaseLanguage(object):
    """Base class for languages."""

    def __init__(self):
        pass

    def refine(self, rule):
        """Generate one refinement for the given rule.

        :param rule: rule for which to generate refinements
        """
        raise NotImplementedError('abstract method')


class TypeModeLanguage(BaseLanguage):
    """Typed and Mode-based representation."""

    MODE_EXIST = '+'     # use existing variable
    MODE_NEW = '-'       # create new variable (do not reuse existing)
    MODE_CONSTANT = 'c'  # insert constant

    def __init__(self, symmetry_breaking=True, **kwargs):
        BaseLanguage.__init__(self)

        self._types = {}
        # dict[tuple[str,int],tuple[str]]: signature / argument types
        # e.g.
        #       {('mother', 2): ['person', 'person'],
        #        ('grandmother', 2): ['person', 'person'],
        #        ('female', 1): ['person'],
        #        ('father', 2): ['person', 'person'],
        #        ('male', 1): ['person'],
        #        ('male_ancestor', 2): ['person', 'person'],
        #        ('parent', 2): ['person', 'person'],
        #        ('female_ancestor', 2): ['person', 'person']
        #       }

        self._values = defaultdict(set)
        # dict[str, set[Term]]: values in data for given type
        # e.g.
        #       {
        #        'person': {katleen, yvonne, lucy, rene, stijn, luc, etienne, prudent, esther,
        #                    lieve, laura, willem, an, soetkin, leon, rose, alice, bart, pieter}
        #       }

        self._modes = []
        # list[tuple] : list of functor, modestr pairs
        # e.g.
        #      < class 'list'>: [('male', ['+']),
        #                        ('parent', ['+', '+']),
        #                        ('parent', ['+', '-']),
        #                        ('parent', ['-', '+'])]

        self._symmetry_breaking = symmetry_breaking
        self._allow_negation = True
        self._allow_recursion = False

    def add_types(self, functor, argtypes):
        """Add type information for a predicate.

        Type information has to be unique for a functor/arity combination.

        :param functor: functor of the predicate
        :type functor: str
        :param argtypes: types of the arguments (arity is length of this list)
        :type argtypes: list[str]
        :raise ValueError: duplicate type definition is given
        """
        key = (functor, len(argtypes))
        if key in self._types:
            raise ValueError("A type definition already exists for '%s/%s'."
                             % (functor, len(argtypes)))
        else:
            self._types[key] = argtypes

    def add_modes(self, functor, argmodes):
        """Add mode information for a predicate.

        :param functor: functor of the predicate
        :type functor: str
        :param argmodes: modes of the arguments (arity is length of this list)
        :type argmodes: list[str]
        """
        self._modes.append((functor, argmodes))

    def add_values(self, typename, *values):
        """Add a value for a predicate.

        :param typename: name of the type
        :type typename: str
        :param values: value to add (can be multiple)
        :type values: collections.Iterable[Term]
        """
        for value in values:
            self._values[typename].add(value)

    def refine(self, rule):
        """Generate ONE refinement for the given rule.

            We refine a rule by adding LITERALS to the BODY of the rule.



        :param rule: rule for which to generate refinements
        :return: GENERATOR of literals that can be added to the rule
        :rtype: collections.Iterable[Term]
        """

        # 1. we need to know how many variables are in the already existing rule.
        #    We also need to know the types of these variables.
        #    This is important information when adding new literals.
        varcount = len(rule.get_variables())
        variables = self.get_variable_types(*rule.get_literals())

        # We check the most recently added body literal.
        # If there is a most recently added body literal,
        #   then we check whether its functor is '_recursive'
        #   If its most recently added body literal is '_recursive',
        #       we cannot extend the body any further,
        #       so the function returns.
        #   Else, we get the set of already generated literals from the last added literal
        # If there is no recently added body literal,
        #       we will have to start from scratch, from an empty set
        if rule.get_literal():
            if rule.get_literal().functor == '_recursive':
                return  # can't extend after recursive
            generated = rule.get_literal().refine_state
        else:
            generated = set()

        # We need to generate a literal to refine the body of the clause
        # There are three possible ways we can add a literal
        # 1. as a positive refinement
        # 2. as a negative refinement
        # 3. as a recursive refinement

        # 1) a positive refinement
        # We have defined which literals can be added in MODES,
        # as their functor and the mode of each of the arguments.
        # We will consider each functor as a possible candidate for refinement
        #
        # SO for each functor in MODES
        for functor, modestr in self._modes:
            # We have defined which literals can be added in MODES,
            # as their functor and the mode of each of the arguments.
            # We will consider each functor as a possible candidate for refinement

            # we will collect the possible arguments for the current functor in a list
            arguments = []
            arity = len(modestr)
            # get the types of the arguments of the given predicate
            types = self.get_argument_types(functor, arity)

            # a functor has multiple variables,
            #       each with their own modes.
            # We have to consider each variable with its mode separately
            # There are three different modes for an argument:
            #       '+': the variable must be unified with an existing variable
            #           --> use an existing variable
            #       '-': create a new variable, do not reuse an old one
            #       'c': insert a constant
            # for each argument of functor:
            #   check its mode
            #       '+' --> add to arguments
            #                   a list of the variables in the rule with the same type as the current argument
            #                   e.g. arguments = [ ..., [X,Y], ...]
            #       '-' --> add to arguments
            #                   a list containing 1 new Var #
            #       'c' --> add to arguments
            #                   a list of all possible constants for the type of the argument
            for argmode, argtype in zip(modestr, types):
                if argmode == '+':
                    # All possible variables of the given type
                    arguments.append(variables.get(argtype, []))
                elif argmode == '-':
                    # A new variable
                    arguments.append([Var('#')])  # what about adding a term a(X,X) where X is new?
                elif argmode == 'c':
                    # Add a constant
                    arguments.append(self.get_type_values(argtype))
                    pass
                else:
                    raise ValueError("Unknown mode specifier '%s'" % argmode)

            # arguments is a list of lists.
            # It contains as many lists as the arity of the functor.
            # Each list corresponds to the possible values in the refined literal of the corresponding variable.
            # To generate all possible combinations,
            # we take the carthesian product of the elements in the lists.
            #
            # SO for each possible combination of arguments:
            #   create a term using the functor and the arguments.
            #   IF the term hasn't already been generated in the past:
            #       IF we want to break symmetries
            #            add the term to the set of already generated terms
            #       Substitute each of the '#'-vars for a new variable
            #       add the term t as the prototype of the substuted term
            # We know want to be return the substituted term
            # But before returning,
            # we want to save the state of this function,
            # so we can generate new terms next time we call this function.
            # To do this, we add the set of generated terms to the new literal.
            # IF we want to break symmetry,
            #   save a shallow copy of the set of generated literals
            # ELSE
            #   save the UNION of the seg of generated literals and {t, -t, t_i, -t_i}
            for args in product(*arguments):
                t = Term(functor, *args)
                if t not in generated:
                    if self._symmetry_breaking:
                        generated.add(t)
                    t_i = t.apply(TypeModeLanguage.ReplaceNew(varcount))
                    t_i.prototype = t
                    if self._symmetry_breaking:
                        t_i.refine_state = generated.copy()
                    else:
                        t_i.refine_state = generated | {t, -t, t_i, -t_i}
                    yield t_i

        # 2) a negative refinement
        if self._allow_negation:
            for functor, modestr in self._modes:
                if '-' in modestr:
                    # No new variables allowed for negative literals
                    continue
                arguments = []
                arity = len(modestr)
                types = self.get_argument_types(functor, arity)
                for argmode, argtype in zip(modestr, types):
                    if argmode == '+':
                        # All possible variables of the given type
                        arguments.append(variables.get(argtype, []))
                    elif argmode == 'c':
                        # Add a constant
                        arguments.append(self.get_type_values(argtype))
                        pass
                    else:
                        raise ValueError("Unknown mode specifier '%s'" % argmode)
                for args in product(*arguments):
                    t = -Term(functor, *args)
                    if t not in generated:
                        if self._symmetry_breaking:
                            generated.add(t)
                        t_i = t.apply(TypeModeLanguage.ReplaceNew(varcount))
                        t_i.prototype = t
                        if self._symmetry_breaking:
                            t_i.refine_state = generated.copy()
                        else:
                            t_i.refine_state = generated | {t, -t, t_i, -t_i}
                        yield t_i

        # 3) recursive
        if self._allow_recursion and rule.previous.previous:  # recursion in the first rule makes no sense
            types = self.get_argument_types(rule.target.functor, rule.target.arity)

            arguments = []
            for argtype in types:
                arguments.append(variables.get(argtype, []))

            for args in product(*arguments):
                t = Term('_recursive', *args)
                t.prototype = t
                if self._symmetry_breaking:
                    generated.add(t)
                if self._symmetry_breaking:
                    t.refine_state = generated.copy()
                else:
                    t.refine_state = generated | {t}
                yield t

    def refine_conjunction_one_literal(self, query):
        # 1. we need to know how many variables are in the already existing rule.
        #    We also need to know the types of these variables.
        #    This is important information when adding new literals.
        varcount = len(query.get_variables())
        variables = self.get_variable_types(*query.get_literals())

        # We check the most recently added body literal.
        # If there is a most recently added body literal,
        #   then we check whether its functor is '_recursive'
        #   If its most recently added body literal is '_recursive',
        #       we cannot extend the body any further,
        #       so the function returns.
        #   Else, we get the set of already generated literals from the last added literal
        # If there is no recently added body literal,
        #       we will have to start from scratch, from an empty set
        if query.get_literal() is not None:
            generated = query.get_literal().refine_state
        else:
            generated = set()

        # We need to generate a literal to refine the body of the clause
        #
        # 1) a positive refinement
        # We have defined which literals can be added in MODES,
        # as their functor and the mode of each of the arguments.
        # We will consider each functor as a possible candidate for refinement
        #
        # SO for each functor in MODES
        for functor, modestr in self._modes:  # e.g. 'parent', ['+', '+']
            # We have defined which literals can be added in MODES,
            # as their functor and the mode of each of the arguments.
            # We will consider each functor as a possible candidate for refinement

            # we will collect the possible arguments for the current functor in a list
            arguments = []
            arity = len(modestr)
            # get the types of the arguments of the given predicate
            types = self.get_argument_types(functor, arity)

            # a functor has multiple variables,
            #       each with their own modes.
            # We have to consider each variable with its mode separately
            # There are three different modes for an argument:
            #       '+': the variable must be unified with an existing variable
            #           --> use an existing variable
            #       '-': create a new variable, do not reuse an old one
            #       'c': insert a constant
            # for each argument of functor:
            #   check its mode
            #       '+' --> add to arguments
            #                   a list of the variables in the rule with the same type as the current argument
            #                   e.g. arguments = [ ..., [X,Y], ...]
            #       '-' --> add to arguments
            #                   a list containing 1 new Var #
            #       'c' --> add to arguments
            #                   a list of all possible constants for the type of the argument
            for argmode, argtype in zip(modestr, types):
                if argmode == '+':
                    # All possible variables of the given type
                    arguments.append(variables.get(argtype, []))
                elif argmode == '-':
                    # A new variable
                    arguments.append([Var('#')])  # what about adding a term a(X,X) where X is new?
                elif argmode == 'c':
                    # Add a constant
                    arguments.append(self.get_type_values(argtype))
                    pass
                else:
                    raise ValueError("Unknown mode specifier '%s'" % argmode)

            # arguments is a list of lists.
            # It contains as many lists as the arity of the functor.
            # Each list corresponds to the possible values in the refined literal of the corresponding variable.
            # To generate all possible combinations,
            # we take the carthesian product of the elements in the lists.
            #
            # SO for each possible combination of arguments:
            #   create a term using the functor and the arguments.
            #   IF the term hasn't already been generated in the past:
            #       IF we want to break symmetries
            #            add the term to the set of already generated terms
            #       Substitute each of the '#'-vars for a new variable
            #       add the term t as the prototype of the substuted term
            # We know want to be return the substituted term
            # But before returning,
            # we want to save the state of this function,
            # so we can generate new terms next time we call this function.
            # To do this, we add the set of generated terms to the new literal.
            # IF we want to break symmetry,
            #   save a shallow copy of the set of generated literals
            # ELSE
            #   save the UNION of the seg of generated literals and {t, -t, t_i, -t_i}
            for args in product(*arguments):
                t = Term(functor, *args)
                if t not in generated:
                    if self._symmetry_breaking:
                        generated.add(t)
                    t_i = t.apply(TypeModeLanguage.ReplaceNew(varcount))
                    t_i.prototype = t
                    if self._symmetry_breaking:
                        t_i.refine_state = generated.copy()
                    else:
                        t_i.refine_state = generated | {t, -t, t_i, -t_i}
                    yield t_i

    def get_type_values(self, typename):
        """Get all values that occur in the data for a given type.

        :param typename: name of type
        :type typename: str
        :return: set of values
        :rtype: set[Term]
        """
        return self._values.get(typename, [])

    def get_argument_types(self, functor, arity):
        """Get the types of the arguments of the given predicate.

        :param functor: functor of the predicate
        :type functor: str
        :param arity: arity of the predicate
        :type arity: int
        :return: tuple of type descriptors, one for each argument
        :rtype: tuple[str]
        """
        return self._types[(functor, arity)]

    def get_variable_types(self, *literals):
        """Get the types of all variables that occur in the given literals.

        :param literals: literals to extract variables from
        :type literals: collections.Iterable[Term]
        :return: dictionary with list of variables for each type
        :rtype: dict[str, list[Term]]
        """
        result = defaultdict(set)
        for lit in literals:
            if lit is None:
                pass
            else:
                if lit.is_negated():
                    lit = -lit

                if lit.functor == '_recursive':
                    # Don't need to process this, variables will occur somewhere else
                    #  because _recursive has mode + on all arguments.
                    continue
                types = self.get_argument_types(lit.functor, lit.arity)
                for arg, argtype in zip(lit.args, types):
                    if is_variable(arg) or arg.is_var():
                        result[argtype].add(arg)
        return result

    def load(self, data):
        """Load from data.

        :param data: datafile
        :type data: DataFile
        """

        for typeinfo in data.query('base', 1):
            typeinfo = typeinfo[0]
            self.add_types(typeinfo.functor, list(map(str, typeinfo.args)))

        for modeinfo in data.query('mode', 1):
            modeinfo = modeinfo[0]
            self.add_modes(modeinfo.functor, list(map(str, modeinfo.args)))

        for predicate, types in self._types.items():
            arg_values = zip(*data.query(*predicate))
            for a, t in zip(arg_values, types):
                self.add_values(t, *a)

        for optname, optvalue in data.query('option', 2):
            if str(optname) == 'negation' and str(optvalue) == 'off':
                self._allow_negation = False
            elif str(optname) == 'recursion' and str(optvalue) == 'on':
                self._allow_recursion = True

    class ReplaceNew(object):
        """Helper class for replacing new variables (indicated by name '#') by unique variables.

        :param count: the current number of variables
        :type count: int
        """

        def __init__(self, count):
            self.count = count

        def _get_name(self, index):
            """Get a name for the new variable.
            This name will be a single letter from A to Z, or V<num> if index > 25.

            :param index: number of the variable
            :type index: int
            :return: name of variable
            :rtype: str
            """
            if index < 26:
                return chr(65 + index)
            else:
                return 'V%d' % index

        def __getitem__(self, name):
            if name == '#':
                name = self._get_name(self.count)
                self.count += 1
                return Var(name)
            else:
                return Var(name)

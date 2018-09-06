import ctypes

from problog.logic import Term

from refactor.query_testing_back_end.django.django_wrapper.c_library import lib_django


class ConversionException(Exception):
    pass


class ClauseWrapper:
    __ajoute_tete = lib_django.AjouteTete
    __ajoute_clause = lib_django.AjouteClause

    __termine_clause = lib_django.TermineClause

    __libere_clause = lib_django.LibereClause
    __affice_clause_fol = lib_django.AfficheClauseFOL

    def __init__(self, clause_id=None):
        self.clause = lib_django.NewClause()
        self.is_destructed = False
        self.has_head = False
        self.is_locked = False
        self.clause_id = clause_id

        self._problog_representation = None

    def destruct(self):
        if not self.is_destructed:
            ClauseWrapper.__libere_clause(self.clause)
            self.is_destructed = True
        else:
            raise ConversionException("double destruct of clause")

    # def __del__(self):
    #     """
    #     WARNING: don't rely on the garbage collector to call the object's destructor.
    #     Cyclic dependencies can prevent the GC from ever calling this method.
    #     ALWAYS call destruct EXPLICITLY.
    #
    #     :return:
    #     """
    #     self.destruct()

    def print_using_c(self):
        if not self.is_destructed:
            ClauseWrapper.__affice_clause_fol(self.clause)

    def lock_adding_to_clause(self):
        if not self.is_destructed:
            if not self.is_locked:
                ClauseWrapper.__termine_clause(self.clause)
                self.is_locked = True
            else:
                raise ConversionException("double lock/end of clause")
        else:
            raise ConversionException("tried locking a destructed clause")

    def add_literal_to_body(self, literal: Term):
        if not self.is_destructed:
            var_array_c = _get_variable_array(literal)

            functor = str(literal.functor).encode('utf-8')
            arity = int(literal.arity)

            ClauseWrapper.__ajoute_clause(self.clause, functor, arity, var_array_c)
        else:
            raise ConversionException("adding literal to body of desctructed clause")

    def add_literal_as_head(self, literal: Term):
        """
        NOTE: not mandatory; can be without head.

        :param literal:
        :return:
        """
        if not self.is_destructed:
            if not self.has_head:
                var_array_c = _get_variable_array(literal)
                functor = str(literal.functor).encode('utf-8')
                arity = int(literal.arity)

                ClauseWrapper.__ajoute_tete(self.clause, functor, arity, var_array_c)
                self.has_head = True
            else:
                raise ConversionException("clause already has a head")
        else:
            raise ConversionException("adding literal as head to destructed clause")

    def __str__(self):
        return str(self._problog_representation)

    def add_problog_clause(self, problog_representation: Term):
        self._problog_representation = problog_representation


class HypothesisWrapper():
    __new_hypothese_base = lib_django.NewHypotheseBase

    __libere_hypothese = lib_django.LibereHypothese

    def __init__(self, clause_wrapper: ClauseWrapper):
        if clause_wrapper.is_destructed:
            raise ConversionException("cannot turn destructed clause into a hypothesis")
        elif not clause_wrapper.is_locked:
            raise ConversionException("cannot turn an unclosed clause into a hypothesis")
        else:
            self.hypothesis = HypothesisWrapper.__new_hypothese_base(clause_wrapper.clause)
            self.is_destructed = False

            self._prolog_hypothesis = clause_wrapper._problog_representation

    def destruct(self):
        if not self.is_destructed:
            HypothesisWrapper.__libere_hypothese(self.hypothesis)
            self.is_destructed = True
        else:
            raise ConversionException("double destruct of hypothesis")

    # def __del__(self):
    #     """
    #     WARNING: don't rely on the garbage collector to call the object's destructor.
    #     Cyclic dependencies can prevent the GC from ever calling this method.
    #     ALWAYS call destruct EXPLICITLY.
    #
    #     :return:
    #     """
    #     self.destruct()

    def __str__(self):
        return str(self._prolog_hypothesis)


#
#
#
# class HypothesisWrapper(ClauseWrapper):
#     __new_hypothese_base = lib_django.NewHypotheseBase
#
#     __libere_hypothese = lib_django.LibereHypothese
#
#     def __init__(self):
#         super().__init__()
#         self.is_set_to_hypothesis = False
#
#     def convert_to_hypothesis(self):
#         if not self.is_destructed:
#             if not self.is_set_to_hypothesis:
#                 HypothesisWrapper.__new_hypothese_base(self.clause, 0)
#                 self.is_set_to_hypothesis = True
#             else:
#                 raise ConversionException("double set to hypothesis")
#         else:
#             raise ConversionException("tried setting a destructed clause as a hypothesis")
#
#     def destruct(self):
#         if not self.is_destructed:
#             HypothesisWrapper.__libere_hypothese(self.clause)
#             self.is_destructed = True
#         else:
#             raise ConversionException("double destruct")


def _get_variable_array(literal: Term):
    VariableArray = ctypes.c_char_p * literal.arity
    var_array_c = VariableArray()

    for i in range(literal.arity):
        var_array_c[i] = str(literal.args[i]).encode('utf-8')

    return var_array_c

from tilde.representation.TILDE_query import TILDEQuery


class QueryWrapper:
    def __init__(self, tilde_query: TILDEQuery, external_representation):
        self.tilde_query = tilde_query
        self.external_representation = external_representation


class FLGGQueryWrapper(QueryWrapper):
    def __str__(self):
        return self.external_representation

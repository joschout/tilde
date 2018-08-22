from refactor.tilde_essentials.query_wrapping import QueryWrapper


class FLGGQueryWrapper(QueryWrapper):
    def __str__(self):
        return self.external_representation

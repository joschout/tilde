from refactor.tilde_essentials.query_wrapping import QueryWrapper


class SubtleQueryWrapper(QueryWrapper):
    def __str__(self):
        return self.external_representation

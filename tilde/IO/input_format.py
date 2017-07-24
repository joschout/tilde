from enum import Enum


class KnowledgeBaseFormatException(Exception):
    pass


class KnowledgeBaseFormat(Enum):
    MODELS = 1
    KEYS = 2

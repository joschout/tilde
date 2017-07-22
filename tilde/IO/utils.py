from enum import Enum


class KnowledgeBaseFormat(Enum):
    MODELS = 1
    KEYS = 2


class InternalExampleFormat(Enum):
    SIMPLEPROGRAM = 1
    CLAUSEDB =2
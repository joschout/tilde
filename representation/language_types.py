from typing import Tuple, List, Dict, Set

from problog.logic import Term

TypeName = str
TypeSignature = Tuple[TypeName, int] # name, arity
TypeArguments = List[TypeName]
TypeDict = Dict[TypeSignature, TypeArguments]
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

ValueSet = Set[Term]
ValuesDict = Dict[TypeName, ValueSet]
# dict[str, set[Term]]: values in data for given type
# e.g.
#       {
#        'person': {katleen, yvonne, lucy, rene, stijn, luc, etienne, prudent, esther,
#                    lieve, laura, willem, an, soetkin, leon, rose, alice, bart, pieter}
#       }

ModeName = str
ModeIndicators = List[str]
Mode = Tuple[ModeName, ModeIndicators]
ModeList = List[Mode]
# list[tuple] : list of functor, modestr pairs
# e.g.
#      < class 'list'>: [('male', ['+']),
#                        ('parent', ['+', '+']),
#                        ('parent', ['+', '-']),
#                        ('parent', ['-', '+'])]




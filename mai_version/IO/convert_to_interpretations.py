"""
ASSUMES A TYPED LANGUAGE



"""
from typing import Dict

from problog.logic import Constant
from problog.program import PrologString, SimpleProgram

from mai_version.IO.parsing_settings.setting_parser import KeysSettingsParser
from mai_version.IO.parsing_settings.utils import FileSettings

fname_kb = "D:\\KUL\\KUL MAI\\Masterproef\\TILDE\\tilde\\fold\\data\\sisya\\t-0-0-0\\sisy.kb"
fname_s = "D:\\KUL\\KUL MAI\\Masterproef\\TILDE\\tilde\\fold\\data\\sisya\\t-0-0-0\\sisy.s"

parsed_settings = KeysSettingsParser().parse(fname_s)  # type: FileSettings
language = parsed_settings.language

kb_pstr = PrologString(fname_kb)




example_key_type_name = "ptid"


example_databases = {}  # type: Dict[Constant, SimpleProgram]

# for statement in kb_pstr:
#
#
# def interpretations(database, example_key_set, foreign_key_set):
#
#
#
#     for k in example_key_set:
#         for line in database:
#             if k in line:
#                 example_databases[k].add(line)
#
#
#     # gathetr all tuples in database that contain
#     for line in database:
#         if line has example key:
#             example_databases[key] += line
#


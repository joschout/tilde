""""
The file app.s contains a number of settings that influence the way in which ACE works.

These settings can mainly be divided in two kinds:
    settings that define the language bias (the kind of patterns that can be found),
     and settings that control the system in some other way.

The language bias can be defined in two ways.
1. For beginning users there are the warmode-settings;
    these are simple to use and allow to define a good language bias very quickly.
    warmode-settings are automatically translated by the system to a lower level
        consisting of rmode, type and other settings.
2. The user can also specify the language directly at this lower level, which offers better control of the
way in which the program traverses the search space but is more complicated.
"""
from tilde.IO.input_format import KnowledgeBaseFormat, KnowledgeBaseFormatException
from tilde.IO.parsing_settings.token_parser import ClassesTokenParser, TypeTokenParser, RmodeTokenParser, \
    PredictionTokenParser
from tilde.IO.parsing_settings.utils import Settings, SettingsParsingError


class SettingParser:
    def __init__(self):
        self.first_setting_token_parser = None
        self.settings = Settings()

    def parse(self, file_path) -> Settings:
        if self.first_setting_token_parser is not None:
            with open(file_path, 'r') as f:
                for line in f:
                    self.first_setting_token_parser.parse_line(line, self.settings)
            return self.settings
        else:
            raise SettingsParsingError("No SettingTokenParser set as first token parser")


class ModelsSettingsParser(SettingParser):
    def __init__(self):
        super().__init__()

        classes_token_parser = ClassesTokenParser()
        type_token_parser = TypeTokenParser()
        rmode_token_parser = RmodeTokenParser()

        self.first_setting_token_parser = classes_token_parser
        classes_token_parser.set_successor(type_token_parser)
        type_token_parser.set_successor(rmode_token_parser)


class KeysSettingsParser(SettingParser):
    def __init__(self):
        super().__init__()

        prediction_token_parser = PredictionTokenParser()
        type_token_parser = TypeTokenParser()
        rmode_token_parser = RmodeTokenParser()

        self.first_setting_token_parser = prediction_token_parser
        prediction_token_parser.set_successor(type_token_parser)
        type_token_parser.set_successor(rmode_token_parser)


class SettingsParserMapper:
    @staticmethod
    def get_settings_parser(kb_format: KnowledgeBaseFormat) -> SettingParser:
        if kb_format is KnowledgeBaseFormat.KEYS:
            return KeysSettingsParser()
        elif kb_format is KnowledgeBaseFormat.MODELS:
            return ModelsSettingsParser()
        else:
            raise KnowledgeBaseFormatException('Only the input formats Models and Key are supported.')

# def get_rmode_from_query():
#     settings_prolog = PrologFile(settings_file_path)
#     # for statement in settings_prolog:
#     #     print(statement)
#     engine = DefaultEngine()
#     # try:
#     settings_db = engine.prepare(settings_prolog)
#     for statement in settings_db:
#         print(statement)
#     # except ParseError as perr:
#     #     print('ParseError thrown')
#     print(engine.query(settings_db, Term('rmode', 'replaceable(+V_0)')))

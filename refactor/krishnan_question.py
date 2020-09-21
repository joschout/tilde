

settings_file_parser = SettingsParserMapper.get_settings_parser(KnowledgeBaseFormat.KEYS)
parsed_settings = settings_file_parser.parse(file_name_data.fname_settings)

language = TypeModeLanguage()


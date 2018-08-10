import json
import os

_package_directory = os.path.dirname(os.path.abspath(__file__))

_default_config_file_name = 'config.json'
_absolute_default_config_file_name = os.path.join(_package_directory, _default_config_file_name)

_subtle_path_key = 'SUBTLE_PATH'
_split_criterion_key = 'SPLIT_CRITERION'
_kb_file_key = 'KB_FILE'
_s_file_key = 'S_FILE'
_bg_file_key = 'BG_FILE'


_default_settings = {_subtle_path_key: '', _split_criterion_key: 'entropy',
                     _kb_file_key: '', _s_file_key: '', _bg_file_key: ''}
_config_file_data = {}


def _get_setting(key):
    try:
        return _config_file_data[key]
    except KeyError as err:
        print(key, ' is not defined in ', _absolute_default_config_file_name)
        raise err


def subtle_path():
    return _get_setting(_subtle_path_key)


def split_criterion():
    return _get_setting(_split_criterion_key)


def kb_file():
    return _get_setting(_kb_file_key)


def s_file():
    return _get_setting(_s_file_key)


def bg_file():
    return _get_setting(_bg_file_key)


try:
    with open(_absolute_default_config_file_name, "r") as config_file:
        print("Reading configuration from: ", _absolute_default_config_file_name)
        _config_file_data = json.load(config_file)

except FileNotFoundError:
    # doesn't exist; write default config
    print("No config file existed at path: ", _absolute_default_config_file_name)
    with open(_absolute_default_config_file_name, "w") as ofile:
        json.dump(_default_settings, ofile, indent=4)

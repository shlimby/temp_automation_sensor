import json
from os import read

SETTING_URL = 'settings.json'

def get_settings():
    """Read settings file and return decoded object"""
    return json.loads(open(SETTING_URL, "r").read())

def set_settings(settings:object):
    """Overwrite settings with given object"""

    # write settings in a nice way
    with open(SETTING_URL, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)
    
    
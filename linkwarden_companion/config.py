import os
import shutil
import logging
import configparser

CONFIG_FILE_PATH = None
DEFAULT_CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'default_config.ini')
if os.name == 'posix':
    CONFIG_FILE_PATH = os.path.expanduser('~/.local/linkwarden_companion/config.ini')
elif os.name == 'nt':
    CONFIG_FILE_PATH = os.path.join(os.getenv('APPDATA'), 'linkwarden_companion', 'config.ini')


class LinkwardenCompanionConfig(configparser.ConfigParser):
    logger = logging.getLogger("linkwarden_companion")

    def save(self):
        handle = open(CONFIG_FILE_PATH, 'w')
        super().write(handle)
        handle.close()


os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)

if not os.path.exists(CONFIG_FILE_PATH):
    # copy default
    shutil.copy(DEFAULT_CONFIG_FILE_PATH, CONFIG_FILE_PATH)

# ensure the config file has all the required sections, and keys
default_config = configparser.ConfigParser()
default_config.read(DEFAULT_CONFIG_FILE_PATH)
LINKWARDEN_COMPANION_CONFIG = LinkwardenCompanionConfig()
LINKWARDEN_COMPANION_CONFIG.read(CONFIG_FILE_PATH)
for section in default_config.sections():
    if section not in LINKWARDEN_COMPANION_CONFIG:
        logging.debug(f"Adding missing section '{section}'")
        LINKWARDEN_COMPANION_CONFIG[section] = {}
    for key, value in default_config.items(section):
        if key not in LINKWARDEN_COMPANION_CONFIG[section].keys():
            logging.debug(f"Adding missing key '{key}' to section '{section}'")
            LINKWARDEN_COMPANION_CONFIG[section][key] = value
LINKWARDEN_COMPANION_CONFIG.save()

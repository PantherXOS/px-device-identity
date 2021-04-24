'''Configuration'''

from pathlib import Path

from appdirs import user_data_dir


KEY_DIR_LEGACY = str(Path.home()) + '/.config/device/'
KEY_DIR = user_data_dir("px-device-identity") + '/'

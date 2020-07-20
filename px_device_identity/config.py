import yaml
from pathlib import Path

from .log import Logger
from .filesystem import Filesystem

log = Logger('CONFIG')

def KEY_DIR():
    home_path = str(Path.home())
    key_dir = '/.config/device/'
    return home_path + key_dir

def CONFIG_DIR():
    return '/etc/px-device-identity/'

def get_device_config():
    log.info('Loading device config from {}.'.format(CONFIG_DIR()))
    fs = Filesystem(CONFIG_DIR(), 'device.yml', 'r')
    file = fs.open_file()
    config = yaml.load(file, Loader=yaml.BaseLoader)
    cfg_device = {
        'id': config.get('id'),
        'deviceType': config.get('deviceType'),
        'keySecurity': config.get('keySecurity'),
        'keyType': config.get('keyType'),
        'isManaged': config.get('isManaged'),
        'host': config.get('host'),
        'configVersion': config.get('configVersion'),
        'initiatedOn': config.get('initiatedOn')
    }
    return cfg_device


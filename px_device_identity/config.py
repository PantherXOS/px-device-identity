import yaml
from .log import Logger
from .util import CONFIG_DIR
from .filesystem import Filesystem

log = Logger('CONFIG')

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


'''Configuration'''

import logging
import platform
from datetime import datetime
from pathlib import Path

import yaml
from appdirs import user_config_dir, user_data_dir

from .classes import DeviceProperties
from .config_schema import CONFIG_SCHEMA

log = logging.getLogger(__name__)
opsys = platform.system()

KEY_DIR_LEGACY = str(Path.home()) + '/.config/device/'
KEY_DIR = user_data_dir("px-device-identity") + '/'

# Important note on CONFIG_DIR
# On Linux we default to `/etc/px-devide-identity/device.yml`
# On Windows we fall-back to whatever's the system default

CONFIG_DIR = '/etc/px-device-identity/'
if opsys == 'Windows':
    CONFIG_DIR = user_config_dir("px-device-identity") + '/'

CONFIG_FILE = CONFIG_DIR + 'device.yml'
CONFIG_VERSION = '0.0.3'


class DeviceConfig():
    '''Primary configuration'''
    def __init__(self):
        self.config_path = CONFIG_FILE
        self.config_schema = CONFIG_SCHEMA
        self.latest_version = CONFIG_VERSION

    def _is_latest_version(self, config):
        return self.latest_version == config['configVersion']

    def _get_config_from_dict(self, config: dict, version: str):
        device_properties = DeviceProperties(
            title=config['title'],
            location=config['location'],
            role=config['role'],
            key_security=config['key_security'],
            key_type=config['key_type'],
            domain=config['domain'],
            host=config['host'],
            id=config['id'],
            client_id=config['client_id'],
            is_managed=config['is_managed']
        )
        return device_properties

    def _save_config_to_file(self, config):
        log.info("=> Saving device identification in {}".format(
            self.config_path
        ))
        with open(self.config_path, 'w') as fs_device_writer:
            fs_device_writer.write(yaml.dump(config))

    def _load_yaml_from_file(self):
        log.debug('=> Loading device config from {}.'.format(self.config_path))
        with open(self.config_path, 'r') as fs_reader:
            file = fs_reader.read()
            return yaml.load(file, Loader=yaml.BaseLoader)

    def migrate_config(self, from_version: str, to_version):
        '''Migrate config between versions (UP only)'''
        config = self._load_yaml_from_file()
        device_config = self._get_config_from_dict(config, from_version)

        for key in self.config_schema[to_version]:
            value = self.config_schema[to_version][key]
            if key == 'NONE':
                print(
                    'Config line |{}| is new in v{}. Please enter a value or leave empty. \
                        Proceed with [ENTER]'.format(value, self.latest_version)
                )
                user_input = input("Enter a {}: ".format(value))
                device_config[value] = user_input
            elif key == 'configVersion':
                device_config[value] = self.latest_version
            else:
                device_config[value] = config[value]

        self._save_config_to_file(device_config)

    def save(self, properties: DeviceProperties):
        try:
            config = {
                'title': properties.title,
                'location': properties.location,
                'role': properties.role,
                'key_security': properties.key_security,
                'key_type': properties.key_type,
                'domain': properties.domain,
                'host': properties.host,
                'id': properties.id,
                'client_id': properties.client_id,
                'is_managed': properties.is_managed,
                'config_version': self.latest_version,
                'initiated_on': str(datetime.now())
            }
            self._save_config_to_file(config)
        except Exception as err:
            log.warning(err)
            raise err

    def get(self):
        '''Get config'''
        config = self._load_yaml_from_file()
        return self._get_config_from_dict(config, config['config_version'])

def get_device_config():
    '''LEGACY! Get config'''
    return DeviceConfig().get()

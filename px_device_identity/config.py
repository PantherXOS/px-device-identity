'''Configuration'''

from pathlib import Path
import yaml
from appdirs import user_data_dir

from .log import Logger
from .config_schema import CONFIG_SCHEMA

log = Logger(__name__)

KEY_DIR_LEGACY = str(Path.home()) + '/.config/device/'
KEY_DIR = user_data_dir("px-device-identity") + '/'
CONFIG_DIR = '/etc/px-device-identity/'
CONFIG_FILE = CONFIG_DIR + 'device.yml'
CONFIG_VERSION = '0.0.2'


class DeviceConfig():
    '''Primary configuration'''
    def __init__(self):
        self.config_path = CONFIG_FILE
        self.config_schema = CONFIG_SCHEMA
        self.latest_version = CONFIG_VERSION

    def _is_latest_version(self, config):
        return self.latest_version == config['configVersion']

    def _get_config_from_dict(self, config: dict, version: str):
        device_config = {}
        for key in self.config_schema[version]:
            device_config[
                self.config_schema[version][key]
            ] = config[self.config_schema[version][key]]
        return device_config

    def _save_config_to_file(self, config):
        with open(self.config_path, 'w') as fs_device_writer:
            fs_device_writer.write(yaml.dump(config))

    def _load_yaml_from_file(self):
        print('=> Loading device config from {}.'.format(self.config_path))
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

    def get(self):
        '''Get config'''
        config = self._load_yaml_from_file()
        return self._get_config_from_dict(config, config['configVersion'])
        # if self._is_latest_version(config):

def get_device_config():
    '''LEGACY! Get config'''
    return DeviceConfig().get()

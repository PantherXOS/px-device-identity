"""Configuration"""

import logging
import platform
from datetime import datetime
from pathlib import Path

import yaml
from appdirs import user_config_dir, user_data_dir

from .classes import DeviceProperties

log = logging.getLogger(__name__)
opsys = platform.system()

KEY_DIR_LEGACY = str(Path.home()) + "/.config/device"
KEY_DIR = user_data_dir("px-device-identity")

# Important note on CONFIG_DIR
# On Linux we default to `/etc/px-devide-identity/device.yml`
# On Windows we fall-back to whatever's the system default

CONFIG_DIR = "/etc/px-device-identity"
if opsys == "Windows":
    CONFIG_DIR = user_config_dir("px-device-identity")

CONFIG_FILE_NAME = "device.yml"
CONFIG_FILE = CONFIG_DIR + "/" + CONFIG_FILE_NAME
CONFIG_VERSION = "0.0.3"

# for device.cache
ACCESS_TOKEN_CACHE = KEY_DIR + "device_access_token"


class DeviceConfig:
    """Primary configuration"""

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.latest_version = CONFIG_VERSION

    def _is_latest_version(self, config):
        return self.latest_version == config["configVersion"]

    def _get_config_from_dict(self, config: dict, version: str):
        device_properties = DeviceProperties(
            title=config["title"],
            location=config["location"],
            role=config["role"],
            key_security=config["key_security"],
            key_type=config["key_type"],
            domain=config["domain"],
            host=config["host"],
            id=config["id"],
            client_id=config["client_id"],
            is_managed=config["is_managed"],
        )
        return device_properties

    def _save_config_to_file(self, config):
        log.info("=> Saving device identification in %s", self.config_path)
        with open(self.config_path, "w", encoding="utf-8") as fs_device_writer:
            fs_device_writer.write(yaml.dump(config))

    def _load_yaml_from_file(self):
        log.debug("=> Loading device config from %s", self.config_path)
        with open(self.config_path, "r", encoding="utf-8") as fs_reader:
            file = fs_reader.read()
            return yaml.load(file, Loader=yaml.BaseLoader)

    def save(self, properties: DeviceProperties):
        try:
            config = {
                "title": properties.title,
                "location": properties.location,
                "role": properties.role,
                "key_security": properties.key_security,
                "key_type": properties.key_type,
                "domain": properties.domain,
                "host": properties.host,
                "id": properties.id,
                "client_id": properties.client_id,
                "is_managed": properties.is_managed,
                "config_version": self.latest_version,
                "initiated_on": str(datetime.now()),
            }
            self._save_config_to_file(config)
        except Exception as err:
            log.warning(err)
            raise err

    def get(self):
        """Get config"""
        config = self._load_yaml_from_file()
        return self._get_config_from_dict(config, config["config_version"])

import logging
from base64 import urlsafe_b64decode, urlsafe_b64encode
from px_device_identity.errors import NotInitiated

import os
from .config import CONFIG_DIR, CONFIG_FILE_NAME, KEY_DIR, DeviceConfig

log = logging.getLogger(__name__)


def is_initiated(key_dir: str = KEY_DIR, config_dir: str = CONFIG_DIR) -> bool:
    '''Checks whether the device has already been initiated
        returns: bool
    '''
    config_file = config_dir + "/" + CONFIG_FILE_NAME

    try:
        if os.path.isfile(config_file):
            # If config exists, try to initiate it
            DeviceConfig(config_path=config_file).get()
            return True

        log.info("No device configuration found at {}.".format(config_file))

        return False
    except Exception as err:
        log.error(err)
        return False


def b64encode(string: bytes) -> str:
    '''base64 encode'''
    s_bin = urlsafe_b64encode(string)
    s_bin = s_bin.replace(b'=', b'')
    return s_bin.decode('ascii')


def b64decode(string: str) -> bytes:
    '''base64 decode'''
    s_bin = string.encode('ascii')
    s_bin += b'=' * (4 - len(s_bin) % 4)
    return urlsafe_b64decode(s_bin)


def split_key_type(key: str):
    '''Split key string
        raise: ValueError
    '''
    key_array = key.split(":")
    key_cryptography = key_array[0]
    if key_cryptography == 'RSA':
        key_strength = int(key_array[1])
    elif key_cryptography == 'ECC':
        key_strength = key_array[1]
    else:
        raise ValueError('Unexpected key format.')
    return key_cryptography, key_strength

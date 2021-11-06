import logging
from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Union

from px_device_identity.errors import NotInitiated

import os
from .config import CONFIG_FILE, KEY_DIR, DeviceConfig

log = logging.getLogger(__name__)


def is_initiated(key_dir: str = KEY_DIR, config_path: str = CONFIG_FILE) -> bool:
    '''Checks whether the device has already been initiated
        returns: bool
    '''
    try:
        # Here we try to load the config to see if it exists.
        DeviceConfig(config_path=config_path).get()
        public_key_path = str(key_dir) + 'public.pem'
        if not os.path.isfile:
            raise IOError('Could not find {}.'.format(public_key_path))
        return True
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

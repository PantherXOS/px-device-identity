import logging
import os
import time

import yaml
from px_device_identity.errors import (
    AccessTokenCacheExpired,
    AccessTokenCacheNotFound
)

from .config import KEY_DIR

ACCESS_TOKEN_CACHE = KEY_DIR + 'device_access_token'

log = logging.getLogger(__name__)


def set_device_access_token_cache(access_token: dict, path: str = ACCESS_TOKEN_CACHE):
    '''Write device_access_token to file'''
    with open(path, 'w') as writer:
        writer.write(yaml.dump(access_token))


def get_device_access_token_cache(path: str = ACCESS_TOKEN_CACHE):
    '''Get device_access_token from file
        1. Checks if file exists
        2. Checks if token is valid

        raise: AccessTokenCacheNotFound()
    '''
    if not os.path.isfile(path):
        log.info('Device access token cache not found.')
        raise AccessTokenCacheNotFound()

    access_token = None
    with open(path, 'r') as reader:
        file = reader.read()
        content = yaml.load(file, Loader=yaml.BaseLoader)
        access_token = {
            'access_token': content['access_token'],
            'expires_at': int(content['expires_at']),
        }

    current_time = int(time.time())
    expiration_time = access_token['expires_at'] - 100

    if current_time > expiration_time:
        time_difference = current_time - expiration_time
        raise AccessTokenCacheExpired(
            'Device access token cache expired {}s ago'.format(time_difference)
        )
    else:
        return access_token

import logging
import os
import time

import yaml
from px_device_identity.errors import (AccessTokenCacheExpired,
                                       AccessTokenCacheNotFound)

from .config import ACCESS_TOKEN_CACHE

log = logging.getLogger(__name__)


def get_path(path: str, aud: str):
    if aud == '/oidc/token/introspection':
        return path + '_introspection'
    else:
        return path


def set_device_access_token_cache(access_token_dict: dict, path: str = ACCESS_TOKEN_CACHE, aud: str = '/oidc/token'):
    '''Write device_access_token to file'''
    with open(get_path(path, aud), 'w') as writer:
        writer.write(yaml.dump(access_token_dict))


def get_device_access_token_cache(path: str = ACCESS_TOKEN_CACHE, aud: str = '/oidc/token'):
    '''Get device_access_token from file
        1. Checks if file exists
        2. Checks if token is valid

        raise: AccessTokenCacheNotFound()
    '''
    path_by_aud = get_path(path, aud)
    if not os.path.isfile(path_by_aud):
        log.info('Device access token cache not found.')
        raise AccessTokenCacheNotFound()

    access_token_dict = None
    with open(path_by_aud, 'r') as reader:
        file = reader.read()
        content = yaml.load(file, Loader=yaml.BaseLoader)
        access_token_dict = {
            'access_token': content['access_token'],
            'expires_at': int(content['expires_at']),
        }

    current_time = int(time.time())
    expiration_time = access_token_dict['expires_at'] - 100

    if current_time > expiration_time:
        time_difference = current_time - expiration_time
        raise AccessTokenCacheExpired(
            'Device access token cache expired {}s ago'.format(time_difference)
        )
    else:
        return access_token_dict

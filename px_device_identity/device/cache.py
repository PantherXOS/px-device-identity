import logging
import os
import time

import yaml

from .config import KEY_DIR

ACCESS_TOKEN_CACHE = KEY_DIR + 'device_access_token'

log = logging.getLogger(__name__)


def set_device_access_token_cache(access_token):
	'''Write device_access_token to file'''
	with open(ACCESS_TOKEN_CACHE, 'w') as writer:
		writer.write(yaml.dump(access_token))

def get_device_access_token_cache():
	'''Get device_access_token from file or return False'''
	if os.path.isfile(ACCESS_TOKEN_CACHE):
		access_token = None
		with open(ACCESS_TOKEN_CACHE, 'r') as reader:
			file = reader.read()
			content = yaml.load(file, Loader=yaml.BaseLoader)
			access_token = {
				'access_token': content['access_token'],
				'expires_at': int(content['expires_at']),
			}

		current_time = time.time()
		# We request a new key long before the old expires
		expiration_time = access_token['expires_at'] - 500
		
		if current_time > expiration_time:
			log.info('current time: {}'.format(current_time))
			log.info('expiration time: {}'.format(expiration_time))
			log.info('Device access_token cache expired.')
			return False
		else:
			log.info('Device access_token cache found.')
			return access_token
	else:
		log.info('Device access_token cache does not exist.')
		return False

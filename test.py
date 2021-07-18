import os
import yaml
import time

KEY_DIR = '/root/.local/share/px-device-identity/'
JWT_CACHE_FILE = KEY_DIR + 'device_jwt'


def set_device_jwt_cache(jwt):
	print('=> Set cache')
	with open(JWT_CACHE_FILE, 'w') as writer:
		writer.write(yaml.dump(jwt))

def get_device_jwt_cache():
	if os.path.isfile(JWT_CACHE_FILE):
		jwt = None
		with open(JWT_CACHE_FILE, 'r') as reader:
			file = reader.read()
			jwt = yaml.load(file, Loader=yaml.BaseLoader)

		current_time = time.time()
		expiration_time = int(jwt['exp']) - 100
		
		if current_time > expiration_time:
			print('Cache expired.')
			return False
		else:
			print('Cache found.')
			return jwt
	else:
		print('Cache does not exist.')
		return False



def get_device_jwt():
	cache = get_device_jwt_cache()
	if cache:
		return cache
	else:
		# do all the things
		response = {
			'device_jwt': 'abc-def',
			'iat': int(time.time()),
			'exp': int(time.time()) + 300
		}
		set_device_jwt_cache(response)

		return response

	
print(get_device_jwt())
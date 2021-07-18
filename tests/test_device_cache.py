import unittest
import time
import os
from px_device_identity.device.cache import set_device_access_token_cache, get_device_access_token_cache, ACCESS_TOKEN_CACHE

DATA = {
    'new_cache': {
        'access_token': '3f30e4c5-f86f-4e36-9e20-fe57c9732cdb',
        'expires_at': int(time.time()) + 3000
    },
    'cache_expired': {
        'access_token': '38837def-01cc-49e2-96fa-cb515c796a72',
        'expires_at': int(time.time())
    }
}


class TestDeviceCache(unittest.TestCase):
    def test_new_cache(self):
        if os.path.isfile(ACCESS_TOKEN_CACHE):
            os.remove(ACCESS_TOKEN_CACHE)
        data = DATA['new_cache']
        set_device_access_token_cache(data)
        result = get_device_access_token_cache()
        if result:
            self.assertEqual(result['expires_at'], data['expires_at'])
        else:
            self.fail()

    def test_expired(self):
        if os.path.isfile(ACCESS_TOKEN_CACHE):
            os.remove(ACCESS_TOKEN_CACHE)
        data = DATA['cache_expired']
        set_device_access_token_cache(data)
        result = get_device_access_token_cache()
        self.assertEqual(result, False)

    def test_overwrite_cache(self):
        if os.path.isfile(ACCESS_TOKEN_CACHE):
            os.remove(ACCESS_TOKEN_CACHE)
        data = DATA['new_cache']
        set_device_access_token_cache(data)
        result = get_device_access_token_cache()
        self.assertEqual(result, data)
        data_later = DATA['new_cache']
        set_device_access_token_cache(data_later)
        result_later = get_device_access_token_cache()
        if result_later:
            self.assertEqual(
                result_later['expires_at'], data_later['expires_at'])
        else:
            self.fail()

import unittest
import time
import os
from px_device_identity.device.cache import set_device_access_token_cache, get_device_access_token_cache
from px_device_identity.errors import AccessTokenCacheExpired
import shutil

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


file_dir = '/tmp/px_device_identity_test_cache/'
cache_path = file_dir + 'device_access_token'


class TestDeviceCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(file_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(file_dir)

    def test_new_cache(self):
        data = DATA['new_cache']
        set_device_access_token_cache(data, cache_path)
        result = get_device_access_token_cache(cache_path)
        if result:
            self.assertEqual(result['expires_at'], data['expires_at'])
        else:
            self.fail()

    def test_expired(self):
        data = DATA['cache_expired']
        set_device_access_token_cache(data, cache_path)
        with self.assertRaises(AccessTokenCacheExpired):
            get_device_access_token_cache(cache_path)

    def test_overwrite_cache(self):
        data = DATA['new_cache']
        set_device_access_token_cache(data, cache_path)
        result = get_device_access_token_cache(cache_path)
        self.assertEqual(result, data)
        data_later = DATA['new_cache']
        set_device_access_token_cache(data_later, cache_path)
        result_later = get_device_access_token_cache(cache_path)
        if result_later:
            self.assertEqual(
                result_later['expires_at'], data_later['expires_at'])
        else:
            self.fail()

import unittest
import time
import os
from px_device_identity.device import Device
from px_device_identity.device.cache import ACCESS_TOKEN_CACHE


class TestDeviceCache(unittest.TestCase):
    def test_get_device_jwt(self):
        jwt = Device().get_device_jwt()
        self.assertIsNotNone(jwt['device_jwt'])
        # we add a second, just to be sure
        current_time = int(time.time()) + 10
        self.assertGreater(jwt['exp'], current_time)

    def test_get_new_device_jwt(self):
        if os.path.isfile(ACCESS_TOKEN_CACHE):
            os.remove(ACCESS_TOKEN_CACHE)
        jwt = Device().get_device_jwt()
        self.assertIsNotNone(jwt['device_jwt'])
        # we add a second, just to be sure
        current_time = int(time.time()) + 10
        self.assertGreater(jwt['exp'], current_time)

    def test_get_access_token(self):
        if os.path.isfile(ACCESS_TOKEN_CACHE):
            os.remove(ACCESS_TOKEN_CACHE)
        access_token = Device().get_access_token()
        self.assertIsNotNone(access_token)

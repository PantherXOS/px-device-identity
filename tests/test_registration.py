import unittest
import time
import os
from px_device_identity import DeviceProperties
from px_device_identity.device import Device
import shutil


file_dir = '/tmp/px_device_identity_test_registration/'
cache_path = file_dir + 'device_access_token'
key_dir = file_dir + 'keys/'
config_dir = file_dir + 'config/'
config_path = config_dir + 'device.yml'


class TestDevice(unittest.TestCase):
    @classmethod
    def setUp(cls):
        if os.path.isdir(file_dir):
            shutil.rmtree(file_dir)
        os.makedirs(file_dir)

    @classmethod
    def tearDown(cls):
        if os.path.isdir(file_dir):
            shutil.rmtree(file_dir)
        os.makedirs(file_dir)

    def test_registration(self):
        device = Device(
            key_dir=key_dir, config_dir=config_dir, config_path=config_path
        )
        properties = DeviceProperties(
            'Test device',
            'Earth',
            'desktop',
            'default',
            'RSA:2048',
            'pantherx.org',
            'http://127.0.0.1:4000'
        )
        device.init(properties)

    def test_registration_and_properties(self):
        device = Device(
            key_dir=key_dir, config_dir=config_dir, config_path=config_path, overwrite=True
        )
        properties = DeviceProperties(
            'Test device #2',
            'Earth',
            'desktop',
            'default',
            'RSA:2048',
            'pantherx.org',
            'http://127.0.0.1:4000',
        )
        device.init(properties)

        '''JWT'''
        jwt = Device(
            key_dir=key_dir, config_dir=config_dir, config_path=config_path
        ).get_device_jwt()
        self.assertIsNotNone(jwt['device_jwt'])
        # we add a second, just to be sure
        current_time = int(time.time()) + 10
        self.assertGreater(jwt['exp'], current_time)

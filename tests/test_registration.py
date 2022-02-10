from px_device_identity.classes import OperationProperties
from px_device_identity.device.config import DeviceConfig
import unittest
import time
import os
from px_device_identity.main import main
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
        # Test if device class initiates properly
        device = Device(
            key_dir=key_dir, config_dir=config_dir, config_path=config_path
        )

        self.assertEqual(device.is_initiated, False)
        self.assertEqual(device.properties, None)
        self.assertEqual(device.overwrite, False)

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

        # Test if device initiates with new config
        device_test = Device(
            key_dir=key_dir, config_dir=config_dir, config_path=config_path
        )

        self.assertEqual(device_test.is_initiated, True)
        self.assertEqual(device_test.properties, properties)
        self.assertEqual(device_test.overwrite, False)

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

        device_config = DeviceConfig(config_path).get()

        self.assertEqual(device_config.title, properties.title)
        self.assertEqual(device_config.location, properties.location)
        self.assertEqual(device_config.role, properties.role)
        self.assertEqual(device_config.domain, properties.domain)
        self.assertEqual(device_config.host, properties.host)

        # Test main
        cl_arguments_Jwk = {
            'operation': OperationProperties(
                'GET_JWK',
                False
            ),
            'device_properties': device_config,
            'message': None,
            'debug': False
        }
        jwk_from_main = main(cl_arguments_Jwk)
        self.assertIsNot(jwk_from_main, None)

        cl_arguments_Jwks = {
            'operation': OperationProperties(
                'GET_JWKS',
                False
            ),
            'device_properties': device_config,
            'message': None,
            'debug': False
        }
        jwks_from_main = main(cl_arguments_Jwks)
        self.assertIsNot(jwks_from_main, None)

        cl_arguments_sign = {
            'operation': OperationProperties(
                'SIGN',
                False
            ),
            'device_properties': device_config,
            'message': 'Some message',
            'debug': False
        }
        sign_from_main = main(cl_arguments_sign)
        self.assertIsNot(sign_from_main, None)

        cl_arguments_access_token = {
            'operation': OperationProperties(
                'GET_ACCESS_TOKEN',
                False
            ),
            'device_properties': device_config,
            'message': None,
            'debug': False
        }
        access_token_from_main = main(cl_arguments_access_token)
        self.assertIsNot(access_token_from_main, None)

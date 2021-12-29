import unittest
import time
import os
import json
from px_device_identity.device import Device
from px_device_identity.device.cache import ACCESS_TOKEN_CACHE

file_dir = '/tmp/px_device_identity_test_device/'
cache_path = file_dir + 'device_access_token'


class TestRegistration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.isfile(ACCESS_TOKEN_CACHE):
            os.remove(ACCESS_TOKEN_CACHE)

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(ACCESS_TOKEN_CACHE):
            os.remove(ACCESS_TOKEN_CACHE)

    def test_get_new_device_jwt(self):
        '''JWT'''
        jwt = Device().get_device_jwt()
        self.assertIsNotNone(jwt['device_jwt'])
        # we add a second, just to be sure
        current_time = int(time.time()) + 10
        self.assertGreater(jwt['exp'], current_time)

    def test_get_new_device_jwt_from_cache(self):
        '''JWT'''
        jwt = Device().get_device_jwt()
        self.assertIsNotNone(jwt['device_jwt'])
        # we add a second, just to be sure
        current_time = int(time.time()) + 10
        self.assertGreater(jwt['exp'], current_time)
        # try again with cache set
        jwt = Device().get_device_jwt()
        self.assertIsNotNone(jwt['device_jwt'])
        # we add a second, just to be sure
        current_time = int(time.time()) + 10
        self.assertGreater(jwt['exp'], current_time)

    def test_get_new_device_jwk(self):
        '''GET_JWK'''
        jwk = Device().get_jwk()
        self.assertIsNotNone(jwk)

    def test_get_new_device_jwks(self):
        '''GET_JWKS'''
        jwks = Device().get_jwks()
        self.assertIsNotNone(jwks)

    def test_get_access_token(self):
        '''GET_ACCESS_TOKEN'''
        access_token = Device().get_access_token()
        self.assertIsNotNone(access_token)

    def test_get_access_token_from_cache(self):
        '''GET_ACCESS_TOKEN'''
        access_token = Device().get_access_token()
        self.assertIsNotNone(access_token)
        # try again with cache set
        access_token = Device().get_access_token()
        self.assertIsNotNone(access_token)

    def test_sign(self):
        '''SIGN'''
        message = 'Test'
        signed = Device().sign(message)
        self.assertIsNotNone(signed)

    def test_introspection(self):
        user_access_token = os.environ['PX_DEVICE_IDENTITY_INTROSPECTION_TEST_TOKEN']
        result = Device().token_introspection(user_access_token)
        try:
            self.assertEqual(
                result['active'], True
            )
        except:
            self.fail(
                'It looks like the PX_DEVICE_IDENTITY_INTROSPECTION_TEST_TOKEN has expired.'
            )

    def test_introspection_fail(self):
        user_access_token = 'HGIvr8n-MHN8bQcPUPqIztW6FRSUJ_Nvz0gf0L074kU'
        result = Device().token_introspection(user_access_token)
        self.assertEqual(
            result['active'], False
        )

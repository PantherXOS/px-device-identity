import unittest
from px_device_identity.device.crypto import Crypto
from px_device_identity.device.classes import DeviceProperties
import os
import shutil


file_dir = '/tmp/px_device_identity_test_crypto/'
private_key_path = '{}private.pem'.format(file_dir)
public_key_path = '{}/public.pem'.format(file_dir)


class TestCrypto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs(file_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(file_dir)

    def test_generate_private_key(self):
        properties = DeviceProperties(
            'Undefined',
            'Earth',
            'desktop',
            'default',
            'RSA:2048',
            'domain.com',
            'https://identity.domain.com',
            'fc795cbd-3a70-49b7-90b6-2da32598df66',
            '8e63efc0-c07a-4b20-815c-d4b5e763e800',
            True
        )
        crypto = Crypto(properties, file_dir)
        private_key = crypto.generate_private_key()
        self.assertIsNotNone(private_key)

    def test_generate_private_key_ECC(self):
        properties = DeviceProperties(
            'Undefined',
            'Earth',
            'desktop',
            'default',
            'ECC:p256',
            'domain.com',
            'https://identity.domain.com',
            'fc795cbd-3a70-49b7-90b6-2da32598df66',
            '8e63efc0-c07a-4b20-815c-d4b5e763e800',
            True
        )
        crypto = Crypto(properties, file_dir)
        private_key = crypto.generate_private_key()
        self.assertIsNotNone(private_key)

    def test_generate_private_key_tpm(self):
        properties = DeviceProperties(
            'Undefined',
            'Earth',
            'desktop',
            'tpm',
            'RSA:2048',
            'domain.com',
            'https://identity.domain.com',
            'fc795cbd-3a70-49b7-90b6-2da32598df66',
            '8e63efc0-c07a-4b20-815c-d4b5e763e800',
            True
        )
        crypto = Crypto(properties, file_dir)
        crypto.generate_private_key()
        private_key_exists = os.path.isfile(crypto.private_key_path)
        self.assertTrue(private_key_exists)

    def test_generate_private_key_tpm_ECC(self):
        properties = DeviceProperties(
            'Undefined',
            'Earth',
            'desktop',
            'tpm',
            'ECC:p256',
            'domain.com',
            'https://identity.domain.com',
            'fc795cbd-3a70-49b7-90b6-2da32598df66',
            '8e63efc0-c07a-4b20-815c-d4b5e763e800',
            True
        )
        crypto = Crypto(properties, file_dir)
        crypto.generate_private_key()
        private_key_exists = os.path.isfile(crypto.private_key_path)
        self.assertTrue(private_key_exists)

    def test_generate_and_save_to_key_path_RSA(self):
        properties = DeviceProperties(
            'Undefined',
            'Earth',
            'desktop',
            'default',
            'RSA:2048',
            'domain.com',
            'https://identity.domain.com',
            'fc795cbd-3a70-49b7-90b6-2da32598df66',
            '8e63efc0-c07a-4b20-815c-d4b5e763e800',
            True
        )
        crypto = Crypto(properties, file_dir)
        crypto.generate_and_save_to_key_path()
        private_key_exists = os.path.isfile(crypto.private_key_path)
        private_key_exists_verify = os.path.isfile(private_key_path)
        public_key_exists = os.path.isfile(crypto.private_key_path)
        self.assertTrue(private_key_exists)
        self.assertTrue(private_key_exists_verify)
        self.assertTrue(public_key_exists)

    def test_generate_and_save_to_key_path_ECC(self):
        properties = DeviceProperties(
            'Undefined',
            'Earth',
            'desktop',
            'default',
            'ECC:p256',
            'domain.com',
            'https://identity.domain.com',
            'fc795cbd-3a70-49b7-90b6-2da32598df66',
            '8e63efc0-c07a-4b20-815c-d4b5e763e800',
            True
        )
        crypto = Crypto(properties, file_dir)
        crypto.generate_and_save_to_key_path()
        private_key_exists = os.path.isfile(crypto.private_key_path)
        private_key_exists_verify = os.path.isfile(private_key_path)
        public_key_exists = os.path.isfile(crypto.private_key_path)
        self.assertTrue(private_key_exists)
        self.assertTrue(private_key_exists_verify)
        self.assertTrue(public_key_exists)

    def test_generate_and_save_to_key_path_tpm_RSA(self):
        properties = DeviceProperties(
            'Undefined',
            'Earth',
            'desktop',
            'tpm',
            'RSA:2048',
            'domain.com',
            'https://identity.domain.com',
            'fc795cbd-3a70-49b7-90b6-2da32598df66',
            '8e63efc0-c07a-4b20-815c-d4b5e763e800',
            True
        )
        crypto = Crypto(properties, file_dir)
        crypto.generate_and_save_to_key_path()
        private_key_exists = os.path.isfile(crypto.private_key_path)
        private_key_exists_verify = os.path.isfile(private_key_path)
        public_key_exists = os.path.isfile(crypto.private_key_path)
        self.assertTrue(private_key_exists)
        self.assertTrue(private_key_exists_verify)
        self.assertTrue(public_key_exists)

    def test_generate_and_save_to_key_path_tpm_ECC(self):
        properties = DeviceProperties(
            'Undefined',
            'Earth',
            'desktop',
            'tpm',
            'ECC:p256',
            'domain.com',
            'https://identity.domain.com',
            'fc795cbd-3a70-49b7-90b6-2da32598df66',
            '8e63efc0-c07a-4b20-815c-d4b5e763e800',
            True
        )
        crypto = Crypto(properties, file_dir)
        crypto.generate_and_save_to_key_path()
        private_key_exists = os.path.isfile(crypto.private_key_path)
        private_key_exists_verify = os.path.isfile(private_key_path)
        public_key_exists = os.path.isfile(crypto.private_key_path)
        self.assertTrue(private_key_exists)
        self.assertTrue(private_key_exists_verify)
        self.assertTrue(public_key_exists)

import unittest
from px_device_identity.util import is_fqdn
from px_device_identity.device.util import split_key_type


class TestUtil(unittest.TestCase):
    # UTIL
    def test_is_fqdn(self):
        hostname = 'domain.com'
        is_domain = is_fqdn(hostname)
        self.assertTrue(is_domain)

    def test_is_fqdn_fail(self):
        hostname = '_domain.com'
        is_domain = is_fqdn(hostname)
        self.assertFalse(is_domain)

    # DEVICE/UTIL
    def test_split_key_type(self):
        key = 'RSA:2048'
        key_cryptography, key_strength = split_key_type(key)
        self.assertEqual(key_cryptography, 'RSA')
        self.assertEqual(key_strength, 2048)

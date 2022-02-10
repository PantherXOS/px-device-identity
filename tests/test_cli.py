import json
import os
import shutil
import unittest

from px_device_identity.cli import get_cl, get_cl_arguments

file_dir = '/tmp/px_device_identity_test_cli/'
register_config_json = file_dir + 'config.json'

params_props = {
    'title': 'Some title',
    'location': 'Some location',
    'role': 'OTHER',
    'key_security': 'TPM',
    'key_type': 'ECC:p384',
    'domain': 'domain.com',
    'host': 'https://identity.domain.com',
}


class TestCLI(unittest.TestCase):
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

    # UTIL
    def test_init_minimal(self):
        input_args = ['-o', 'INIT', '-a', params_props['host'],
                      '-dn', params_props['domain']
                      ]
        parsed_args = get_cl(input_args)
        res = get_cl_arguments(parsed_args, register_config_json)

        operation = res['operation']
        device_props = res['device_properties']
        message = res['message']
        debug = res['debug']

        self.assertEqual(operation.action, 'INIT')
        self.assertEqual(operation.force_operation, False)

        self.assertIsNotNone(device_props.title)
        self.assertEqual(device_props.location, 'Undefined')
        self.assertEqual(device_props.role, 'desktop')
        self.assertEqual(device_props.key_security, 'default')
        self.assertEqual(device_props.key_type, 'RSA:2048')
        self.assertEqual(device_props.domain, params_props['domain'])
        self.assertEqual(device_props.host, params_props['host'])

        self.assertIsNotNone(device_props.id)
        self.assertIsNone(device_props.client_id)
        self.assertEqual(device_props.is_managed, True)

        self.assertIsNone(message)

    def test_init_full(self):
        input_args = ['-o', 'INIT', '-a', params_props['host'],
                      '-dn', params_props['domain'],
                      '-s', params_props['key_security'],
                      '-k', params_props['key_type'],
                      '-t', params_props['title'],
                      '-l', params_props['location'],
                      '-r', params_props['role'],
                      '-f', 'TRUE',
                      '-d', 'FALSE'
                      ]
        parsed_args = get_cl(input_args)
        res = get_cl_arguments(parsed_args, register_config_json)

        operation = res['operation']
        device_props = res['device_properties']
        message = res['message']
        debug = res['debug']

        self.assertEqual(operation.action, 'INIT')
        self.assertEqual(operation.force_operation, True)

        self.assertIsNotNone(device_props.title)
        self.assertEqual(device_props.location, params_props['location'])
        self.assertEqual(device_props.role, params_props['role'].lower())
        self.assertEqual(
            device_props.key_security,
            params_props['key_security'].lower()
        )
        self.assertEqual(
            device_props.key_type,
            params_props['key_type']
        )
        self.assertEqual(device_props.domain, params_props['domain'])
        self.assertEqual(device_props.host, params_props['host'])

        self.assertIsNotNone(device_props.id)
        self.assertIsNone(device_props.client_id)
        self.assertEqual(device_props.is_managed, True)

        self.assertIsNone(message)

    def test_init_from_json(self):

        with open(register_config_json, 'w') as writer:
            writer.write(json.dumps({
                "type": "DESKTOP",
                "timezone": params_props['role'],
                "locale": "en_US.utf8",
                "title": params_props['title'],
                "location": params_props['location'],
                "role": params_props['role'],
                "key_security": params_props['key_security'],
                "key_type": params_props['key_type'],
                "domain": params_props['domain'],
                "host": params_props['host']
            }))

        input_args = [
            '-o', 'INIT_FROM_CONFIG', '-f', 'TRUE',
        ]
        parsed_args = get_cl(input_args)
        res = get_cl_arguments(parsed_args, register_config_json)

        operation = res['operation']
        device_props = res['device_properties']
        message = res['message']
        debug = res['debug']

        self.assertEqual(operation.action, 'INIT')
        self.assertEqual(operation.force_operation, True)

        self.assertIsNotNone(device_props.title)
        self.assertEqual(device_props.location, params_props['location'])
        self.assertEqual(device_props.role, params_props['role'].lower())
        self.assertEqual(
            device_props.key_security,
            params_props['key_security'].lower()
        )
        self.assertEqual(
            device_props.key_type,
            params_props['key_type']
        )
        self.assertEqual(device_props.domain, params_props['domain'])
        self.assertEqual(device_props.host, params_props['host'])

        self.assertIsNotNone(device_props.id)
        self.assertIsNone(device_props.client_id)
        self.assertEqual(device_props.is_managed, True)

        self.assertIsNone(message)

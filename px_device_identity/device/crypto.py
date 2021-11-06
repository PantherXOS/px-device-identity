import logging
import os

from Cryptodome.PublicKey import ECC, RSA
from px_device_identity.errors import CryptoGenError
from px_device_identity.util import run_commands

from .classes import DeviceProperties
from .config import KEY_DIR
from .util import split_key_type

log = logging.getLogger(__name__)


class Crypto:
    '''Handles RSA/ECC key generation'''

    def __init__(self, device_properties: 'DeviceProperties', key_dir=KEY_DIR):
        self.key_security = device_properties.key_security
        self.key_type = device_properties.key_type
        self.key_dir = key_dir
        self.private_key_path = key_dir + 'private.pem'
        self.public_key_path = key_dir + 'public.pem'

    def generate_private_key(self):
        '''Generate private key
            - 'default': returns key
            - 'tpm': saves private key
        '''
        key_cryptography, key_strength = split_key_type(self.key_type)
        log.info(
            '=> Generating new {} private key. This might take a moment ...'.format(
                self.key_type
            )
        )
        if self.key_security == 'default':
            '''Generate file-based Key'''
            if key_cryptography == 'RSA':
                return RSA.generate(bits=key_strength)
            elif key_cryptography == 'ECC':
                return ECC.generate(curve=key_strength)
        elif self.key_security == 'tpm':
            '''Generate TPM-based key'''

            if not os.path.isdir(self.key_dir):
                os.makedirs(self.key_dir)

            if key_cryptography == 'RSA':
                try:
                    commands = [
                        "tpm2tss-genkey",
                        "-a", "rsa",
                        "-s", str(key_strength),
                        self.private_key_path
                    ]
                    run_commands(commands)
                    log.info('Saved private key {}'.format(
                        self.private_key_path)
                    )
                except Exception as err:
                    log.error(err)
                    raise CryptoGenError(
                        'Could not generate RSA private key (TPM)'
                    )

            elif key_cryptography == 'ECC':
                key_strength_with_prefix = 'nist_' + str(key_strength)
                try:
                    commands = [
                        "tpm2tss-genkey",
                        "-a", "ecdsa",
                        "-c", str(key_strength_with_prefix),
                        self.private_key_path
                    ]
                    run_commands(commands)
                    log.info('Saved private key {}'.format(
                        self.private_key_path)
                    )
                except Exception as err:
                    log.error(err)
                    raise CryptoGenError(
                        'Could not generate ECC private key (TPM)'
                    )
            else:
                raise KeyError(
                    'Invalid key cryptography: {}'.format(
                        key_cryptography
                    )
                )
        else:
            raise KeyError(
                'Invalid key security: {}'.format(self.key_security)
            )

    def get_private_key_from_file(self):
        log.debug('=> Loading private key from file')
        try:
            with open(self.private_key_path, 'rb', buffering=0) as reader:
                return reader.read()
        except Exception as err:
            log.error(err)
            IOError('Could not read private key from {}'.format(
                    self.private_key_path
                    ))

    def get_public_key_from_private_key(self, key):
        key_cryptography = split_key_type(self.key_type)[0]
        log.debug('=> Loading {} public key from private key.'.format(
            key_cryptography))
        if key_cryptography == 'RSA':
            return key.publickey()
        elif key_cryptography == 'ECC':
            return key.public_key()

    def get_and_save_public_key_from_tpm_private_key(self):
        key_cryptography = split_key_type(self.key_type)[0]
        log.info(
            '=> Loading {} public key from TPM private key and saving as {}.'.format(
                key_cryptography, self.public_key_path)
        )
        if key_cryptography == 'RSA':
            try:
                commands = [
                    "openssl", "rsa",
                    "-engine", "tpm2tss",
                    "-inform", "engine",
                    "-in", self.private_key_path,
                    "-pubout", "-outform", "pem",
                    "-out", self.public_key_path
                ]
                run_commands(commands)
                log.debug('Saved public key {}'.format(
                    self.public_key_path)
                )
            except:
                raise CryptoGenError(
                    'Could not save public key from RSA TPM private key.'
                )
        elif key_cryptography == 'ECC':
            try:
                commands = [
                    "openssl", "ec",
                    "-engine", "tpm2tss",
                    "-inform", "engine",
                    "-in", self.private_key_path,
                    "-pubout", "-outform", "pem",
                    "-out", self.public_key_path
                ]
                run_commands(commands)
                log.debug('Saved public key {}'.format(
                    self.public_key_path)
                )
            except:
                raise CryptoGenError(
                    'Could not save public key from RSA TPM private key.'
                )

    def generate_and_save_to_key_path(self):
        key_cryptography = split_key_type(self.key_type)[0]

        if self.key_security == "default":
            private_key = self.generate_private_key()
            public_key = self.get_public_key_from_private_key(private_key)
            if not private_key or not public_key:
                raise ValueError('Could not generate file-based private key')

            private_key_pem = b''
            public_key_pem = b''
            if key_cryptography == 'RSA':
                private_key_pem = private_key.export_key(format='PEM')
                public_key_pem = public_key.export_key(format='PEM')
            elif key_cryptography == 'ECC':
                private_key_pem = private_key.export_key(
                    format='PEM'
                ).encode('utf8')
                public_key_pem = public_key.export_key(
                    format='PEM'
                ).encode('utf8')

            if not os.path.isdir(self.key_dir):
                os.makedirs(self.key_dir)

            with open(self.private_key_path, 'wb') as writer:
                writer.write(private_key_pem)

            with open(self.public_key_path, 'wb') as writer:
                writer.write(public_key_pem)

        elif self.key_security == "tpm":
            self.generate_private_key()
            self.get_and_save_public_key_from_tpm_private_key()
        else:
            raise ValueError(
                'Invalid key security. Expected `default` or `tpm`. Found {}'.format(
                    self.key_security
                )
            )

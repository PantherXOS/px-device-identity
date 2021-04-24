import logging
import os
import subprocess
import sys

from Cryptodome.PublicKey import ECC, RSA
from exitstatus import ExitStatus

from .classes import DeviceProperties
from .config import KEY_DIR
from .filesystem import Filesystem
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
        key_cryptography, key_strength = split_key_type(self.key_type)
        log.info(
            '=> Generating new {} private key. This might take a moment ...'.format(self.key_type)
        )
        if self.key_security == 'default':
            '''Generate file-based Key'''
            if key_cryptography == 'RSA':
                return RSA.generate(bits=key_strength)
            elif key_cryptography == 'ECC':
                return ECC.generate(curve=key_strength)
        elif self.key_security == 'tpm':
            '''Generate TPM-based key'''

            if os.path.isdir(KEY_DIR) == False:
                os.makedirs(KEY_DIR)

            if key_cryptography == 'RSA':
                try:
                    process_result = subprocess.run([
                        "tpm2tss-genkey",
                        "-a", "rsa",
                        "-s", str(key_strength),
                        self.private_key_path
                    ])
                    # TODO: Sanity check; look for response of process instead
                    if os.path.isfile(self.private_key_path):
                        log.info('Saved private key to {}'.format(self.private_key_path))
                        return True
                except EnvironmentError as err:
                    log.error(err)
                    raise err

            elif key_cryptography == 'ECC':
                key_strength = 'nist_' + str(key_strength)
                try:
                    process_result = subprocess.run([
                        "tpm2tss-genkey",
                        "-a", "ecdsa",
                        "-c", str(key_strength),
                        self.private_key_path
                    ])
                    if process_result.returncode == 1:
                        log.error('Could not get or save EC private key.')
                        sys.exit(ExitStatus)
                    # TODO: Sanity check; look for response of process instead
                    if os.path.isfile(self.private_key_path):
                        log.info('Saved private key {}'.format(self.private_key_path))
                        return True
                except EnvironmentError as err:
                    log.error(err)
                    raise err

        log.error('Could not generate TPM private key.')
        sys.exit(ExitStatus.failure)

    def get_private_key_from_file(self):
        log.debug('=> Loading private key from file')
        try:
            with open(self.private_key_path, 'rb', buffering=0) as reader:
                return reader.read()
        except:
            log.error('Could not read private key from {}'.format(self.private_key_path))
            sys.exit(ExitStatus.failure)

    def get_public_key_from_private_key(self, key):
        key_cryptography = split_key_type(self.key_type)[0]
        log.debug('=> Loading {} public key from private key.'.format(key_cryptography))
        if key_cryptography == 'RSA':
            return key.publickey()
        elif key_cryptography == 'ECC':
            return key.public_key()

    def get_and_save_public_key_from_tpm_private_key(self):
        key_cryptography = split_key_type(self.key_type)[0]
        log.info(
            '=> Loading {} public key from TPM private key and saving as {}.'.format(key_cryptography, self.public_key_path)
        )
        if key_cryptography == 'RSA':
            try:
                subprocess.run([
                    "openssl", "rsa",
                    "-engine", "tpm2tss",
                    "-inform", "engine",
                    "-in", self.private_key_path,
                    "-pubout", "-outform", "pem",
                    "-out", self.public_key_path
                ])
                # TODO: Sanity check; look for response of process instead
                if os.path.isfile(self.public_key_path):
                    log.debug('Saved public key {}'.format(self.public_key_path))
                    return True
            except:
                pass
        elif key_cryptography == 'ECC':
            try:
                subprocess.run([
                    "openssl", "ec",
                    "-engine", "tpm2tss",
                    "-inform", "engine",
                    "-in", self.private_key_path,
                    "-pubout", "-outform", "pem",
                    "-out", self.public_key_path
                ])
                # TODO: Sanity check; look for response of process instead
                if os.path.isfile(self.public_key_path):
                    log.debug('Saved public key {}'.format(self.public_key_path))
                    return True
            except:
                pass
        log.error('Could not save public key from TPM private key.')
        return False

    def generate_and_save_to_key_path(self) -> True:
        key_cryptography = split_key_type(self.key_type)[0]
        result_private_key = False
        result_public_key = False

        if self.key_security == "default":
            private_key = self.generate_private_key()
            public_key = self.get_public_key_from_private_key(private_key)
            fs_private_key = Filesystem(self.key_dir, 'private.pem', 'wb')
            fs_public_key = Filesystem(self.key_dir, 'public.pem', 'wb')
            if key_cryptography == 'RSA':
                private_key_pem = private_key.export_key('PEM')
                public_key_pem = public_key.export_key('PEM')
            elif key_cryptography == 'ECC':
                private_key_pem = private_key.export_key(format='PEM').encode('utf8')
                public_key_pem = public_key.export_key(format='PEM').encode('utf8')
            result_private_key = fs_private_key.create_file(private_key_pem)
            result_public_key = fs_public_key.create_file(public_key_pem)
        elif self.key_security == "tpm":
            result_private_key = self.generate_private_key()
            result_public_key = self.get_and_save_public_key_from_tpm_private_key()
        else:
            log.error(
                'Invalid key security. Expected `default` or `tpm`. Found {}'.format(self.key_security)
            )
            sys.exit(ExitStatus.failure)
            

        if result_public_key is True and result_private_key is True:
            return True
        else:
            log.error('Could not save key file(s).')
            sys.exit(ExitStatus.failure)

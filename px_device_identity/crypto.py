import os.path
from sys import exit
from Cryptodome.PublicKey import RSA, ECC
from exitstatus import ExitStatus

from .filesystem import Filesystem
from .classes import RequestedOperation
from .config import KEY_DIR, CONFIG_DIR
from .util import split_key_type
from .log import Logger

import subprocess

log = Logger('Crypto')

class Crypto:
    def __init__(self, operation_class: RequestedOperation, key_dir = KEY_DIR()):
        self.security =  operation_class.security
        self.key_type =  vars(operation_class)['key_type']
        self.key_dir = key_dir
        self.private_key_path = key_dir + 'private.pem'
        self.public_key_path = key_dir + 'public.pem'

    def generate_private_key(self):
        key_cryptography, key_strength = split_key_type(self.key_type)
        log.info('=> Generating new {} private key. This might take a moment ...'.format(self.key_type))
        if self.security == 'DEFAULT':
            if key_cryptography == 'RSA':
                return RSA.generate(bits=key_strength)
            elif key_cryptography == 'ECC':
                return ECC.generate(curve=key_strength)
        elif self.security == 'TPM':

            if key_cryptography == 'RSA':
                try:
                    process_result = subprocess.run(["tpm2tss-genkey", "-a", "rsa", "-s", str(key_strength), self.private_key_path])
                    # TODO: Sanity check; look for response of process instead
                    if os.path.isfile(self.private_key_path):
                        log.info('Saved private key.')
                        return True
                except EnvironmentError as e:
                    log.error(e)

            elif key_cryptography == 'ECC':
                key_strength = 'nist_' + key_strength
                try:
                    process_result = subprocess.run(["tpm2tss-genkey", "-a", "ecdsa", "-c", str(key_strength), self.private_key_path])
                    if process_result.returncode == 1:
                        log.error('Could not get or save EC private key.')
                        exit(ExitStatus)
                    # TODO: Sanity check; look for response of process instead
                    if os.path.isfile(self.private_key_path):
                        log.info('Saved private key.')
                        return True
                except EnvironmentError as e:
                    log.error(e)

        log.error('Could not generate TPM private key.')
        exit(ExitStatus.failure)

    def get_private_key_from_file(self):
        log.info('=> Loading private key from file')
        try:
            with open(self.private_key_path, 'rb', buffering=0) as reader:
                return reader.read()
        except:
            log.error('Could not read private key from {}'.format(self.private_key_path))
            exit(ExitStatus.failure)

    def get_public_key_from_private_key(self, key):
        key_cryptography = split_key_type(self.key_type)[0]
        log.info('=> Loading {} public key from private key.'.format(key_cryptography))
        if key_cryptography == 'RSA':
            return key.publickey()
        elif key_cryptography == 'ECC':
            return key.public_key()

    def get_and_save_public_key_from_tpm_private_key(self):
        key_cryptography = split_key_type(self.key_type)[0]
        log.info('=> Loading {} public key from TPM private key and saving as {}.'.format(key_cryptography, self.public_key_path))
        if key_cryptography == 'RSA':
            try:
                subprocess.run(["openssl", "rsa", "-engine", "tpm2tss", "-inform", "engine", "-in", self.private_key_path, "-pubout", "-outform", "pem", "-out", self.public_key_path])
                # TODO: Sanity check; look for response of process instead
                if os.path.isfile(self.public_key_path):
                    log.info('Saved public key.')
                    return True
            except:
                pass
        elif key_cryptography == 'ECC':
            try:
                subprocess.run(["openssl", "ec", "-engine", "tpm2tss", "-inform", "engine", "-in", self.private_key_path, "-pubout", "-outform", "pem", "-out", self.public_key_path])
                # TODO: Sanity check; look for response of process instead
                if os.path.isfile(self.public_key_path):
                    log.info('Saved public key.')
                    return True
            except:
                pass
        log.error('Could not save public key from TPM private key.')
        return False

    def generate_and_save_to_key_path(self) -> True:
        key_cryptography = split_key_type(self.key_type)[0]
        result_private_key = False
        result_public_key = False

        if self.security == "DEFAULT":
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
        elif self.security == "TPM":
            result_private_key =  self.generate_private_key()
            result_public_key = self.get_and_save_public_key_from_tpm_private_key()

        if result_public_key == True and result_private_key == True:
            return True
        else:
            log.error('Could not save key file(s).')
            exit(ExitStatus.failure)
import os.path
from sys import exit
from Cryptodome.PublicKey import RSA, ECC
from exitstatus import ExitStatus

from .filesystem import Filesystem
from .util import KEY_DIR, CONFIG_DIR, split_key_type
from .log import Logger

import subprocess

log = Logger('Crypto')

class Crypto:
    def __init__(self, security, key_type, key_dir = KEY_DIR()):
        self.security = security
        self.key_type = key_type
        self.key_dir = key_dir
        self.private_key_path = key_dir + 'private.pem'
        self.public_key_path = key_dir + 'public.pem'

    def generate_private_key(self):
        key_cryptography, key_strength = split_key_type(self.key_type)
        log.info('=> Generating new private key with {}-bits. This might take a moment ...'.format(key_strength))
        if self.security == 'DEFAULT':
            if key_cryptography == 'RSA':
                return RSA.generate(bits=key_strength)
            elif key_cryptography == 'ECC':
                return ECC.generate(curve=key_strength)
        elif self.security == 'TPM':
            if self.key_type != 'RSA:2048':
                log.error("Anything other than 'RSA:2048' is currently not supported with TPM2.")
                exit(ExitStatus.failure)
            try:
                subprocess.run(["tpm2tss-genkey", "-a", "rsa", "-s", str(key_strength), self.private_key_path])
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
        key_cryptography = split_key_type(self.key_type)
        log.info('=> Loading public key from private key.')
        if key_cryptography == 'RSA':
            return key.publickey()
        elif key_cryptography == 'ECC':
            return key.public_key()

    def get_and_save_public_key_from_tpm_private_key(self):
        log.info('=> Loading public key from TPM private key and saving as {}.'.format(self.public_key_path))
        try:
            subprocess.run(["openssl", "rsa", "-engine", "tpm2tss", "-inform", "engine", "-in", self.private_key_path, "-pubout", "-outform", "pem", "-out", self.public_key_path])
            # TODO: Sanity check; look for response of process instead
            if os.path.isfile(self.public_key_path):
                log.info('Saved public key.')
                return True
        except:
            pass
        log.error('Could not save public key from TPM private key.')
        return False

    def generate_and_save_to_config_path(self):
        result_private_key = False
        result_public_key = False

        if self.security == "DEFAULT":
            private_key = self.generate_private_key()
            public_key = self.get_public_key_from_private_key(private_key)
            fs_private_key = Filesystem(self.key_dir, 'private.pem', 'wb')
            result_private_key = fs_private_key.create_file(private_key.export_key("PEM"))
            fs_public_key = Filesystem(self.key_dir, 'public.pem', 'wb')
            result_public_key = fs_public_key.create_file(public_key.export_key("PEM"))
        elif self.security == "TPM":
            result_private_key =  self.generate_private_key()
            result_public_key = self.get_and_save_public_key_from_tpm_private_key()

        if result_public_key == True and result_private_key == True:
            return True
        else:
            log.error('Could not save key file(s).')
            exit(ExitStatus.failure)
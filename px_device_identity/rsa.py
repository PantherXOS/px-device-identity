from sys import exit
from Cryptodome.PublicKey import RSA as _RSA
from exitstatus import ExitStatus

from .filesystem import Filesystem
from .log import Logger

import subprocess

log = Logger('RSA')

class RSA:
    def __init__(self, config_path, security):
        self.config_path = config_path
        self.security = security
        self.private_key_path = config_path + 'private.pem'
        self.public_key_path = config_path + 'public.pem'

    def generate_private_key(self):
        key_size = 2048
        log.info('=> Generating new private key with {}-bits. This might take a moment ...'.format(key_size))
        if self.security == 'DEFAULT':
            return _RSA.generate(key_size)
        elif self.security == 'TPM':
            try:
                subprocess.run(["tpm2tss-genkey", "-a", "rsa", "-s", str(key_size), self.private_key_path])
                return True
            except EnvironmentError as e:
                log.error('Could not generate TPM private key.')
                log.error(e)
                exit(ExitStatus.failure)
        return False

    def get_private_key_from_file(self):
        log.info('=> Loading private key from file')
        file_path = self.config_path + 'private.pem'
        with open(file_path, 'rb', buffering=0) as reader:
            key = reader.read()
            return key

    def get_public_key_from_private_key(self, key):
        log.info('=> Loading public key from private key.')
        return key.publickey()

    def get_and_save_public_key_from_tpm_private_key(self):
        log.info('=> Loading public key from TPM private key and saving as {}.'.format(self.public_key_path))
        try:
            subprocess.run(["openssl", "rsa", "-engine", "tpm2tss", "-inform", "engine", "-in", self.private_key_path, "-pubout", "-outform", "pem", "-out", self.public_key_path])
            log.info('Saved public key.')
            return True
        except:
            log.error('Could not save public key from TPM private key.')
        return False

    def generate_and_save_to_config_path(self):
        result_private_key = False
        result_public_key = False

        if self.security == "DEFAULT":
            private_key = self.generate_private_key()
            public_key = self.get_public_key_from_private_key(private_key)
            fs_private_key = Filesystem(self.config_path, 'private.pem', 'wb')
            result_private_key = fs_private_key.create_file(private_key.export_key("PEM"))
            fs_public_key = Filesystem(self.config_path, 'public.pem', 'wb')
            result_public_key = fs_public_key.create_file(public_key.export_key("PEM"))
        elif self.security == "TPM":
            result_private_key =  self.generate_private_key()
            result_public_key = self.get_and_save_public_key_from_tpm_private_key()

        if result_public_key == True and result_private_key == True:
            return True
        else:
            log.error('Could not save key file(s).')
            exit(ExitStatus.failure)
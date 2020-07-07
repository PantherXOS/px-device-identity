import subprocess

from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from tempfile import gettempdir
from shutil import rmtree
from os import mkdir, path, times

from .filesystem import Filesystem
from .util import KEY_DIR, CONFIG_DIR, b64encode
from .log import Logger

log = Logger('main')
class Sign:
    def __init__(self, security, message):
        self.security = security
        self.message = message
        self.key_dir = KEY_DIR()
        self.private_key_dir = KEY_DIR() + 'private.pem'

    def sign_with_rsa_signing_key(self, key):
        log.info("=> Signing {} RSA key".format(self.message))
        key = RSA.import_key(key)
        m = SHA256.new(self.message.encode('utf8'))
        return b64encode(PKCS1_v1_5.new(key).sign(m))

    def remove_tmp_path(self, tmp_path):
        log.info("=> Removing temp directory")
        rmtree(tmp_path, ignore_errors=True)

    def sign_with_rsa_tpm_signing_key(self):
        log.info("=> Signing {} with TPM RSA key".format(self.message))
        message = SHA256.new(self.message.encode('utf8'))
        message_base64 = b64encode(message.digest()).encode('utf8')
        
        tmp_path = path.join(gettempdir(), '.{}'.format(hash(times())))
        log.info("=> Creating temp directory at {}".format(tmp_path))
        mkdir(tmp_path)
        
        message_tmp_file_path = tmp_path + '/message'
        signature_tmp_file = tmp_path + '/signature'

        try:
            with open(message_tmp_file_path, 'wb') as message_writer:
                message_writer.write(message_base64)
        except:
            log.error("Could not write message to {}".format(message_tmp_file_path))
            self.remove_tmp_path(tmp_path)
            return False

        try:
            key_path = self.private_key_dir
            subprocess.run(["openssl", "pkeyutl", "-engine", "tpm2tss", "-keyform", "engine", "-inkey", key_path, "-sign", "-in", message_tmp_file_path, "-out", signature_tmp_file])
        except:
            log.error("Could not sign message with TPM.")
            self.remove_tmp_path(tmp_path)
            return False

        try:
            with open(signature_tmp_file, 'rb', buffering=0) as signature_reader:
                signature = signature_reader.read()
                self.remove_tmp_path(tmp_path)
            return b64encode(signature)
        except:
            log.error("Could not read signature from {}".format(signature_tmp_file))

        self.remove_tmp_path(tmp_path)
        return False

    def sign(self):
        log.info('=> Signing message with type {}'.format(self.security))
        if self.security == 'DEFAULT':
            fs = Filesystem(self.key_dir, 'private.pem', 'rb')
            return self.sign_with_rsa_signing_key(fs.open_file())
        if self.security == 'TPM':
            return self.sign_with_rsa_tpm_signing_key()
        return False
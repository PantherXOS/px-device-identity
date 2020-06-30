from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256

from .filesystem import Filesystem
from .util import b64encode
from .log import Logger

log = Logger('main')
class Sign:
    def __init__(self, config_path, operation_type, message):
        self.config_path = config_path
        self.operation_type = operation_type
        self.message = message

    def sign_with_rsa_signing_key(self, key):
        key = RSA.import_key(key)
        m = SHA256.new(self.message.encode('utf8'))
        return b64encode(PKCS1_v1_5.new(key).sign(m))

    def sign(self):
        log.info('=> Signing string with type {}'.format(self.operation_type))
        if self.operation_type == 'TPM':
            log.error('TPM is not supported at this moment')
        if self.operation_type == 'DEFAULT':
            fs = Filesystem(self.config_path, 'private.pem', 'rb')
            return self.sign_with_rsa_signing_key(fs.open_file())
        return False
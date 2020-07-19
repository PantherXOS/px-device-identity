from pathlib import Path
from authlib.jose import jwk, jwt
from exitstatus import ExitStatus
from json import dumps as json_dumps 

from .log import Logger
from .config import KEY_DIR, CONFIG_DIR
from .util import split_key_type
from .classes import RequestedOperation

log = Logger('JWK')

class JWK:
    def __init__(self, operation_class: RequestedOperation, key_dir = KEY_DIR()):
        self.security = vars(operation_class)['security']
        self.key_type = vars(operation_class)['key_type']
        self.key_dir = key_dir
        self.jwk_path = key_dir + 'public_jwk.json'
        self.public_key_path = key_dir + 'public.pem'

    def generate(self):
        key_cryptography = split_key_type(self.key_type)[0]

        with open(self.public_key_path, 'rb', buffering=0) as reader:
            file_content = reader.read()
            if key_cryptography == 'RSA':
                key = jwk.dumps(file_content, kty='RSA')
            elif key_cryptography == 'ECC':
                key = jwk.dumps(file_content, kty='EC')
            if self.key_type == 'RSA:2048':
                key['alg'] = 'RS256'
            elif self.key_type == 'ECC:p256':
                key['alg'] = 'ES256'
            elif self.key_type == 'ECC:p384':
                key['alg'] = 'ES384'
            elif self.key_type == 'ECC:p521':
                key['alg'] = 'ES521'
            else:
                log.error('Unsupported key type.')
                exit(ExitStatus.failure)
            return key

    def save_to_key_path(self):
        key = self.generate()
        formatted_key = bytearray(json_dumps(key, ensure_ascii=True).encode('utf8'))
        with open(self.jwk_path, 'wb') as writer:
            writer.write(formatted_key)
            return True

    def get(self):
        return self.generate()

    def get_jwks(self):
        jwk = self.get()
        jwks = {
            'keys': [jwk]
        }
        return jwks
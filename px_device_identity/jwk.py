from pathlib import Path
from authlib.jose import jwk
from exitstatus import ExitStatus
from json import dumps as json_dumps 

from .util import KEY_DIR, CONFIG_DIR, split_key_type

class JWK:
    def __init__(self, security, key_type, key_dir = KEY_DIR()):
        self.security = security
        self.key_type = key_type
        self.key_dir = key_dir
        self.jwk_path = key_dir + 'public_jwk.json'
        self.public_key_path = key_dir + 'public.pem'

    def generate(self):
        key_cryptography, key_strength = split_key_type(self.key_type)

        with open(self.public_key_path, 'rb', buffering=0) as reader:
            file_content = reader.read()
            key = jwk.dumps(file_content, kty=key_cryptography)
            if self.key_type == 'RSA:2048':
                key['alg'] = 'RS256'
            elif self.key_type == 'ECC:p256':
                key['alg'] = 'ES256'
            elif self.key_type = 'ECC:p384':
                key['alg'] = 'ES384'
            elif self.key_type = 'ECC:p521':
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
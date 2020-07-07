from pathlib import Path
from authlib.jose import jwk
from json import dumps as json_dumps 

from .util import KEY_DIR, CONFIG_DIR

class JWK:
    def __init__(self, security):
        self.security = security
        self.jwk_path = KEY_DIR() + 'public_jwk.json'
        self.public_key_path = KEY_DIR() + 'public.pem'

    def generate(self):
        with open(self.public_key_path, 'rb', buffering=0) as reader:
            file_content = reader.read()
            key = jwk.dumps(file_content, kty='RSA')
            key['alg'] = 'RS256'
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
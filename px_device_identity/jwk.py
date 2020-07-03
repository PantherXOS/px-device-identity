from pathlib import Path
from authlib.jose import jwk
from json import dumps as json_dumps 

class JWK:
    def __init__(self, config_path, security):
        self.config_path = config_path
        self.security = security
        self.jwk_path = config_path + 'public_jwk.json'
        self.public_key_path = config_path + 'public.pem'

    def __repr__(self):
        return f'JWK({self.config_path!r})'

    def generate(self):
        with open(self.public_key_path, 'rb', buffering=0) as reader:
            file_content = reader.read()
            key = jwk.dumps(file_content, kty='RSA')
            key['alg'] = 'RS256'
            return key

    def save_to_config_path(self):
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
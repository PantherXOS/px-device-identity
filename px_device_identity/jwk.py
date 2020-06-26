from pathlib import Path
from authlib.jose import jwk
import json

class JWK:
    def __init__(self, config_path, operation_type):
        self.config_path = config_path
        self.operation_type = operation_type
        self.jwk_path = config_path + 'public_jwk.json'
        self.public_key_path = config_path + 'public.pem'

    def __repr__(self):
        return f'JWK({self.config_path!r})'

    def generate(self):
        with open(self.public_key_path, 'rb', buffering=0) as reader:
            file_content = reader.read()
            return jwk.dumps(file_content, kty='RSA')

    def save_to_config_path(self):
        key = self.generate()
        formatted_key = bytearray(json.dumps(key, ensure_ascii=True).encode('utf8'))
        with open(self.public_key_path, 'wb') as writer:
            writer.write(formatted_key)
            return True

    def get(self):
        return self.generate()
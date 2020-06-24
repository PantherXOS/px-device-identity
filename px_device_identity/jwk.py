from authlib.jose import JsonWebKey
from .filesystem import open_file, create_file
import json

def save_jwk(path, file_name, jwk):
    return create_file(path, file_name, json.dumps(jwk))

def generate_key(path: str):
    file_path = path + 'public.pem'
    public_key = open_file(file_path)
    try:
        return JsonWebKey.dumps(public_key, {'kty': 'RSA'})
    except Exception as e:
        print(e)
    return False

def generate_jwk(path: str):
    return generate_key(path)

def get_jwk(path: str):
    file_path = path + 'public_jwk.json'
    return open_file(file_path)
    
def generate_and_save_jwk(path: str):
    jwk = generate_key(path)
    if jwk == False:
        return jwk
    print(jwk.as_json())
    file_name = 'public_jwk.json'
    saved_jwk = save_jwk(path, file_name, jwk)
    if saved_jwk:
        return True
    return False
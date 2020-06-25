from authlib.jose import jwk
from .filesystem import open_file, create_file
import json
import array

def save_jwk(path, file_name, jwk_data):
    return create_file(path, file_name, json.dumps(jwk_data))

def generate_key_from_pem(path: str):
    file_path = path + 'public.pem'
    file_content = open_file(file_path, 'rb')
    if file_content == False:
        return file_content

    try:
        return jwk.dumps(file_content, kty='RSA')
    except Exception as e:
            print(".. Failed to get JWK from {}".format(file_path))
            print(e)
    return False

def generate_jwk(path: str):
    print("Generating JWK")
    return generate_key_from_pem(path)

def get_jwk(path: str):
    file_path = path + 'public_jwk.json'
    print("Loading JWK from {}".format(file_path))
    return open_file(file_path, 'rb')
    
def generate_and_save_jwk(path: str):
    jwk_data = generate_jwk(path)
    if jwk_data == False:
        return jwk_data
    print(".. Successfully generated JWK from public key")
    print(jwk_data)
    file_name = 'public_jwk.json'
    file_path = path + file_name
    print(".. Saving JWK at {}".format(file_path))
    jwk_data_formatted = json.dumps(jwk_data, ensure_ascii=True).encode('utf8')
    return create_file(path, file_name, jwk_data_formatted)
import sys
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256
from .filesystem import create_file, open_file, create_path
from base64 import b64encode, b64decode
from .jwk import get_jwk, generate_and_save_jwk
import json
from authlib.jose import jwt

def generate_key():
    return RSA.generate(2048)

def get_private_key(path: str):
    print(path)
    file_path = path + 'private.pem'
    private_key = open_file(file_path, 'rb')
    return private_key

# Default only (not supported by TPM)
def save_private_key(key: str, path: str):
    file_name = 'private.pem'
    print('.. Saving private key as {} at {}'.format(file_name, path))
    private_key = key.export_key("PEM")
    return create_file(path, file_name, private_key, "wb")

def save_public_key(key: str, path: str):
    file_name = 'public.pem'
    print('.. Saving public key as {} at {}'.format(file_name, path))
    public_key = key.publickey().export_key(format='PEM')
    return create_file(path, file_name, public_key, "wb")

def generate_rsa_keys(type: str, path: str):
    print("# Generating and saving RSA keys: {}".format(type))
    if type == 'tpm':
        print('.. Error: TPM is not supported at this moment. Exitting.')
        sys.exit()

    key = generate_key()
    saved_private_key = save_private_key(key, path)
    saved_public_key = save_public_key(key, path)

    if saved_private_key and saved_public_key:
        return True
    else:
        return False

def generate_keys(path: str, type: str):
    created_path = create_path(path)
    if created_path == False:
        return {
            'status': 'error',
            'status_signature': 'error:path',
            'message': 'Error: Could not create path.'
        }

    generated_rsa_keys = generate_rsa_keys(type, path)
    if generated_rsa_keys == False:
        return {
            'status': 'error',
            'status_signature': 'error:rsa' ,
            'message': 'Could not generate RSA keys.'
        }
    print('Success: Generated RSA keys')

    generated_jwk = generate_and_save_jwk(path)
    if generated_jwk == False:
        return {
            'status': 'error',
            'status_signature': 'error.jwk',
            'message': 'Could not generate JWK from existing RSA keys.'
        }
    print('Success: Generated JWK key')

    return {
        'status': 'success',
        'status_signature': 'success',
        'message': 'We are done here..'
    }
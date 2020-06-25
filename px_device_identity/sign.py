from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Hash import SHA256

from .filesystem import open_file

def sign_with_rsa_signing_key(message: str, private_key):
    key = RSA.import_key(private_key)
    m = SHA256.new(message.encode('utf8'))
    return PKCS1_v1_5.new(key).sign(m)

def sign(type: str, path: str, message: str):
    print('Signing string with type {}'.format(type))
    if type == 'tpm':
        print('ERROR: TPM is not supported at this moment')
    if type == 'default':
        file_path = path + 'private.pem'
        private_key = open_file(file_path, 'rb')
        return sign_with_rsa_signing_key(message, private_key)
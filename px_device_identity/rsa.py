from Crypto.PublicKey import RSA
from .filesystem import create_file

def generate_key():
    return RSA.generate(2048)

# Default only (not supported by TPM)
def save_private_key(key: str, path: str):
    private_key = key.export_key("PEM")
    file_name = 'private.pem'
    return create_file(path, file_name, private_key)

def save_public_key(key: str, path: str):
    public_key = key.publickey().export_key("PEM")
    file_name = 'public.pem'
    return create_file(path, file_name, public_key)

def generate_rsa_keys(type: str, path: str):
    if type == 'tpm':
        print('TPM is not supported at this moment')
        return False

    rsa_key = generate_key()
    saved_private_key = save_private_key(rsa_key, path)
    saved_public_key = save_public_key(rsa_key, path)

    if saved_private_key and saved_public_key:
        return True
    else:
        return False
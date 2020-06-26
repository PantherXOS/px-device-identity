import sys
from Cryptodome.PublicKey import RSA as _RSA

class RSA:
    def __init__(self, config_path, operation_type):
        self.config_path = config_path
        self.operation_type = operation_type
        self.private_key_path = config_path + 'private.pem'
        self.public_key_path = config_path + 'public.pem'

    def generate_private_key(self):
        print('=> Generating new private key')
        if self.operation_type == 'DEFAULT':
            return _RSA.generate(2048)
        else:
            print('ERROR: Unsupported method {}'.format(self.operation_type))
            # TODO: Implement TPM
            return False

    def get_private_key_from_file(self):
        print('=> Loading private key from file')
        file_path = self.config_path + 'private.pem'
        with open(file_path, 'rb', buffering=0) as reader:
            key = reader.read()
            return key

    def get_public_key_from_private_key(self, key):
        print('=> Loading public key from private key')
        return key.publickey()

    def generate_and_save_to_config_path(self):
        private_key = self.generate_private_key()
        public_key = self.get_public_key_from_private_key(private_key)
        with open(self.private_key_path, 'wb') as writer:
            writer.write(bytearray(private_key.export_key("PEM")))
        with open(self.public_key_path, 'wb') as writer:
            writer.write(bytearray(public_key.export_key("PEM")))
        return True
import subprocess

from Cryptodome.PublicKey import RSA, ECC
from Cryptodome.Signature import PKCS1_v1_5, DSS
from Cryptodome.Hash import SHA256, SHA384, SHA512
from exitstatus import ExitStatus

from .filesystem import Filesystem, create_tmp_path, remove_tmp_path
from .config import KEY_DIR, CONFIG_DIR
from .util import b64encode, split_key_type, handle_result
from .log import Logger

log = Logger('SIGN')

class Sign:
    def __init__(self, operation_class, message, key_dir = KEY_DIR()):
        self.security =  vars(operation_class)['security']
        self.key_type =  vars(operation_class)['key_type']
        self.message = message
        self.key_dir = key_dir
        self.private_key_dir = key_dir + 'private.pem'
        self.public_key_dir = key_dir + 'public.pem'

    def sign_with_rsa_signing_key(self, key):
        log.info("=> Signing '{}' with RSA key".format(self.message))
        key = RSA.import_key(key)
        m = SHA256.new(self.message.encode('utf8'))
        return b64encode(PKCS1_v1_5.new(key).sign(m))

    def sign_with_ecc_signing_key(self, key):
        key_strength = split_key_type(self.key_type)[1]
        log.info("=> Signing '{}' with ECC key".format(self.message))
        m = ''
        key = ECC.import_key(key)
        if key_strength == 'p256':
            m = SHA256.new(self.message.encode('utf8'))
        elif key_strength == 'p384':
            m = SHA384.new(self.message.encode('utf8'))
        elif key_strength == 'p521':
            m = SHA512.new(self.message.encode('utf8'))
        signer = DSS.new(key, 'fips-186-3')
        return b64encode(signer.sign(m))

    def write_message_to_temp_path(self, message, file_path):
        log.info("=> Writing message '{}' to {}".format(message, file_path))
        try:
            with open(file_path, 'wb') as message_writer:
                message_writer.write(message)
            return True
        except:
            log.error("Could not write message to {}".format(file_path))
            return False
    
    def get_signature_from_temp_path(self, file_path):
        log.info("=> Reading signature from {}.".format(file_path))
        try:
            with open(file_path, 'rb', buffering=0) as signature_reader:
                signature = signature_reader.read()
            return b64encode(signature)
        except:
            log.error("Could not read signature from {}".format(file_path))
            return False

    def sign_with_ecc_tpm_signing_key(self):
        key_strength = split_key_type(self.key_type)[1]
        log.info("=> Signing '{}' with TPM ECC key".format(self.message))
        m = ''
        digest = ''
        if key_strength == 'p256':
            digest = 'sha256'
            m = SHA256.new(self.message.encode('utf8'))
        elif key_strength == 'p385':
            digest = 'sha384'
            m = SHA384.new(self.message.encode('utf8'))
        elif key_strength == 'p521':
            digest = 'sha512'
            m = SHA512.new(self.message.encode('utf8'))
        message_digest = m.digest()
        
        tmp_path = create_tmp_path()
        message_tmp_file_path = tmp_path + '/message'
        signature_tmp_file = tmp_path + '/signature'

        result = self.write_message_to_temp_path(message_digest, message_tmp_file_path)
        handle_result(result, "Could not write message to path.", tmp_path)

        log.info('=> Engaging openssl to sign message hash with ECC key.')
        try:
            digest = "digest:" + digest
            result = subprocess.run(["openssl", "pkeyutl", "-engine", "tpm2tss", "-keyform", "engine", "-inkey", self.private_key_dir, "-sign", "-in", message_tmp_file_path, "-out", signature_tmp_file, "-pkeyopt", digest])
            #handle_result(result, "Unknown error signing message hash with openssl application.", tmp_path)
        except:
            handle_result(False, "Could not sign message with TPM.", tmp_path)

        signature = self.get_signature_from_temp_path(signature_tmp_file)
        handle_result(signature, "Could not read signature from path.", tmp_path)
        
        remove_tmp_path(tmp_path)
        return signature

    def sign_with_rsa_tpm_signing_key(self):
        log.info("=> Signing '{}' with TPM RSA key".format(self.message))
        m = SHA256.new(self.message.encode('utf8'))
        message_digest = m.digest()
        
        tmp_path = create_tmp_path()
        message_tmp_file_path = tmp_path + '/message'
        signature_tmp_file = tmp_path + '/signature'

        result = self.write_message_to_temp_path(message_digest, message_tmp_file_path)
        handle_result(result, "Could not write message to path.", tmp_path)

        log.info('=> Engaging openssl to sign message hash with RSA key.')
        try:
            result = subprocess.run(["openssl", "pkeyutl", "-engine", "tpm2tss", "-keyform", "engine", "-inkey", self.private_key_dir, "-sign", "-in", message_tmp_file_path, "-out", signature_tmp_file, "-pkeyopt", "digest:sha256"])
            #handle_result(result, "Unknown error signing message hash with openssl application.", tmp_path)
        except:
            handle_result(False, "Could not sign message with TPM.", tmp_path)

        signature = self.get_signature_from_temp_path(signature_tmp_file)
        handle_result(signature, "Could not read signature from path.", tmp_path)
        
        remove_tmp_path(tmp_path)
        return signature

    def sign(self):
        key_cryptography = split_key_type(self.key_type)[0]
        log.info('=> Signing message with type {}'.format(self.security))
        if self.security == 'DEFAULT':
            fs = Filesystem(self.key_dir, 'private.pem', 'rb')
            if key_cryptography == 'RSA':
                return self.sign_with_rsa_signing_key(fs.open_file())
            elif key_cryptography == 'ECC':
                return self.sign_with_ecc_signing_key(fs.open_file())
        if self.security == 'TPM':
            if key_cryptography == 'RSA':
                return self.sign_with_rsa_tpm_signing_key()
            elif key_cryptography == 'ECC':
               return self.sign_with_ecc_tpm_signing_key()
import subprocess

from Cryptodome.PublicKey import RSA, ECC
from Cryptodome.Signature import PKCS1_v1_5, DSS
from Cryptodome.Hash import SHA256, SHA384, SHA512

from px_device_identity.log import Logger

from .filesystem import Filesystem, create_tmp_path, remove_tmp_path
from .config import KEY_DIR
from .util import b64encode, split_key_type, handle_result

log = Logger(__name__)


class Sign:
    '''Sign message using RSA/ECC keys'''
    def __init__(
        self, device_properties: 'DeviceProperties', message: str, key_dir=KEY_DIR
    ):
        self.key_security: str = device_properties.key_security
        self.key_type: str = device_properties.key_type
        self.message: str = message
        self.key_dir = key_dir
        self.private_key_dir = key_dir + 'private.pem'
        self.public_key_dir = key_dir + 'public.pem'

    def _sign_with_rsa_signing_key(self, key) -> str:
        '''Sign with RSA keys (no TPM)'''
        log.info("=> Signing '{}' with RSA key".format(self.message))
        key = RSA.import_key(key)
        msg = SHA256.new(self.message.encode('utf8'))
        return b64encode(PKCS1_v1_5.new(key).sign(msg))

    def _sign_with_ecc_signing_key(self, key) -> str:
        '''Sign with ECC keys (no TPM)'''
        key_strength = split_key_type(self.key_type)[1]
        log.info("=> Signing '{}' with ECC key".format(self.message))
        msg = ''
        key = ECC.import_key(key)
        if key_strength == 'p256':
            msg = SHA256.new(self.message.encode('utf8'))
        elif key_strength == 'p384':
            msg = SHA384.new(self.message.encode('utf8'))
        elif key_strength == 'p521':
            msg = SHA512.new(self.message.encode('utf8'))
        signer = DSS.new(key, 'fips-186-3')
        return b64encode(signer.sign(msg))

    def _write_message_to_temp_path(self, message, file_path) -> bool:
        '''Write message to file before signing'''
        log.info("=> Writing message '{}' to {}".format(message, file_path))
        try:
            with open(file_path, 'wb') as message_writer:
                message_writer.write(message)
            return True
        except:
            log.error("Could not write message to {}".format(file_path))
            return False

    def _get_signature_from_temp_path(self, file_path):
        '''Get signature from file after signing'''
        log.info("=> Reading signature from {}.".format(file_path))
        try:
            with open(file_path, 'rb', buffering=0) as signature_reader:
                signature = signature_reader.read()
            return b64encode(signature)
        except:
            log.error("Could not read signature from {}".format(file_path))

    def _sign_with_ecc_tpm_signing_key(self):
        '''Sign with ECC keys (TPM)'''
        key_strength = split_key_type(self.key_type)[1]
        log.info("=> Signing '{}' with TPM ECC key".format(self.message))
        msg = ''
        digest = ''
        if key_strength == 'p256':
            digest = 'sha256'
            msg = SHA256.new(self.message.encode('utf8'))
        elif key_strength == 'p385':
            digest = 'sha384'
            msg = SHA384.new(self.message.encode('utf8'))
        elif key_strength == 'p521':
            digest = 'sha512'
            msg = SHA512.new(self.message.encode('utf8'))
        message_digest = msg.digest()

        tmp_path = create_tmp_path()
        message_tmp_file_path = tmp_path + '/message'
        signature_tmp_file = tmp_path + '/signature'

        result = self._write_message_to_temp_path(message_digest, message_tmp_file_path)
        handle_result(result, "Could not write message to path.", tmp_path)

        log.info('=> Engaging openssl to sign message hash with ECC key.')
        try:
            digest = "digest:" + digest
            result = subprocess.run([
                "openssl", "pkeyutl", "-engine", "tpm2tss",
                "-keyform", "engine",
                "-inkey", self.private_key_dir,
                "-sign", "-in", message_tmp_file_path,
                "-out", signature_tmp_file,
                "-pkeyopt", digest
            ])
            #handle_result(result, "Unknown error signing message hash with openssl application.", tmp_path)
        except:
            handle_result(False, "Could not sign message with TPM.", tmp_path)

        signature = self._get_signature_from_temp_path(signature_tmp_file)
        handle_result(signature, "Could not read signature from path.", tmp_path)

        remove_tmp_path(tmp_path)
        return signature

    def _sign_with_rsa_tpm_signing_key(self):
        '''Sign with RSA keys (TPM)'''
        log.info("=> Signing '{}' with TPM RSA key".format(self.message))
        msg = SHA256.new(self.message.encode('utf8'))
        message_digest = msg.digest()

        tmp_path = create_tmp_path()
        message_tmp_file_path = tmp_path + '/message'
        signature_tmp_file = tmp_path + '/signature'

        result = self._write_message_to_temp_path(message_digest, message_tmp_file_path)
        handle_result(result, "Could not write message to path.", tmp_path)

        log.info('=> Engaging openssl to sign message hash with RSA key.')
        try:
            result = subprocess.run([
                "openssl", "pkeyutl",
                "-engine", "tpm2tss",
                "-keyform", "engine",
                "-inkey", self.private_key_dir,
                "-sign", "-in", message_tmp_file_path,
                "-out", signature_tmp_file,
                "-pkeyopt", "digest:sha256"
            ])
            #handle_result(result, "Unknown error signing message hash with openssl application.", tmp_path)
        except:
            handle_result(False, "Could not sign message with TPM.", tmp_path)

        signature = self._get_signature_from_temp_path(signature_tmp_file)
        handle_result(signature, "Could not read signature from path.", tmp_path)

        remove_tmp_path(tmp_path)
        return signature

    def sign(self):
        '''Sign the message'''
        key_cryptography = split_key_type(self.key_type)[0]
        log.info('=> Signing message with type {}'.format(self.key_security))
        if self.key_security == 'default':
            fs = Filesystem(self.key_dir, 'private.pem', 'rb')
            if key_cryptography == 'RSA':
                return self._sign_with_rsa_signing_key(fs.open_file())
            elif key_cryptography == 'ECC':
                return self._sign_with_ecc_signing_key(fs.open_file())
        if self.key_security == 'tpm':
            if key_cryptography == 'RSA':
                return self._sign_with_rsa_tpm_signing_key()
            elif key_cryptography == 'ECC':
                return self._sign_with_ecc_tpm_signing_key()

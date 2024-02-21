import logging
from px_device_identity.errors import SigningError
import subprocess

from Cryptodome.Hash import SHA256, SHA384, SHA512
from Cryptodome.PublicKey import ECC, RSA
from Cryptodome.Signature import DSS, PKCS1_v1_5

from .classes import DeviceProperties
from .config import KEY_DIR
from .filesystem import create_tmp_dir, remove_tmp_dir
from .util import b64encode, split_key_type

log = logging.getLogger(__name__)


class Sign:
    '''Sign message using RSA/ECC keys'''

    def __init__(
        self,
        device_properties: "DeviceProperties",
        message: str,
        key_dir: str = KEY_DIR,
    ):
        self.key_security: str = device_properties.key_security
        self.key_type: str = device_properties.key_type
        self.message: str = message
        self.key_dir = key_dir
        self.private_key_dir = key_dir + "/" + "private.pem"
        self.public_key_dir = key_dir + "/" + "public.pem"

    def _sign_with_rsa_signing_key(self, key_content: str) -> str:
        '''Sign with RSA keys (no TPM)'''
        log.debug("=> Signing '{}' with RSA key".format(self.message))
        key = RSA.import_key(key_content)
        msg = SHA256.new(self.message.encode('utf8'))
        return b64encode(PKCS1_v1_5.new(key).sign(msg))

    def _sign_with_ecc_signing_key(self, key_content: str) -> str:
        '''Sign with ECC keys (no TPM)'''
        key_strength = split_key_type(self.key_type)[1]
        log.debug("=> Signing '{}' with ECC key".format(self.message))
        msg = ''
        key = ECC.import_key(key_content)
        if key_strength == 'p521':
            msg = SHA512.new(self.message.encode('utf8'))
        elif key_strength == 'p384':
            msg = SHA384.new(self.message.encode('utf8'))
        else:
            log.info('Defaulting to SHA256.')
            msg = SHA256.new(self.message.encode('utf8'))
        signer = DSS.new(key, 'fips-186-3')
        return b64encode(signer.sign(msg))

    def _write_message_to_temp_path(self, message: bytes, file_path: str):
        '''Write message to file before signing'''
        log.debug("=> Writing message '{}' to {}".format(message, file_path))
        try:
            with open(file_path, 'wb') as message_writer:
                message_writer.write(message)
        except:
            log.error("Could not write message to {}".format(file_path))
            raise

    def _get_signature_from_temp_path(self, file_path):
        '''Get signature from file after signing'''
        log.debug("=> Reading signature from {}.".format(file_path))
        try:
            signature = ''
            with open(file_path, 'rb', buffering=0) as signature_reader:
                signature = signature_reader.read()

            return b64encode(signature)
        except:
            log.error("Could not read signature from {}".format(file_path))
            raise

    def _sign_with_ecc_tpm_signing_key(self):
        '''Sign with ECC keys (TPM)'''
        key_strength = split_key_type(self.key_type)[1]
        log.debug("=> Signing '{}' with TPM ECC key".format(self.message))

        msg = ''
        digest = ''
        if key_strength == 'p521':
            digest = 'sha512'
            msg = SHA512.new(self.message.encode('utf8'))
        elif key_strength == 'p385':
            digest = 'sha384'
            msg = SHA384.new(self.message.encode('utf8'))
        else:
            digest = 'sha256'
            msg = SHA256.new(self.message.encode('utf8'))
        message_digest = msg.digest()

        tmp_dir = create_tmp_dir()
        message_tmp_file_path = tmp_dir + '/message'
        signature_tmp_file = tmp_dir + '/signature'

        self._write_message_to_temp_path(
            message_digest, message_tmp_file_path
        )

        log.debug('=> Engaging openssl to sign message hash with ECC key.')
        try:
            digest = "digest:" + digest
            result = subprocess.run([
                "openssl", "pkeyutl",
                "-engine", "tpm2tss",
                "-keyform", "engine",
                "-inkey", self.private_key_dir,
                "-sign", "-in", message_tmp_file_path,
                "-out", signature_tmp_file,
                "-pkeyopt", digest
            ])

            log.info(result)
            if result.stderr:
                log.error(result.stderr)
                raise SigningError('Failed to sign with TPM ECC key')
        except Exception as err:
            remove_tmp_dir(tmp_dir)
            raise err

        signature = self._get_signature_from_temp_path(signature_tmp_file)

        remove_tmp_dir(tmp_dir)
        return signature

    def _sign_with_rsa_tpm_signing_key(self):
        '''Sign with RSA keys (TPM)

            raises: SigningError
        '''
        log.debug("=> Signing '{}' with TPM RSA key".format(self.message))
        msg = SHA256.new(self.message.encode('utf8'))
        message_digest = msg.digest()

        tmp_dir = create_tmp_dir()
        message_tmp_file_path = tmp_dir + '/message'
        signature_tmp_file = tmp_dir + '/signature'

        self._write_message_to_temp_path(
            message_digest, message_tmp_file_path
        )

        log.debug('=> Engaging openssl to sign message hash with RSA key.')
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

            log.info(result)
            if result.stderr:
                log.error(result.stderr)
                raise SigningError('Failed to sign with TPM RSA key.')
        except Exception as err:
            remove_tmp_dir(tmp_dir)
            raise err

        signature = self._get_signature_from_temp_path(signature_tmp_file)

        remove_tmp_dir(tmp_dir)
        return signature

    def sign(self):
        '''Sign the message

            raises: SigningError (child)
        '''
        key_cryptography = split_key_type(self.key_type)[0]
        log.debug('=> Signing message with type {}'.format(self.key_security))
        if self.key_security == 'default':
            with open('{}/private.pem'.format(self.key_dir)) as reader:
                key_content = reader.read()
                if not key_content:
                    raise IOError(
                        'The private key private.pem could not be found.'
                    )
            if key_cryptography == 'RSA':
                return self._sign_with_rsa_signing_key(key_content)
            elif key_cryptography == 'ECC':
                return self._sign_with_ecc_signing_key(key_content)
        if self.key_security == 'tpm':
            if key_cryptography == 'RSA':
                return self._sign_with_rsa_tpm_signing_key()
            elif key_cryptography == 'ECC':
                return self._sign_with_ecc_tpm_signing_key()

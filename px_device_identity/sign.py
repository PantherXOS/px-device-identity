import subprocess

from Cryptodome.PublicKey import RSA, ECC
from Cryptodome.Signature import PKCS1_v1_5, DSS
from Cryptodome.Hash import SHA256
from exitstatus import ExitStatus
from tempfile import gettempdir
from shutil import rmtree
from os import mkdir, path, times

from .filesystem import Filesystem
from .util import KEY_DIR, CONFIG_DIR, b64encode, split_key_type
from .log import Logger

log = Logger('main')
class Sign:
    def __init__(self, security, key_type, message, key_dir = KEY_DIR()):
        self.security = security
        self.key_type = key_type
        self.message = message
        self.key_dir = key_dir
        self.private_key_dir = key_dir + 'private.pem'
        self.public_key_dir = key_dir + 'public.pem'

    def sign_with_rsa_signing_key(self, key):
        log.info("=> Signing {} RSA key".format(self.message))
        key = RSA.import_key(key)
        m = SHA256.new(self.message.encode('utf8'))
        return b64encode(PKCS1_v1_5.new(key).sign(m))

    def sign_with_ecc_signign_key(self, key):
        log.info("=> Signing with {} ECC key".format(self.message))
        key = ECC.import_key(key)
        m = SHA256.new(self.message.encode('utf8'))
        signer = DSS.new(key, 'fips-186-3')
        return b64encode(signer.sign(m))

    def remove_tmp_path(self, tmp_path):
        log.info("=> Removing temp directory")
        rmtree(tmp_path, ignore_errors=True)

    def sign_with_rsa_tpm_signing_key(self):
        log.info("=> Signing {} with TPM RSA key".format(self.message))
        message = SHA256.new(self.message.encode('utf8'))
        message_digest = message.digest()
        
        tmp_path = path.join(gettempdir(), '.{}'.format(hash(times())))
        log.info("=> Creating temp directory at {}".format(tmp_path))
        mkdir(tmp_path)
        
        message_tmp_file_path = tmp_path + '/message'
        signature_tmp_file = tmp_path + '/signature'

        try:
            with open(message_tmp_file_path, 'wb') as message_writer:
                message_writer.write(message_digest)
        except:
            log.error("Could not write message to {}".format(message_tmp_file_path))
            self.remove_tmp_path(tmp_path)
            return False

        try:
            key_path = self.private_key_dir
            subprocess.run(["openssl", "pkeyutl", "-engine", "tpm2tss", "-keyform", "engine", "-inkey", key_path, "-sign", "-in", message_tmp_file_path, "-out", signature_tmp_file, "-pkeyopt", "digest:sha256"])
        except:
            log.error("Could not sign message with TPM.")
            self.remove_tmp_path(tmp_path)
            return False

        # try:
        #     subprocess.run(["openssl", "pkeyutl", "-pubin", "-inkey", self.public_key_dir, "-verify", "-in", message_tmp_file_path, "-sigfile", signature_tmp_file])
        # except:
        #     log.error("Could not verify signature.")

        try:
            with open(signature_tmp_file, 'rb', buffering=0) as signature_reader:
                signature = signature_reader.read()
                self.remove_tmp_path(tmp_path)
            return b64encode(signature)
        except:
            log.error("Could not read signature from {}".format(signature_tmp_file))

        self.remove_tmp_path(tmp_path)
        return False

    def sign(self):
        key_cryptography = split_key_type(self.key_type)
        log.info('=> Signing message with type {}'.format(self.security))
        if self.security == 'DEFAULT':
            fs = Filesystem(self.key_dir, 'private.pem', 'rb')
            if key_cryptography == 'RSA':
                return self.sign_with_rsa_signing_key(fs.open_file())
            elif key_cryptography == 'ECC':
                return self.sign_with_ecc_signign_key(fs.open_file())
        if self.security == 'TPM':
            if self.key_type != 'RSA:2048':
                log.error('Unsupported.')
                exit(ExitStatus.failure)
            return self.sign_with_rsa_tpm_signing_key()
        return False
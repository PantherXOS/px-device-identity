
from sys import exit
import random
from uuid import uuid4, UUID
from exitstatus import ExitStatus
from string import ascii_uppercase

from .classes import RequestedOperation
from .rsa import RSA
from .filesystem import Filesystem
from .log import Logger
from .cm import CM
from .jwk import JWK

log = Logger('DEVICE')

class Device:
    def __init__(self, config_path, operation: RequestedOperation, device_type):
        self.config_path = config_path
        self.operation_type = operation.operation_type
        self.device_type = device_type
        self.force_operation = operation.force_operation
        self.id = uuid4()
        self.device_id_path = config_path + 'device_id'

    def generate_random_device_name(self):
        letters = ascii_uppercase
        identifier = ''.join(random.choice(letters) for i in range(8))
        return 'Device-' + identifier

    def check_init(self):
        try:
            with open(self.device_id_path, 'r') as reader:
                device_id = reader.read()
                try:
                    if len(device_id) == 21:
                        log.info('Found Nano ID. Assuming MANAGED device.')
                    else:
                        UUID(device_id, version=4)
                    try:
                        public_key_path = self.config_path + 'public.pem'
                        with open(public_key_path) as public_key_reader:
                            public_key_reader.read()
                            return True
                    except FileNotFoundError:
                        return False
                except ValueError:
                    return False
        except FileNotFoundError:
            return False

    def init(self, host: str):
        initiated = self.check_init()
        if initiated:
            log.error('Device has already been initiated.')
            if self.force_operation:
                log.warning("=> OVERWRITING")
            else:
                log.error("Use '--force True' to overwrite. Use with caution!")
                exit(ExitStatus.failure)
        else:
            log.info("=> Initiating a new device")
            fs = Filesystem(self.config_path, 'device_id', 'r')
            fs.create_path()
        
        device_id = self.id
        
        rsa = RSA(self.config_path, self.operation_type)
        rsa.generate_and_save_to_config_path()

        if self.device_type == 'MANAGED':
            log.info("This is a MANAGED device.")
            jwk = JWK(self.config_path, self.operation_type)
            jwks = jwk.get_jwks()
            #identity = {
            #    'label': 'IdP',
            #    'sopin': 'abc',
            #    'userpin': 'abc',
            #    'path': '~/.data/tpm2'
            #}
            registration = {
                "public_key": jwks,
                "title": self.generate_random_device_name(),
                "location": "Unknown",
            }
            cm = CM(registration, host)
            device_id = cm.register_device()
            if device_id == False:
                log.error("Did not receive 'device_id' from remote server.")
                exit(ExitStatus.failure)

        if self.device_type == 'UNMANAGED':
            log.info('This is an UNAMANAGED device.')
            pass
        
        log.info("=> Saving identification as uuid4 in {}".format(self.device_id_path))
        filesystem = Filesystem(self.config_path, 'device_id', 'w')
        saved = filesystem.create_file(str(device_id))
        if saved:
            return True
        else:
            return False
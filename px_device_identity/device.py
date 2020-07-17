
import yaml
import shortuuid

from sys import exit
from datetime import datetime
from uuid import uuid4, UUID
from exitstatus import ExitStatus
from string import ascii_uppercase

from .classes import DeviceClass, RequestedOperation
from .crypto import Crypto
from .filesystem import Filesystem
from .log import Logger
from .cm import CM
from .jwk import JWK
from .util import KEY_DIR, CONFIG_DIR

log = Logger('DEVICE')

class Device:
    def __init__(self, operation_class, device_class: DeviceClass, key_dir = KEY_DIR()):
        self.operation_class = operation_class
        self.security = operation_class.security
        self.key_type = vars(operation_class)['key_type']
        self.device_type = vars(device_class)['device_type']
        self.device_is_managed = vars(device_class)['device_is_managed']
        self.force_operation = vars(operation_class)['force_operation']
        self.id = uuid4()
        self.device_key_dir = key_dir
        self.device_config_dir = CONFIG_DIR()
        self.device_config_path = CONFIG_DIR() + 'device.yml'

    def generate_random_device_name(self, host: str):
        try:
            return 'Device-' + shortuuid.uuid(name=host)
        except:
            log.error("Could not generate device ID with uuid.NAMESPACE_URL {}".format(host))
            exit(ExitStatus.failure)

    def check_init(self) -> bool:
        try:
            with open(self.device_config_path, 'r') as reader:
                file_content = reader.read()
                try:
                    device_config = yaml.load(file_content, Loader=yaml.BaseLoader)
                    if len(device_config.get('id')) == 21:
                        log.info('Found Nano ID. Assuming MANAGED device.')
                    else:
                        UUID(device_config.get('id'), version=4)
                    try:
                        public_key_path = self.device_key_dir + 'public.pem'
                        with open(public_key_path) as public_key_reader:
                            public_key_reader.read()
                        return True
                    except FileNotFoundError:
                        return False
                except ValueError:
                    return False
        except FileNotFoundError:
            return False

    def check_is_managed(self):
        log.info('=> Verifying whether device is Managed.')
        try:
            with open(self.device_config_path, 'r') as reader:
                file_content = reader.read()
                try:
                    device_config = yaml.load(file_content, Loader=yaml.BaseLoader)
                    device_is_managed = device_config.get('isManaged')
                    host = device_config.get('host')
                    if host != 'NONE' and device_is_managed == True:
                        return True
                except:
                    log.error('Could not find load yaml-formatted config from {}'.format(self.device_config_path))
        except:
            log.error('Could not read config file at {}'.format(self.device_config_path))
        return False
        
    def init(self, host: str):
        if self.check_init():
            if self.force_operation:
                log.warning('Device has already been initiated.')
                log.warning("=> FORCE OVERWRITE")
            else:
                log.error('Device has already been initiated.')
                log.error("Use '--force True' to overwrite. Use with caution!")
                exit(ExitStatus.failure)
        else:
            log.info("=> Initiating a new device")
            fs = Filesystem(CONFIG_DIR(), 'device_id', 'r')
            fs.create_path()
        
        crypto = Crypto(self.operation_class)
        crypto.generate_and_save_to_config_path()

        if self.device_is_managed == True:
            log.info("This is a MANAGED device.")
            jwk = JWK(self.security)
            jwks = jwk.get_jwks()
            registration = {
                "public_key": jwks,
                "title": self.generate_random_device_name(host),
                "location": "Unknown",
            }
            cm = CM(registration, host)
            device_id = cm.register_device()
            if device_id == False:
                log.error("Did not receive 'device_id' from remote server.")
                exit(ExitStatus.failure)
        else:
            device_id = self.id

        device_id_str = str(device_id)
        cfg_device = {
            'id': device_id_str,
            'deviceType': self.device_type,
            'keySecurity': self.security,
            'keyType': str(self.key_type),
            'isManaged': self.device_is_managed,
            'host': str(host),
            'configVersion': '0.0.1',
            'initiatedOn': str(datetime.now())
        }

        if self.device_is_managed == True:
            log.info("=> Saving device identification as NanoID in {}".format(self.device_config_path))
        else:
            cfg_device['host'] = 'NONE'
            log.info('This is an UNAMANAGED device.')
            log.info("=> Saving device identification as uuid4 in {}".format(self.device_config_path))

        try:
            with open(self.device_config_path, 'w') as fs_device_writer:
                fs_device_writer.write(yaml.dump(cfg_device))
        except:
            log.error("Could not write device configuration.")
            return False
        return True
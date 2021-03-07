import sys
from shutil import rmtree
from os.path import isdir
from json import dumps as json_dumps
from exitstatus import ExitStatus
from px_device_identity.log import Logger
from .filesystem import Filesystem
from .jwk import JWK
from .util import is_initiated
from .classes import DeviceRegistrationProperties
from .config import DeviceConfig, CONFIG_DIR, CONFIG_FILE, KEY_DIR
from .cm import CM
from .crypto import Crypto
from .sign import Sign

log = Logger(__name__)


def create_keys(properties: 'DeviceProperties'):
    crypto = Crypto(properties)
    crypto.generate_and_save_to_key_path()


class Device:
    '''Handles configuration and keys'''
    def __init__(self, overwrite: bool = False, key_dir=KEY_DIR):
        # Paths and Config
        self.key_dir: str = key_dir
        self.config_dir = CONFIG_DIR
        self.config_path = CONFIG_FILE
        # Device
        self.config = DeviceConfig()
        self.is_initiated: bool = is_initiated()
        properties = None
        if self.is_initiated and overwrite is False:
            properties = self.config.get()
        self.properties = properties
        self.overwrite = overwrite

    def _init_managed(self, properties: 'DeviceProperties'):
        '''Initiated managed device'''
        log.info("This is a MANAGED device.")
        public_key = JWK(properties).get_jwks()
        registration = DeviceRegistrationProperties(public_key, properties)
        result = CM(registration).register_device()
        if result is False:
            log.error("Did not receive the expected response from remote server.")
            sys.exit(ExitStatus.failure)
        device_id = result[0]
        client_id = result[1]

        properties.id = device_id
        properties.client_id = client_id

        self.config.save(properties)

    def _init_standalone(self, properties: 'DeviceProperties'):
        '''Initiate standalone device'''
        log.info('This device does not belong to any organization (UNMANAGED).')
        self.config.save(properties)

    def init(self, properties: 'DeviceProperties') -> bool:
        '''Initiate the device'''
        is_managed = properties.is_managed
        if self.is_initiated:
            if self.overwrite:
                log.warning('Device has already been initiated.')
                log.warning("=> FORCE OVERWRITE")
                self.destroy()
                self._recreate()
            else:
                log.error('Device has already been initiated.')
                log.error("Use '--force True' to overwrite. Use with caution!")
                sys.exit(ExitStatus.failure)
        else:
            log.info("=> Initiating a new device")
            self._recreate()
        # log.info("Device has been initiated")

        create_keys(properties)

        if is_managed:
            self._init_managed(properties)
        else:
            self._init_standalone(properties)

    def destroy(self):
        '''Delete device configuration and key(s)'''
        if isdir(self.key_dir):
            log.info('=> Deleting {}'.format(self.key_dir))
            rmtree(self.key_dir)
        if isdir(self.config_dir):
            log.info('=> Deleting {}'.format(self.config_dir))
            rmtree(self.config_dir)

    def _recreate(self):
        '''Create config dir'''
        fs = Filesystem(CONFIG_DIR, 'none', 'none')
        fs.create_path()

    def get_jwk(self):
        '''Generates and returns JWK'''
        return json_dumps(JWK(self.properties).get())

    def get_jwks(self):
        '''Generates JWK and returns JWKS'''
        return json_dumps(JWK(self.properties).get_jwks())

    def sign(self, message: str):
        '''Sign the message'''
        return Sign(self.properties, message).sign()

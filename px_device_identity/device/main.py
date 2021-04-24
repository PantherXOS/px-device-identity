from json import dumps as json_dumps
import logging
from os.path import isdir
from shutil import rmtree
import sys

from exitstatus import ExitStatus

from .classes import DeviceProperties, DeviceRegistrationProperties
from .cm import CM
from .config import CONFIG_DIR, CONFIG_FILE, DeviceConfig, KEY_DIR
from .crypto import Crypto
from .filesystem import Filesystem
from .jwk import JWK
from .jwt import generate_signature_content_from_dict, get_device_jwt_content
from .sign import Sign
from .util import is_initiated

log = logging.getLogger(__name__)


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
        log.debug("This is a MANAGED device.")
        public_key = JWK(properties).get_jwks()
        registration = DeviceRegistrationProperties(public_key, properties)
        try:
            result = CM(properties).register_device(registration)
            properties.id = result[0] # device_id
            properties.client_id = result[1] # client_id
            self.config.save(properties)
        except Exception as err:
            log.error("Could not complete device registration.", exc_info=err)
            raise err

    def _init_standalone(self, properties: 'DeviceProperties'):
        '''Initiate standalone device'''
        log.debug('This device does not belong to any organization (UNMANAGED).')
        self.config.save(properties)

    def init(self, properties: 'DeviceProperties'):
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

        create_keys(properties)

        try:
            if is_managed:
                self._init_managed(properties)
            else:
                self._init_standalone(properties)
        except Exception as err:
            log.info('=> Rolling back all changes.', exc_info=err)
            self.destroy()

    def destroy(self):
        '''Delete device configuration and key(s)'''
        if isdir(self.key_dir):
            log.debug('=> Deleting {}'.format(self.key_dir))
            rmtree(self.key_dir)
        if isdir(self.config_dir):
            log.debug('=> Deleting {}'.format(self.config_dir))
            rmtree(self.config_dir)

    def _recreate(self):
        '''Create config dir'''
        fs = Filesystem(CONFIG_DIR, 'none', 'none')
        fs.create_path()

    def get_jwk(self):
        '''Generates and returns JWK'''
        if self.properties is None: raise Exception('Device is not initiated.')
        return json_dumps(JWK(self.properties).get())

    def get_jwks(self):
        '''Generates JWK and returns JWKS'''
        if self.properties is None: raise Exception('Device is not initiated.')
        return json_dumps(JWK(self.properties).get_jwks())

    def get_device_jwt(self):
        '''
        Generates and returns device JWT

            Returns: {
                device_jwt,
                iat: int,
                exp: int
            }
        '''
        if self.properties is None: raise Exception('Device is not initiated.')
        device_token_jwt_claim = get_device_jwt_content(self.properties)
        iat = device_token_jwt_claim['iat']
        exp = device_token_jwt_claim['exp']
        signature_content = generate_signature_content_from_dict(device_token_jwt_claim, iat, exp)
        signature = Sign(self.properties, signature_content).sign()
        device_jwt = "{}.{}".format(signature_content, signature)

        return {
            'device_jwt': device_jwt,
            'iat': iat,
            'exp': exp
        }

    def sign(self, message: str):
        '''
        Sign the message
        
            Returns: str
        '''
        if self.properties is None: raise Exception('Device is not initiated.')
        return Sign(self.properties, message).sign()

    def get_access_token(self):
        '''
        Get Device access token and store it in data dir
        
            Returns: {
                access_token: str,
                expires_at: int
            }
        '''
        if self.properties is None: raise Exception('Device is not initiated.')
        device_jwt_props = self.get_device_jwt()

        return CM(self.properties).request_access_token(device_jwt_props['device_jwt'])

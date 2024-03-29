import logging
from json import dumps as json_dumps
from os import mkdir
from os.path import isdir
from shutil import rmtree

from px_device_identity.errors import NotInitiated

from .cache import get_device_access_token_cache, set_device_access_token_cache
from .classes import DeviceProperties, DeviceRegistrationProperties
from .cm import CM
from .config import CONFIG_DIR, CONFIG_FILE_NAME, KEY_DIR, DeviceConfig
from .crypto import Crypto
from .jwk import JWK
from .jwt import generate_signature_content_from_dict, get_device_jwt_content
from .sign import Sign
from .util import is_initiated

log = logging.getLogger(__name__)


def create_keys(properties: "DeviceProperties", key_dir: str):
    crypto = Crypto(properties, key_dir)
    crypto.generate_and_save_to_key_path()


class Device:
    '''Handles configuration and keys'''

    def __init__(
        self,
        overwrite: bool = False,
        key_dir: str = KEY_DIR,
        config_dir: str = CONFIG_DIR,
    ):
        # Paths and Config
        self.key_dir = key_dir
        self.config_dir = config_dir
        self.config_path = config_dir + "/" + CONFIG_FILE_NAME
        # Device
        self.config = DeviceConfig(config_path=self.config_path)
        self.is_initiated = False
        self.properties = None
        if not overwrite:
            '''If we are not overwriting with --force, check if device is initiated'''
            initiated = is_initiated(config_dir=self.config_dir)
            if initiated:
                '''If the device is initiated'''
                self.is_initiated = initiated
                self.properties = self.config.get()

        self.overwrite = overwrite

    def _init_managed(self, properties: 'DeviceProperties'):
        '''Initiated managed device'''
        log.debug("This is a MANAGED device.")
        public_key = JWK(properties, key_dir=self.key_dir).get_jwks()
        registration = DeviceRegistrationProperties(public_key, properties)
        try:
            result = CM(properties).register_device(registration)
            properties.id = result[0]  # device_id
            properties.client_id = result[1]  # client_id
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
                self._recreate_config_dir()
            else:
                log.error('Device has already been initiated.')
                log.error("Use '--force True' to overwrite. Use with caution!")
                raise EnvironmentError('Device has already been initiated.')
        else:
            log.info("=> Initiating a new device")
            self._recreate_config_dir()

        create_keys(properties, key_dir=self.key_dir)

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

    def _recreate_config_dir(self):
        '''Create config dir'''
        if not isdir(self.config_dir):
            mkdir(self.config_dir)
        else:
            log.warning(
                'Config dir already exists {}. Skipping ...'.format(
                    self.config_dir)
            )

    def get_jwk(self):
        '''Generates and returns JWK'''
        if self.properties is None:
            raise NotInitiated()
        return json_dumps(JWK(self.properties, key_dir=self.key_dir).get())

    def get_jwks(self):
        '''Generates JWK and returns JWKS'''
        if self.properties is None:
            raise NotInitiated()
        return json_dumps(JWK(self.properties, key_dir=self.key_dir).get_jwks())

    def get_device_jwt(self, aud: str = '/oidc/token'):
        '''
        Generates and returns device JWT
        CACHED: Does not request new JWT if one exists and is valid

            Params:
                aud: usually either '/oidc/token' (default) or '/oidc/token/introspection'

            Returns: {
                    device_jwt,
                    iat: int,
                    exp: int
            }

            raise: SigningError
        '''
        if self.properties is None:
            raise NotInitiated()

        device_token_jwt_claim = get_device_jwt_content(self.properties, aud)
        iat = device_token_jwt_claim['iat']
        exp = device_token_jwt_claim['exp']
        signature_content = generate_signature_content_from_dict(
            device_token_jwt_claim, iat, exp
        )
        try:
            signature = Sign(self.properties, signature_content).sign()
        except:
            log.error('Could not get device signature')
            raise
        else:
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
        if self.properties is None:
            raise NotInitiated()
        return Sign(self.properties, message, self.key_dir).sign()

    def get_access_token(self, aud: str = '/oidc/token'):
        '''
        Get Device access token and store it in data dir

            Returns: {
                    access_token: str,
                    expires_at: int
            }
        '''
        if self.properties is None:
            raise NotInitiated()

        '''(1) Try the cache'''
        try:
            cache = get_device_access_token_cache(aud=aud)
        except Exception as err:
            log.info(err)
        else:
            return cache

        '''(2) Get new device JWT'''
        device_jwt = None
        try:
            device_jwt_props = self.get_device_jwt(aud)
        except Exception as err:
            log.error("Could not get device JWT %s", err)
            raise
        else:
            device_jwt = device_jwt_props['device_jwt']

        '''(3) Get access token'''
        try:
            response = CM(self.properties).request_access_token(
                device_jwt
            )
            if response is None:
                raise ValueError('Access token request response is empty.')
            set_device_access_token_cache(response, aud=aud)
        except:
            log.error('Could not get access token')
            raise
        else:
            return response

    def token_introspection(self, user_access_token):
        '''
        Introspection to validate a user access token

            returns {
                active,
                client_id
                sub,
                exp,
                iat,
                iss,
                jti,
                scope,
                token_type
            }
        '''
        if self.properties is None:
            raise NotInitiated()

        # aud='/oidc/token/introspection'
        device_jwt_dict = self.get_device_jwt(aud='/oidc/token/introspection')
        try:
            response = CM(self.properties).token_introspection(
                user_access_token, device_jwt_dict['device_jwt']
            )
            return response
        except:
            log.error('Token introspection failed.')
            raise

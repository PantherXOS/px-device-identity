from requests.models import HTTPError


class AccessTokenCacheNotFound(Exception):
    def __init__(self, message='Device access token cache not set.'):
        self.message = message
        self.error_code = 11


class AccessTokenCacheExpired(Exception):
    def __init__(self, message='Device access token cache expired.'):
        self.message = message
        self.error_code = 12


class RegistrationError(Exception):
    def __init__(self, message='Something went wrong with the registration.'):
        self.message = message
        self.error_code = 20


class RegistrationRejected(RegistrationError):
    def __init__(self, message='Device registration was rejected.'):
        self.message = message
        self.error_code = 21


class RegistrationStatusError(RegistrationError):
    def __init__(self, message='Device registration failed with error.'):
        self.message = message
        self.error_code = 22


class RegistrationStatusServerError(RegistrationError):
    def __init__(self, status_code):
        self.message = 'Something went wrong: Received an error {} from the server.'.format(
            status_code
        )
        self.error_code = 23


class RegistrationStatusNotFound(RegistrationError):
    def __init__(self, message='Cannot find pending registration. Did you register already?'):
        self.message = message
        self.error_code = 24


class NotInitiated(Exception):
    def __init__(self, message='This device has not been initiated.'):
        self.message = message
        self.error_code = 2


class CMAuthenticationFailed(HTTPError):
    def __init__(self, message='Failed to authenticate with Central Management.'):
        self.message = message
        self.error_code = 31


class CMServerError(HTTPError):
    '''CM: 500'''

    def __init__(self, message='Central Management has encountered an error.'):
        self.message = message
        self.error_code = 31


class SigningError(Exception):
    '''For module device/sign'''

    def __init__(self, message='Could not sign message with private key'):
        self.message = message
        self.error_code = 40


class CryptoError(Exception):
    '''For module device/crypto'''

    def __init__(self, message):
        self.message = message
        self.error_code = 50


class CryptoGenError(CryptoError):
    def __init__(self, message='Could not generate key pair.'):
        self.message = message
        self.error_code = 51

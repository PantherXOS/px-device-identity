import logging
import sys
from base64 import urlsafe_b64decode, urlsafe_b64encode

from authlib.jose import jwk
from exitstatus import ExitStatus

from .config import KEY_DIR, DeviceConfig
from .filesystem import remove_tmp_path

log = logging.getLogger(__name__)


def is_initiated() -> bool:
    '''Checks whether the device has already been initiated'''
    try:
        device_properties = DeviceConfig().get()
        if len(device_properties.id) == 21:
            log.debug('Found Nano ID. Assuming MANAGED device.')
        #else:
        #    UUID(device_properties.id, version=4)
        try:
            public_key_path = KEY_DIR + 'public.pem'
            with open(public_key_path) as public_key_reader:
                public_key_reader.read()
            return True
        except FileNotFoundError:
            log.error('Could not find {}.'.format(public_key_path))
            return False
    except FileNotFoundError:
        return False

    except KeyError:
        log.error('The configuration appears to be invalid.')
        return False


def b64encode(string: bytes) -> str:
    '''base64 encode'''
    s_bin = urlsafe_b64encode(string)
    s_bin = s_bin.replace(b'=', b'')
    return s_bin.decode('ascii')


def b64decode(string: str) -> bytes:
    '''base64 decode'''
    s_bin = string.encode('ascii')
    s_bin += b'=' * (4 - len(s_bin) % 4)
    return urlsafe_b64decode(s_bin)


def handle_error(error: str):
    log.error(error)
    sys.exit(ExitStatus.failure)


def handle_result(result, error: str, tmp_path: str = None):
    if isinstance(result, bool):
        if result is False:
            if tmp_path is not None:
                remove_tmp_path(tmp_path)
            handle_error(error)
    else:
        has_return_code = 'returncode' in result
        if has_return_code and result.get('returncode') == 1:
            if tmp_path is not None:
                remove_tmp_path(tmp_path)
            handle_error(error)


def split_key_type(key: str):
    '''Split string'''
    key_array = key.split(":")
    key_cryptography = key_array[0]
    if key_cryptography == 'RSA':
        key_strength = int(key_array[1])
    elif key_cryptography == 'ECC':
        key_strength = key_array[1]
    return key_cryptography, key_strength

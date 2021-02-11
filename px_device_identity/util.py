import re
from base64 import (
    urlsafe_b64encode,
    urlsafe_b64decode,
)
from exitstatus import ExitStatus

from .log import Logger
from .filesystem import remove_tmp_path

log = Logger('UTIL')

def b64encode(s: bytes) -> str:
    s_bin = urlsafe_b64encode(s)
    s_bin = s_bin.replace(b'=', b'')
    return s_bin.decode('ascii')

def b64decode(s: str) -> bytes:
    s_bin = s.encode('ascii')
    s_bin += b'=' * (4 - len(s_bin) % 4)
    return urlsafe_b64decode(s_bin)

def split_key_type(key: str):
    key_array = key.split(":")
    key_cryptography = key_array[0]
    if key_cryptography == 'RSA':
        key_strength =int(key_array[1])
    elif key_cryptography == 'ECC':
        key_strength =key_array[1]
    return key_cryptography, key_strength

def handle_error(error: str):
    log.error(error)
    exit(ExitStatus.failure)

def handle_result(result, error: str, tmp_path: str = None):
    print(type(result))
    if type(result) == bool:
        if result == False:
            if tmp_path is not None:
                remove_tmp_path(tmp_path)
            handle_error(error)
    else:
        has_return_code = 'returncode' in result
        if has_return_code and result.get('returncode') == 1:
            if tmp_path is not None:
                remove_tmp_path(tmp_path)
            handle_error(error)

def is_fqdn(hostname: str) -> bool:
    """
    https://en.m.wikipedia.org/wiki/Fully_qualified_domain_name
    """
    if not 1 < len(hostname) < 253:
        return False

    # Remove trailing dot
    if hostname[-1] == '.':
        hostname = hostname[0:-1]

    #  Split hostname into list of DNS labels
    labels = hostname.split('.')

    #  Define pattern of DNS label
    #  Can begin and end with a number or letter only
    #  Can contain hyphens, a-z, A-Z, 0-9
    #  1 - 63 chars allowed
    fqdn = re.compile(r'^[a-z0-9]([a-z-0-9-]{0,61}[a-z0-9])?$', re.IGNORECASE)

    # Check that all labels match that pattern.
    return all(fqdn.match(label) for label in labels)
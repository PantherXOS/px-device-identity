from pathlib import Path
from base64 import (
    urlsafe_b64encode,
    urlsafe_b64decode,
)

def b64encode(s: bytes) -> str:
    s_bin = urlsafe_b64encode(s)
    s_bin = s_bin.replace(b'=', b'')
    return s_bin.decode('ascii')

def b64decode(s: str) -> bytes:
    s_bin = s.encode('ascii')
    s_bin += b'=' * (4 - len(s_bin) % 4)
    return urlsafe_b64decode(s_bin)

def KEY_DIR():
    home_path = str(Path.home())
    config_path = '/.config/device/'
    return home_path + config_path

def CONFIG_DIR():
    return '/etc/px-device-identity/'

def split_key_type(key: str):
    key_array = key.split(":")
    key_cryptography = key_array[0]
    key_strength =key_array[1]
    return key_cryptography, key_strength
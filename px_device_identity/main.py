from pathlib import Path
import json
import binascii

from .device import init
from .jwk import generate_and_save_jwk, get_jwk
from .cli import get_cl_arguments
from .sign import sign

def get_config_path():
    home_path = str(Path.home())
    config_path = '/.config/device/'
    return home_path + config_path

def run_all():
    # TODO; device `title`
    # TODO: device `location`
    # type = 'fs'
    path = get_config_path()
    cl_arguments = get_cl_arguments()
    operation = cl_arguments.get('operation')
    string = cl_arguments.get('string')
    type = 'default'

    if operation == 'init':
        result = init(path, type)
        return json.dumps(result)

    if operation == 'getJWK':
        result = get_jwk(path)
        return json.dumps(result)

    if operation == 'sign':
        result = sign('default', path, string)
        conv = binascii.b2a_base64(result)
        return conv

    unknownError = {
        'status': 'error',
        'status_signature': 'error:unknown',
        'message': 'An unknown error has occured.'
    }
    return unknownError
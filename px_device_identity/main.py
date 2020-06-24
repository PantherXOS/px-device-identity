from .rsa import generate_rsa_keys
from .jwk import generate_and_save_jwk, get_jwk
from .filesystem import create_path
from .cli import get_cl_arguments
from pathlib import Path
import json

def get_config_path():
    home_path = str(Path.home())
    config_path = '/.config/device/'
    return home_path + config_path

def generate_keys():
    type = 'fs'
    path = get_config_path()

    created_path = create_path(path)
    if created_path == False:
        return {
            'status': 'error',
            'status_signature': 'error:path',
            'message': 'Could not create path.'
        }

    generated_rsa_keys = generate_rsa_keys(type, path)
    if generated_rsa_keys == False:
        return {
            'status': 'error',
            'status_signature': 'error:rsa' ,
            'message': 'Could not generate RSA keys.'
        }
    print('Generated RSA keys')

    generated_jwk = generate_and_save_jwk(path)
    if generated_jwk == False:
        return {
            'status': 'error',
            'status_signature': 'error.jwk',
            'message': 'Could not generate JWK from existing RSA keys.'
        }
    print('Generated JWK keys')

    return {
        'status': 'success',
        'status_signature': 'success',
        'message': 'All done.'
    }

def run_all():
    # type = 'fs'
    path = get_config_path
    cl_arguments = get_cl_arguments()
    operation = cl_arguments.get('operation')

    if operation == 'generateKeys':
        result = generate_keys()
        return json.dumps(result)

    if operation == 'getJWK':
        result = get_jwk(path)
        return json.dumps(result)
        
    unknownError = {
        'status': 'error',
        'status_signature': 'error:unknown',
        'message': 'An unknown error has occured.'
    }
    return unknownError
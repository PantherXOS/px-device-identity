import sys
from pathlib import Path
import json
import binascii

from .device import Device
from .jwk import JWK
from .cli import get_cl_arguments
from .sign import Sign
from .cm import CM

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
    message = cl_arguments.get('message')
    host = cl_arguments.get('host')
    force_operation = cl_arguments.get('force')
    operation_type = cl_arguments.get('operation_type')

    device = Device(path, operation_type, force_operation)
    INITIATED = device.check_init()

    if operation != 'INIT' and INITIATED == False:
        print('ERROR: Device is not initiated.')
        print('Initiate device with --operation INIT --type <DEFAULT|TPM>')
        sys.exit()

    if operation == 'INIT':
        device = Device(path, operation_type, force_operation)
        success = device.init()
        if success:
            return 'SUCCESS'
        else:
            return 'ERROR'

    if operation == 'GET_JWK':
        jwk = JWK(path, operation_type)
        return json.dumps(jwk.get())

    if operation == 'SIGN':
        sign = Sign(path, operation_type, message)
        signed = sign.sign()
        signed_converted = binascii.b2a_base64(signed)
        return signed_converted

    if operation == 'REGISTER':
        identity: TPM2KeyIdentity = {
            'label': 'IdP',
            'sopin': 'abc',
            'userpin': 'abc',
            'path': '~/.data/tpm2'
        }
        # TODO: Actual values!
        registration: DeviceRegistration = {
            'public_key': '',
            'title': 'Device-ABC',
            'location': 'BK1',
        }
        cm = CM(registration, host)
        registered =  cm.register_device()
        if registered:
            print('Registered')
        print('Failed to register.')
        return 'ERROR'

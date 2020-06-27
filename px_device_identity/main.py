import sys
from exitstatus import ExitStatus
from pathlib import Path
import json
import binascii

from .device import Device
from .jwk import JWK
from .cli import get_cl_arguments
from .sign import Sign
from .cm import CM
from .log import Logger

log = Logger('MAIN')

def get_config_path():
    home_path = str(Path.home())
    config_path = '/.config/device/'
    return home_path + config_path

def handle_result(success):
    if success:
        sys.exit(ExitStatus.success)
    else:
        sys.exit(ExitStatus.failure)

def main():
    log.info('Welcome to PantherX Device Identity Service')
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
        log.error('Device is not initiated.')
        log.error('Initiate device with --operation INIT --type <DEFAULT|TPM>')
        sys.exit(ExitStatus.failure)

    if operation == 'INIT':
        device = Device(path, operation_type, force_operation)
        initiated = device.init()
        handle_result(initiated)

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
        handle_result(registered)

if __name__ == '__main__':
    main()
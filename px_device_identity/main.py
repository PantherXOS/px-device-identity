from sys import exit
from exitstatus import ExitStatus
from pathlib import Path
from json import dumps as json_dumps
from getpass import getuser

from .classes import DeviceClass, RequestedOperation
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
        log.info("We're done here.")
        exit(ExitStatus.success)
    else:
        log.info("Something went wrong.")
        exit(ExitStatus.failure)

def main():
    log.info('------')
    log.info('Welcome to PantherX Device Identity Service')
    log.info('------')

    current_user = getuser()
    if current_user != 'root':
        log.warning('!!! This application is designed to run as root on the target device !!!')
        log.warning('!!! Current user: {}'.format(current_user))

    config_path = get_config_path()

    cl_arguments = get_cl_arguments()
    operation_dict: RequestedOperation = cl_arguments.get('operation')
    device_dict: DeviceClass = cl_arguments.get('device')
    message = cl_arguments.get('message')
    host = cl_arguments.get('host')

    device = Device(config_path, operation_dict, device_dict)
    INITIATED = device.check_init()

    if operation_dict.action != 'INIT' and INITIATED == False:
        log.error('Device is not initiated.')
        log.error('Initiate device with --operation INIT --type <DEFAULT|TPM>')
        exit(ExitStatus.failure)

    if operation_dict.action == 'INIT':
        device = Device(config_path, operation_dict, device_dict)
        initiated = device.init(host)
        handle_result(initiated)

    if operation_dict.action == 'GET_JWK':
        jwk = JWK(config_path, operation_dict)
        return json_dumps(jwk.get())

    if operation_dict.action == 'GET_JWKS':
        jwk = JWK(config_path, operation_dict)
        return json_dumps(jwk.get_jwks())

    if operation_dict.action == 'SIGN':
        sign = Sign(config_path, operation_dict.security, message)
        return sign.sign()

if __name__ == '__main__':
    main()
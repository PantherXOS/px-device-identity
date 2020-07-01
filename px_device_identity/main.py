from sys import exit
from exitstatus import ExitStatus
from pathlib import Path
from json import dumps as json_dumps

from .classes import RequestedOperation
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
    log.info('Welcome to PantherX Device Identity Service')
    log.info("--- This application should be run as root on the target device! ---")
    path = get_config_path()
    cl_arguments = get_cl_arguments()
    operation: RequestedOperation = cl_arguments.get('operation')
    message = cl_arguments.get('message')
    host = cl_arguments.get('host')
    device_type = cl_arguments.get('device_type')

    device = Device(path, operation, device_type)
    INITIATED = device.check_init()

    if operation.action != 'INIT' and INITIATED == False:
        log.error('Device is not initiated.')
        log.error('Initiate device with --operation INIT --type <DEFAULT|TPM>')
        exit(ExitStatus.failure)

    if operation.action == 'INIT':
        device = Device(path, operation, device_type)
        initiated = device.init(host)
        handle_result(initiated)

    if operation.action == 'GET_JWK':
        jwk = JWK(path, operation)
        return json_dumps(jwk.get())

    if operation.action == 'GET_JWKS':
        jwk = JWK(path, operation)
        return json_dumps(jwk.get_jwks())

    if operation.action == 'SIGN':
        sign = Sign(path, operation.operation_type, message)
        signed = sign.sign()
        signed_converted = signed
        return signed_converted

if __name__ == '__main__':
    main()
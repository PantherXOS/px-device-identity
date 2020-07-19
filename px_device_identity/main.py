from sys import exit
from exitstatus import ExitStatus
from json import dumps as json_dumps
from getpass import getuser

from .classes import DeviceClass, RequestedOperation
from .device import Device
from .jwk import JWK
from .cli import get_cl_arguments
from .sign import Sign
from .log import Logger
from .config import get_device_config

log = Logger('MAIN')

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
        exit()

    cl_arguments = get_cl_arguments()
    operation_class = cl_arguments.get('operation')
    device_type: str = cl_arguments.get('device_type')
    device_is_managed: bool = cl_arguments.get('device_is_managed')
    message: str = cl_arguments.get('message')
    host: str = cl_arguments.get('host')

    device_dict = DeviceClass(device_type, device_is_managed)

    device_init_check = Device(operation_class, device_dict)
    INITIATED = device_init_check.check_init()

    if operation_class.action != 'INIT' and INITIATED == False:
        log.error('Device is not initiated.')
        log.error('Initiate device with --operation INIT --type <DEFAULT|TPM>')
        exit(ExitStatus.failure)

    if operation_class.action == 'INIT':
        device = Device(operation_class, device_dict)
        initiated = device.init(host)
        handle_result(initiated)

    config = get_device_config()
    operation_class.security = config.get('keySecurity')
    operation_class.key_type = config.get('keyType')

    log.info('DEVICE CONFIG')
    log.info(config)

    if operation_class.action == 'GET_JWK':
        jwk = JWK(operation_class)
        return json_dumps(jwk.get())

    if operation_class.action == 'GET_JWKS':
        jwk = JWK(operation_class)
        return json_dumps(jwk.get_jwks())

    if operation_class.action == 'SIGN':
        sign = Sign(operation_class, message)
        return sign.sign()

if __name__ == '__main__':
    main()
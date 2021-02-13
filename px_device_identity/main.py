import sys
from getpass import getuser
from json import dumps as json_dumps
import pkg_resources

from exitstatus import ExitStatus

from .classes import DeviceClass
from .device import Device
from .jwk import JWK
from .cli import get_cl_arguments
from .sign import Sign
from .log import Logger
from .config import DeviceConfig
from .migration import first_migration_key_dir, second_migration_add_config_key_domain

log = Logger(__name__)
version = pkg_resources.require("px_device_identity")[0].version


def handle_result(success):
    if success:
        log.info("We're done here.")
        sys.exit(ExitStatus.success)
    else:
        log.info("Something went wrong.")
        sys.exit(ExitStatus.failure)

def main():
    log.info('------')
    log.info('Welcome to PantherX Device Identity Service')
    log.info('v{}'.format(version))
    log.info('------')

    current_user = getuser()
    if current_user != 'root':
        log.warning('!!! This application is designed to run as root on the target device !!!')
        log.warning('!!! Current user: {}'.format(current_user))
        sys.exit()

    cl_arguments = get_cl_arguments()
    operation_class = cl_arguments.get('operation')
    device_type: str = cl_arguments.get('device_type')
    device_is_managed: bool = cl_arguments.get('device_is_managed')
    message: str = cl_arguments.get('message')
    host: str = cl_arguments.get('host')
    domain: str = cl_arguments.get('domain')
    location: str = cl_arguments.get('location')

    device_dict = DeviceClass(device_type, device_is_managed)

    device = Device(operation_class, device_dict)
    INITIATED = device.check_init()
    if INITIATED is True:
        '''Run required migrations'''
        first_migration_key_dir()
        second_migration_add_config_key_domain()

    if operation_class.action != 'INIT' and INITIATED is False:
        log.error('Device is not initiated.')
        log.error('Initiate device with --operation INIT --type <DEFAULT|TPM>')
        sys.exit(ExitStatus.failure)

    if operation_class.action == 'INIT':
        initiated = device.init(host, domain, location)
        handle_result(initiated)

    config = DeviceConfig().get()
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

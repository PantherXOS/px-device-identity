'''PantherX Device Identity'''

import sys
import pkg_resources

from exitstatus import ExitStatus

from .cli import get_cl_arguments
from .log import Logger
# from .migration import first_migration_key_dir, second_migration_add_config_key_domain
from .util import is_superuser_or_quit
from .classes import OperationProperties
from .device import Device, DeviceProperties
import json

log = Logger(__name__)

version = pkg_resources.require("px_device_identity")[0].version


def main():
    log.info('------')
    log.info('Welcome to PantherX Device Identity Service')
    log.info('v{}'.format(version))
    log.info('------')

    is_superuser_or_quit()

    cl_arguments = get_cl_arguments()
    operation: OperationProperties = cl_arguments['operation']
    device_properties: DeviceProperties = cl_arguments['device_properties']
    message: str = cl_arguments['message']
    # debug: bool = cl_arguments['debug']

    device = Device(operation.force_operation)

    is_initiated = device.is_initiated
    # if is_initiated is True:
        # print('Supposed to run migration.')
        # '''Run required migrations'''
        # first_migration_key_dir()
        # second_migration_add_config_key_domain()

    if operation.action != 'INIT' and is_initiated is False:
        log.error('Device is not initiated.')
        log.error('Initiate device with --operation INIT --type <DEFAULT|TPM>')
        sys.exit(ExitStatus.failure)

    if operation.action == 'INIT':
        try:
            device.init(device_properties)
        except:
            print(sys.exc_info()[0])
            log.info("Something went wrong.")
            sys.exit(ExitStatus.failure)

        sys.exit(ExitStatus.success)

    # Here we initiate the device properties from config, since we are not initiating
    if operation.action == 'GET_JWK':
        return device.get_jwk()

    if operation.action == 'GET_JWKS':
        return device.get_jwks()

    if operation.action == 'SIGN':
        return device.sign(message)

    if operation.action == 'GET_ACCESS_TOKEN':
        return json.dumps(device.get_access_token())

if __name__ == '__main__':
    main()

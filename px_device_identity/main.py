'''PantherX Device Identity'''

import json
import logging
import sys
from typing import Union

import pkg_resources

from .classes import OperationProperties
from .cli import get_cl_arguments
from .device import Device, DeviceProperties
from .log import *
from .util import is_superuser_or_quit

version = pkg_resources.require("px_device_identity")[0].version

log = logging.getLogger(__name__)


def main(cl_arguments_overwrite: Union[dict, None] = None):
    log.info('Welcome to PantherX Device Identity v{}'.format(version))

    is_superuser_or_quit()

    cl_arguments = None
    if cl_arguments_overwrite:
        cl_arguments = cl_arguments_overwrite
    else:
        cl_arguments = get_cl_arguments()
    operation: OperationProperties = cl_arguments['operation']
    device_properties: DeviceProperties = cl_arguments['device_properties']
    key_dir = cl_arguments["key_dir"]
    config_dir = cl_arguments["config_dir"]
    message: str = cl_arguments['message']
    debug: bool = cl_arguments["debug"]

    if debug:
        ch.setLevel(logging.DEBUG)

    device = Device(operation.force_operation, key_dir=key_dir, config_dir=config_dir)

    is_initiated = device.is_initiated

    if operation.action != 'INIT' and is_initiated is False:
        log.error('Device is not initiated.')
        log.error('Initiate device with --operation INIT --type <DEFAULT|TPM>')
        sys.exit(1)
    elif operation.action == 'INIT' and is_initiated and operation.force_operation != True:
        log.error('Device has already been initiated.')
        log.error("Use '--force True' to overwrite. Use with caution!")
        sys.exit(1)

    if operation.action == 'INIT':
        try:
            device.init(device_properties)
        except Exception as err:
            print(err)
            log.error("Something went wrong.", )
            sys.exit(1)

        sys.exit(1)

    # Here we initiate the device properties from config, since we are not initiating
    if operation.action == 'GET_JWK':
        return device.get_jwk()

    if operation.action == 'GET_JWKS':
        return device.get_jwks()

    if operation.action == 'SIGN':
        return device.sign(message)

    if operation.action == 'GET_ACCESS_TOKEN':
        access_token = device.get_access_token()
        if not access_token:
            print('Could not get access token')
        return json.dumps(access_token)


if __name__ == '__main__':
    main()

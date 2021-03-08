'''Command line interface'''

import argparse
import sys

from exitstatus import ExitStatus

from .device import DeviceProperties
from .classes import OperationProperties
from .log import Logger
from .util import is_fqdn

log = Logger(__name__)


def get_cl_arguments():
    '''Command line arguments'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", type=str, required=True,
                        choices=['INIT', 'SIGN', 'GET_JWK', 'GET_JWKS', 'GET_ACCESS_TOKEN'],
                        help="Primary operations."
                       )
    parser.add_argument("-s", "--security", type=str, default='DEFAULT',
                        choices=['DEFAULT', 'TPM'],
                        help="Operating types: On supported hardware, the usage of TPM is encouraged. Defaults to DEFAULT."
                       )
    parser.add_argument("-k", "--keytype", required=False, default='RSA:2048',
                        choices=['RSA:2048', 'RSA:3072', 'ECC:p256', 'ECC:p384', 'ECC:p521'],
                        help="Key type and relative strength RSA:BITS / ECC:curve. Supported with TPM: ONLY RSA:2048 currently."
                       )
    parser.add_argument("-m", "--message", type=str,
                        help="Pass message to SIGN operation"
                        )
    parser.add_argument("-a", "--address", type=str,
                        help="Define host for INIT: This turns the device into a MANAGED one."
                       )
    parser.add_argument("-dn", "--domain", type=str,
                        help="Organization domain name. This is required for managed devices. Ex.: pantherx.org"
                       )
    parser.add_argument("-t", "--title", type=str,
                        help="Device title: An optional label for easier recognition."
                       )
    parser.add_argument("-l", "--location", type=str,
                        help="Device location: An optional label for easier recognition."
                       )
    parser.add_argument("-r", "--role", type=str, default='DESKTOP',
                        choices=['PUBLIC', 'DESKTOP', 'SERVER', 'ADMIN_TERMINAL', 'REGISTRATION_TERMINAL', 'OTHER'],
                        help="Device role. Defaults to DESKTOP."
                       )
    parser.add_argument("-f", "--force", type=bool, default=False,
                        choices=[True, False],
                        help="Force operations: Overwrite existing device registration."
                       )
    parser.add_argument("-d", "--debug", type=bool, default=False,
                        help="Turn on debug messages"
                       )
    args = parser.parse_args()
    operation = args.operation

    if operation == 'INIT' and args.address is not None:
        if args.domain is None:
            log.error("You need to indicate the organization domain name.")
            sys.exit(ExitStatus.failure)
            if not is_fqdn(args.domain):
                log.warning("{} is not a valid domain name (FQN).".format(args.domain))

    if operation == 'SIGN':
        if args.message is None:
            log.error("You need to pass a --message for signing.")
            sys.exit(ExitStatus.failure)

    '''Operation'''
    operation = OperationProperties(
        operation,
        args.force
    )

    '''Device'''
    device_properties = DeviceProperties(
        args.title,
        args.location,
        args.role,
        args.security,
        args.keytype,
        args.domain,
        args.address
    )

    print(device_properties)

    return {
        'operation': operation,
        'device_properties': device_properties,
        'message': args.message,
        'debug': args.debug,
    }

import argparse
from sys import exit
from exitstatus import ExitStatus

from .log import Logger
from .classes import DeviceClass, RequestedOperation

log = Logger('CLI')

def get_cl_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", type=str, required=True,
        choices=['INIT', 'SIGN', 'GET_JWK', 'GET_JWKS'],
        help="Primary operations."),
    parser.add_argument("-s", "--security", type=str,
        choices=['DEFAULT', 'TPM'],
        help="Operating types: On supported hardware, the usage of TPM is encouraged.")
    parser.add_argument("-k", "--keytype", required=False, default='RSA:2048',
        choices=['RSA:2048', 'RSA:3072', 'ECC:p256','ECC:p384', 'ECC:p521'],
        help="Key type and relative strength RSA:BITS / ECC:curve. Supported with TPM: ONLY RSA:2048 currently.")
    parser.add_argument("-t", "--type", type=str, default='DESKTOP',
        choices=['DESKTOP', 'SERVER', 'CLOUD', 'ENTERPRISE'],
        help="Device type. Defaults to DESKTOP.")
    parser.add_argument("-m", "--message", type=str,
        help="Pass message to SIGN operation")
    parser.add_argument("-a", "--address", type=str,
        help="Define host for INIT: This turns the device into a MANAGED one.")
    parser.add_argument("-f", "--force", type=bool, default=False,
        choices=[True, False],
        help="Force operations: Overwrite existing device registration.")
    parser.add_argument("-d", "--debug", type=bool, default=False,
        help="Turn on debug messages")
    args = parser.parse_args()

    device_is_managed = False
    if args.operation == 'INIT':
        if args.security is None:
            log.error("You need to indicate the key security with --security <DEFAULT|TPM>.")
            exit(ExitStatus.failure)
        if args.address is not None:
            device_is_managed = True
            
    if args.operation == 'SIGN':
        if args.message is None:
            log.error("You need to pass a --message for signing.")
            exit(ExitStatus.failure)

    operation_class = RequestedOperation(args.operation, args.security, args.keytype, args.force)

    return {
        'operation': operation_class, # RequestedOperation
        'device_type': args.type,
        'device_is_managed': device_is_managed,
        'message': args.message,
        'host': args.address,
        'debug': args.debug
    }
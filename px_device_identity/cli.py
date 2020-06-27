import sys
import argparse
from exitstatus import ExitStatus
from .log import Logger
from .classes import RequestedOperation

log = Logger('CLI')

def get_cl_arguments():
    device_type = 'UNMANAGED'

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", type=str,
                        help="Operation; Options: -- operation <INIT|GET_JWK|GET_JWKS|SIGN>")
    parser.add_argument("-t", "--type", type=str,
                        help="Operation type; Options: --type <DEFAULT|TPM>")
    parser.add_argument("-m", "--message", type=str,
                        help="Message type for signing; works only with 'SIGN' operation.")
    parser.add_argument("-a", "--address", type=str,
                         help="Define host for INIT: This turns the device into a MANAGED one.")
    parser.add_argument("-f", "--force", type=bool, default=False,
                        help="Overwrite existing device identity")
    parser.add_argument("-d", "--debug", type=bool, default=False,
                        help="Turn on debug messages")
    args = parser.parse_args()

    if args.operation is None:
        log.error("You need to specify a operation.")
        sys.exit()

    if args.operation == 'INIT':
        if args.address is not None:
            device_type = 'MANAGED'
    elif args.operation == 'GET_JWK' or args.operation == 'GET_JWKS':
        pass
    elif args.operation == 'SIGN':
        if args.message is None:
            log.error("You need to pass a --message for signing.")
            sys.exit(ExitStatus.failure)
    else:
        log.error("You need to specify a operation.")
        log.error("Options: --operation <INIT|GET_JWK|GET_JWKS|SIGN>")
        sys.exit(ExitStatus.failure)

    if args.type != 'DEFAULT' and args.type != 'TPM':
        log.error("You need to specify an operation type.")
        log.error("Options: --type <DEFAULT|TPM>")
        sys.exit(ExitStatus.failure)

    operation = RequestedOperation(args.operation, args.type, args.force)

    return {
        'operation': operation,
        'device_type': device_type,
        'message': args.message,
        'host': args.address,
        'debug': args.debug
    }
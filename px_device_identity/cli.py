import sys
import argparse
from exitstatus import ExitStatus
from .log import Logger

log = Logger('CLI')

def get_cl_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", type=str,
                        help="Operation; Options: -- operation <INIT|GET_JWK|SIGN|REGISTER>")
    parser.add_argument("-t", "--type", type=str,
                        help="Operation type; Options: --type <DEFAULT|TPM>")
    parser.add_argument("-m", "--message", type=str,
                        help="Message type for signing; works only with 'SIGN' operation.")
    parser.add_argument("-a", "--address", type=str,
                         help="Define host for registration")
    parser.add_argument("-f", "--force", type=bool, default=False,
                        help="Overwrite existing device identity")
    parser.add_argument("-d", "--debug", type=bool, default=False,
                        help="Turn on debug messages")
    args = parser.parse_args()

    if args.operation is None:
        log.error("ERROR: You need to specify a operation.")
        log.error("ERROR: You need to specify a operation.")
        sys.exit()

    if args.operation == 'INIT' or args.operation == 'GET_JWK':
        pass
    elif args.operation == 'REGISTER':
        if args.address is None:
            log.error("ERROR: You need to provide a host for registration: --address 'https://....'")
    elif args.operation == 'SIGN':
        if args.message is None:
            log.error("You need to pass a --message for signing.")
            sys.exit(ExitStatus.failure)
    else:
        log.error("ERROR: You need to specify a operation.")
        log.error("Options: -- operation <INIT|GET_JWK|SIGN>")
        sys.exit(ExitStatus.failure)

    if args.type != 'DEFAULT' and args.type != 'TPM':
        log.error("ERROR: You need to specify an operation type.")
        log.error("Options: --type <DEFAULT|TPM>")
        sys.exit(ExitStatus.failure)

    return {
        'operation': args.operation,
        'operation_type': args.type,
        'message': args.message,
        'host': args.address,
        'force': args.force,
        'debug': args.debug
    }
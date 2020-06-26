import sys
import argparse

def get_cl_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", type=str,
                        help="Operation; Options: -- operation <INIT|GET_JWK|SIGN>")
    parser.add_argument("-t", "--type", type=str,
                        help="Operation type; Options: --type <DEFAULT|TPM>")
    parser.add_argument("-m", "--message", type=str,
                        help="Message type for signing; works only with 'SIGN' operation.")
    parser.add_argument("-f", "--force", type=bool, default=False,
                        help="Overwrite existing device identity")
    parser.add_argument("-d", "--debug", type=bool, default=False,
                        help="Turn on debug messages")
    args = parser.parse_args()

    if args.operation is None:
        print("ERROR: You need to specify a operation.")
        print("Options: -- operation <INIT|GET_JWK|SIGN>")
        sys.exit()

    if args.operation == 'INIT' or args.operation == 'GET_JWK':
        pass
    elif args.operation == 'SIGN':
        if args.message is None:
            print("You need to pass a --message for signing.")
            sys.exit()
    else:
        print("ERROR: You need to specify a operation.")
        print("Options: -- operation <INIT|GET_JWK|SIGN>")
        sys.exit()

    if args.type != 'DEFAULT' and args.type != 'TPM':
        print("ERROR: You need to specify an operation type.")
        print("Options: --type <DEFAULT|TPM>")
        sys.exit()

    return {
        'operation': args.operation,
        'operation_type': args.type,
        'message': args.message,
        'force': args.force,
        'debug': args.debug
    }
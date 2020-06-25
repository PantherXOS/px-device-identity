import sys
import argparse

def get_cl_arguments():
    debug = False

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", type=str,
                        help="Type of operation; options: 'init', 'getJWK', 'sign'")
    parser.add_argument("-t", "--type", type=str,
                        help="Whether to use TPM; options: 'default', 'tpm'")
    parser.add_argument("-s", "--string", type=str,
                        help="String type for signing; works only with 'sign' operation.")
    parser.add_argument("-d", "--debug", type=bool,
                        help="Turn on debug messages")
    args = parser.parse_args()

    if args.operation is None:
        print("You need to specify an operation: 'generateKeys', 'getJWK', 'sign")
        sys.exit()

    if args.type is None:
        print("You need to specify whether to use the default, or TPM for key operations. Do -t")
        sys.exit()

    if args.operation == 'sign' and args.string is None:
        print("You need to pass a string for signing.")
        sys.exit()

    if args.debug is not None:
        if args.debug == True:
            debug = True

    return {
        'operation': args.operation,
        'string': args.string,
        'debug': debug
    }
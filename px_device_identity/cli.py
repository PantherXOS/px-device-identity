import sys
import argparse

def get_cl_arguments():
    debug = False

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation", type=str,
                        help="Type of operation; options: generateKeys, getJWK")
    parser.add_argument("-d", "--debug", type=bool,
                        help="Turn on debug messages")
    args = parser.parse_args()


    if args.operation is None:
        print("You need to specify an operation: generateKeys, getJWK")
        sys.exit()


    if args.debug is not None:
        if args.debug == True:
            debug = True


    return {
        'operation': args.operation,
        'debug': debug
    }
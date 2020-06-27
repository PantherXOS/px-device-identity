import sys
import os
import px_device_identity

def main():
    r = px_device_identity.main()
    if type(r) == str:
        sys.stdout.write(r)
    else:
        sys.stdout.buffer.write(r)
    sys.stdout.flush()

if __name__ == '__main__':
    main()
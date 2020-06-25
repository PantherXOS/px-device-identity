import sys
import os
import px_device_identity

def run():
    r = px_device_identity.run_all()
    if type(r) == str:
        sys.stdout.write(r)
    else:
        sys.stdout.buffer.write(r)
    sys.stdout.flush()

run()
import sys
import px_device_identity

def run():
    r = px_device_identity.run_all()
    sys.stdout.write(r)
    sys.stdout.flush()

run()
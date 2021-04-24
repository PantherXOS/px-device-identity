from sys import stdout
import px_device_identity

def main():
    res = px_device_identity.main()
    stdout.flush()
    if isinstance(res, str):
        stdout.write(res)
    elif isinstance(res, bytes):
        stdout.buffer.write(res)
    stdout.flush()

if __name__ == '__main__':
    main()

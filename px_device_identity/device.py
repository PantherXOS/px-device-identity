
import uuid
from .rsa import generate_keys
from .filesystem import create_file

def init(path, type):
    print('# Initiating a new device')
    device_uuid = uuid.uuid4()
    print('.. Device identificiation: {}'.format(device_uuid))
    print(".. Saving identification as uuid4 as 'device_id' at {}".format(path))
    file_path = path + 'device_id'
    with open(file_path, 'w') as writer:
        writer.write(str(device_uuid))
    return generate_keys(path, type)
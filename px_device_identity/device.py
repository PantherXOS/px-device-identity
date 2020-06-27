
import sys
import uuid
from uuid import UUID
from .rsa import RSA
from .filesystem import Filesystem
from .log import Logger

log = Logger('DEVICE')

class Device:
    def __init__(self, config_path, operation_type, force_operation):
        self.config_path = config_path
        self.operation_type = operation_type
        self.force_operation = force_operation
        self.id = uuid.uuid4()
        self.device_id_path = config_path + 'device_id'

    def check_init(self):
        try:
            with open(self.device_id_path, 'r') as reader:
                device_id = reader.read()
                try:
                    UUID(device_id, version=4)
                    try:
                        public_key_path = self.config_path + 'public.pem'
                        with open(public_key_path) as public_key_reader:
                            public_key_reader.read()
                            return True
                    except FileNotFoundError:
                        return False
                except ValueError:
                    return False
        except FileNotFoundError:
            return False

    def init(self):
        initiated = self.check_init()
        if initiated:
            log.error('# Device already initiated.')
            if self.force_operation:
                log.warning('=> OVERWRITING')
            else:
                log.error('=> Use --force TRUE to overwrite')
                sys.exit()
        else:
            log.info('# Initiating a new device')
            fs = Filesystem(self.config_path, 'device_id', 'r')
            fs.create_path()
        log.info("=> Saving identification as uuid4 as 'device_id' at {}".format(self.config_path))
        with open(self.device_id_path, 'w') as writer:
            writer.write(str(self.id))
        rsa = RSA(self.config_path, self.operation_type)
        return rsa.generate_and_save_to_config_path()


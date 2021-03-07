import sys
from dataclasses import dataclass
import uuid
import shortuuid
from px_device_identity.log import Logger

log = Logger(__name__)


def generate_random_name(role: str, domain: str) -> str:
    '''Generates a random device name'''
    try:
        return role + '-' + shortuuid.uuid(name=domain)
    except:
        log.error("Could not generate device ID with uuid.NAMESPACE_URL {}".format(domain))
        sys.exit(ExitStatus.failure)


@dataclass
class DeviceProperties:
    '''Attributes related primarily to the device itself'''
    title: str = None
    location: str = 'Undefined'
    role: str = 'desktop'
    key_security: str = 'default'
    key_type: str = 'RSA:2048'
    domain: str = 'Undefined'
    host: str = 'https://identity.pantherx.org'
    id: str = uuid.uuid4()
    client_id: str = 'Undefined'
    is_managed: bool = False

    def __post_init__(self):
        if self.title is None:
            self.title = generate_random_name(self.role, self.domain)

        if self.domain is not None or self.domain == 'Undefined':
            self.is_managed = True

        self.role = self.role.lower()
        self.key_security = self.key_security.lower()


@dataclass
class DeviceRegistrationProperties:
    '''Attributes related primarily to the registration'''
    public_key: str
    device_properties: DeviceProperties
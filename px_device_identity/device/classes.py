import logging
import uuid
from dataclasses import dataclass

import shortuuid

log = logging.getLogger(__name__)


def generate_random_name(role: str, domain: str) -> str:
    '''Generates a random device name'''
    try:
        return role + '-' + shortuuid.uuid(name=domain)
    except Exception as e:
        log.error("Could not generate device ID with uuid.NAMESPACE_URL {}".format(domain))
        raise e


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
    id: str = str(uuid.uuid4())
    client_id: str = 'Undefined'
    is_managed: bool = False

    def __post_init__(self):
        if self.title is None:
            self.title = generate_random_name(self.role, self.domain)

        if self.domain is not None or self.domain == 'Undefined':
            self.is_managed = True

        if self.location is None:
            self.location = 'Undefined'

        self.role = self.role.lower()
        self.key_security = self.key_security.lower()


@dataclass
class DeviceRegistrationProperties:
    '''Attributes related primarily to the registration'''
    public_key: dict
    device_properties: DeviceProperties

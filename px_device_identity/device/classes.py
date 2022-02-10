import logging
import uuid
from dataclasses import dataclass
from typing import Union

import shortuuid

log = logging.getLogger(__name__)


def generate_random_name(role: str, domain: str) -> str:
    '''Generates a random device name'''
    try:
        return role + '-' + shortuuid.uuid(name=domain)
    except Exception as err:
        log.error(
            "Could not generate device ID with uuid.NAMESPACE_URL {}".format(domain))
        raise err


@dataclass
class DeviceProperties:
    '''Attributes related primarily to the device itself'''
    title: Union[str, None] = None
    location: str = 'Undefined'
    role: str = 'desktop'
    key_security: str = 'default'
    key_type: str = 'RSA:2048'
    domain: str = 'Undefined'
    host: str = 'https://identity.pantherx.org'
    id: str = str(uuid.uuid4())
    client_id: Union[str, None] = None
    is_managed: bool = False

    def __post_init__(self):
        if self.title is None or self.title == 'Undefined':
            self.title = generate_random_name(self.role, self.domain)

        if self.location is None:
            self.location = 'Undefined'

        if self.domain is not None or self.domain == 'Undefined':
            self.is_managed = True

        self.role = self.role.lower()
        self.key_security = self.key_security.lower()


@dataclass
class DeviceRegistrationProperties:
    '''Attributes related primarily to the registration'''
    public_key: dict
    device_properties: DeviceProperties

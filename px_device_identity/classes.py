class DeviceRegistration:
    def __init__ (self, public_key, title: str, location: str):
        self.publicKey: str = public_key
        self.title: str = title
        self.location: str = location

class RequestedOperation:
    def __init__(self, action: str, security: str, key_type: str, force_operation: bool = False):
        self.action = action
        self.security = security
        self.key_type = key_type
        self.force_operation = force_operation

class DeviceClass:
    def __init__(self, device_type: str, device_is_managed: bool):
        self.device_type = device_type
        self.device_is_managed = device_is_managed

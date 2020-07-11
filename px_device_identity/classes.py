class TPM2KeyIdentity:
    def __init__ (self, label, sopin, userpin, path):
        self.label: str = label
        self.sopin: str = sopin
        self.userpin: str = userpin
        self.path: str = path
        
class DeviceRegistration:
    def __init__ (self, public_key, title, location):
        self.public_key: str = public_key
        self.title: str = title
        self.location: str = location

class RequestedOperation:
    def __init__(self, action, security, key_type, force_operation):
        self.action = action
        self.security = security
        self.key_type = key_type
        self.force_operation = force_operation

class DeviceClass:
    def __init__(self, device_type, device_is_managed):
        self.device_type = device_type
        self.device_is_managed = device_is_managed

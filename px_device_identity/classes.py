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
    def __init__(self, action, operation_type, force_operation):
        self.action = action
        self.operation_type = operation_type
        self.force_operation = force_operation
class TPM2KeyIdentity:
    def __init__ (self, label, sopin, userpin, path):
        self.label: str = label
        self.sopin: str = sopin
        self.userpin: str = userpin
        self.path: str = path

# TODO: public_key should be in JWKS format
class DeviceRegistration:
    def __init__ (self, public_key, title, location):
        self.public_key: str = public_key
        self.title: str = title
        self.location: str = location
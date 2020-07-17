import yaml
#from .filesystem import Filesystem


def open_file():
    with open('/etc/px-device-identity/device.yml', 'r') as reader:
        print('reading')
        return reader.read()

def get_device_config():
    #fs = Filesystem('/etc/px-device-identity/', 'device.yml', 'r')
    file = open_file()
    config = yaml.load(file, Loader=yaml.BaseLoader)
    cfg_device = {
            'id': config.get('id'),
            'deviceType': config.get('deviceType'),
            'keySecurity': config.get('keySecurity'),
            'keyType': config.get('keyType'),
            'isManaged': config.get('isManaged'),
            'host': config.get('host'),
            'configVersion': config.get('configVersion'),
            'initiatedOn': config.get('initiatedOn')
        }
    print(cfg_device)
    print(cfg_device.get('id'))

get_device_config()
    
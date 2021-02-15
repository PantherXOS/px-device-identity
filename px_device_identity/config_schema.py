'''Configuration scheme by version'''

CONFIG_SCHEMA = {
    '0.0.1': {
        'id': 'id',
        'deviceType': 'deviceType',
        'keySecurity': 'keySecurity',
        'keyType': 'keyType',
        'isManaged': 'isManaged',
        'host': 'host',
        'configVersion': 'configVersion',
        'initiatedOn': 'initiatedOn'
    },
    '0.0.2': {
        'id': 'id',
        'NONE': 'clientId'
        'deviceType': 'deviceType',
        'keySecurity': 'keySecurity',
        'keyType': 'keyType',
        'isManaged': 'isManaged',
        'host': 'host',
        'NONE': 'domain',
        'configVersion': 'configVersion',
        'initiatedOn': 'initiatedOn'
    }
}

import uuid
import time
import calendar
import json
import base64


def base64UrlEncode(val):
    return base64.urlsafe_b64encode(val.encode()).decode().rstrip("=")


def get_unix_time_in_seconds():
    '''Seconds since the epoch in UTC time'''
    return calendar.timegm(time.gmtime())


def get_device_token_jwt_claim(device_properties: 'DeviceProperties') -> dict:
    unix_time = get_unix_time_in_seconds()
    unix_time_plus_offset = unix_time + 300
    aud = device_properties.host + '/oidc/token'
    device_token_jwt_claim = {
        'iss': device_properties.client_id,
        'sub': device_properties.client_id,
        'aud': aud,
        'jti': str(uuid.uuid4()),
        'iat': unix_time,
        'exp': unix_time_plus_offset,
    }
    return device_token_jwt_claim


def generate_jwt_header(alg: str, iat: str, exp: str) -> dict:
    nbf = iat - 10
    header = {
        'alg': 'RS256',
        'typ': 'JWT',
        'exp': exp,
        'nbf': nbf,
        'iat': iat
    }
    return header


def generate_jwt_signature_content(device_token_jwt_claim: dict):
    alg = 'RS256'
    iat = device_token_jwt_claim['iat']
    exp = device_token_jwt_claim['exp']
    stringifiedHeader = json.dumps(generate_jwt_header(alg, iat, exp))
    encodedHeader = base64UrlEncode(stringifiedHeader)

    stringifiedPayload = json.dumps(device_token_jwt_claim)
    encodedPayload = base64UrlEncode(stringifiedPayload)
    return "{}.{}".format(encodedHeader, encodedPayload)



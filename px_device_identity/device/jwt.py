import base64
import calendar
import json
import time
import uuid

from .classes import DeviceProperties


def base64UrlEncode(val):
    return base64.urlsafe_b64encode(val.encode()).decode().rstrip("=")


def get_unix_time_in_seconds():
    '''Seconds since the epoch in UTC time'''
    return calendar.timegm(time.gmtime())


def get_device_jwt_content(device_properties: 'DeviceProperties') -> dict:
    '''Get device JWT content primarily for access_token request'''
    iat = get_unix_time_in_seconds()
    device_token_jwt_claim = {
        'iss': device_properties.client_id,
        'sub': device_properties.client_id,
        'aud': device_properties.host + '/oidc/token',
        'jti': str(uuid.uuid4()),
        'iat': iat,
        'exp': iat + 300,
    }
    return device_token_jwt_claim


def get_jwt_header(alg: str, iat: int, exp: int) -> dict:
    nbf = iat - 5
    header = {
        'alg': alg,
        'typ': 'JWT',
        'exp': exp,
        'nbf': nbf,
        'iat': iat
    }
    return header


def generate_signature_content_from_dict(content: dict, iat: int = None, exp: int = None) -> str:
    '''Generate device signature content: encoded_header.encoded_payload'''
    if iat is None:
        iat = get_unix_time_in_seconds()

    if exp is None:
        exp = iat + 300

    stringified_header = json.dumps(get_jwt_header('RS256', iat, exp))
    encoded_header = base64UrlEncode(stringified_header)

    stringified_payload = json.dumps(content)
    encoded_payload = base64UrlEncode(stringified_payload)

    return "{}.{}".format(encoded_header, encoded_payload)

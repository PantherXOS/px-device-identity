'''Central Management Module: Communication with identity server.'''

import logging
from json import loads as json_loads
from time import sleep

from requests import ConnectionError, get, post

from .classes import DeviceProperties, DeviceRegistrationProperties
from .host import system_information
from .jwt import get_unix_time_in_seconds

log = logging.getLogger(__name__)


class CM:
    '''Central Management communication'''
    def __init__(self, device_properties: 'DeviceProperties'):
        self.device_properties = device_properties

        self.api_register_url = self.device_properties.host + '/devices/registration'
        self.api_status_url = self.device_properties.host + '/devices/registration/status/'
        self.api_token_url = self.device_properties.host + '/oidc/token'
        '''Set once the device registration has been posted'''
        self.verification_code = None

    def _registration_content(self, registration: 'DeviceRegistrationProperties'):
        system = system_information()
        content = {
            "publicKey": registration.public_key,
            "title": self.device_properties.title,
            "location": self.device_properties.location,
            "domain": self.device_properties.domain,
            "role": self.device_properties.role,
            "operatingSystem": system['operating_system'],
            "operatingSystemRelease": system['operating_system_release'],
            "systemArchitecture": system['system_architecture'],
            "systemMemory": system['system_memory']
        }
        return content

    def _post_registration(self, registration: 'DeviceRegistrationProperties'):
        '''Post new device registration'''
        try:
            log.info("=> Posting registration to {}".format(self.api_register_url))
            result = post(self.api_register_url, json=self._registration_content(registration))
            if result.status_code == 201:
                formatted_result = json_loads(result.text)
                verification_code: str = formatted_result["verification_code"]
                log.info("    ------------------")
                log.info("    Received verification code: {}".format(verification_code))
                log.info("    -> Awaiting confirmation from administrator.")
                log.info("    ------")
                self.verification_code = verification_code
            else:
                log.error("Could not post device registration. Status {}".format(result.status_code))
        except ConnectionError:
            log.error('Connection to {} failed. Please verify the address.'.format(self.api_register_url))
            raise
        except Exception as err:
            raise err

    def check_registration_result(self):
        '''Check device registration result'''
        try:
            api_url = self.api_status_url + str(self.verification_code)
            return get(api_url)
        except Exception as err:
            log.error("Something went wrong checking for the registration result: {}".format(err))
            raise err

    def _check_registration_result_retry(self):
        '''Check device registration result after 60 seconds'''
        wait_time = 60
        result = self.check_registration_result()
        if result is not False:
            return result
        else:
            log.warning("Will try one more time in {}s".format(wait_time))
            sleep(wait_time)
            return self.check_registration_result()

    def _check_registration_result_loop(self):
        '''Loop to check device registration until definite result'''
        limit = 200
        wait_time = 10
        # TODO: Very rudimentaty. Should be based on actual time run
        waited_time_approx = 0
        total_time_approx = limit * wait_time
        for i in range(limit):
            if i == limit:
                log.warning('Last try!')
            result = self._check_registration_result_retry()
            if result is False:
                raise Exception('Could not complete registration. Timeout exceeded.')
            status_code = result.status_code
            result_formatted = json_loads(result.text)
            if status_code == 200:
                waited_time_approx += wait_time + 1
                status = result_formatted["status"]
                log.debug('Request status: {}'.format(status))
                if status == 'pending':
                    timeout = total_time_approx - waited_time_approx
                    log.info(
                        '=> Waiting for approval ... Going to sleep for {}s. \
                            Timeout in {}s.'.format(wait_time, timeout)
                    )
                    sleep(wait_time)
                if status == 'rejected':
                    raise Exception("The device registration was rejected after {}s.".format(waited_time_approx))
                if status == 'approved':
                    log.info(
                        "The device registration was approved after {}s".format(waited_time_approx)
                    )
                    device_id: str = str(result_formatted["deviceId"])
                    client_id: str = str(result_formatted["clientId"])
                    return device_id, client_id
                if status == 'error':
                    raise Exception('Something went wrong: Received an error from the server.')
            else:
                log.error("Request failed with status code {}".format(status_code))
                if status_code == 404:
                    log.error("Cannot find pending registration. Did you register already?")
                if status_code == 500:
                    log.error("Did not receive expected response from the server. Please contact the administrator.")
                    raise Exception('Did not receive expected response from the server. Please contact the administrator.')

    def register_device(self, registration: 'DeviceRegistrationProperties'):
        '''Register the device'''
        self._post_registration(registration)
        log.debug('=> Initial request done. Checking for result ...')
        device_id, client_id = self._check_registration_result_loop()
        return device_id, client_id

    def request_access_token(self, device_jwt: str):
        form = {
            'grant_type': 'client_credentials',
            'client_id': self.device_properties.client_id,
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': device_jwt
        }

        response = post(self.api_token_url, form)
        if response.status_code == 200:
            response_content = response.json()
            return {
                'access_token': response_content['access_token'],
                'expires_at': response_content['expires_in']
            }
        if response.status_code == 401:
            raise Exception('Not authorized to request a new token.')

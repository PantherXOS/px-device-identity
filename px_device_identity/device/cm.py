'''Central Management Module: Communication with identity server.'''

from time import sleep
from json import loads as json_loads
from requests import post, get

from px_device_identity.log import Logger

from .host import system_information

log = Logger(__name__)


class CM:
    '''Central Management communication'''
    def __init__(self, registration: 'DeviceRegistrationProperties'):
        self.public_key = registration.public_key
        self.device_properties: 'DeviceProperties' = registration.device_properties

        self.api_register = self.device_properties.host + '/devices/registration'
        self.api_status = self.device_properties.host + '/devices/registration/status/'

    def _registration_content(self):
        system = system_information()
        content = {
            "publicKey": self.public_key,
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

    def _post_registration(self):
        '''Post new device registration'''
        try:
            log.info("=> Posting registration to {}".format(self.api_register))
            log.info(self._registration_content)
            result = post(self.api_register, json=self._registration_content())
            log.info(result)
            log.info(result.text)
            if result.status_code == 201:
                formatted_result = json_loads(result.text)
                verification_code: str = formatted_result["verification_code"]
                log.info("------")
                log.info("Received verification code: {}".format(verification_code))
                log.info("------")
                return verification_code
            else:
                log.error("Could not post device registration.")
                if result.content:
                    log.error(result.content)
        except:
            log.error("Something went wrong posting the registration.")
        return False

    def check_registration_result(self, verification_code: str):
        '''Check device registration result'''
        try:
            api_url = self.api_status + str(verification_code)
            return get(api_url)
        except:
            log.error("Something went wrong checking for the registration result.")
        return False

    def _check_registration_result_retry(self, verification_code: str):
        '''Check device registration result after 60 seconds'''
        wait_time = 60
        result = self.check_registration_result(verification_code)
        if result is not False:
            return result
        else:
            log.warning("Will try one more time in {}s".format(wait_time))
            sleep(wait_time)
            return self.check_registration_result(verification_code)

    def _check_registration_result_loop(self, verification_code: str):
        '''Loop to check device registration until definite result'''
        limit = 200
        wait_time = 10
        # TODO: Very rudimentaty. Should be based on actual time run
        waited_time_approx = 0
        total_time_approx = limit * wait_time
        for i in range(limit):
            if i == limit:
                log.warning('Last try!')
            result = self._check_registration_result_retry(verification_code)
            if result is False:
                return result
            status_code = result.status_code
            result_formatted = json_loads(result.text)
            if status_code == 200:
                waited_time_approx += wait_time + 1
                status = result_formatted["status"]
                log.info('Request status: {}'.format(status))
                if status == 'pending':
                    timeout = total_time_approx - waited_time_approx
                    log.info(
                        '=> Waiting for approval ... Going to sleep for {}s. \
                            Timeout in {}s.'.format(wait_time, timeout)
                    )
                    sleep(wait_time)
                if status == 'rejected':
                    log.error(
                        "The device registration was rejected after {}s.".format(waited_time_approx)
                    )
                    return False
                if status == 'approved':
                    log.info(
                        "The device registration was approved after {}s".format(waited_time_approx)
                    )
                    device_id: str = str(result_formatted["deviceId"])
                    client_id: str = str(result_formatted["clientId"])
                    return device_id, client_id
                if status == 'error':
                    log.error("Something went wrong during.")
                    return False
            else:
                log.error("Request failed with status code {}".format(status_code))
                if status_code == 404:
                    log.error("Cannot find pending registration. Did you register already?")
        return False

    def register_device(self):
        '''Register the device'''
        registration_result = self._post_registration()
        if registration_result is not False:
            verification_code: str = registration_result
            registration_approval = self._check_registration_result_loop(verification_code)
            if registration_approval is not False:
                device_id, client_id = registration_approval
                return device_id, client_id
        return False

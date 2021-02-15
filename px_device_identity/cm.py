'''Central Management Module: Communication with identity server.'''

from time import sleep
from json import loads as json_loads
from requests import post, get

from .classes import DeviceRegistration
from .log import Logger

log = Logger(__name__)


class CM:
    '''Central Management communication'''
    def __init__(self, registration: DeviceRegistration, host: str):
        self.registration = registration
        self.host = host

    def _post_registration(self):
        '''Post new device registration'''
        try:
            api_url = self.host +  '/devices/registration'
            log.info("=> Posting registration to {}".format(api_url))
            log.info(self.registration)
            result = post(api_url, json=self.registration)
            log.info(result)
            log.info(result.text)
            if result.status_code == 201:
                formatted_result = json_loads(result.text)
                verification_code: str = formatted_result["verification_code"]
                log.info("Received verification code: {}".format(verification_code))
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
            api_url = self.host + '/devices/registration/status/' + str(verification_code)
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

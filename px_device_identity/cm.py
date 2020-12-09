from requests import post, get
from json import loads as json_loads
from time import sleep

from .classes import DeviceRegistration
from .filesystem import Filesystem
from .log import Logger

log = Logger('CM')

class CM:
    def __init__(self, registration: DeviceRegistration, host: str):
        self.registration = registration
        self.host = host

    def post_registration(self):
        try:
            api_url = self.host +  '/device/register'
            log.info("=> Posting registration to {}".format(api_url))
            log.info(self.registration)
            result = post(api_url, json=self.registration)
            log.info(result)
            log.info(result.text)
            if result.status_code == 200:
                # TODO: Probably going to fail
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
        try:
            api_url = self.host + '/device/register/' + str(verification_code)
            return get(api_url)
        except:
            log.error("Something went wrong checking for the registration result.")
        return False

    def check_registration_result_retry(self, verification_code: str):
        wait_time = 60
        result = self.check_registration_result(verification_code)
        if result != False:
            return result
        else:
            log.warning("Will try one more time in {}s".format(wait_time))
            sleep(wait_time)
            return self.check_registration_result(verification_code)

    def check_registration_result_loop(self, verification_code: str):
        limit = 200
        wait_time = 10
        # TODO: Very rudimentaty. Should be based on actual time run (and average time of each loop + wait_time)
        waited_time_approx = 0
        total_time_approx = limit * wait_time
        for i in range(limit):
            if i == limit:
                log.warning('Last try!')
            result = self.check_registration_result_retry(verification_code)
            if result == False:
                return result
            status_code = result.status_code
            result_formatted = json_loads(result.text)
            if status_code == 200:
                waited_time_approx += wait_time + 1
                status = result_formatted["status"]
                log.info('Request status: {}'.format(status))
                if status == 'pending':
                    timeout = total_time_approx - waited_time_approx
                    log.info('=> Waiting for approval ... Going to sleep for {}s. Timeout in {}s.'.format(wait_time, timeout))
                    sleep(wait_time)
                if status == 'rejected':
                    log.error("The device registration was rejected after {}s.".format(waited_time_approx))
                    return False
                if status == 'accepted':
                    log.info("The device registration was accepted after {}s".format(waited_time_approx))
                    app_id: str  = result_formatted["deviceId"]
                    return app_id
            else:
                log.error("Request failed with status code {}".format(status_code))
                if status_code == 404:
                    log.error("Cannot find pending registration. Did you register already?")
        return False

    def register_device(self):
        registration_result = self.post_registration()
        if registration_result != False:
            verification_code: str = registration_result
            registration_approval = self.check_registration_result_loop(verification_code)
            if registration_approval != False:
                app_id: str = registration_approval
                return str(app_id)
        return False

import requests
from time import sleep
from .classes import DeviceRegistration
from .filesystem import Filesystem

class CM:
    def __init__(self, registration: DeviceRegistration, host: str):
        self.registration = registration
        self.host = host

    def post_registration(self):
        try:
            api_url = self.host +  '/kyc/register'
            print("=> Posting registration to {}".format(api_url))
            result = requests.post(api_url, data=self.registration)
            if result.status_code == 200:
                # TODO: Probably going to fail
                verification_code: str = result.text
                return verification_code
        except:
            print("ERROR: Something went wrong posting the registration.")
        return False

    def check_registration_result(self, verification_code: str):
        try:
            api_url = self.host + '/kyc/register/' + verification_code
            return requests.get(api_url)
        except:
            print("ERROR: Something went wrong checking for the registration result.")
        return False

    def check_registration_result_loop(self, verification_code: str):
        limit = 100
        wait_time = 5
        # TODO: Very rudimentaty. Should be based on actual time run (and average time of each loop + wait_time)
        waited_time_approx = 0
        total_time_approx = limit * wait_time
        for i in range(limit):
            if i == limit:
                print('Last try!')
            result = self.check_registration_result(verification_code)
            if result == False:
                return result
            status_code = result.status_code
            if status_code == 200:
                waited_time_approx += wait_time + 1
                status = result.json.__getattribute__(status)
                if status == 'pending':
                    timeout = total_time_approx - waited_time_approx
                    print('=> Waiting for approval ... Going to sleep for {}s. Timeout in {}s.'.format(wait_time, timeout))
                    sleep(0, wait_time)
                if status == 'rejected':
                    print("=> The device registration was rejected after {}s.".format(waited_time_approx))
                    return False
                if status == 'accepted':
                    print("=> The device registration was accepted after {}s".format(waited_time_approx))
                    app_id: str  = result.json.__getattribute__(app_id)
                    return app_id
            else:
                print("Request failed with status code {}".format(status_code))
                if status_code == 404:
                    print("ERROR: Cannot find pending registration. Did you register already?")
        return False

    def register_device(self):
        registration_result = self.post_registration()
        if registration_result != False:
            verification_code: str = registration_result
            registration_approval = self.check_registration_result_loop(verification_code)
            if registration_approval != False:
                app_id: str = registration_approval
                fs = Filesystem(self.config_path, 'registration', 'w', app_id)
                fs.create_file()
                return app_id
        return False

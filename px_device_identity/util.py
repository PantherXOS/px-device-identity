import logging
import platform
import re
import subprocess
import sys
from getpass import getuser

log = logging.getLogger(__name__)


def is_fqdn(hostname: str) -> bool:
    """Verifies if a given string is a valid domain (FQDN)."""
    if not 1 < len(hostname) < 253:
        return False

    if hostname[-1] == '.':
        hostname = hostname[0:-1]

    labels = hostname.split('.')

    fqdn = re.compile(r'^[a-z0-9]([a-z-0-9-]{0,61}[a-z0-9])?$', re.IGNORECASE)

    return all(fqdn.match(label) for label in labels)


def is_superuser_or_quit():
    '''Checks whether the current user is either root (Linux) or administrator (Windows)'''
    opsys = platform.system()
    if opsys == 'Linux':
        current_user = getuser()
        if current_user != 'root':
            log.warning(
                'IMPORTANT: This application is designed to run as root on the target device.'
            )
            log.warning('Current user: {}'.format(current_user))
            sys.exit()
    if opsys == 'Windows':
        import ctypes
        is_windows_admin = False
        try:
            is_windows_admin = ctypes.windll.shell32.IsUserAnAdmin() == 1
        except:
            log.warning(
                'Something went wrong checking if the current user is an administrator'
            )
        if not is_windows_admin:
            log.warning(
                'IMPORTANT: This application is designed to run as administrator on the target device.'
            )
            # sys.exit()


def list_of_commands_to_string(command: list):
    final = ''
    total = len(command)
    count = 1
    for item in command:
        if count == total:
            final += item
        else:
            final += "{} ".format(item)
        count += 1
    return final


def run_commands(commands: list):
    commands_string = list_of_commands_to_string(commands)
    log.debug("Running command: %s", commands_string)
    result = subprocess.run(
        commands_string, capture_output=True, shell=True, check=True
    )
    if result.returncode == 1:
        log.error(result.stderr)
        raise subprocess.CalledProcessError(
            result.returncode, commands, result.stderr
        )

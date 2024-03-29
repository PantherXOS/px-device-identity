import logging
from logging.handlers import RotatingFileHandler, SysLogHandler
from platform import system
import os

opsys = system()

log = logging.getLogger('px_device_identity')
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S"
)
formatter_cli = logging.Formatter('%(levelname)s: %(message)s')

if opsys == 'Linux':
    file_logger = os.environ.get('PX_DEVICE_IDENTITY_FILE_LOGGER')
    if file_logger != 'DISABLED':
        # On Linux we log all events to file
        fh = RotatingFileHandler(
            '/var/log/px-device-identity.log', maxBytes=10000, backupCount=1)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        log.addHandler(fh)

    sys_logger = os.environ.get('PX_DEVICE_IDENTITY_SYS_LOGGER')
    if sys_logger != 'DISABLED':
        # On Linux we engage syslog
        sh = SysLogHandler()
        sh.setLevel(logging.WARNING)
        sh.setFormatter(formatter)
        log.addHandler(sh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter_cli)
log.addHandler(ch)

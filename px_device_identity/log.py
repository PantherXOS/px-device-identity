
import logging
from logging.handlers import SysLogHandler
from platform import system
opsys = system()


log = logging.getLogger('px_device_identity')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

log.setLevel(logging.DEBUG)

if opsys == 'Linux':
    import syslog

    # On Linux we log all events to file
    fh = logging.FileHandler('/var/log/px-device-identity.log')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    #On Linux we engage syslog
    sh = SysLogHandler()
    sh.setLevel(logging.WARNING)
    sh.setFormatter(formatter)
    log.addHandler(sh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
log.addHandler(ch)
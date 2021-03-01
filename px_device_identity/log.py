import logging
from os import environ

import platform
opsys = platform.system()

if opsys == 'Linux':
    import syslog

logging.basicConfig(level=environ.get("LOGLEVEL", "INFO"))


class Logger:
    def __init__(self, context, application="px-device-identity"):
        self.context = context
        self.name = application
        self.log = logging.getLogger(self.name)

    def info(self, message):
        self.log.info(message)

    def warning(self, message):
        self.log.warn(message)
        if opsys == 'Linux':
            syslog.syslog(syslog.LOG_WARNING, message)

    def error(self, message):
        self.log.error(message)
        if opsys == 'Linux':
            syslog.syslog(syslog.LOG_ERR, message)

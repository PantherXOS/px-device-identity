import sys
import syslog
import logging
from os import environ

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
        syslog.syslog(syslog.LOG_WARNING, message)

    def error(self, message):
        self.log.error(message)
        syslog.syslog(syslog.LOG_ERR, message)
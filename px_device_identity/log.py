import os
import logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("LOG")

class Logger:
    def __init__(self, context):
        self.context = context

    def info(self, message):
        log.info(message)

    def warning(self, message):
        log.warn(message)

    def error(self, message):
        log.error(message)
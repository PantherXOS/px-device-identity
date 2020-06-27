import sys
import os
import base64
from pathlib import Path
from exitstatus import ExitStatus

from .log import Logger

log = Logger('FILESYSTEM')
class Filesystem():
    def __init__(self, config_path, file_name, mode):
        self.config_path = config_path
        self.file_name = file_name
        self.file_path = config_path + file_name
        self.mode = mode

    def config_path_exits(self):
        try:
            return os.path.isdir(self.config_path)
        except EnvironmentError:
            return False

    def file_exists(self):
        try:
            return os.path.isfile(self.file_path)
        except FileNotFoundError:
            return False

    def create_path(self):
        if self.config_path_exits() == False:
            try:
                os.mkdir(self.config_path)
                return True
            except EnvironmentError:
                log.error("Could not create path {}".format(self.config_path))
                sys.exit(ExitStatus.failure)
        return True
    
    def create_file(self, content):
        log.info("=> Creating file at {}".format(self.file_path))
        self.create_path()
        if self.mode == 'wb':
            formatted_content = bytearray(content)
        else:
            formatted_content = content
        try:
            with open(self.file_path, self.mode) as writer:
                writer.write(formatted_content)
                log.info("=> Created file.")
                return True
        except EnvironmentError:
            log.error("Could not create file {}".format(self.file_path))
        return False
    
    def open_file(self):
        log.info("=> Opening file at {}".format(self.file_path))
        if self.file_exists:
            with open(self.file_path, self.mode, buffering=0) as reader:
                try:
                    file_content = reader.read()
                    return file_content
                except:
                    log.error("Could not open file at {}".format(self.file_path))
        return False
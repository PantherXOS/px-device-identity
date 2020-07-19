from sys import exit
from shutil import rmtree
from os import mkdir, path, times, makedirs
from tempfile import gettempdir
from exitstatus import ExitStatus

from .log import Logger

log = Logger('FILESYSTEM')
class Filesystem():
    def __init__(self, file_dir, file_name, mode):
        self.file_dir = file_dir
        self.file_name = file_name
        self.file_path = file_dir + file_name
        self.mode = mode

    def file_dir_exits(self):
        try:
            return path.isdir(self.file_dir)
        except EnvironmentError:
            return False

    def file_exists(self):
        try:
            return path.isfile(self.file_path)
        except FileNotFoundError:
            return False

    def create_path(self):
        if self.file_dir_exits() == False:
            try:
                makedirs(self.file_dir)
                return True
            except EnvironmentError:
                log.error("Could not create path {}".format(self.file_dir))
                exit(ExitStatus.failure)
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
            buffering = 0
            if self.mode == 'r':
                buffering = 1
            with open(self.file_path, self.mode, buffering) as reader:
                try:
                    file_content = reader.read()
                    return file_content
                except:
                    log.error("Could not open file at {}".format(self.file_path))
        return False

def create_tmp_path():
        tmp_path = path.join(gettempdir(), '.{}'.format(hash(times())))
        log.info("=> Creating temp directory at {}".format(tmp_path))
        mkdir(tmp_path)
        return tmp_path

def remove_tmp_path(tmp_path):
    log.info("=> Removing temp directory at '{}'.".format(tmp_path))
    rmtree(tmp_path, ignore_errors=True)
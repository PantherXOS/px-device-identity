import logging
from os import makedirs, mkdir, path, times
from shutil import rmtree
from tempfile import gettempdir

log = logging.getLogger(__name__)


class Filesystem():
    def __init__(self, file_dir, file_name, mode):
        self.file_dir = file_dir
        self.file_name = file_name
        self.file_path = file_dir + file_name
        self.mode = mode

    def file_dir_exits(self) -> bool:
        try:
            return path.isdir(self.file_dir)
        except EnvironmentError:
            return False

    def file_exists(self) -> bool:
        try:
            return path.isfile(self.file_path)
        except:
            return False

    def create_path(self) -> bool:
        if self.file_dir_exits() is False:
            try:
                makedirs(self.file_dir)
                return True
            except EnvironmentError as err:
                log.error("Could not create path {}".format(self.file_dir))
                raise EnvironmentError(err)
        else:
            return True

    def create_file(self, content) -> bool:
        log.info("=> Creating file at {}".format(self.file_path))
        self.create_path()
        if self.mode == 'wb':
            formatted_content = bytearray(content)
        else:
            formatted_content = content
        try:
            with open(self.file_path, self.mode) as writer:
                writer.write(formatted_content)
                return True
        except EnvironmentError as err:
            log.error("Could not create file {}".format(self.file_path))
            raise EnvironmentError(err)

    def open_file(self):
        log.debug("=> Opening file at {}".format(self.file_path))
        if self.file_exists:
            buffering = 0
            if self.mode == 'r':
                buffering = 1
            with open(self.file_path, self.mode, buffering) as reader:
                try:
                    file_content = reader.read()
                    return file_content
                except EnvironmentError as err:
                    log.warning(
                        "Could not open file at {}".format(self.file_path))
                    raise EnvironmentError(err)


def create_tmp_path() -> str:
    tmp_path = path.join(gettempdir(), '.{}'.format(hash(times())))
    try:
        log.debug("=> Creating temp directory at {}".format(tmp_path))
        mkdir(tmp_path)
    except EnvironmentError as err:
        log.error("Could not create temp directory.")
        raise EnvironmentError(err)
    else:
        return tmp_path


def remove_tmp_path(tmp_path):
    log.debug("=> Removing temp directory at '{}'.".format(tmp_path))
    rmtree(tmp_path, ignore_errors=True)

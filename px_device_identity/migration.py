'''Migrations'''

import shutil
import os

from .log import Logger
from .config import KEY_DIR_LEGACY, KEY_DIR
from .config import DeviceConfig

log = Logger(__name__)


def first_migration_key_dir(key_dir=KEY_DIR):
    '''Migrates key dir

    from, to:
        /.config/device/
        /.config/px-device-identity/
    '''
    if os.path.isdir(KEY_DIR_LEGACY):
        log.warning('========> IMPORTANT <========')
        log.warning(
            'Found old key dir at {}. From v0.7.0 the key dir resides at {}'.format(
                KEY_DIR_LEGACY, key_dir
            )
        )
        if os.path.isdir(key_dir):
            log.warning(
                'Config has already been migrated. Delete {} whenver you are ready.'.format(
                    KEY_DIR_LEGACY
                )
            )
        else:
            os.makedirs(key_dir)
            log.info('=> Copying config from {} to {}'.format(KEY_DIR_LEGACY, key_dir))
            files = os.listdir(KEY_DIR_LEGACY)
            for file_name in files:
                shutil.copy(os.path.join(KEY_DIR_LEGACY, file_name), key_dir)
                log.info('Copied {}'.format(file_name))
                log.warning(
                    'All files have been copied. Delete {} whenver you are ready.'.format(
                        KEY_DIR_LEGACY
                    )
                )
        # From 1.0.0
        # log.info('=> Removing {}'.format(KEY_DIR_LEGACY))
        # shutil.rmtree(KEY_DIR_LEGACY)

def second_migration_add_config_key_domain():
    '''Migrates config to include new key

    key:
        domain
    '''
    config = DeviceConfig()
    device_config = config.get()
    if device_config['configVersion'] == '0.0.1':
        log.warning('========> IMPORTANT <========')
        log.warning(
            'Found old configuration file. From v0.7.3 the config includes a |domain| key'
        )
        config.migrate_config('0.0.1', '0.0.2')

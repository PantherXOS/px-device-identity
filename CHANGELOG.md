# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)

## [0.10.8]

### Added

- More tests to verify `main` and check various `Device` states

### Fixed

- Actually check if device config exists before trying to load the config

### Changed

- Last except statement now properly prints exception instead of some traceback

## [0.10.7]

### Added

- Automatically register device from enterprise configuration `--operation INIT_FROM_CONFIG`

## [0.10.6]

### Added

- Expanded tests

### Changed

- Cleaned-up some code; docs; no functional change

## [0.10.5]

### Added

- Option to disable file-logging for non-root modules accessing classes

## [0.10.4]

### Added

- Tests to cover introspection

### Fixed

- Issue related to introspection token

## [0.10.3]

### Added

- `Device.get_device_jwt` supports an optional `aud` param
- Token introspection

### Fixed

- Remove version fix for `pycryptodomex`

### Changed

- Switch to MIT license
- Removed `exitstatus` dependency

## [0.9.11]

### Changed

- Added support for role 'SELF'

## [0.9.10]

### Changed

- Turned some loggers to debug (less output)

### Added

- Device access token is now cached for 1500s
- A few, rudimentary tests have been added

## [0.9.9]

### Fixed

- Bumped `pyyaml` package dependency to include support for `v5.*`

## [0.9.8]

### Changed

- No major changes or fixes; mostly some edge cases from static type checking

### Added

- Added some supporting features for `px-user-identity-service`

## [0.9.7]

### Fixed

- Fixed an issue where we'd create a path from filename instead of path

## [0.9.6]

### Fixed

- TPM private key would not save if the data directory does not exist

## [0.9.5]

### Changed

- Cleanup command line logs
- More readable logging time format
- Log rotation

## [0.9.4]

### Changed

- Proper logging implementation

## [0.9.3]

### Fixed

- Variable error

## [0.9.2]

### Added

- Bump

## [0.9.1]

### Added

- Now supports fetching an access token `--operation GET_ACCESS_TOKEN`

## [0.9.0]

### Changed

- Restructured application to be more clear
- Added new data classes to cover operation and device logic and config

## [0.8.9]

### Changed

- Bump

## [0.8.8]

### Fixed

- Fixed boolean (was js-format)

## [0.8.7]

### Fixed

- Adapted root / administrator check to work on Windows

## [0.8.6]

### Fixed

- Made syslog dependency Linux-only; avoid import errors on Windows

### Changed

- New default `CONFIG_DIR` on Windows

## [0.8.5]

### Fixed

- Correctly look for `deviceId` instead of `id` in reg. response
- Check whether result to CM has succeeded

## [0.8.4]

### Fixed

- Config schema; missing `,`

## [0.8.3]

### Fixed

- Now captures `id` and `clientId` from server response
- Updated config to include `clientId` (also schema `v0.0.2`)

## [0.8.2]

### Fixed

- REST url `/devices/*`

### Changed

- Use domain name to generate unique device name

## [0.8.1]

### Fixed

- Force overwrite deleted, but did not create a new config dir
- Run migrations after explicit init check

## [0.8.0]

### Changed

- Bump

## [0.7.5]

### Changed

- Updated dependencies
- Migrations: Updated notes to reflect removal at v1.0.0
- Added some default exports (Device, Sign, Logger, DeviceConfig, ...)

## [0.7.4]

### Changed

- General cleanup; more comments; alignments ...

## [0.7.3]

### Changed

- Initial adaptation to new CM
- Add new migration for additional config field `domain`
- Fixed some importat pylint erros

## [0.7.2]

### Fixed

- Issues related to new config path; missing `/`

## [0.7.1]

### Fixed

- Added missing dependency `appdirs`

## [0.7.0]

### Changed

- Keys move from `/root/.config/device` to `/root/.local/share/px-device-identity`

### Fixed

- Fixed an issue where `--force` would fail

## [0.6.9]

### Fixed

- Found another `app_id` in response `result_formatted["deviceId"]`

## [0.6.8]

### Fixed

- Found one more `public_key` in registration. Changed to `publicKey`.

## [0.6.7]

### Fixed

- Device registration now expects a `publicKey`. Fixed.

## [0.6.6]

### Changed

- Fixed incorrect import

## [0.6.5]

### Changed

- Proper syslog logging for WARNING and ERROR

### Added

- CLI application outputs version in info log on run

## [0.6.4]

### Changed or Fixed

- Minor improvements logging
- Better error handling in filesystem module

## [0.6.3]

### Changed or Fixed

- Fixed an error that would occur during enterprise device registration

## [0.6.2]

### Changed or Fixed

- Simplified some functions
- Introduced defaults where it makes sense
- Added more typing markup

## [0.6.1]

### Changed or Fixed

- Removed outdated `argparse` dependency (part of Python std. library)
- Improved error recognition by checking `openssl` process response codes
- Moved functions related to temp path to file system; misc changes

### Added

- TPM2 support for ECC keys: p256, p384 and p521
- Added `tested.sh` script for rudimentary testing of all included features

## [0.6.0]

### Changed or Fixed

- Simplified CLI: Reads many previously required flags from config
- It's no longer necessary to pass <DEFAULT|TPM> flag for any command, for already initiated devices

### Added

- ECC key support (file-based): p256, p384 and p521

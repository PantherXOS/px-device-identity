# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)

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
# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)

## [0.6.1]
### Changed or Fixed

- Removed outdated `argparse` dependency (part of Python std. library)
- Improved error recognition by checking `openssl` process response codes
- Moved functions related to temp path to filesystem; misc changes

### Added

- TPM2 support for ECC keys: p256, p384 and p521
- Added `tested.sh` script for rundimentary testing of all included features

## [0.6.0]
### Changed or Fixed

- Simplified CLI: Reads many previously required flags from config
- It's no longer necessary to pass <DEFAULT|TPM> flag for any command, for already initiated devices

### Added

- ECC key support (file-based): p256, p384 and p521
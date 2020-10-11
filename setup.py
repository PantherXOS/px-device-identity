##
# Device Identity --- Initiate PantherX Devices
# Copyright © 2020 Franz Geffke <franz@pantherx.org>
#
# This file is part of PantherX OS
#
# GNU Guix is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or (at
# your option) any later version.
#
# GNU Guix is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Guix.  If not, see <http://www.gnu.org/licenses/>.

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.6.6'
PACKAGE_NAME = 'px-device-identity'
AUTHOR = 'Franz Geffke'
AUTHOR_EMAIL = 'franz@pantherx.org'
URL = 'https://git.pantherx.org/development/applications/px-device-identity'

LICENSE = ''
DESCRIPTION = 'Initiates device; provides JWK, JWKS and Signing Services'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'requests>=2.22.0,<2.24.0',
    'authlib>=0.14.3,<0.15',
    'pycryptodomex>=3.9.8,<3.10',
    'exitstatus>=2.0.1,<2.1',
    'shortuuid>=1.0.1,<1.1',
    'pyyaml>=5.3.1,<5.4'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      entry_points = {
        'console_scripts': ['px-device-identity=px_device_identity.command_line:main'],
      },
      packages=find_packages(),
      zip_safe=False
      )
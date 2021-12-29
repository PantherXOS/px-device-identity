import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.10.3'
PACKAGE_NAME = 'px-device-identity'
AUTHOR = 'Franz Geffke'
AUTHOR_EMAIL = 'franz@pantherx.org'
URL = 'https://git.pantherx.org/development/applications/px-device-identity'

LICENSE = 'MIT'
DESCRIPTION = 'Initiates device; provides JWK, JWKS and Signing Services'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'requests>=2.22.0,<2.30',
    'authlib>=0.14.3,<0.15',
    'pycryptodomex',
    'shortuuid>=1.0.1,<1.1',
    'pyyaml',
    'appdirs>=1.4.1,<1.5',
    'psutil>=5.7.2,<5.9'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    license=LICENSE,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': ['px-device-identity=px_device_identity.command_line:main'],
    },
    packages=find_packages(),
    zip_safe=False
)

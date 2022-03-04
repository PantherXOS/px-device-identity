# PantherX Device Identity Manager

- Generates ECC/RSA keypair
  - saves to file `/root/.local/share/px-device-identity/` (`private.pem`, `public.pem`)
  - via TPM2 (RSA only)
- Generates and saves JWK from public key
  - saves to file `/root/.local/share/px-device-identity/` (`public_jwk.json`)

### Supported cryptography

**RSA** with

- 2048 bits `RSA:2048`
- 3072 bits `RSA:3072`

**ECC** with

- p256 curve `ECC:p256`
- p384 curve `ECC:p384`
- p521 curve `ECC:p521`

All supported options work for both file-based and TPM2-based key-pairs.

### Supported devices

File-based keys should work everywhere but we specifically test TPM2-support on the following devices:

- ThinkPad T450, X1CG7
- ThinkStation M625q
- Camino Tiny

## Setup

**Requirements**

- `openssl`
- [`tpm2-tss-engine`](https://github.com/tpm2-software/tpm2-tss-engine)

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install .
```

### Install with pip package manager

```bash
pip3 install https://source.pantherx.org/px-device-identity_latest.tgz
```

## Run

### Initiate device:

#### Unmanaged

Defaults to _type_ `DESKTOP`:

```bash
$ px-device-identity --operation INIT --security <DEFAULT|TPM>
```

All options:

```bash
$ px-device-identity --operation INIT --security <DEFAULT|TPM> --role <PUBLIC|DESKTOP|SERVER> --keytype <RSA:2048|RSA:3072|ECC:p256|ECC:p384|ECC:p521>
```

A good default for devices without TPM2 support is:

```bash
$ px-device-identity --operation INIT --security DEFAULT --role <PUBLIC|DESKTOP|SERVER> --keytype ECC:p256
```

#### Managed

Registering a device with role `SERVER`, `ADMIN_TERMINAL` or `REGISTRATION_TERMINAL` automatically creatres a new, related application.

| device role           | application type |
| --------------------- | ---------------- |
| ADMIN_TERMINAL        | CLIENT           |
| REGISTRATION_TERMINAL | CLIENT_KYC       |
| SERVER                | SERVER           |

Defaults to _role_ `DESKTOP`:

```bash
$ px-device-identity --operation INIT --address https://identity.pantherx.dev --domain pantherx.org --security <DEFAULT|TPM> --role <PUBLIC|DESKTOP|SERVER|ADMIN_TERMINAL|REGISTRATION_TERMINAL|SELF>
```

All options:

```bash
$ px-device-identity --operation INIT --address https://identity.pantherx.dev --domain pantherx.org --security <DEFAULT|TPM> --role <PUBLIC|DESKTOP|SERVER|ADMIN_TERMINAL|REGISTRATION_TERMINAL|SELF> --title "Marketing-01 PC" --location "Head office"
```

- `DEFAULT` - private key stored as PEM file
- `TPM` - private key stored in TPM2

**TIP** Registering a device with role `SERVER`, `ADMIN_TERMINAL` or `REGISTRATION_TERMINAL` automatically creatres a new, related application. Additionally, a device with role `SERVER` that contains `Matrix` in it's title will specifically create an applicate an

This generates the following files:

```bash
/etc/px-device-identity/device.yml
/root/.local/share/px-device-identity/public.pem
/root/.local/share/px-device-identity/private.pem
```

The `device.yml` contains the device configuration:

Here's an example for a managed desktop:

```yml
client_id: d5fe8500-6003-49fd-9b8f-7adaf102e9a3
config_version: 0.0.3
domain: pantherx.org
host: http://127.0.0.1:4000
id: 8b477978-c63d-46f5-9492-67fafdd0d68e
initiated_on: "2021-03-08 15:22:00.816527"
is_managed: true
key_security: default
key_type: RSA:2048
location: undefined
role: desktop
title: DESKTOP-MkVLwku9JybTrq9MkgjeU2
```

**To overwrite an existing device identification**, do:

```bash
px-device-identity --operation INIT --security <DEFAULT|TPM> --force TRUE
```

#### Managed, Automated

If you installed the device from a enterprise configuration, chances are that you have a `/etc/config.json`. If that's the case, you can register the device as follows:

```
px-device-identity --operation INIT_FROM_CONFIG
```

or if necessary:

```
px-device-identity --operation INIT_FROM_CONFIG --force TRUE
```

### Get the JWK for the device public key

```bash
px-device-identity --operation GET_JWK
```

### Get the JWK as JWKS

```bash
px-device-identity --operation GET_JWKS
```

### Sign a hash

```bash
px-device-identity --operation SIGN --message <MESSAGE>
```

returns `base64`

### Get access token

```bash
px-device-identity --operation GET_ACCESS_TOKEN
```

returns

```json
{
  "access_token": "_Y6E2rRFcQBGu6uRAlahCqw_5ChSLXtqoPUgy82Wbil",
  "expires_at": 1615231820
}
```

#### Example for JWT

Request signature:

```bash
px-device-identity --operation SIGN --message eyJhbGciOiAiUlMyNTYiLCAidHlwZSI6ICJKV1QifQ.eyJhcHBfaWQiOiAiYzNlZmMzYTYtZGE1MS00N2IwLWFiNTYtOTA4MjRkYTFmNDNmIn0
```

Response:

```bash
UWyxzPn_r9VAdKH0MKwHirI3saCn21IuHpYNxMMgzq0KQk1PK83MBYTxqhnEwpq17ruKwQehhXb5bPg4Z9XF6a_dotdyZ8gYlrOefyBPBD712k0gPFOmf0KtJn6jYaR10lPbRyKI-fo21sb-0COp7Sb62rwNPv43tABiFD5C7mltYlH2EF2lN58uDytQypUCToWSapcRgfO9L5NCGShsjubBKkoLjzrP4qPC-AB8-EQx8jCm2hzy0dPg0GtppG1ZnLzeB0g2Vt4dFH21bjVO4o97CNb95PP6pZhNdqOq5LjsTfS6CbFi3h5bXHQQN_VU2mjq_E_5_QDeH8SAAFW-2g
```

### Misc

To output to a file, simply

```bash
> jwk.json
```

## Use in a non-root module

Set process environment variable:

```
PX_DEVICE_IDENTITY_FILE_LOGGER=DISABLED
```

**Important**: This is mostly to access stuff like `DeviceProperties`. Most features are designed to be run as `root` user.

## Troubleshooting

Find logs at `/var/log/`

## Development

Create a guix environment like so:

(1) Switch to root `su - root`

(2) Spawn a guix environment:

```bash
guix environment --pure \
--ad-hoc python tpm2-tss tpm2-tss-engine python-setuptools python-psutil coreutils bash
```

(3) Open the repo; create a new virtual env `python3 -m venv venv`

(4) Activate the environment `source venv/bin/activate`

(5) Install dependencies with `pip3 install .`

_If you're getting errors in the virtual environment: `exit; rm -rf venv` and resume at (2)._

### Tests

_These paths will change..._

Follow "Development" setup, then set environment variables:

(1) `ls /gnu/store | grep px-device-identity-0.10.5`

(2) `cat /gnu/store/4cx57qhzx1h0yg2frajhsz8j6bp8vvpw-px-device-identity-0.10.5/bin/px-device-identity`

```bash
export OPENSSL_CONF="/gnu/store/r1cad9m26xncpj8jb907mc2g8zw1vfvz-tpm2-tss-engine-1.1.0/etc/openssl-tss2.conf${OPENSSL_CONF:+:}$OPENSSL_CONF"
export PATH="/gnu/store/r1cad9m26xncpj8jb907mc2g8zw1vfvz-tpm2-tss-engine-1.1.0/bin/${PATH:+:}$PATH"
export PATH="/gnu/store/cs1kihs34ccqhc69yx0c4kaf3rkiwyyy-openssl-1.1.1l/bin/${PATH:+:}$PATH"
export TPM2TSSENGINE_TCTI="/gnu/store/1a0qagvjvapk252q798w5d899is5p059-tpm2-tss-3.0.3/lib/libtss2-tcti-device.so:/dev/tpm0${TPM2TSSENGINE_TCTI:+:}$TPM2TSSENGINE_TCTI"
export TPM2TOOLS_TCTI="/gnu/store/1a0qagvjvapk252q798w5d899is5p059-tpm2-tss-3.0.3/lib/libtss2-tcti-device.so:/dev/tpm0${TPM2TOOLS_TCTI:+:}$TPM2TOOLS_TCTI"
```

(3) Set a active access token (for ex. `master` user) for introspection test:

```
export PX_DEVICE_IDENTITY_INTROSPECTION_TEST_TOKEN=HGIvr8n-MHN8bQcPUPqIztW6FRSUJ_Nvz0gf0L074kU
```

Run tests:

```bash
$ python3 -m unittest -v

----------------------------------------------------------------------
Ran 31 tests in 56.183s
```

```
# pycryptodomex==3.9.8 exitstatus==2.0.1
```

### Misc

Create a package to manually install `px-device-identity`:

```bash
python3 setup.py sdist --format=tar
pip install px-device-identity-0.*.*.tar
```

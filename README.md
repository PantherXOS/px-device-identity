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

## Run

### Initiate device:

**Unmanaged**

Defaults to _type_ `DESKTOP`:

```bash
$ px-device-identity --operation INIT --security <DEFAULT|TPM>
```

All options:

```bash
$ px-device-identity --operation INIT --security <DEFAULT|TPM> --type <DESKTOP|SERVER|CLOUD|ENTERPRISE> --keytype <RSA:2048|RSA:3072|ECC:p256|ECC:p384|ECC:p521>
```

A good default for devices without TPM2 support is:

```bash
$ px-device-identity --operation INIT --security DEFAULT --type <DESKTOP|SERVER|CLOUD|ENTERPRISE> --keytype ECC:p256
```

**Managed**

Defaults to _type_ `DESKTOP`:

```bash
$ px-device-identity --operation INIT --address https://idp.dev.pantherx.dev --security <DEFAULT|TPM> --type <DESKTOP|SERVER|CLOUD|ENTERPRISE>
```

- `DEFAULT` - private key stored as PEM file
- `TPM` - private key stored in TPM2

This generates the following files:

```bash
/etc/px-device-identity/device.yml
/root/.local/share/px-device-identity/public.pem
/root/.local/share/px-device-identity/private.pem
```

The `device.yml` contains the device configuration:

```yml
id: str # ['UUID4', 'NanoID']
clientId: str
deviceType: str # ['DESKTOP', 'SERVER', 'CLOUD', 'ENTERPRISE']
keySecurity: str # ['DEFAULT', 'TPM']
keyType: str # ['RSA:bitrate', 'ECDSA:curve']
isManaged: bool # [true, false]
host: str # ['NONE', 'https://....']
domain: str # ['NONE', 'pantherx.org']
configVersion: str # ['*.*.*']
initiatedOn: dateTime # ['2020-07-03 23:02:36.733746']
```

Here's an example for an unmanaged desktop (basically a home user):

```yml
configVersion: 0.0.1
clientId: NONE
deviceType: DESKTOP
host: NONE
id: 99fa5f7e-e68d-4bf0-947d-8e4e485f61dd
initiatedOn: '2020-07-03 23:07:41.008684'
isManaged: false
domain: NONE
keySecurity: TPM
keyType: RSA:2048
```

**To overwrite an existing device identification**, do:

```bash
px-device-identity --operation INIT --security <DEFAULT|TPM> --force TRUE
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

Create a package to manually install `px-device-identity`:

```bash
python setup.py sdist --format=tar
pip install px-device-identity-0.*.*.tar
```
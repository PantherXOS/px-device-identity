# PantherX Device Identity Manager

- Generates RSA keypair
   - saves to file `~/.config/device` (`private.pem`, `public.pem`)
   - via TPM (planned)
- Generates and saves JWK from public key
   - saves to file `~/.config/device` (`public_jwk.json`)

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install .
```

## Run

### Initiate device:

**Unmanaged**

Defaults to _type_ `DESKTOP`:

```bash
px-device-identity --operation INIT --security <DEFAULT|TPM>
```

All options:

```bash
px-device-identity --operation INIT --security <DEFAULT|TPM> --type <DESKTOP|SERVER|CLOUD|ENTERPRISE>
```

**Managed**

Defaults to _type_ `DESKTOP`:

```bash
px-device-identity --operation INIT --address https://idp.dev.pantherx.dev --security <DEFAULT|TPM> # --type <DESKTOP|SERVER|CLOUD|ENTERPRISE>
```

This generates the following files:

```bash
device.yml   public.pem  private.pem
```

The `device.yml` contains the device configuration:

```yml
id: str # ['UUID4', 'NanoID']
deviceType: str # ['DESKTOP', 'SERVER', 'CLOUD', 'ENTERPRISE']
keySecurity: str # ['DEFAULT', 'TPM']
isManaged: bool # [true, false]
host: str # ['NONE', 'https://....']
```

**DEPRECIATION**:

The `~/.config/device/device_id` file is depreciated with `v0.4.0` and will be removed. Read the configuration including device ID from `~/.config/device/device.yml` instead.

**To overwrite an existing device identification**, do:

```bash
px-device-identity --operation INIT --security <DEFAULT|TPM> --force TRUE
```

### Get the JWK for the device public key

```bash
px-device-identity --operation GET_JWK --security <DEFAULT|TPM>
```

### Get the JWK as JWKS

```bash
px-device-identity --operation GET_JWKS --security <DEFAULT|TPM>
```

### Sign a hash

```bash
px-device-identity --operation SIGN --security <DEFAULT|TPM> --message <HASH>
```

returns `base64`

#### Example for JWT

Request signature:

```bash
px-device-identity --operation SIGN --security DEFAULT --message eyJhbGciOiAiUlMyNTYiLCAidHlwZSI6ICJKV1QifQ.eyJhcHBfaWQiOiAiYzNlZmMzYTYtZGE1MS00N2IwLWFiNTYtOTA4MjRkYTFmNDNmIn0
```

Response:

```bash
UWyxzPn_r9VAdKH0MKwHirI3saCn21IuHpYNxMMgzq0KQk1PK83MBYTxqhnEwpq17ruKwQehhXb5bPg4Z9XF6a_dotdyZ8gYlrOefyBPBD712k0gPFOmf0KtJn6jYaR10lPbRyKI-fo21sb-0COp7Sb62rwNPv43tABiFD5C7mltYlH2EF2lN58uDytQypUCToWSapcRgfO9L5NCGShsjubBKkoLjzrP4qPC-AB8-EQx8jCm2hzy0dPg0GtppG1ZnLzeB0g2Vt4dFH21bjVO4o97CNb95PP6pZhNdqOq5LjsTfS6CbFi3h5bXHQQN_VU2mjq_E_5_QDeH8SAAFW-2g
```

### Debug Messages

To show debug messages (default: False):

```bash
--debug true
```

To output to a file, simply

```bash
> jwk.json
```
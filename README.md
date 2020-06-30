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

```bash
px-device-identity --operation INIT --type <DEFAULT|TPM>
```

**Managed**

```bash
px-device-identity --operation INIT --address https://idp.dev.pantherx.dev --type <DEFAULT|TPM>
```

This generates the following files:

```bash
device_id   public_jwk.json  public.pem  private.pem # not for TPM
```

**To overwrite an existing device identification**, do:

```bash
px-device-identity --operation INIT --type <DEFAULT|TPM> --force TRUE
```

### Get the JWK for the device public key

```bash
px-device-identity --operation GET_JWK --type <DEFAULT|TPM>
```

### Get the JWK as JWKS

```bash
px-device-identity --operation GET_JWKS --type <DEFAULT|TPM>
```

### Sign a hash

```bash
px-device-identity --operation SIGN --type <DEFAULT|TPM> --message <HASH>
```

returns `base64`

#### Example for JWT

Request signature:

```bash
px-device-identity --operation SIGN --type DEFAULT --message eyJhbGciOiAiUlMyNTYiLCAidHlwZSI6ICJKV1QifQ.eyJhcHBfaWQiOiAiYzNlZmMzYTYtZGE1MS00N2IwLWFiNTYtOTA4MjRkYTFmNDNmIn0
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
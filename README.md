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

### Sign a hash

```bash
px-device-identity --operation SIGN --type <DEFAULT|TPM> --message <HASH>
```

returns `binascii.b2a_base64`

### Debug Messages

To show debug messages (default: False):

```bash
--debug true
```

To output to a file, simply

```bash
> jwk.json
```
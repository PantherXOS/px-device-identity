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

Key operations

```bash
python3 run.py --operation <init|getJWK> --type <default|tpm>
```

This generates the following files:

```bash
device_id  private.pem  public_jwk.json  public.pem
```

Signing

```bash
python3 run.py --operation sign --type <default|tpm> --string <hash>
```

returns `binascii.b2a_base64`

To show debug messages (default: False):

```bash
--debug true
```

To output to a file, simply

```bash
> jwk.json
```
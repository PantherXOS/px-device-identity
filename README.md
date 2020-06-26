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

```bash
python3 run.py --operation INIT --type <DEFAULT|TPM>
```

This generates the following files:

```bash
device_id  private.pem  public_jwk.json  public.pem
```

and should respond with either 'SUCCESS'  or 'ERROR' depending on the outcome of the operation.

**To overwrite an existing device identification**, do:

```bash
python3 run.py --operation INIT --type <DEFAULT|TPM> --force TRUE
```

### Get the JWK for the device `public.pem`

```bash
python3 run.py --operation GET_JWK --type <DEFAULT|TPM>
```

### Sign a hash

```bash
python3 run.py --operation SIGN --type <DEFAULT|TPM> --message <HASH>
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
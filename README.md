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

```bash
python3 run.py --operation <generateKeys|getJWK>
```

To show debug messages (default: False):

```bash
--debug true
```

To output to a file, simply

```bash
> jwk.json
```
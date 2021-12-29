# Helper script to quickly setup a development environment

python3 -m venv venv
source venv/bin/activate
pip3 install .
export OPENSSL_CONF="/gnu/store/r1cad9m26xncpj8jb907mc2g8zw1vfvz-tpm2-tss-engine-1.1.0/etc/openssl-tss2.conf${OPENSSL_CONF:+:}$OPENSSL_CONF"
export PATH="/gnu/store/r1cad9m26xncpj8jb907mc2g8zw1vfvz-tpm2-tss-engine-1.1.0/bin/${PATH:+:}$PATH"
export PATH="/gnu/store/cs1kihs34ccqhc69yx0c4kaf3rkiwyyy-openssl-1.1.1l/bin/${PATH:+:}$PATH"
export TPM2TSSENGINE_TCTI="/gnu/store/1a0qagvjvapk252q798w5d899is5p059-tpm2-tss-3.0.3/lib/libtss2-tcti-device.so:/dev/tpm0${TPM2TSSENGINE_TCTI:+:}$TPM2TSSENGINE_TCTI"
export TPM2TOOLS_TCTI="/gnu/store/1a0qagvjvapk252q798w5d899is5p059-tpm2-tss-3.0.3/lib/libtss2-tcti-device.so:/dev/tpm0${TPM2TOOLS_TCTI:+:}$TPM2TOOLS_TCTI"
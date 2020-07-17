#!/bin/sh
# PantherX Device Init Test-Script
# Version 0.0.1
# Author: Franz Geffke <franz@pantherx.org> | PantherX.DEV

PROGNAME=$(basename $0)

error_exit()
{
	echo "${PROGNAME}: ${1:-"Unknown Error"}" 1>&2
	exit 1
}

function common {
    px-device-identity --operation GET_JWK --security DEFAULT || error_exit
    px-device-identity --operation GET_JWKS --security DEFAULT || error_exit
    px-device-identity --operation SIGN --security DEFAULT --message ABC || error_exit
}

function common_tpm {
    px-device-identity --operation GET_JWK --security TPM || error_exit
    px-device-identity --operation GET_JWKS --security TPM || error_exit
    px-device-identity --operation SIGN --security TPM --message ABC || error_exit
}

echo "###################"
echo "Test 1: Default"
px-device-identity --operation INIT --security DEFAULT --type DESKTOP --force True
common
echo "###################"
echo "Test 2: Default with TPM"
px-device-identity --operation INIT --security TPM --type DESKTOP --force True
common_tpm
echo "###################"
echo "Test 3: ECC"
px-device-identity --operation INIT --security DEFAULT --type DESKTOP --keytype ECC:p256 --force True
common
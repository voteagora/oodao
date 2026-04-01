#!/usr/bin/env bash
set -euo pipefail

# Check for required network argument
if [ $# -ne 2 ]; then
  echo "Usage: $0 <network>, $1 <upgrade_path> 0,1"
  echo "Networks: ethmain, ethtest, opmain, optest"
  echo "Upgrade path: 0 - VotesResolver, 1 - EntityResolver"
  exit 1
fi

export UPGRADE_PATH=$2
NETWORK=$1
# Set environment variables based on network
case $NETWORK in
  ethmain)
    if [ $2 -eq 0 ]; then
        export PROXY_CONTRACT="0x576c9f4C976e2E6AF9E7093F1A23Fa31B21D4cB3"
        export PROXY_ADMIN="0x4Ee4b7e6eE98e0b5361dACcF9062733858c4B066"
    elif [ $2 -eq 1 ]; then
        export PROXY_CONTRACT="0xf246C55a4f91f08c991F566fcF063156f67e6c03"
        export PROXY_ADMIN="0x8D7512290251bd5417A00730aBFA0E5fdba1094A"
    fi
    export EAS_CONTRACT="0xA1207F3BBa224E2c9c3c6D5aF63D0eb1582Ce587"
    export RPC_URL="https://eth.llamarpc.com"
    ;;
  ethtest)
    if [ $2 -eq 0 ]; then
        export PROXY_CONTRACT="0xC8EA7C7651245728BE57c2d4C5638F8eF843b0E7"
        export PROXY_ADMIN="0xaFb13914085154869a6770d6bbcE1Cc9B3aDE560"
    elif [ $2 -eq 1 ]; then
        export PROXY_CONTRACT="0x7106847Cc6c99E3D730D4f2a8312A905c0ad2ad7"
        export PROXY_ADMIN="0xe84969F17B2628C71B421d552450b7F131bE07A2"
    fi
    export EAS_CONTRACT="0xC2679fBD37d54388Ce493F1DB75320D236e1815e"
    export RPC_URL="https://ethereum-sepolia-rpc.publicnode.com"
    ;;
  *)
    echo "Error: Unknown network '$NETWORK'"
    echo "Valid networks: ethmain, ethtest"
    exit 1
    ;;
esac

KEYSTORE_PATH="$HOME/.foundry/keystores/0xA6222"

echo "Deploying to $NETWORK"
echo "EAS_CONTRACT: $EAS_CONTRACT"
echo "RPC_URL: $RPC_URL"
echo "PROXY_ADMIN: $PROXY_ADMIN"
echo "PROXY_CONTRACT: $PROXY_CONTRACT"

forge script script/UpgradeEASContracts.s.sol:UpgradeEASContracts \
  --rpc-url "$RPC_URL" \
  --broadcast \
  --keystore "$KEYSTORE_PATH" \
  --slow


#!/usr/bin/env bash
set -euo pipefail

# Check for required network argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <network>"
  echo "Networks: ethmain, ethtest, opmain, optest"
  exit 1
fi

NETWORK=$1

# Set environment variables based on network
case $NETWORK in
  ethmain)
    export EAS_CONTRACT="0xA1207F3BBa224E2c9c3c6D5aF63D0eb1582Ce587"
    export RPC_URL="https://eth.llamarpc.com"
    ;;
  ethtest)
    export EAS_CONTRACT="0xC2679fBD37d54388Ce493F1DB75320D236e1815e"
    export RPC_URL="https://ethereum-sepolia-rpc.publicnode.com"
    ;;
  opmain)
    export EAS_CONTRACT="0x4200000000000000000000000000000000000021"
    export RPC_URL="https://optimism-rpc.publicnode.com"
    ;;
  optest)
    export EAS_CONTRACT="0x4200000000000000000000000000000000000021"
    export RPC_URL="https://sepolia.optimism.io"
    ;;
  *)
    echo "Error: Unknown network '$NETWORK'"
    echo "Valid networks: ethmain, ethtest, opmain, optest"
    exit 1
    ;;
esac

KEYSTORE_PATH="$HOME/.foundry/keystores/0xA6222"

echo "Deploying to $NETWORK"
echo "EAS_CONTRACT: $EAS_CONTRACT"
echo "RPC_URL: $RPC_URL"

forge script script/DeployVotesResolver.s.sol:DeployVotesResolverScript \
  --rpc-url "$RPC_URL" \
  --broadcast \
  --keystore "$KEYSTORE_PATH"
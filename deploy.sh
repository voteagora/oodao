#!/usr/bin/env bash
set -euo pipefail

# -------------------------
# Config
# -------------------------

# Replace this with the SchemaRegistry address on your target network.
# Example: Sepolia SchemaRegistry
SCHEMA_REGISTRY=0xA0aFaa2c02b1b50d7a60e1e15C08e9Ec77C5A79d

# Replace with your deployer private key or set via env (e.g., export PRIVATE_KEY=...)
PRIVATE_KEY=${PRIVATE_KEY:?must export PRIVATE_KEY}

# RPC URL for your chain (example: Sepolia)
RPC_URL=${RPC_URL:-https://sepolia.infura.io/v3/YOUR_KEY}

# -------------------------
# Schemas
# -------------------------

declare -A SCHEMAS
SCHEMAS[INSTANTIATE]="bytes32 dao_uuid,string protocol_version,string name"
SCHEMAS[GRANT]="bytes32 dao_uuid,address subject,string permission,uint8 level,string filter"
SCHEMAS[CREATE_PROPOSAL_TYPE]="bytes32 dao_uuid,bytes32 proposal_type_uuid,string class,string kwargs"
SCHEMAS[CREATE_PROPOSAL]="bytes32 dao_uuid,bytes32 proposal_uuid,bytes32 proposal_type_uuid,string title,string description,uint64 startts,uint64 endts"
SCHEMAS[SIMPLE_VOTE]="bytes32 dao_uuid,bytes32 proposal_uuid,address voter,int8 choice,string reason,uint256 weight"
SCHEMAS[ADVANCED_VOTE]="bytes32 dao_uuid,bytes32 proposal_uuid,address voter,string choice,string reason,uint256 weight"
SCHEMAS[UNDO]="bytes32 dao_uuid,bytes32 uid"

# -------------------------
# Register
# -------------------------

for NAME in "${!SCHEMAS[@]}"; do
  SCHEMA="${SCHEMAS[$NAME]}"

  echo "Registering schema: $NAME"
  TX=$(cast send $SCHEMA_REGISTRY \
    "register(string,address,bool)(bytes32)" \
    "$SCHEMA" \
    0x0000000000000000000000000000000000000000 \
    true \
    --rpc-url $RPC_URL \
    --private-key $PRIVATE_KEY)

  echo "✅ $NAME registered. Tx: $TX"
done

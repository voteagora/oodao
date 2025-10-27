# An On & Offchain DAO Protocol using EAS

A Python command-line tool for deploying schemas and creating attestations using the [On & Offchain Attestation DAO Protocol](./protocol.md) with Ethereum Attestation Service (EAS).

## Overview

This CLI wraps Foundry's `forge` commands to simplify interaction with the DAO governance protocol defined in [protocol.md](./protocol.md). 

## Deployments

# Eth Mainnet Entity Resolver Proxy:
-

# Eth Sepolia Entity Resolver Proxy:
0x0292b0ce4f6791ee6d91befbc9f16aed463d1412

# Eth Sepolia Votes Resolver Proxy:
0x990885ca636aaba3513e82d4e74b82b1f76bbb04

# Entities Implementation
forge verify-contract \
  --chain sepolia \
  --etherscan-api-key JIF6AGF7HBFSH1RKAK398KAZ2UHZM9TBTJ \
  0x198c4171b7de6e1ea1b752896ad1555ad04b68f1 \
  resolvers/EntitiesResolver.sol:EntitiesResolver

# Votes Implementation
forge verify-contract \
  --chain sepolia \
  --etherscan-api-key JIF6AGF7HBFSH1RKAK398KAZ2UHZM9TBTJ \
  0xa3de35c6e91c9226b3e283782b9d16396112a506 \
  resolvers/VotesResolver.sol:VotesResolver

# Entities Proxy? (not working yet)
forge verify-contract \
  --chain sepolia \
  --etherscan-api-key JIF6AGF7HBFSH1RKAK398KAZ2UHZM9TBTJ \
  0xdf0e5df7af27076e5ea57be9dc068ea36d970bc4 \
  lib/openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol:TransparentUpgradeableProxy



### Schema Hashes

#### Sepolia Deployment

```
INSTANTIATE : 0x572f7d8834633948ea8827c710d08bbe9d80b87e8d7192185acb43b2af706dff
PERMA_INSTANTIATE : 0x25566ed7860fc90849725cbd7b90e618a291685e9cb0d0b40d51bcf08538eec5
GRANT : 0x3d3490aa99eca912f5ae133f02495e592c01e257e0a49f023fd9df6197dfc4ca
CREATE_PROPOSAL_TYPE : 0xafc8d20711ca74a92a5c0ed26d7ca7796d2c78e20a17b76389f24c4dfbba54e5
CREATE_PROPOSAL : 0x442d586d8424b5485de1ff46cb235dcb96b41d19834926bbad1cd157fbeeb8fc
CHECK_PROPOSAL : 0xf022af215cd4eabc4bf1773d04fdec714f47097d9dc7a037eb01f23bdfaa5533
SET_PROPOSAL_TYPE : 0x2e0208e92ffe9439d6ce12fbd9928ad8f6d79b652068bd3cf6032ef64dba12fa
SET_PARAM_VALUE : 0x860fbb1b78677152aaea5cf8855866c268fde8c0d814c10f2a55d73d6562269c
DELEGATED_SIMPLE_VOTE : 0xde80f2c4e6168c2f68c1b466087ffba7994c2b7ff8f4113689c75ee82ef59c61
DELEGATED_ADVANCED_VOTE : 0x4aa210b34a3b488c54f7ec482763c5ec8a52be5669c24216d3814b009076fb50
SIMPLE_VOTE : 0x2b0e624e00310c7e88a1b7840238e285152b38ab00160b14c0d4e54e0a53a3aa
ADVANCED_VOTE : 0xa7497737b4bdc0eaf60e90a290602216fb2a0e8c886e50bad63324ca8b76a587
DELETE : 0x28b4a65500ba66b7328de552b9e5cf7f2211143e141a4c8cf915ba894d8e81a8
```

```
X - INSTANTIATE
X - PERMA_INSTANTIATE
X - GRANT
X - CREATE_PROPOSAL_TYPE
O - CREATE_PROPOSAL
X - CHECKED_PROPOSAL
X - SET_PROPOSAL_TYPE
X - SET_PARAM_VALUE
V - DELEGATED_SIMPLE_VOTE
V - DELEGATED_ADVANCED_VOTE
V - SIMPLE_VOTE
V - ADVANCED_VOTE
X - DELETE
```

## Installation

### Prerequisites

- Python 3.7+
- [Foundry](https://book.getfoundry.sh/getting-started/installation) (forge)

### Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your values:
```env
CHAIN_ID=11155111                                    # Network chain ID
RPC_URL=https://ethereum-sepolia-rpc.publicnode.com  # RPC endpoint
FORGE_ACCOUNT=default                                 # Forge account name
```

3. Make the CLI executable (optional):
```bash
chmod +x eas_cli.py
```

## Usage

### Deploy Command

Deploy a schema for an attestation type:

```bash
./eas_cli.py deploy <ATTESTATION_COMMAND>
```

**Examples:**
```bash
./eas_cli.py deploy INSTANTIATE
./eas_cli.py deploy GRANT
./eas_cli.py deploy CREATE_PROPOSAL_TYPE
```

### Attest Command

Create an attestation with the specified arguments:

```bash
./eas_cli.py attest <ATTESTATION_COMMAND> <args...>
```

Arguments must match the schema field order defined in [protocol.md](./protocol.md).

## Examples

### 1. Instantiate a DAO

Deploy the INSTANTIATE schema:
```bash
./eas_cli.py deploy INSTANTIATE
```

Create an INSTANTIATE attestation:
```bash
./eas_cli.py attest INSTANTIATE \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  "v0.1.0" \
  "My DAO"
```

**Schema:** `bytes32 dao_uuid, string protocol_version, string name`

### 2. Grant Permissions

Deploy the GRANT schema:
```bash
./eas_cli.py deploy GRANT
```

Grant CREATE_PROPOSAL permission to an address:
```bash
./eas_cli.py attest GRANT \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  0xABCDEF1234567890ABCDEF1234567890ABCDEF12 \
  "CREATE_PROPOSAL" \
  7 \
  ""
```

**Schema:** `bytes32 dao_uuid, address subject, string permission, uint8 level, string filter`

**Permission levels** (bitmask):
- Bit 0 (1): CREATE
- Bit 1 (2): REVOKE
- Bit 2 (4): UNDO
- Example: `7` (binary 111) = CREATE + REVOKE + UNDO

### 3. Create a Proposal Type

Deploy the CREATE_PROPOSAL_TYPE schema:
```bash
./eas_cli.py deploy CREATE_PROPOSAL_TYPE
```

Define a standard proposal type:
```bash
./eas_cli.py attest CREATE_PROPOSAL_TYPE \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 \
  "standard" \
  '{"quorum": "50%", "threshold": "majority"}'
```

**Schema:** `bytes32 dao_uuid, bytes32 proposal_type_uuid, string class, string kwargs`

**Supported classes:** `standard`, `approval`, `optimistic`

### 4. Create a Proposal

Deploy the CREATE_PROPOSAL schema:
```bash
./eas_cli.py deploy CREATE_PROPOSAL
```

Submit a proposal:
```bash
./eas_cli.py attest CREATE_PROPOSAL \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  0xfedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321 \
  0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 \
  "Treasury Allocation" \
  "Allocate 100 ETH to development fund" \
  1704067200 \
  1704153600
```

**Schema:** `bytes32 dao_uuid, bytes32 proposal_uuid, bytes32 proposal_type_uuid, string title, string description, uint64 startts, uint64 endts`

**Timestamps:** POSIX timestamps in seconds (UTC)

### 5. Cast a Simple Vote

Deploy the SIMPLE_VOTE schema:
```bash
./eas_cli.py deploy SIMPLE_VOTE
```

Vote on a proposal:
```bash
./eas_cli.py attest SIMPLE_VOTE \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  0xfedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321 \
  0xVOTER_ADDRESS \
  1 \
  "I support this allocation" \
  1000000000000000000
```

**Schema:** `bytes32 dao_uuid, bytes32 proposal_uuid, address voter, int8 choice, string reason, uint256 weight`

**Vote choices:**
- `1` = For
- `-1` = Against
- `0` = Abstain

### 6. Cast an Advanced Vote

Deploy the ADVANCED_VOTE schema:
```bash
./eas_cli.py deploy ADVANCED_VOTE
```

Vote with complex choice data:
```bash
./eas_cli.py attest ADVANCED_VOTE \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  0xfedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321 \
  0xVOTER_ADDRESS \
  '{"option_a": 60, "option_b": 40}' \
  "Split vote based on priorities" \
  1000000000000000000
```

**Schema:** `bytes32 dao_uuid, bytes32 proposal_uuid, address voter, string choice, string reason, uint256 weight`

### 7. Undo an Attestation

Deploy the UNDO schema:
```bash
./eas_cli.py deploy UNDO
```

Retroactively nullify an attestation:
```bash
./eas_cli.py attest UNDO \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  0xATTESTATION_UID_TO_UNDO
```

**Schema:** `bytes32 dao_uuid, bytes32 uid`

**Note:** UNDO retroactively invalidates attestations. Requires UNDO permission (bit 2 in GRANT level).

## Protocol Reference

For complete protocol specification, security considerations, and governance flow details, see [protocol.md](./protocol.md).

### Key Concepts

- **dao_uuid**: Unique identifier for a DAO (bytes32)
- **Permissions**: Authority delegated via GRANT attestations
- **Proposal Types**: Classes that define voting rules (standard, approval, optimistic)
- **Timestamps**: POSIX seconds since epoch (UTC)

### Example Governance Flow

1. Platform issues `INSTANTIATE` to create DAO
2. Initial authority grants `CREATE_PROPOSAL_TYPE` permission to council
3. Council member creates proposal type via `CREATE_PROPOSAL_TYPE`
4. Delegates create proposals via `CREATE_PROPOSAL`
5. Members vote via `SIMPLE_VOTE` or `ADVANCED_VOTE`
6. Results tallied offchain (or onchain with custom resolvers)
7. If needed, authorized actors can issue `UNDO` to nullify attestations

## License

Open source under the protocol defined in [protocol.md](./protocol.md).
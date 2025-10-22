# An On & Offchain DAO Protocol using EAS

A Python command-line tool for deploying schemas and creating attestations using the [On & Offchain Attestation DAO Protocol](./protocol.md) with Ethereum Attestation Service (EAS).

## Overview

This CLI wraps Foundry's `forge` commands to simplify interaction with the DAO governance protocol defined in [protocol.md](./protocol.md). It supports all seven attestation types:

- `INSTANTIATE` - Declare a DAO and assign initial authority
- `GRANT` - Assign permissions to addresses within a DAO
- `CREATE_PROPOSAL_TYPE` - Define proposal classes for the DAO
- `CREATE_PROPOSAL` - Submit proposals under a DAO-defined type
- `SIMPLE_VOTE` - Record votes with numeric choices (For/Against/Abstain)
- `ADVANCED_VOTE` - Record votes with JSON-encoded choice payloads
- `UNDO` - Retroactively nullify an attestation

### Schema Hashes

```
INSTANTIATE : 0x8ba7508bd53801fb932a73f12e2b4f78026bcf88d4e1c7a098ced7c0612ed211
PERMA_INSTANTIATE : 0xaeff4a05b483128622bca8fc08c8b46fcf45a2402c86d050c627596492447913
GRANT : 0x860ae1305cdafc30118cdf9b3aaece03c686e7498d77f00a7af3f466b88a3bd2
CREATE_PROPOSAL_TYPE : 0xb7e54e56dd2ed7426f0dd3dff926675594cd2f7e03da14ce9759f8f0b5bcfb3b
CREATE_PROPOSAL : 0x12e8600c9bb57b5b436fa09735cfc63e95098552122001c465b610261eea8a93
SET_PROPOSAL_TYPE : 0xc218b18af140c97644087c59e8ab35b981e73e026ffaf318f371c4ddc56efcb9
SET_PARAM_VALUE : 0x654f697d66f87c1ee3f72a28e1383463418a9b8b8d54863b304acd558e98c675
DELEGATED_SIMPLE_VOTE : 0xffcc8fe77f55448bee5f0e24844ee76f83c3c2718dcf8a75de750cf4797ad0bc
DELEGATED_ADVANCED_VOTE : 0x16c4ffdf71c55b73e4ebf099baf78b97376020f6ba9ede5b618900bcb9101e0b
SIMPLE_VOTE : 0x04cb5678af613212e584cf8d117ee3fcd038a9ab657ecf0c596cabe1e6ebd9f0
ADVANCED_VOTE : 0x724c8d6579c5098a5d3c44717a5b5a8ea9e7064078ff8ca7d3de3f4ad5097627
DELETE : 0xf691b5231d1f526f9fb59610734a7f4bf91d0330e6d559fd821d69adbda0fc8b
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
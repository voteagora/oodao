# An On & Offchain DAO Protocol using EAS

A Python command-line tool for deploying schemas and creating attestations using the [On & Offchain Attestation DAO Protocol](./protocol.md) with Ethereum Attestation Service (EAS).

## Overview

This CLI wraps Foundry's `forge` commands to simplify interaction with the DAO governance protocol defined in [protocol.md](./protocol.md). 

## Deployments

# Eth Mainnet

## Entity Resolver Proxy:
0x7f730aea758432bb0d5a1359746f2255e345f4e1

## Votes Resolver Proxy:
0x6d04c55db4b1f647ead847fb1feccd29ac0bfa84

## Entities Implementation
forge verify-contract \
  --chain mainnet \
  --etherscan-api-key JIF6AGF7HBFSH1RKAK398KAZ2UHZM9TBTJ \
  0x5ec8fdaa5040be3408c04cc1ee84481c735bbcd9 \
  resolvers/EntitiesResolver.sol:EntitiesResolver

## Votes Implementation
forge verify-contract \
  --chain mainnet \
  --etherscan-api-key JIF6AGF7HBFSH1RKAK398KAZ2UHZM9TBTJ \
  0xe00fbb29000d4a3cf5eff1d6a2def4b7a388c761 \
  resolvers/VotesResolver.sol:VotesResolver


# Eth Sepolia 

## Entity Resolver Proxy:
0xdf0e5df7af27076e5ea57be9dc068ea36d970bc4

## Votes Resolver Proxy:
0x990885ca636aaba3513e82d4e74b82b1f76bbb04

## Entities Implementation
forge verify-contract \
  --chain sepolia \
  --etherscan-api-key JIF6AGF7HBFSH1RKAK398KAZ2UHZM9TBTJ \
  0x198c4171b7de6e1ea1b752896ad1555ad04b68f1 \
  resolvers/EntitiesResolver.sol:EntitiesResolver

## Votes Implementation
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

#### Mainnet Deployment

```
{
   'INSTANTIATE' : '0x9ae11105c3161551c7c9a4c0c4eae3343e21f5d76df578ca6ed7189a23a4bb5c',
   'PERMA_INSTANTIATE' : '0xe9f31c7a33877623b7833cf85031544865d45fc99673a3584470417d89d8d355',
   'GRANT' : '0xc95eea0923b6637554da6b4eccf377c2204b3fd8d840b64bee4657ba3c9096ce',
   'CREATE_PROPOSAL_TYPE' : '0x9c20478c45568b58f31b3d3bbd8f8235c1da82a90f6d684e28ace2de620dc1ad',
   'CREATE_PROPOSAL' : '0x442d586d8424b5485de1ff46cb235dcb96b41d19834926bbad1cd157fbeeb8fc',
   'CHECK_PROPOSAL' : '0x479e42ce8c35c53a243718c4c2eb1867e1215006e7d72885c178342f4df3ca01',
   'SET_PROPOSAL_TYPE' : '0xe01a97552181ccc84fa3d962867b0f78ccab131a8a4a3b78c9396bc61926dff2',
   'SET_PARAM_VALUE' : '0x2338b41569bd8e26d938bf7555890d4cc2fc8b4e8ecaf567e2ae821d4367cd28',
   'DELEGATED_SIMPLE_VOTE' : '0x60d1d0641b8ab83aabf8bd7e49fece644a9a20e05a4132ac85a3e1efd9c319ee',
   'DELEGATED_ADVANCED_VOTE' : '0x7712a927f5378bec2425e543a42a8d8e57ab98639e66d2c11fb9a69a3094edbd',
   'SIMPLE_VOTE' : '0x3bc2cb5268eedcc69ce64646cd096ed4ef2ed0537cb6bbed80e5f7a844060610',
   'ADVANCED_VOTE' : '0x6e464ac3ba1761e2e44057a8769e5ecbb3b09fa3332475cbeca27cce115aa46e',
   'DELETE' : '0xd5c8d8a5f9eb7b9691acb2aa95e8a769984ce55d4c113511ba9ac366c29e1d62',
}
```

#### Sepolia Deployment

```
{
   'INSTANTIATE' : '0x6bd280a85f895b15798d2b8e524a651e034f42b3ce614cb394c9d5e2ae2b10c7',
   'PERMA_INSTANTIATE' : '0x01a6e34a0b986043b892902536c69a24f37fcfdaea39fbd2216dedbc6d53d83f',
   'GRANT' : '0x7e4752a595f69560a5759e1acc1c70995758b45f00972374de9e1b801d19b758',
   'CREATE_PROPOSAL_TYPE' : '0x880613f78650605d0a0617ec006b8181de80f688a12da6e78f1a8bf3d6b4f922',
   'CREATE_PROPOSAL' : '0x442d586d8424b5485de1ff46cb235dcb96b41d19834926bbad1cd157fbeeb8fc',
   'CHECK_PROPOSAL' : '0xd0fa030b9d06e954b910a86eeffc02aa641eaeef4216f9402ab4503f44c8e6a8',
   'SET_PROPOSAL_TYPE' : '0x4468df37e17deb20b5096fb12107d4841b79ff6a62292e798eb7b79d0e764eb5',
   'SET_PARAM_VALUE' : '0x7ac5f4a1c2c47e910132a546af770c1a6ff0c02e931020de6f955cf42eae9a6b',
   'DELEGATED_SIMPLE_VOTE' : '0xde80f2c4e6168c2f68c1b466087ffba7994c2b7ff8f4113689c75ee82ef59c61',
   'DELEGATED_ADVANCED_VOTE' : '0x4aa210b34a3b488c54f7ec482763c5ec8a52be5669c24216d3814b009076fb50',
   'SIMPLE_VOTE' : '0x2b0e624e00310c7e88a1b7840238e285152b38ab00160b14c0d4e54e0a53a3aa',
   'ADVANCED_VOTE' : '0xa7497737b4bdc0eaf60e90a290602216fb2a0e8c886e50bad63324ca8b76a587',
   'DELETE' : '0x42793d748cbdd8d815556d7bbeacae5e82cbce605ea048474e7e60a02577cf49',
}
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
# An On & Offchain DAO Protocol using EAS

A Python command-line tool for deploying schemas and creating attestations using the [On & Offchain Attestation DAO Protocol](./protocol.md) with Ethereum Attestation Service (EAS).

## Overview

This CLI wraps Foundry's `forge` commands to simplify interaction with the DAO governance protocol defined in [protocol.md](./protocol.md). 

## Deployments

# Eth Mainnet

## Entity Resolver Proxy:
0xf246C55a4f91f08c991F566fcF063156f67e6c03

ProxyAdmin: 0x8D7512290251bd5417A00730aBFA0E5fdba1094A

## Votes Resolver Proxy:
0x576c9f4C976e2E6AF9E7093F1A23Fa31B21D4cB3

ProxyAdmin: 0x4Ee4b7e6eE98e0b5361dACcF9062733858c4B066

## Entities Implementation
forge verify-contract \
  --chain mainnet \
  --etherscan-api-key JIF6AGF7HBFSH1RKAK398KAZ2UHZM9TBTJ \
  0x76004fe594c9bc82effe6d6791b2269d4a85c7f4 \
  resolvers/EntitiesResolver.sol:EntitiesResolver

## Votes Implementation
forge verify-contract \
  --chain mainnet \
  --etherscan-api-key JIF6AGF7HBFSH1RKAK398KAZ2UHZM9TBTJ \
  0x3bc0b1a341fdc3e09935f7e3cf69a4a401b2a982 \
  resolvers/VotesResolver.sol:VotesResolver


# Eth Sepolia 

## Entity Resolver Proxy:
0x7106847Cc6c99E3D730D4f2a8312A905c0ad2ad7

ProxyAdmin: 0xe84969F17B2628C71B421d552450b7F131bE07A2

## Votes Resolver Proxy:
0xC8EA7C7651245728BE57c2d4C5638F8eF843b0E7

ProxyAdmin: 0xaFb13914085154869a6770d6bbcE1Cc9B3aDE560

## Entities Implementation
forge verify-contract \
  --chain sepolia \
  --etherscan-api-key JIF6AGF7HBFSH1RKAK398KAZ2UHZM9TBTJ \
  0x3c8398c931a0dce8e7dfcf71ddf818fb20012878 \
  resolvers/EntitiesResolver.sol:EntitiesResolver

## Votes Implementation
forge verify-contract \
  --chain sepolia \
  --etherscan-api-key JIF6AGF7HBFSH1RKAK398KAZ2UHZM9TBTJ \
  0x4eb776bded70c78838ad48547003e1e9790133bc \
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
   'INSTANTIATE' : '0x4ca31403392556d861e0d1b52eff1617a33128de3a5f479745b6c8556100f65e',
   'PERMA_INSTANTIATE' : '0x9d13a1c5cc8ddf2a08fa83c2450703aca6f17d4db86caff5982ce3b20b9f1d2a',
   'GRANT' : '0x366e5dd3956e245e20a87c7048e8254cf7d024d3d47c0a872a50d0020b77a75f',
   'CREATE_PROPOSAL_TYPE' : '0x13194d67b1c5d22f8ea698bc37b0b376fcd35cc1d4baa43aebb99c30d69b6edb',
   'CREATE_PROPOSAL' : '0x442d586d8424b5485de1ff46cb235dcb96b41d19834926bbad1cd157fbeeb8fc',
   'CHECK_PROPOSAL' : '0x675048a4668d59d117cdbc5810912a1da791eb927fc8986ddbacccb4473d8b30',
   'SET_PROPOSAL_TYPE' : '0x5e302e7f8743e8369750afaf8a822d6ca4ecbee78b737c4276220732c4488d7a',
   'SET_PARAM_VALUE' : '0x23c692259d71fb2aa717353252e86560299fdeba8a3c839d808839d8eae5e17a',
   'DELEGATED_SIMPLE_VOTE' : '0x4a0cdb428e86fa169d4d619ac22f0a7184ff3f63f02abca5ed059319646d0e43',
   'DELEGATED_ADVANCED_VOTE' : '0x7cddf052e2011a22bdbcf2004655ca25b006a8e0955e0d537515907a94b88b1e',
   'SIMPLE_VOTE' : '0xa6abd1e115de8e83b71f6db6db22d44d730a217f21e6008034f94e682efe9c70',
   'ADVANCED_VOTE' : '0x4baeed1a31235fddb0757c6b0e006fee241019cd0ed3e0706ec2b2d1329acfe4',
   'DELETE' : '0x3dd1714d33cc8dc91f24307758d4309a54a3b17080a3059bc67585e97a769a1e',
}
```

#### Sepolia Deployment

```
{
   'INSTANTIATE' : '0xa45718ef6b8758277682e9914ed85b960e19fd8331ed75e24641d228b7efcd2d',
   'PERMA_INSTANTIATE' : '0x3921c650e5c0a565fe4e2b5dad38546999588bd18904a3354641ca6c998f6bc4',
   'GRANT' : '0xd430f8dc7a9503e92e621503eed2c716a524604be530842601d7fb0e1bb8ff15',
   'CREATE_PROPOSAL_TYPE' : '0x4147434e77680f972dcaa494427b876fa0f5ecdfde56131dd24a988ad90a6950',
   'CREATE_PROPOSAL' : '0x38bfba767c2f41790962f09bcf52923713cfff3ad6d7604de7cc77c15fcf169a',
   'CHECK_PROPOSAL' : '0x08df8e6e629077cabef4ed15cd4ff4f2359c2a60ad65b8355ac1f905b8f23a6f',
   'SET_PROPOSAL_TYPE' : '0xa6ca209ead271e33d86bf969fb5b9d5f559bf3fb22765ede70652b1faa4973b5',
   'SET_PARAM_VALUE' : '0xa1e21d322b14d3d79bd697b106b7374e19a61eb766907ef27d392dd635d9642f',
   'DELEGATED_SIMPLE_VOTE' : '0x291f9b12f6624076505cb07cc62acf79bd7403cceb435e91d279dcbe6336c94b',
   'DELEGATED_ADVANCED_VOTE' : '0xd9a51aa77ea609950350db55093af36e4c0dce621a131164cb7b410b9c2435bc',
   'SIMPLE_VOTE' : '0x19c36b80a224c4800fd6ed68901ec21f591563c8a5cb2dd95382d430603f91ff',
   'ADVANCED_VOTE' : '0x991b014c62b19364882fc89dbf3baa6104b4598ee2c4f29152be2cbcfcb4cb81',
   'DELETE' : '0x2c451b53c595d44441eb1e8242912a0446e7bfc5f745535537908bef47e6e334',
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

Submit a standard proposal:
```bash
./eas_cli.py attest CREATE_PROPOSAL \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  0xfedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321 \
  0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 \
  "Treasury Allocation" \
  "Allocate 100 ETH to development fund" \
  1704067200 \
  1704153600 \
  '{"voting_module": "standard"}'
```

Submit an approval proposal:
```bash
./eas_cli.py attest CREATE_PROPOSAL \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  0xfedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321 \
  0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 \
  "Treasury Allocation" \
  "Allocate 100 ETH to development fund" \
  1704067200 \
  1704153600 \
  '{"voting_module": "approval", "choices": ["A", "B", "C"], "max_approvals": 2, "criteria": "TOP_CHOICES", "criteria_value": 2}'
```

Submit an optimistic proposal:
```bash
./eas_cli.py attest CREATE_PROPOSAL \
  0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef \
  0xfedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321 \
  0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890 \
  "Treasury Allocation" \
  "Allocate 100 ETH to development fund" \
  1704067200 \
  1704153600 \
  '{"voting_module": "optimistic"}'
```

**Schema:** `bytes32 dao_uuid, bytes32 proposal_uuid, bytes32 proposal_type_uuid, string title, string description, uint64 startts, uint64 endts, string kwargs`

**kwargs:**
`kwargs` is a JSON-encoded blob that allows clients to express richer proposal configuration without changing the onchain schema. This is where you specify details needed to support different proposal classes such as **approval**, and **optimistic** voting.

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

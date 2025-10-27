#!/usr/bin/env python3
"""
EAS Protocol CLI Tool
Wraps forge commands for deploying schemas and creating attestations.
"""

import os
import sys
import subprocess
from typing import Dict
from dotenv import load_dotenv
import click

# from eth_abi import encode
from eth_utils import keccak, to_checksum_address

# Load .env file
load_dotenv()

SCHEMA_CONTRACTS = {'11155111': '0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0'}

EAS_CONTRACTS = {'11155111': '0xC2679fBD37d54388Ce493F1DB75320D236e1815e'}

# Client Generates the dao_id -> could be collissions, 
# but as long as collissions are resolved by using the latest instantiate by a permissioned address... does it matter? Vanity addresses are possible here.
# but then, people could pollute the attestation space. 
SCHEMAS = {
    "INSTANTIATE":              "uint8 protocol_version,string name,uint32 voting_period,uint32 voting_delay",                # recipient = address dao_id, address refUID = 0x0 -> bytes32 discarded
    "PERMA_INSTANTIATE":        "uint8 protocol_version,string name,uint32 voting_period,uint32 voting_delay",                # recipient = address dao_id, address refUID = 0x0 -> bytes32 discarded
    "GRANT":                    "address verb,string permission,uint8 level,string filter",                                   # recipient = address dao_id, address refUID = 0x0 -> bytes32 discarded
    "CREATE_PROPOSAL_TYPE":     "uint32 quorum,uint32 approval_threshold,string name,string description,string class",        # recipient = address dao_id, address refUID = 0x0 -> bytes32 proposal_type_uid
    "CREATE_PROPOSAL":          "string title,string description,uint64 startts,uint64 endts,string tags",                    # recipient = address dao_id, bytes32 refUID = proposal_type_uid | 0x0 -> bytes32 proposal_id
    "CHECK_PROPOSAL":           "string[] passed,string[] failed",                                                            # recipient = address dao_id, bytes32 refUID = proposal_id
    "SET_PROPOSAL_TYPE":        "bytes32 proposal_id",                                                                        # recipient = address dao_id, bytes32 refUID = proposal_type_uid
    "SET_PARAM_VALUE":          "string param_name,uint256 param_value",                                                      # recipient = address dao_id, bytes32 refUID = 0x0 -> bytes32 discarded
    "DELEGATED_SIMPLE_VOTE":    "address voter,int8 choice,string reason",                                                    # recipient = address dao_id, bytes32 refUID = proposal_id
    "DELEGATED_ADVANCED_VOTE":  "address voter,string choice,string reason",                                                  # recipient = address dao_id, bytes32 refUID = proposal_id
    "SIMPLE_VOTE":              "int8 choice,string reason",                                                                  # recipient = address dao_id, bytes32 refUID = proposal_id
    "ADVANCED_VOTE":            "string choice,string reason",                                                                # recipient = address dao_id, bytes32 refUID = proposal_id
    "DELETE":                   "string verb,bytes32 schema_id"                                                               # recipient = address dao_id, bytes32 refUID = uid_of_attestation_to_undo
}

RESOLVER = {schema : "entity_resolver" for schema in SCHEMAS.keys()}
RESOLVER['DELEGATED_SIMPLE_VOTE'] = 'votes_resolver'
RESOLVER['DELEGATED_ADVANCED_VOTE'] = 'votes_resolver'
RESOLVER['SIMPLE_VOTE'] = 'votes_resolver'
RESOLVER['ADVANCED_VOTE'] = 'votes_resolver'
RESOLVER['CREATE_PROPOSAL'] = None

# Should we declare a set of chain-id->token-addresses at instantiation?

REVOCABILITY = {k : "true" for k in SCHEMAS.keys()}
REVOCABILITY['PERMA_INSTANTIATE'] = "false"
REVOCABILITY['DELEGATED_SIMPLE_VOTE'] = "false"
REVOCABILITY['DELEGATED_ADVANCED_VOTE'] = "false"
REVOCABILITY['SIMPLE_VOTE'] = "false"
REVOCABILITY['ADVANCED_VOTE'] = "false"
REVOCABILITY['DELETE'] = "false"
REVOCABILITY['SET_PARAM_VALUE'] = "false"
REVOCABILITY['CHECK_PROPOSAL'] = "false"

OPTIONAL_REFUID = ['CREATE_PROPOSAL']
REQUIRES_REFUID = ['CHECK_PROPOSAL', 'SET_PROPOSAL_TYPE', 'DELETE', 'DELEGATED_SIMPLE_VOTE', 'DELEGATED_ADVANCED_VOTE','SIMPLE_VOTE', 'ADVANCED_VOTE' ]

def get_env_config() -> Dict[str, str]:
    """Load configuration from .env file."""
    chain_id = os.getenv("CHAIN_ID")
    forge_account = os.getenv("FORGE_ACCOUNT")
    rpc_url = os.getenv("RPC_URL")
    dao_id = os.getenv("DAO_ID")

    dao_id = to_checksum_address(dao_id)    

    if not all([chain_id, rpc_url, forge_account, dao_id]):
        click.echo("Error: Missing required environment variables in .env file", err=True)
        click.echo("Required: CHAIN_ID, RPC_URL, FORGE_ACCOUNT, DAO_ID", err=True)
        sys.exit(1)

    return {
        "chain_id": chain_id,
        "rpc_url": rpc_url,
        "forge_account": forge_account,
        "dao_id": dao_id
    }

def get_deployment_config(chain_id):

    if chain_id == 1:
        rpc_url = 'https://eth.llamarpc.com'
        votes_resolver = ...
        entity_resolver = ...
    elif chain_id == 11155111:
        rpc_url = 'https://ethereum-sepolia-rpc.publicnode.com'
        votes_resolver = '0x990885ca636aaba3513e82d4e74b82b1f76bbb04'
        entity_resolver = '0x0292b0ce4f6791ee6d91befbc9f16aed463d1412'
    elif chain_id == 10:
        rpc_url = 'https://optimism-rpc.publicnode.com'
        votes_resolver = ...
        entity_resolver = ...
    elif chain_id == 11155420:
        rpc_url = 'https://sepolia.optimism.io'
        votes_resolver = ...
        entity_resolver = ...
    else:
        raise Exception(f"Chain ID unsupported: {chain_id}")


    return {
        "rpc_url": rpc_url,
        "votes_resolver": votes_resolver,
        "entity_resolver": entity_resolver
    }  


def run_ext_command(binary, args: list) -> subprocess.CompletedProcess:
    """Execute a forge command."""
    cmd = [binary] + args
    click.echo(f"Running: {' '.join(cmd)}")

    print(" ".join(cmd))
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result
    except subprocess.CalledProcessError as e:
        click.echo(f"Error executing command: {e}", err=True)
        click.echo(f"stdout: {e.stdout}", err=True)
        click.echo(f"stderr: {e.stderr}", err=True)
        sys.exit(1)


@click.group()
def cli():
    """EAS Protocol CLI - Deploy schemas and create attestations."""
    pass


# @cli.command()
# @click.argument("attestation_command", type=click.Choice(list(SCHEMAS.keys()), case_sensitive=False))
# @click.argument("chainid")
def deploy(attestation_command: str, chain_id: int):
    """Deploy a schema for the given attestation command.

    ATTESTATION_COMMAND: One of INSTANTIATE, GRANT, CREATE_PROPOSAL_TYPE,
    CREATE_PROPOSAL, SIMPLE_VOTE, ADVANCED_VOTE, UNDO
    """
    attestation_command = attestation_command.upper()
    config = get_deployment_config(chain_id)
    env_config = get_env_config()
    schema = SCHEMAS[attestation_command]

    click.echo(f"Deploying schema for {attestation_command}")
    click.echo(f"Schema: {schema}")

    schema_contract = SCHEMA_CONTRACTS[str(chain_id)]

    resolver_label = RESOLVER[attestation_command]
    if resolver_label:
        resolver = config[resolver_label]
    else:
        resolver = '0x0000000000000000000000000000000000000000'

    # Build forge command for schema deployment
    # forge script is commonly used for deployments
    
    revocability = REVOCABILITY[attestation_command]

    args = [
        "send",
        schema_contract,
        "register(string,address,bool)(bytes32)",
        schema,
        resolver,
        revocability,
        "--rpc-url", config["rpc_url"],
        "--account", env_config["forge_account"],
        "--chain-id", str(chain_id)
    ]

    result = run_ext_command("cast", args)
    click.echo("Schema deployment initiated successfully!")
    click.echo(result.stdout)

@cli.command()
@click.argument("chainid")
def deployall(chainid:int):
    for i, schema in enumerate(SCHEMAS.keys()):
        print(i, schema)
        try:
            deploy(schema, int(chainid))
        except:
            print(f"Failed to deploy schema: {schema}")

def get_schema_id(attestation_command: str, chainid: int):

    schema = SCHEMAS[attestation_command]

    deploy_config = get_deployment_config(chainid)

    resolver_label = RESOLVER[attestation_command]

    if resolver_label:
        resolver = deploy_config[resolver_label]
    else:
        resolver = '0x0000000000000000000000000000000000000000'

    resolver = to_checksum_address(resolver)
    revocable = REVOCABILITY[attestation_command]

    # print(["string", "address", "bool"], [schema, resolver, revocable == "true"])

    # abi.encodePacked equivalent:
    packed = b""
    packed += schema.encode("utf-8")           # string → utf-8 bytes
    packed += bytes.fromhex(resolver[2:])      # address → 20 bytes
    packed += b"\x01" if (revocable == "true") else b"\x00"  # bool → 1 byte

    uid = keccak(packed).hex()

    return uid


def normalize_bytes32(val: str) -> str:
    """
    Normalize a CLI argument into a valid 0x-prefixed 32-byte hex string.
    - Pads with trailing zeros if too short.
    - Errors if longer than 32 bytes.
    """
    if not val.startswith("0x"):
        raise click.ClickException(f"bytes32 must start with 0x: {val}")

    hexstr = val[2:]
    if len(hexstr) < 64:
        hexstr = hexstr.ljust(64, "0")  # pad with zeros
    elif len(hexstr) > 64:
        raise click.ClickException(f"Value too long for bytes32: {val}")

    return "0x" + hexstr.lower()


@cli.command()
@click.argument("attestation_command", type=click.Choice(list(SCHEMAS.keys()), case_sensitive=False), required=False)
def schema_hash(attestation_command: str = None):
    """Generate the Keccak-256 hash (schema UID) for schemas.

    If ATTESTATION_COMMAND is provided, generates the hash for that specific schema.
    Otherwise, generates hashes for all schemas in the SCHEMAS dictionary.

    Examples:

      eas_cli.py schema-hash

      eas_cli.py schema-hash INSTANTIATE
    """
    if attestation_command:
        # Generate hash for specific schema
        attestation_command = attestation_command.upper()
        schema = SCHEMAS[attestation_command]
        schema_uid = get_schema_id(attestation_command)
        revocable = REVOCABILITY[attestation_command]

        click.echo(f"\nSchema: {attestation_command}")
        click.echo(f"  Definition: {schema}")
        click.echo(f"  Revocable: {revocable}")
        click.echo(f"  UID: 0x{schema_uid}")
    else:
        # Generate hashes for all schemas
        click.echo("\nGenerating schema UIDs for all schemas:\n")
        for schema_name in SCHEMAS.keys():
            schema = SCHEMAS[schema_name]
            schema_uid = get_schema_id(schema_name)
            revocable = REVOCABILITY[schema_name]

            click.echo(f"{schema_name}:")
            click.echo(f"  Definition: {schema}")
            click.echo(f"  Revocable: {revocable}")
            click.echo(f"  UID: 0x{schema_uid}")
            click.echo()


@cli.command()
@click.argument("chainid")
def schema_hashes(chainid:int):
    """List all schema names with their UIDs in compact format.

    Example output:
      INSTANTIATE : 0x1aabc49db4e9e0bbff60eb079e9316524d183cd783da298ca54f2db449218923
      PERMA_INSTANTIATE : 0xe85e53a6d27f83a8d9e6ee94d01a312f54e82de919a708c17a9da6a899258cd1
      ...
    """
    click.echo("{")
    for schema_name in SCHEMAS.keys():
        schema_uid = get_schema_id(schema_name, int(chainid))
        click.echo(f"   '{schema_name}' : '0x{schema_uid}',")
    click.echo("}")


@cli.command()
@click.argument("attestation_command", type=click.Choice(list(SCHEMAS.keys()), case_sensitive=False))
@click.argument("args", nargs=-1)
def attest(attestation_command: str, args: tuple):
    """Create an attestation with the given arguments.

    DAO_UUID: Address of the DAO (used as recipient)

    ATTESTATION_COMMAND: One of INSTANTIATE, GRANT, CREATE_PROPOSAL_TYPE,
    CREATE_PROPOSAL, SIMPLE_VOTE, ADVANCED_VOTE, UNDO

    ARGS: Space-separated arguments matching the schema fields

    Examples:

      eas_cli.py attest INSTANTIATE 0x123... 1 "My DAO"

      eas_cli.py attest GRANT 0x123... 0xabc... CREATE_PROPOSAL 1 ""

      eas_cli.py attest SIMPLE_VOTE 0x123... 0xdef... 0xabc... 1 "I support this" 100
    """
    attestation_command = attestation_command.upper()
    config = get_env_config()
    schema = SCHEMAS[attestation_command]

    dao_id = config['dao_id']

    schema_uid = get_schema_id(attestation_command, int(config["chain_id"]))
    eas_contract = EAS_CONTRACTS[config["chain_id"]]

    # Parse schema fields (types only)
    schema_fields = [f.strip().split()[0] for f in schema.split(",")]

    REFUID_LEN = len("0x0000000000000000000000000000000000000000000000000000000000000000")

    check = False

    if attestation_command in OPTIONAL_REFUID:

        if len(args) == len(schema_fields):
            check = True
            refuid = "0x0000000000000000000000000000000000000000000000000000000000000000" 
        elif (len(args) == len(schema_fields)) + 1:
            check = True
            refuid = args[-1]
            args = args[:-1]
            assert len(refuid) == REFUID_LEN

    elif attestation_command in REQUIRES_REFUID:

        if (len(args) == len(schema_fields)) + 1:
            check = True
            refuid = args[-1]
            args = args[:-1]
            assert len(refuid) == REFUID_LEN

    else:
        if len(args) == len(schema_fields):
            check = True
            refuid = "0x0000000000000000000000000000000000000000000000000000000000000000" 

    if not check:
        click.echo(f"Error: Expected {len(schema_fields)} arguments for {attestation_command}", err=True)
        click.echo(f"Schema fields: {schema}", err=True)
        click.echo(f"Received {len(args)} arguments", err=True)
        sys.exit(1)

    # Normalize arguments (auto-pad bytes32)
    normalized_args = []
    for arg, typ in zip(args, schema_fields):
        if typ == "bytes32":
            normalized_args.append(normalize_bytes32(arg))
        else:
            normalized_args.append(arg)

    click.echo(f"Creating attestation: {attestation_command}")
    click.echo(f"Arguments: {normalized_args}")

    # Step 1: ABI-encode schema payload
    abi_sig = f"f({','.join(schema_fields)})"
    encode_cmd = ["abi-encode", abi_sig, *normalized_args]
    enc_result = run_ext_command("cast", encode_cmd)
    encoded_bytes = enc_result.stdout.strip()
    revocable = REVOCABILITY[attestation_command]

    # Step 2: Build AttestationRequestData tuple
    attestation_data = (
        "(" +
        f"{dao_id}," +                                 # recipient
        "0," +                                         # expirationTime
        revocable +"," +                               # revocable
        f"{refuid}," +  # refUID
        f"{encoded_bytes}," +                          # data
        "0" +                                          # value
        ")"
    )

    print(attestation_data)

    # Step 3: Call EAS.attest
    full_request = f"(0x{schema_uid},{attestation_data})"

    cast_args = [
        "send",
        eas_contract,
        "attest((bytes32,(address,uint64,bool,bytes32,bytes,uint256)))",
        full_request,
        "--rpc-url", config["rpc_url"],
        "--account", config["forge_account"],
        "--chain-id", str(config["chain_id"]),
    ]

    result = run_ext_command("cast", cast_args)
    click.echo("✅ Attestation created successfully!")
    click.echo(result.stdout)

if __name__ == "__main__":
    cli()



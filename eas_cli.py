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

from eth_abi import encode
from eth_utils import keccak, to_checksum_address

# Load .env file
load_dotenv()

SCHEMA_CONTRACTS = {'11155111': '0x0a7E2Ff54e76B8E6659aedc9103FB21c038050D0'}

EAS_CONTRACTS = {'11155111': '0xC2679fBD37d54388Ce493F1DB75320D236e1815e'}

# Schema definitions for each attestation type
SCHEMAS = {
    "INSTANTIATE": "bytes32 dao_uuid,uint8 protocol_version,string name",
    "GRANT": "bytes32 dao_uuid,address subject,string permission,uint8 level,string filter",
    "CREATE_PROPOSAL_TYPE": "bytes32 dao_uuid,bytes32 proposal_type_uuid,string class,string kwargs",
    "CREATE_PROPOSAL": "bytes32 dao_uuid,bytes32 proposal_uuid,bytes32 proposal_type_uuid,string title,string description,uint64 startts,uint64 endts",
    "SIMPLE_VOTE": "bytes32 dao_uuid,bytes32 proposal_uuid,address voter,int8 choice,string reason,uint256 weight",
    "ADVANCED_VOTE": "bytes32 dao_uuid,bytes32 proposal_uuid,address voter,string choice,string reason,uint256 weight",
    "UNDO": "bytes32 dao_uuid,bytes32 uid"
}

REVOCABILITY = {k : "true" for k in SCHEMAS.keys()}
REVOCABILITY['INSTANTIATE'] = "false"
REVOCABILITY['SIMPLE_VOTE'] = "false"
REVOCABILITY['ADVANCED_VOTE'] = "false"
REVOCABILITY['UNDO'] = "false"


def get_env_config() -> Dict[str, str]:
    """Load configuration from .env file."""
    chain_id = os.getenv("CHAIN_ID")
    rpc_url = os.getenv("RPC_URL")
    forge_account = os.getenv("FORGE_ACCOUNT")

    if not all([chain_id, rpc_url, forge_account]):
        click.echo("Error: Missing required environment variables in .env file", err=True)
        click.echo("Required: CHAIN_ID, RPC_URL, FORGE_ACCOUNT", err=True)
        sys.exit(1)

    return {
        "chain_id": chain_id,
        "rpc_url": rpc_url,
        "forge_account": forge_account
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


@cli.command()
@click.argument("attestation_command", type=click.Choice(list(SCHEMAS.keys()), case_sensitive=False))
def deploy(attestation_command: str):
    """Deploy a schema for the given attestation command.

    ATTESTATION_COMMAND: One of INSTANTIATE, GRANT, CREATE_PROPOSAL_TYPE,
    CREATE_PROPOSAL, SIMPLE_VOTE, ADVANCED_VOTE, UNDO
    """
    attestation_command = attestation_command.upper()
    config = get_env_config()
    schema = SCHEMAS[attestation_command]

    click.echo(f"Deploying schema for {attestation_command}")
    click.echo(f"Schema: {schema}")

    schema_contract = SCHEMA_CONTRACTS[config["chain_id"]]

    # Build forge command for schema deployment
    # forge script is commonly used for deployments
    
    revocability = REVOCABILITY[attestation_command]

    args = [
        "send",
        schema_contract,
        "register(string,address,bool)(bytes32)",
        schema,
        "0x0000000000000000000000000000000000000000",
        revocability,
        "--rpc-url", config["rpc_url"],
        "--account", config["forge_account"],
        "--chain-id", config["chain_id"]
    ]

    result = run_ext_command("cast", args)
    click.echo("Schema deployment initiated successfully!")
    click.echo(result.stdout)


def get_schema_id(attestation_command: str):

    schema = SCHEMAS[attestation_command]
    resolver = to_checksum_address("0x0000000000000000000000000000000000000000")
    revocable = REVOCABILITY[attestation_command]

    print(["string", "address", "bool"], [schema, resolver, revocable == "true"])

    # abi.encodePacked equivalent:
    packed = b""
    packed += schema.encode("utf-8")           # string → utf-8 bytes
    packed += bytes.fromhex(resolver[2:])      # address → 20 bytes
    packed += b"\x01" if (revocable == "true") else b"\x00"  # bool → 1 byte

    uid = keccak(packed).hex()

    return uid


@cli.command()
@click.argument("attestation_command", type=click.Choice(list(SCHEMAS.keys()), case_sensitive=False))
@click.argument("args", nargs=-1)
def attest(attestation_command: str, args: tuple):
    """Create an attestation with the given arguments.

    ATTESTATION_COMMAND: One of INSTANTIATE, GRANT, CREATE_PROPOSAL_TYPE,
    CREATE_PROPOSAL, SIMPLE_VOTE, ADVANCED_VOTE, UNDO

    ARGS: Space-separated arguments matching the schema fields

    Examples:

      eas_cli.py attest INSTANTIATE 0x123... v0.1.0 "My DAO"

      eas_cli.py attest GRANT 0x123... 0xabc... CREATE_PROPOSAL 1 ""

      eas_cli.py attest SIMPLE_VOTE 0x123... 0xdef... 0xabc... 1 "I support this" 100
    """
    attestation_command = attestation_command.upper()
    config = get_env_config()
    schema = SCHEMAS[attestation_command]

    uid = get_schema_id(attestation_command)  

    print(uid)

    # Parse schema to get expected field count
    schema_fields = [f.strip().split()[1] for f in schema.split(',')]

    if len(args) != len(schema_fields):
        click.echo(f"Error: Expected {len(schema_fields)} arguments for {attestation_command}", err=True)
        click.echo(f"Schema fields: {', '.join(schema_fields)}", err=True)
        click.echo(f"Received {len(args)} arguments", err=True)
        sys.exit(1)

    click.echo(f"Creating attestation: {attestation_command}")
    click.echo(f"Arguments: {args}")

    eas_contract = EAS_CONTRACTS[config["chain_id"]]

    uid = get_schema_id(attestation_command)

    # Build forge command for attestation
    # Encode arguments as ABI-encoded data
    cast_args = [
        "send",
        eas_contract,
        "attest((bytes32,(address,uint64,bool,bytes32,bytes,uint256)))(bytes32)",
        uid,
        *args,
        "--rpc-url", config["rpc_url"],
        "--account", config["forge_account"],
        "--chain-id", config["chain_id"]
    ]

    result = run_ext_command("cast", cast_args)
    click.echo("Attestation created successfully!")
    click.echo(result.stdout)


@cli.command()
@click.argument("attestation_command", type=click.Choice(list(SCHEMAS.keys()), case_sensitive=False))
@click.argument("args", nargs=-1)
def attest2(attestation_command: str, args: tuple):
    """Create an attestation with the given arguments.

    ATTESTATION_COMMAND: One of INSTANTIATE, GRANT, CREATE_PROPOSAL_TYPE,
    CREATE_PROPOSAL, SIMPLE_VOTE, ADVANCED_VOTE, UNDO

    ARGS: Space-separated arguments matching the schema fields

    Examples:

      eas_cli.py attest INSTANTIATE 0x123... v0.1.0 "My DAO"

      eas_cli.py attest GRANT 0x123... 0xabc... CREATE_PROPOSAL 1 ""

      eas_cli.py attest SIMPLE_VOTE 0x123... 0xdef... 0xabc... 1 "I support this" 100
    """
    attestation_command = attestation_command.upper()
    config = get_env_config()
    schema = SCHEMAS[attestation_command]

    schema_uid = get_schema_id(attestation_command)
    eas_contract = EAS_CONTRACTS[config["chain_id"]]

    # Parse schema fields (extract only the types)
    schema_fields = [f.strip().split()[0] for f in schema.split(',')]

    if len(args) != len(schema_fields):
        click.echo(f"Error: Expected {len(schema_fields)} arguments for {attestation_command}", err=True)
        click.echo(f"Schema fields: {schema}", err=True)
        click.echo(f"Received {len(args)} arguments", err=True)
        sys.exit(1)

    click.echo(f"Creating attestation: {attestation_command}")
    click.echo(f"Arguments: {args}")

    # Step 1: ABI-encode the schema-specific payload
    abi_sig = "f(" + ",".join(schema_fields) + ")"
    encode_cmd = ["abi-encode", abi_sig, *args]
    enc_result = run_ext_command("cast", encode_cmd)
    encoded_bytes = enc_result.stdout.strip()

    # Step 2: Construct AttestationRequestData
    # recipient=0x0, expirationTime=0, revocable=true, refUID=0, data=encoded_bytes, value=0
    attestation_data = (
        f"(0x0000000000000000000000000000000000000000,"
        f"0,true,"
        f"0x0000000000000000000000000000000000000000000000000000000000000000,"
        f"{encoded_bytes},"
        f"0)"
    )

    # Step 3: Call EAS.attest
    cast_args = [
        "send",
        eas_contract,
        "attest((bytes32,(address,uint64,bool,bytes32,bytes,uint256)))(bytes32)",
        schema_uid,
        attestation_data,
        "--rpc-url", config["rpc_url"],
        "--account", config["forge_account"],
        "--chain-id", str(config["chain_id"])
    ]

    result = run_ext_command("cast", cast_args)
    click.echo("✅ Attestation created successfully!")
    click.echo(result.stdout)


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
@click.argument("attestation_command", type=click.Choice(list(SCHEMAS.keys()), case_sensitive=False))
@click.argument("args", nargs=-1)
def attest3(attestation_command: str, args: tuple):
    """Create an attestation with the given arguments.

    ATTESTATION_COMMAND: One of INSTANTIATE, GRANT, CREATE_PROPOSAL_TYPE,
    CREATE_PROPOSAL, SIMPLE_VOTE, ADVANCED_VOTE, UNDO

    ARGS: Space-separated arguments matching the schema fields

    Examples:

      eas_cli.py attest2 INSTANTIATE 0x123... v0.1.0 "My DAO"

      eas_cli.py attest2 GRANT 0x123... 0xabc... CREATE_PROPOSAL 1 ""

      eas_cli.py attest2 SIMPLE_VOTE 0x123... 0xdef... 0xabc... 1 "I support this" 100
    """
    attestation_command = attestation_command.upper()
    config = get_env_config()
    schema = SCHEMAS[attestation_command]

    schema_uid = get_schema_id(attestation_command)
    eas_contract = EAS_CONTRACTS[config["chain_id"]]

    # Parse schema fields (types only)
    schema_fields = [f.strip().split()[0] for f in schema.split(",")]

    if len(args) != len(schema_fields):
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
        "0x0000000000000000000000000000000000000000," +  # recipient
        "0," +                                         # expirationTime
        revocable +"," +                                      # revocable
        "0x0000000000000000000000000000000000000000000000000000000000000000," +  # refUID
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



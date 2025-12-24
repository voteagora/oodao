from eth_utils import keccak

def pack_eth_address(ascii_str: str, num4: int, num1: int, num2: int) -> str:
    """
    Pack components into a 20-byte Ethereum address.

    Components:
    - ascii_str: up to 10-character string (padded with '.' to 10 bytes)
    - num4: 4-byte integer
    - num1: 1-byte integer
    - num2: 2-byte integer
    - 3 bytes left over for checksum
    """
    # Pad or truncate ASCII string to 10 characters
    ascii_str = ascii_str.ljust(10, ".")[:10]

    # Validate numeric ranges
    if not (0 <= num1 <= 0xFF):
        raise ValueError("num1 must fit in 1 byte")
    if not (0 <= num2 <= 0xFFFF):
        raise ValueError("num2 must fit in 2 bytes")
    if not (0 <= num4 <= 0xFFFFFFFF):
        raise ValueError("num4 must fit in 4 bytes")

    # Convert components to bytes
    ascii_bytes = ascii_str.encode("ascii")        # 10 bytes
    num4_bytes = num4.to_bytes(4, "big")          # 4 bytes
    num1_bytes = num1.to_bytes(1, "big")          # 1 byte
    num2_bytes = num2.to_bytes(2, "big")          # 2 bytes

    # Concatenate partial address (17 bytes)
    partial = ascii_bytes + num4_bytes + num1_bytes + num2_bytes

    # 3-byte checksum from keccak of partial bytes
    checksum = keccak(partial)[:3]

    # Final 20-byte Ethereum address
    final_bytes = partial + checksum
    assert len(final_bytes) == 20

    # Convert to hex string
    hex_address = "0x" + final_bytes.hex()
    return hex_address

# Example usage:

customer_nonce = 0

print("Sepolia:")
version = 1
address = pack_eth_address("syndicate", 11155111, version, customer_nonce)
print(address)

print("Mainnet:")
address = pack_eth_address("syndicate", 1, version, customer_nonce)
print(address)


print("Base:")
address = pack_eth_address("towns", 8453, version, customer_nonce)
print(address)

"""
Sepolia (syndicate):
0x73796e6469636174652e00aa36a701000079e0f1
Mainnet (syndicate):
0x73796e6469636174652e000000010100000a2f00
Base (towns):
0x746f776e732e2e2e2e2e00002105010000e5ebe1
"""
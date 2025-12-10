from eth_utils import to_bytes, to_hex

def unpack_eth_address(hex_address: str):
    """
    Unpack a 20-byte Ethereum address created with the following format:
    - 10 bytes ASCII string (padded with '.')
    - 4 bytes integer
    - 1 byte integer
    - 2 bytes integer
    - 3 bytes checksum
    """
    # Convert hex address to bytes
    addr_bytes = to_bytes(hexstr=hex_address)
    
    if len(addr_bytes) != 20:
        raise ValueError("Address must be exactly 20 bytes")

    # Slice bytes
    ascii_bytes = addr_bytes[0:10]
    num4_bytes = addr_bytes[10:14]
    num1_bytes = addr_bytes[14:15]
    num2_bytes = addr_bytes[15:17]
    checksum_bytes = addr_bytes[17:20]

    # Decode/convert values
    ascii_str = ascii_bytes.decode("ascii").rstrip(".")  # remove padding dots
    num4 = int.from_bytes(num4_bytes, "big")
    num1 = int.from_bytes(num1_bytes, "big")
    num2 = int.from_bytes(num2_bytes, "big")
    checksum = to_hex(checksum_bytes)

    return {
        "ascii_str": ascii_str,
        "num4": num4,
        "num1": num1,
        "num2": num2,
        "checksum": checksum
    }

# Example usage:
packed_address = "0x73796e6469636174652e000000010000008e2647"
unpacked = unpack_eth_address(packed_address)
print(unpacked)

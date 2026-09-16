"""Data encoding functionality for QR-generator."""

from qr_generator import version_info

BYTE_MODE = "0100"
TERMINATOR = "0000"
_PAD_BYTES = ("11101100", "00010001")  # 0xEC, 0x11


def encode(data: str) -> str:
    """Encode text data into a QR Code byte-mode bitstream.

    This implements the first stage of QR Code data encoding:
    byte mode, character count, and raw data bits.

    Error correction, terminator bits, and padding
    will be implemented in later versions.
    """
    if not isinstance(data, str):
        raise TypeError("data must be a string")

    encoded = data.encode("utf-8")
    character_count = len(encoded)

    count_bits = format(character_count, "08b")
    data_bits = "".join(format(byte, "08b") for byte in encoded)

    return BYTE_MODE + count_bits + data_bits


def encode_and_pad(data: str, version: int, level: str) -> str:
    """Encode data and pad it to the exact capacity of a version/level.

    Adds the terminator, pads to a byte boundary, and repeats the
    standard 0xEC/0x11 pad codewords until the bitstream exactly
    fills the data capacity for the given version and error
    correction level.
    """
    bits = encode(data)
    capacity_bits = version_info.total_data_codewords(version, level) * 8

    if len(bits) > capacity_bits:
        raise ValueError(
            f"Data does not fit in version {version} "
            f"(error correction level {level})"
        )

    bits += TERMINATOR[:max(0, min(4, capacity_bits - len(bits)))]

    if len(bits) % 8 != 0:
        bits += "0" * (8 - len(bits) % 8)

    pad_index = 0
    while len(bits) < capacity_bits:
        bits += _PAD_BYTES[pad_index % 2]
        pad_index += 1

    return bits
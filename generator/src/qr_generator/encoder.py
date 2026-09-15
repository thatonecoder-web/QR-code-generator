"""Data encoding functionality for QR-generator."""

BYTE_MODE = "0100"


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
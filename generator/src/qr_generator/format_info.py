"""QR format information: encoding and placement."""

from qr_generator.matrix import QRMatrix
from qr_generator import version_info
from qr_generator.mask import MASK_COUNT

# Generator polynomial for the (15,5) BCH code used by format
# information, and the fixed mask XORed into the result so that the
# all-zero data word never produces an all-light format strip.
_GENERATOR_POLYNOMIAL = 0b10100110111
_FORMAT_MASK = 0b101010000010010
_DATA_BITS = 5
_TOTAL_BITS = 15


def encode_format_information(level: str, mask_id: int) -> str:
    """Return the 15-bit error-corrected format information string.

    Combines the error-correction level and mask pattern into a
    5-bit value, protects it with a (15,5) BCH code, and applies the
    fixed format mask, per the QR Code specification.
    """
    if level not in version_info.ERROR_CORRECTION_LEVELS:
        raise ValueError(
            f"level must be one of {version_info.ERROR_CORRECTION_LEVELS}"
        )

    from qr_generator.mask import MASK_COUNT

    if not 0 <= mask_id < MASK_COUNT:
        raise ValueError(f"mask_id must be between 0 and {MASK_COUNT - 1}")

    data = (version_info.ERROR_CORRECTION_BITS[level] << 3) | mask_id
    ec_bit_count = _TOTAL_BITS - _DATA_BITS

    # Polynomial long division (in GF(2)) of (data << 10) by the
    # generator polynomial, keeping only the remainder.
    value = data << ec_bit_count
    for bit in range(_TOTAL_BITS - 1, ec_bit_count - 1, -1):
        if value & (1 << bit):
            value ^= _GENERATOR_POLYNOMIAL << (bit - ec_bit_count)

    codeword = (data << ec_bit_count) | value
    codeword ^= _FORMAT_MASK

    return format(codeword, f"0{_TOTAL_BITS}b")


def add_format_information(
    matrix: QRMatrix,
    level: str,
    mask_id: int,
) -> None:
    """Write both copies of the format information into a matrix."""
    bits = encode_format_information(level, mask_id)
    # bit 0 is the most-significant bit of the encoded string.
    values = [bit == "1" for bit in bits]

    for i in range(6):
        matrix.set_reserved(8, i, values[i])
    matrix.set_reserved(8, 7, values[6])
    matrix.set_reserved(8, 8, values[7])
    matrix.set_reserved(7, 8, values[8])
    for i in range(9, 15):
        matrix.set_reserved(14 - i, 8, values[i])

    for i in range(8):
        matrix.set_reserved(matrix.size - 1 - i, 8, values[i])
    for i in range(8, 15):
        matrix.set_reserved(8, matrix.size - 15 + i, values[i])


def read_format_information(matrix: QRMatrix) -> str:
    """Read the first copy of format information bits from a matrix.

    Used for verification/round-tripping; assumes an undamaged
    symbol, so no error correction is performed on the read bits.
    """
    bits = []

    for i in range(6):
        bits.append(matrix.get(8, i))
    bits.append(matrix.get(8, 7))
    bits.append(matrix.get(8, 8))
    bits.append(matrix.get(7, 8))
    for i in range(9, 15):
        bits.append(matrix.get(14 - i, 8))

    return "".join("1" if bit else "0" for bit in bits)

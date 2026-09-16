import pytest

from qr_generator.matrix import QRMatrix
from qr_generator.patterns import add_patterns
from qr_generator.format_info import (
    encode_format_information,
    add_format_information,
    read_format_information,
)


def test_encode_format_information_length():
    bits = encode_format_information("M", 0)

    assert len(bits) == 15
    assert set(bits) <= {"0", "1"}


def test_encode_format_information_known_value():
    # A well-known reference value: error correction level M with
    # mask pattern 0 produces an all-zero data word, so the final
    # format string is exactly the fixed XOR mask itself.
    assert encode_format_information("M", 0) == "101010000010010"


def test_encode_format_information_changes_with_mask():
    first = encode_format_information("M", 0)
    second = encode_format_information("M", 1)

    assert first != second


def test_encode_format_information_changes_with_level():
    first = encode_format_information("L", 0)
    second = encode_format_information("M", 0)

    assert first != second


def test_encode_format_information_is_deterministic():
    first = encode_format_information("Q", 5)
    second = encode_format_information("Q", 5)

    assert first == second


def test_encode_format_information_is_a_valid_bch_codeword():
    # The codeword (before the fixed XOR mask is applied) must be an
    # exact multiple of the format-information generator polynomial.
    generator = 0b10100110111
    mask = 0b101010000010010

    for level in ("L", "M", "Q", "H"):
        for mask_id in range(8):
            bits = encode_format_information(level, mask_id)
            codeword = int(bits, 2) ^ mask

            value = codeword
            for bit in range(14, 9, -1):
                if value & (1 << bit):
                    value ^= generator << (bit - 10)

            assert value == 0


def test_encode_format_information_rejects_invalid_level():
    with pytest.raises(ValueError):
        encode_format_information("Z", 0)


def test_encode_format_information_rejects_invalid_mask():
    with pytest.raises(ValueError):
        encode_format_information("M", 8)


def test_add_format_information_writes_both_copies_consistently():
    matrix = QRMatrix(21)
    add_patterns(matrix, 1)

    add_format_information(matrix, "Q", 3)

    bits = encode_format_information("Q", 3)
    values = [bit == "1" for bit in bits]

    # Second copy, first 8 bits (bottom-left column near top-left finder).
    for i in range(8):
        assert matrix.get(matrix.size - 1 - i, 8) == values[i]

    # Second copy, remaining bits (top-right row).
    for i in range(8, 15):
        assert matrix.get(8, matrix.size - 15 + i) == values[i]


def test_read_format_information_round_trips():
    matrix = QRMatrix(21)
    add_patterns(matrix, 1)

    add_format_information(matrix, "H", 6)

    assert read_format_information(matrix) == encode_format_information("H", 6)

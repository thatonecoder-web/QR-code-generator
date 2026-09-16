import pytest

from qr_generator.encoder import encode, encode_and_pad
from qr_generator import version_info


def test_encode_text():
    result = encode("Hello")

    assert isinstance(result, str)
    assert result == (
        "0100"
        "00000101"
        "01001000"
        "01100101"
        "01101100"
        "01101100"
        "01101111"
    )


def test_encode_single_character():
    result = encode("A")

    assert result == "01000000000101000001"


def test_encode_empty_string():
    assert encode("") == "010000000000"


def test_encode_rejects_non_string():
    with pytest.raises(TypeError):
        encode(123)

def test_encode_and_pad_fills_exact_capacity():
    bits = encode_and_pad("HI", 1, "L")

    assert len(bits) == version_info.total_data_codewords(1, "L") * 8


def test_encode_and_pad_includes_terminator_and_padding():
    bits = encode_and_pad("A", 1, "L")

    # Mode (4) + count (8) + "A" (8) = 20 bits, then terminator/padding.
    assert bits.startswith("0100" + "00000001" + "01000001")
    assert bits.endswith("00010001" + "11101100" + "00010001")


def test_encode_and_pad_rejects_data_too_large():
    too_long = "x" * (version_info.max_byte_capacity(1, "H") + 1)

    with pytest.raises(ValueError):
        encode_and_pad(too_long, 1, "H")


def test_encode_and_pad_exact_fit_has_no_padding_bytes():
    capacity = version_info.max_byte_capacity(1, "L")
    data = "x" * capacity

    bits = encode_and_pad(data, 1, "L")

    assert len(bits) == version_info.total_data_codewords(1, "L") * 8

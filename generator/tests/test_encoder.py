from qr_generator.encoder import encode


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
    try:
        encode(123)
    except TypeError:
        pass
    else:
        raise AssertionError("encode() should reject non-string input")

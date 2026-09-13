from qr_generator.encoder import encode


def test_encode_text():
    result = encode("Hello")
    assert isinstance(result, bytes)
    assert result == b"Hello"


def test_encode_empty_string():
    assert encode("") == b""


def test_encode_rejects_non_string():
    try:
        encode(123)
    except TypeError:
        pass
    else:
        raise AssertionError("encode() should reject non-string input")

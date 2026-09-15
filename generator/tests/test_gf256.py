import pytest

from qr_generator.gf256 import (
    add,
    subtract,
    multiply,
    divide,
    power,
    inverse,
)


def test_add_uses_xor():
    assert add(0x57, 0x83) == 0xD4


def test_subtract_uses_xor():
    assert subtract(0x57, 0x83) == 0xD4


def test_add_zero():
    assert add(0, 42) == 42
    assert add(42, 0) == 42


def test_subtract_zero():
    assert subtract(0, 42) == 42
    assert subtract(42, 0) == 42


def test_multiply_by_zero():
    assert multiply(0, 123) == 0
    assert multiply(123, 0) == 0


def test_multiply_by_one():
    assert multiply(1, 123) == 123
    assert multiply(123, 1) == 123


def test_multiplication_is_commutative():
    assert multiply(0x53, 0xCA) == multiply(0xCA, 0x53)


def test_divide_by_one():
    assert divide(123, 1) == 123


def test_zero_divided_by_nonzero():
    assert divide(0, 123) == 0


def test_division_reverses_multiplication():
    value = multiply(0x53, 0xCA)

    assert divide(value, 0xCA) == 0x53


def test_power_zero_exponent():
    assert power(123, 0) == 1


def test_power_one_exponent():
    assert power(123, 1) == 123


def test_power_of_zero():
    assert power(0, 5) == 0


def test_inverse():
    value = 0x53
    inverse_value = inverse(value)

    assert multiply(value, inverse_value) == 1


def test_inverse_of_one():
    assert inverse(1) == 1


def test_negative_power_matches_inverse():
    value = 0x53

    assert power(value, -1) == inverse(value)


def test_division_by_zero_rejected():
    with pytest.raises(ZeroDivisionError):
        divide(123, 0)


def test_inverse_of_zero_rejected():
    with pytest.raises(ZeroDivisionError):
        inverse(0)


def test_invalid_element_type_rejected():
    with pytest.raises(TypeError):
        multiply("1", 2)


def test_negative_element_rejected():
    with pytest.raises(ValueError):
        multiply(-1, 2)


def test_element_above_255_rejected():
    with pytest.raises(ValueError):
        multiply(256, 2)
import pytest

from qr_generator.error_correction import (
    generate_generator_polynomial,
    generate_error_correction,
)


def test_generator_polynomial_has_correct_degree():
    polynomial = generate_generator_polynomial(7)

    assert len(polynomial) == 8


def test_generator_polynomial_starts_with_one():
    polynomial = generate_generator_polynomial(7)

    assert polynomial[0] == 1


def test_generator_polynomial_for_seven_error_codewords():
    polynomial = generate_generator_polynomial(7)

    assert polynomial == [
        1,
        127,
        122,
        154,
        164,
        11,
        68,
        117,
    ]


def test_generator_polynomial_rejects_zero():
    with pytest.raises(ValueError):
        generate_generator_polynomial(0)


def test_generator_polynomial_rejects_negative():
    with pytest.raises(ValueError):
        generate_generator_polynomial(-1)


def test_error_correction_returns_requested_number_of_codewords():
    data = [32, 65, 0, 236, 17]

    result = generate_error_correction(data, 7)

    assert len(result) == 7


def test_error_correction_returns_gf256_values():
    data = [32, 65, 0, 236, 17]

    result = generate_error_correction(data, 7)

    assert all(0 <= value <= 255 for value in result)


def test_error_correction_returns_integers():
    data = [32, 65, 0, 236, 17]

    result = generate_error_correction(data, 7)

    assert all(isinstance(value, int) for value in result)


def test_error_correction_is_deterministic():
    data = [32, 65, 0, 236, 17]

    first = generate_error_correction(data, 7)
    second = generate_error_correction(data, 7)

    assert first == second


def test_error_correction_changes_when_data_changes():
    first_data = [32, 65, 0, 236, 17]
    second_data = [32, 65, 0, 236, 18]

    first = generate_error_correction(first_data, 7)
    second = generate_error_correction(second_data, 7)

    assert first != second


def test_error_correction_rejects_zero():
    with pytest.raises(ValueError):
        generate_error_correction([1, 2, 3], 0)


def test_error_correction_rejects_negative():
    with pytest.raises(ValueError):
        generate_error_correction([1, 2, 3], -1)
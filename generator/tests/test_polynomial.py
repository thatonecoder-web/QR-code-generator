import pytest

from qr_generator.polynomial import (
    add_polynomials,
    multiply_polynomials,
    evaluate_polynomial,
)


def test_add_polynomials():
    first = [1, 2, 3]
    second = [1, 1]

    assert add_polynomials(first, second) == [1, 3, 2]


def test_add_polynomials_same_length():
    first = [1, 2, 3]
    second = [4, 5, 6]

    assert add_polynomials(first, second) == [
        1 ^ 4,
        2 ^ 5,
        3 ^ 6,
    ]


def test_add_polynomial_with_zero():
    first = [1, 2, 3]

    assert add_polynomials(first, [0, 0, 0]) == first


def test_multiply_polynomials():
    first = [1, 1]
    second = [1, 1]

    assert multiply_polynomials(first, second) == [1, 0, 1]


def test_multiply_polynomial_by_constant():
    first = [1, 2, 3]
    second = [5]

    assert multiply_polynomials(first, second) == [5, 10, 15]


def test_multiply_polynomial_by_zero():
    first = [1, 2, 3]

    assert multiply_polynomials(first, [0]) == [0, 0, 0]


def test_evaluate_polynomial_at_zero():
    polynomial = [1, 2, 3]

    assert evaluate_polynomial(polynomial, 0) == 3


def test_evaluate_polynomial_at_one():
    polynomial = [1, 2, 3]

    assert evaluate_polynomial(polynomial, 1) == 0


def test_evaluate_constant_polynomial():
    polynomial = [42]

    assert evaluate_polynomial(polynomial, 100) == 42


def test_evaluate_polynomial_in_gf256():
    polynomial = [1, 0, 1]

    # x² + 1 evaluated at x = 2.
    # 2² = 4, then 4 XOR 1 = 5.
    assert evaluate_polynomial(polynomial, 2) == 5


def test_empty_polynomial_multiplication_rejected():
    with pytest.raises(ValueError):
        multiply_polynomials([], [1])


def test_empty_polynomial_evaluation_rejected():
    with pytest.raises(ValueError):
        evaluate_polynomial([], 1)
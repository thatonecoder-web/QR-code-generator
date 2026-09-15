"""Polynomial arithmetic for QR-generator."""

from qr_generator.gf256 import add, multiply


def add_polynomials(
    first: list[int],
    second: list[int],
) -> list[int]:
    """Add two polynomials over GF(256)."""
    length = max(len(first), len(second))

    first = [0] * (length - len(first)) + first
    second = [0] * (length - len(second)) + second

    return [
        add(a, b)
        for a, b in zip(first, second)
    ]


def multiply_polynomials(
    first: list[int],
    second: list[int],
) -> list[int]:
    """Multiply two polynomials over GF(256)."""
    if not first or not second:
        raise ValueError("Polynomials must not be empty")

    result = [0] * (len(first) + len(second) - 1)

    for first_index, first_value in enumerate(first):
        for second_index, second_value in enumerate(second):
            result[first_index + second_index] ^= multiply(
                first_value,
                second_value,
            )

    return result


def evaluate_polynomial(
    polynomial: list[int],
    value: int,
) -> int:
    """Evaluate a polynomial at a GF(256) value."""
    if not polynomial:
        raise ValueError("Polynomial must not be empty")

    result = 0

    for coefficient in polynomial:
        result = multiply(result, value)
        result ^= coefficient

    return result
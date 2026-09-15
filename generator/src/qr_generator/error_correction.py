"""Reed-Solomon error correction for QR-generator."""

from qr_generator.gf256 import GENERATOR, multiply, power
from qr_generator.polynomial import multiply_polynomials


def generate_generator_polynomial(error_codewords: int) -> list[int]:
    """Generate a Reed-Solomon generator polynomial.

    Args:
        error_codewords: Number of error-correction codewords required.

    Returns:
        The generator polynomial coefficients.
    """
    if error_codewords <= 0:
        raise ValueError("error_codewords must be positive")

    polynomial = [1]

    for exponent in range(error_codewords):
        polynomial = multiply_polynomials(
            polynomial,
            [1, power(GENERATOR, exponent)],
        )

    return polynomial


def generate_error_correction(
    data_codewords: list[int],
    error_codewords: int,
) -> list[int]:
    """Generate Reed-Solomon error-correction codewords.

    Args:
        data_codewords: Data codewords to protect.
        error_codewords: Number of error-correction codewords.

    Returns:
        A list containing the generated error-correction codewords.
    """
    if not data_codewords:
        raise ValueError("data_codewords must not be empty")

    if error_codewords <= 0:
        raise ValueError("error_codewords must be positive")

    if any(not 0 <= codeword <= 255 for codeword in data_codewords):
        raise ValueError("data_codewords must contain values from 0 to 255")

    generator = generate_generator_polynomial(error_codewords)

    message = data_codewords + [0] * error_codewords

    for index in range(len(data_codewords)):
        coefficient = message[index]

        if coefficient == 0:
            continue

        for generator_index, generator_value in enumerate(generator):
            message[index + generator_index] ^= multiply(
                generator_value,
                coefficient,
            )

    return message[-error_codewords:]
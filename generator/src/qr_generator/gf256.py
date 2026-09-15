"""Galois Field GF(256) arithmetic for QR-generator."""

PRIMITIVE_POLYNOMIAL = 0x11D
FIELD_SIZE = 256
GENERATOR = 2


def _build_exp_table() -> list[int]:
    """Build the GF(256) exponentiation table."""
    table = [0] * 512
    value = 1

    for index in range(255):
        table[index] = value
        value <<= 1

        if value & 0x100:
            value ^= PRIMITIVE_POLYNOMIAL

    for index in range(255, 512):
        table[index] = table[index - 255]

    return table


def _build_log_table(exp_table: list[int]) -> list[int]:
    """Build the GF(256) logarithm table."""
    table = [0] * FIELD_SIZE

    for index in range(255):
        table[exp_table[index]] = index

    return table


EXP_TABLE = _build_exp_table()
LOG_TABLE = _build_log_table(EXP_TABLE)


def add(a: int, b: int) -> int:
    """Add two GF(256) elements."""
    _validate_element(a)
    _validate_element(b)

    return a ^ b


def subtract(a: int, b: int) -> int:
    """Subtract two GF(256) elements."""
    _validate_element(a)
    _validate_element(b)

    return a ^ b


def multiply(a: int, b: int) -> int:
    """Multiply two GF(256) elements."""
    _validate_element(a)
    _validate_element(b)

    if a == 0 or b == 0:
        return 0

    log_a = LOG_TABLE[a]
    log_b = LOG_TABLE[b]

    return EXP_TABLE[log_a + log_b]


def divide(a: int, b: int) -> int:
    """Divide one GF(256) element by another."""
    _validate_element(a)
    _validate_element(b)

    if b == 0:
        raise ZeroDivisionError("cannot divide by zero in GF(256)")

    if a == 0:
        return 0

    log_a = LOG_TABLE[a]
    log_b = LOG_TABLE[b]

    exponent = (log_a - log_b) % 255

    return EXP_TABLE[exponent]


def power(a: int, exponent: int) -> int:
    """Raise a GF(256) element to an integer power."""
    _validate_element(a)

    if exponent < 0:
        if a == 0:
            raise ZeroDivisionError("zero cannot be raised to a negative power")

        return power(inverse(a), -exponent)

    if exponent == 0:
        return 1

    if a == 0:
        return 0

    log_a = LOG_TABLE[a]
    result_exponent = (log_a * exponent) % 255

    return EXP_TABLE[result_exponent]


def inverse(a: int) -> int:
    """Return the multiplicative inverse of a GF(256) element."""
    _validate_element(a)

    if a == 0:
        raise ZeroDivisionError("zero has no multiplicative inverse")

    log_a = LOG_TABLE[a]

    return EXP_TABLE[(255 - log_a) % 255]


def _validate_element(value: int) -> None:
    """Validate that a value is a valid GF(256) element."""
    if not isinstance(value, int):
        raise TypeError("GF(256) elements must be integers")

    if not 0 <= value < FIELD_SIZE:
        raise ValueError("GF(256) elements must be between 0 and 255")
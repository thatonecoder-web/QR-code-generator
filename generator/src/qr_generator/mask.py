"""The 8 QR Code data-masking patterns, penalty scoring, and selection."""

from qr_generator.matrix import QRMatrix

_MASK_FUNCTIONS = [
    lambda row, col: (row + col) % 2 == 0,
    lambda row, col: row % 2 == 0,
    lambda row, col: col % 3 == 0,
    lambda row, col: (row + col) % 3 == 0,
    lambda row, col: (row // 2 + col // 3) % 2 == 0,
    lambda row, col: (row * col) % 2 + (row * col) % 3 == 0,
    lambda row, col: ((row * col) % 2 + (row * col) % 3) % 2 == 0,
    lambda row, col: ((row + col) % 2 + (row * col) % 3) % 2 == 0,
]

MASK_COUNT = len(_MASK_FUNCTIONS)


def apply_mask(matrix: QRMatrix, mask_id: int) -> QRMatrix:
    """Return a new matrix with the given mask pattern XORed into it.

    Reserved modules (function patterns, format information, the dark
    module) are left untouched, matching the QR Code specification.
    """
    if not 0 <= mask_id < MASK_COUNT:
        raise ValueError(f"mask_id must be between 0 and {MASK_COUNT - 1}")

    mask_function = _MASK_FUNCTIONS[mask_id]
    masked = QRMatrix(matrix.size)

    for row in range(matrix.size):
        for col in range(matrix.size):
            value = matrix.get(row, col)

            if matrix.is_reserved(row, col):
                masked.set_reserved(row, col, value)
                continue

            if mask_function(row, col):
                value = not value

            masked.set(row, col, value)

    return masked


def calculate_penalty(matrix: QRMatrix) -> int:
    """Return the total QR Code penalty score for a masked matrix."""
    return (
        _penalty_consecutive_modules(matrix)
        + _penalty_blocks(matrix)
        + _penalty_patterns(matrix)
        + _penalty_dark_module_ratio(matrix)
    )


def select_best_mask(matrix: QRMatrix) -> tuple[int, QRMatrix]:
    """Try every mask and return the id and matrix with lowest penalty."""
    best_mask_id = None
    best_matrix = None
    best_penalty = None

    for mask_id in range(MASK_COUNT):
        candidate = apply_mask(matrix, mask_id)
        penalty = calculate_penalty(candidate)

        if best_penalty is None or penalty < best_penalty:
            best_mask_id = mask_id
            best_matrix = candidate
            best_penalty = penalty

    return best_mask_id, best_matrix


def _penalty_consecutive_modules(matrix: QRMatrix) -> int:
    penalty = 0

    for row in range(matrix.size):
        values = [matrix.get(row, col) for col in range(matrix.size)]
        penalty += _run_penalty(values)

    for col in range(matrix.size):
        values = [matrix.get(row, col) for row in range(matrix.size)]
        penalty += _run_penalty(values)

    return penalty


def _run_penalty(values: list) -> int:
    penalty = 0
    run_value = values[0]
    run_length = 1

    for value in values[1:]:
        if value == run_value:
            run_length += 1
            continue

        if run_length >= 5:
            penalty += 3 + (run_length - 5)

        run_value = value
        run_length = 1

    if run_length >= 5:
        penalty += 3 + (run_length - 5)

    return penalty


def _penalty_blocks(matrix: QRMatrix) -> int:
    penalty = 0

    for row in range(matrix.size - 1):
        for col in range(matrix.size - 1):
            corners = (
                matrix.get(row, col),
                matrix.get(row, col + 1),
                matrix.get(row + 1, col),
                matrix.get(row + 1, col + 1),
            )

            if len(set(corners)) == 1:
                penalty += 3

    return penalty


# A dark-light-dark-dark-dark-light-dark run flanked by 4 light
# modules on either side (only the flanking side that exists needs to
# match) resembles a finder pattern and is penalized.
_FINDER_LIKE_PATTERN = (
    True, False, True, True, True, False, True,
)
_LIGHT_RUN = (False, False, False, False)


def _penalty_patterns(matrix: QRMatrix) -> int:
    penalty = 0

    for row in range(matrix.size):
        values = tuple(matrix.get(row, col) for col in range(matrix.size))
        penalty += _pattern_penalty_in_line(values)

    for col in range(matrix.size):
        values = tuple(matrix.get(row, col) for row in range(matrix.size))
        penalty += _pattern_penalty_in_line(values)

    return penalty


def _pattern_penalty_in_line(values: tuple) -> int:
    penalty = 0
    pattern_length = len(_FINDER_LIKE_PATTERN)
    light_run_length = len(_LIGHT_RUN)

    for start in range(len(values) - pattern_length + 1):
        window = values[start:start + pattern_length]

        if window != _FINDER_LIKE_PATTERN:
            continue

        before = values[max(0, start - light_run_length):start]
        after = values[start + pattern_length:
                        start + pattern_length + light_run_length]

        before_is_light = (
            len(before) == light_run_length and all(v is False for v in before)
        )
        after_is_light = (
            len(after) == light_run_length and all(v is False for v in after)
        )

        if before_is_light or after_is_light:
            penalty += 40

    return penalty


def _penalty_dark_module_ratio(matrix: QRMatrix) -> int:
    total_modules = matrix.size * matrix.size
    dark_modules = sum(
        1
        for row in range(matrix.size)
        for col in range(matrix.size)
        if matrix.get(row, col)
    )

    percent_dark = (dark_modules * 100) / total_modules
    deviation = abs(percent_dark - 50)

    return int(deviation // 5) * 10

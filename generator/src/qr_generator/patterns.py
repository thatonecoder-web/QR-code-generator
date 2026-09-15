"""QR structural pattern construction functionality."""

from qr_generator.matrix import QRMatrix


VERSION_1_SIZE = 21
FINDER_SIZE = 7


def add_patterns(matrix: QRMatrix) -> None:
    """Add Version 1 QR structural patterns to a matrix.

    Adds the three finder patterns, their separators,
    and the horizontal and vertical timing patterns.
    """
    if matrix.size != VERSION_1_SIZE:
        raise ValueError("Version 1 QR codes require a 21x21 matrix")

    _add_finder_pattern(matrix, 0, 0)
    _add_finder_pattern(matrix, 0, matrix.size - FINDER_SIZE)
    _add_finder_pattern(matrix, matrix.size - FINDER_SIZE, 0)

    _add_finder_separator(matrix, 0, 0)
    _add_finder_separator(matrix, 0, matrix.size - FINDER_SIZE)
    _add_finder_separator(matrix, matrix.size - FINDER_SIZE, 0)

    _add_timing_patterns(matrix)


def _add_finder_pattern(
    matrix: QRMatrix,
    start_row: int,
    start_column: int,
) -> None:
    """Add a 7x7 finder pattern and reserve its modules."""
    for row in range(FINDER_SIZE):
        for column in range(FINDER_SIZE):
            is_dark = (
                row in (0, FINDER_SIZE - 1)
                or column in (0, FINDER_SIZE - 1)
                or (
                    row in (1, FINDER_SIZE - 2)
                    and column in (1, FINDER_SIZE - 2)
                )
                or (
                    2 <= row <= 4
                    and 2 <= column <= 4
                )
            )

            if row in (1, FINDER_SIZE - 2) and column in (2, 3, 4):
                is_dark = False
            if column in (1, FINDER_SIZE - 2) and row in (2, 3, 4):
                is_dark = False

            matrix.set_reserved(
                start_row + row,
                start_column + column,
                is_dark,
            )


def _add_finder_separator(
    matrix: QRMatrix,
    start_row: int,
    start_column: int,
) -> None:
    """Add the white separator surrounding a finder pattern."""
    for row in range(-1, FINDER_SIZE + 1):
        for column in range(-1, FINDER_SIZE + 1):
            if 0 <= start_row + row < matrix.size and \
                    0 <= start_column + column < matrix.size:

                if (
                    row in (-1, FINDER_SIZE)
                    or column in (-1, FINDER_SIZE)
                ):
                    matrix.set_reserved(
                        start_row + row,
                        start_column + column,
                        False,
                    )


def _add_timing_patterns(matrix: QRMatrix) -> None:
    """Add the horizontal and vertical timing patterns."""
    for column in range(8, matrix.size - 8):
        value = column % 2 == 0

        if not matrix.is_reserved(6, column):
            matrix.set_reserved(6, column, value)

    for row in range(8, matrix.size - 8):
        value = row % 2 == 0

        if not matrix.is_reserved(row, 6):
            matrix.set_reserved(row, 6, value)
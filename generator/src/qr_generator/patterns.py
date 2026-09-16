"""QR structural pattern construction functionality."""

from qr_generator.matrix import QRMatrix
from qr_generator import version_info


VERSION_1_SIZE = 21
FINDER_SIZE = 7
ALIGNMENT_SIZE = 5


def add_patterns(matrix: QRMatrix, version: int = 1) -> None:
    """Add QR structural patterns to a matrix for the given version.

    Adds the three finder patterns and their separators, the
    horizontal and vertical timing patterns, any alignment patterns,
    a placeholder for the format information areas, and the single
    always-dark module. Defaults to Version 1 for backward
    compatibility.
    """
    expected_size = version_info.matrix_size(version)

    if matrix.size != expected_size:
        raise ValueError(
            f"Version {version} QR codes require a "
            f"{expected_size}x{expected_size} matrix"
        )

    _add_finder_pattern(matrix, 0, 0)
    _add_finder_pattern(matrix, 0, matrix.size - FINDER_SIZE)
    _add_finder_pattern(matrix, matrix.size - FINDER_SIZE, 0)

    _add_finder_separator(matrix, 0, 0)
    _add_finder_separator(matrix, 0, matrix.size - FINDER_SIZE)
    _add_finder_separator(matrix, matrix.size - FINDER_SIZE, 0)

    _add_timing_patterns(matrix)

    for center_row, center_column in version_info.alignment_centers(version):
        _add_alignment_pattern(matrix, center_row, center_column)

    _reserve_format_information_areas(matrix)

    # The dark module: always dark, position fixed relative to version.
    matrix.set_reserved(4 * version + 9, 8, True)


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


def _add_alignment_pattern(
    matrix: QRMatrix,
    center_row: int,
    center_column: int,
) -> None:
    """Add a 5x5 alignment pattern centered on the given position."""
    offset = ALIGNMENT_SIZE // 2

    for delta_row in range(-offset, offset + 1):
        for delta_column in range(-offset, offset + 1):
            is_dark = (
                abs(delta_row) == offset
                or abs(delta_column) == offset
                or (delta_row == 0 and delta_column == 0)
            )

            matrix.set_reserved(
                center_row + delta_row,
                center_column + delta_column,
                is_dark,
            )


def _reserve_format_information_areas(matrix: QRMatrix) -> None:
    """Reserve the two format-information strips with placeholders.

    The real bits are written later by
    ``format_info.add_format_information`` once the chosen mask
    pattern and error-correction level are known. Reserving them now
    (with an arbitrary placeholder value) keeps data placement from
    using these modules.
    """
    for column in range(9):
        if not matrix.is_reserved(8, column):
            matrix.set_reserved(8, column, False)

    for row in range(8):
        if not matrix.is_reserved(row, 8):
            matrix.set_reserved(row, 8, False)

    for offset in range(8):
        row = matrix.size - 1 - offset
        if not matrix.is_reserved(row, 8):
            matrix.set_reserved(row, 8, False)

    for offset in range(8):
        column = matrix.size - 8 + offset
        if not matrix.is_reserved(8, column):
            matrix.set_reserved(8, column, False)


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
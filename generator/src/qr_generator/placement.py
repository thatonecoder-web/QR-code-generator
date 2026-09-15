"""QR data placement functionality."""

from qr_generator.matrix import QRMatrix


def place_data(matrix: QRMatrix, bits: str) -> None:
    """Place a bitstream into the available QR matrix modules.

    Data is placed using the standard QR Code zig-zag traversal,
    starting from the bottom-right corner and moving through
    two-column strips.

    Reserved modules are skipped.
    """
    if any(bit not in "01" for bit in bits):
        raise ValueError("bits must contain only '0' and '1'")

    bit_index = 0
    upward = True

    column = matrix.size - 1

    while column > 0:
        # Column 6 is reserved for the vertical timing pattern.
        if column == 6:
            column -= 1

        rows = range(
            matrix.size - 1,
            -1,
            -1,
        ) if upward else range(matrix.size)

        for row in rows:
            for current_column in (column, column - 1):
                if matrix.is_reserved(row, current_column):
                    continue

                if bit_index >= len(bits):
                    return

                matrix.set(
                    row,
                    current_column,
                    bits[bit_index] == "1",
                )

                bit_index += 1

        upward = not upward
        column -= 2

    if bit_index < len(bits):
        raise ValueError("Bitstream is too large for the QR matrix")
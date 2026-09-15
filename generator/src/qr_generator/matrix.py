"""QR matrix construction functionality."""

from typing import Optional


class QRMatrix:
    """Represent a QR code matrix."""

    def __init__(self, size: int = 21) -> None:
        if size <= 0:
            raise ValueError("Matrix size must be positive")

        self.size = size
        self._grid: list[list[Optional[bool]]] = [
            [None for _ in range(size)]
            for _ in range(size)
        ]
        self._reserved: list[list[bool]] = [
            [False for _ in range(size)]
            for _ in range(size)
        ]

    def get(self, row: int, column: int) -> Optional[bool]:
        """Return the value at a matrix position."""
        self._validate_position(row, column)

        return self._grid[row][column]

    def set(
        self,
        row: int,
        column: int,
        value: Optional[bool],
    ) -> None:
        """Set the value at a matrix position."""
        self._validate_position(row, column)

        self._grid[row][column] = value

    def is_reserved(self, row: int, column: int) -> bool:
        """Return whether a matrix position is reserved."""
        self._validate_position(row, column)

        return self._reserved[row][column]

    def reserve(self, row: int, column: int) -> None:
        """Reserve a matrix position for structural QR data."""
        self._validate_position(row, column)

        self._reserved[row][column] = True

    def set_reserved(
        self,
        row: int,
        column: int,
        value: bool,
    ) -> None:
        """Set and reserve a matrix position."""
        self._validate_position(row, column)

        self._reserved[row][column] = True
        self._grid[row][column] = value

    def to_list(self) -> list[list[Optional[bool]]]:
        """Return the matrix as a list of rows."""
        return [row.copy() for row in self._grid]

    def __str__(self) -> str:
        """Return a printable representation of the matrix."""
        rows = []

        for row in self._grid:
            rows.append(
                "".join(
                    "  " if value is None else
                    "██" if value else
                    "  "
                    for value in row
                )
            )

        return "\n".join(rows)

    def _validate_position(self, row: int, column: int) -> None:
        """Validate that a matrix position is within bounds."""
        if not 0 <= row < self.size:
            raise IndexError("Row index out of range")

        if not 0 <= column < self.size:
            raise IndexError("Column index out of range")
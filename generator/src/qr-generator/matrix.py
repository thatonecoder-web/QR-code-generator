"""QR matrix construction functionality."""

class QRMatrix:
"""Represent a QR code matrix."""

```
def __init__(self, size: int = 21) -> None:
    if size <= 0:
        raise ValueError("Matrix size must be positive")

    self.size = size
    self._grid = [[None for _ in range(size)] for _ in range(size)]

def get(self, row: int, column: int):
    """Return the value at a matrix position."""
    return self._grid[row][column]

def set(self, row: int, column: int, value) -> None:
    """Set the value at a matrix position."""
    self._grid[row][column] = value

def to_list(self) -> list[list]:
    """Return the matrix as a list of rows."""
    return [row.copy() for row in self._grid]
```

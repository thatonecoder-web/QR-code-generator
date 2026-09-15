from qr_generator.encoder import encode
from qr_generator.matrix import QRMatrix
from qr_generator.patterns import add_patterns
from qr_generator.placement import place_data


def bits_to_codewords(bits: str) -> list[int]:
    """Convert a bitstream into 8-bit codewords."""
    if len(bits) % 8 != 0:
        raise ValueError("Bitstream length must be a multiple of 8")

    return [
        int(bits[index:index + 8], 2)
        for index in range(0, len(bits), 8)
    ]


def codewords_to_bits(codewords: list[int]) -> str:
    """Convert codewords into an 8-bit-per-codeword bitstream."""
    return "".join(
        format(codeword, "08b")
        for codeword in codewords
    )


def main() -> None:
    data = "Hello, QR-generator!"

    encoded = encode(data)
    data_codewords = bits_to_codewords(encoded)

    matrix = QRMatrix()

    add_patterns(matrix)
    place_data(matrix, encoded)

    print(f"Input: {data}")
    print(f"Encoded bitstream: {encoded}")
    print(f"Bit length: {len(encoded)}")
    print(f"Data codewords: {data_codewords}")
    print(f"Data codeword count: {len(data_codewords)}")
    print(f"Matrix size: {matrix.size}x{matrix.size}")
    print()
    print("QR Matrix:")
    print(matrix)


if __name__ == "__main__":
    main()
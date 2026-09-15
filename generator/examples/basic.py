from qr_generator.encoder import encode
from qr_generator.matrix import QRMatrix
from qr_generator.patterns import add_patterns
from qr_generator.placement import place_data


def main() -> None:
    data = "Hello, QR-generator!"

    encoded = encode(data)
    matrix = QRMatrix()

    add_patterns(matrix)
    place_data(matrix, encoded)

    print(f"Input: {data}")
    print(f"Encoded bitstream: {encoded}")
    print(f"Bit length: {len(encoded)}")
    print(f"Matrix size: {matrix.size}x{matrix.size}")
    print()
    print("QR Matrix:")
    print(matrix)


if __name__ == "__main__":
    main()
from qr_generator.encoder import encode
from qr_generator.matrix import QRMatrix


def main() -> None:
    data = "Hello, QR-generator!"

    encoded = encode(data)
    matrix = QRMatrix()

    print(f"Input: {data}")
    print(f"Encoded: {encoded}")
    print(f"Matrix size: {matrix.size}x{matrix.size}")


if __name__ == "__main__":
    main()

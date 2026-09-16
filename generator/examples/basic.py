from qr_generator.generator import generate


def main() -> None:
    data = "Hello, QR-generator!"
    error_correction = "M"

    matrix = generate(data, error_correction)

    print(f"Input: {data}")
    print(f"Error correction level: {error_correction}")
    print(f"Matrix size: {matrix.size}x{matrix.size}")
    print()
    print("QR Matrix:")
    print(matrix)


if __name__ == "__main__":
    main()

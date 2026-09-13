# QR-generator

A QR code generator built from scratch in Python.

QR-generator is a learning-focused implementation of the QR Code standard, built without relying on external QR-generation libraries. The goal is to understand how QR codes work internally, from data encoding and error correction to matrix construction and rendering.

## 🚧 Status

**Early development**

The project is currently being built incrementally, with features being added and tested as development progresses.

## 🎯 Goals

* Implement QR encoding from scratch
* Support multiple QR data modes
* Implement error correction
* Generate and apply QR masking patterns
* Construct valid QR matrices
* Render QR codes as images and/or SVG
* Provide a simple command-line interface
* Build a comprehensive test suite

## 🛠️ Planned Features

* [ ] Basic QR matrix generation
* [ ] Numeric encoding
* [ ] Alphanumeric encoding
* [ ] Byte/text encoding
* [ ] Error correction
* [ ] QR masking
* [ ] Multiple QR versions
* [ ] PNG rendering
* [ ] SVG rendering
* [ ] Command-line interface
* [ ] Automated tests
* [ ] QR decoding compatibility tests

## 📚 Why?

Most QR-code libraries make generating a QR code as simple as calling one function.

That's useful, but it doesn't explain what is actually happening underneath.

QR-generator is an attempt to build that process from the ground up and learn the algorithms, mathematics, and data structures involved along the way.

## 🧪 Development

QR-generator is written in **Python** and developed incrementally using versioned releases.

The project follows a test-driven approach where practical, with each major feature being verified as development progresses.

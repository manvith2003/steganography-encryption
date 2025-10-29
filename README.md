# Steganography with AES Encryption

A Python application providing double-layer security by combining AES-256 encryption with LSB steganography to hide secret messages inside images.

## 🔐 Features

- **AES-256 Encryption**: Military-grade encryption
- **LSB Steganography**: Invisible data hiding in images
- **PBKDF2 Key Derivation**: Secure password-to-key conversion
- **User-Friendly GUI**: Easy-to-use interface
- **Password Strength Indicator**: Real-time security feedback

## 📋 Requirements

- Python 3.8 or higher
- See `requirements.txt` for dependencies

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/steganography-encryption.git
cd steganography-encryption

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the GUI application
python gui.py

# Run tests
python test_demo.py
```

## 📖 How It Works

1. **Encryption Layer**: Message is encrypted using AES-256-CBC
2. **Steganography Layer**: Encrypted data is hidden in image LSBs
3. **Result**: Image looks identical but contains hidden encrypted message

## 🎓 Project Information

- **Course**: CSS411 - Cryptography and Network Security
- **Type**: Mini Project
- **Topics Covered**: AES, Block Ciphers, Key Derivation, Steganography

## 📁 Project Structure

```
steganography-encryption/
├── crypto_stego.py       # Core encryption/steganography module
├── gui.py                # GUI application
├── test_demo.py          # Testing suite
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── test_images/          # Sample cover images
├── output/               # Output stego images
└── docs/                 # Documentation
```

## 🔒 Security Features

- AES-256 encryption (256-bit key)
- PBKDF2 with 100,000 iterations
- Random salt per encryption
- Random IV per encryption
- PKCS7 padding

## 📸 Screenshots

[Add screenshots here]

## 🤝 Contributing

This is an educational project. Feel free to fork and improve!

## 📄 License

Educational use only.

## 👨‍💻 Author

[Your Name] - CSS411 Mini Project

## 🙏 Acknowledgments

- Cryptography library
- Pillow (PIL) library
- NumPy library

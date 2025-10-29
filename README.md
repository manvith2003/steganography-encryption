# Steganography with AES Encryption

A Python application that provides double-layer security by combining AES-256 encryption with LSB (Least Significant Bit) steganography to hide secret messages inside images.

## 🔐 Features

- **AES-256 Encryption**: Military-grade encryption for your messages
- **LSB Steganography**: Hide encrypted data invisibly in images
- **PBKDF2 Key Derivation**: Secure password-to-key conversion with 100,000 iterations
- **Password Strength Indicator**: Real-time feedback on password security
- **User-Friendly GUI**: Easy-to-use interface with image preview
- **Capacity Calculator**: Know how much data your image can hide
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

- Python 3.8 to 3.12
- Required packages (see `requirements.txt`)

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
# Create project directory
mkdir steganography_project
cd steganography_project
```

### Step 2: Install Dependencies

```bash
pip install cryptography Pillow numpy
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```

### Step 3: Download the Files

Save the following files in your project directory:

- `crypto_stego.py` - Core encryption and steganography module
- `gui.py` - GUI application
- `requirements.txt` - Python dependencies

## 💻 Usage

### Running the Application

```bash
python gui.py
```

### Encoding a Message

1. **Enter Your Message**: Type or paste your secret message in the text area
2. **Set Password**: Enter a strong password (8+ characters recommended)
3. **Select Cover Image**: Choose a PNG, JPG, or BMP image
   - Larger images can hide more data
   - PNG format recommended for best results
4. **Click "ENCODE & HIDE MESSAGE"**
5. **Save Stego Image**: Choose where to save the output (must be PNG)

### Decoding a Message

1. **Select Stego Image**: Choose the image containing the hidden message
2. **Enter Password**: Type the same password used for encoding
3. **Click "EXTRACT & DECRYPT MESSAGE"**
4. **View Result**: Your decrypted message will appear in the text area
5. **Copy**: Use the copy button to save the message to clipboard

## 🔬 How It Works

### Encoding Process

```
1. User enters: Message + Password + Cover Image

2. Password → PBKDF2 (100,000 iterations) → 256-bit AES Key + 16-byte Salt

3. Message → AES-256-CBC Encryption → Encrypted Data

4. Prepare payload:
   [Message Length (4 bytes)] + [Salt (16 bytes)] + [IV (16 bytes)] + [Encrypted Data]

5. Convert payload to binary (bits)

6. For each bit in payload:
   - Get next pixel's RGB channel
   - Replace Least Significant Bit (LSB) with data bit
   - Human eye cannot detect these tiny changes

7. Save modified image as PNG (lossless format)
```

### Decoding Process

```
1. User provides: Stego Image + Password

2. Extract LSBs from image pixels → Binary data

3. Parse binary data:
   - First 4 bytes: Message length
   - Next 16 bytes: Salt
   - Next 16 bytes: IV
   - Remaining bytes: Encrypted message

4. Password + Salt → PBKDF2 → AES Key

5. Encrypted message + AES Key + IV → AES Decryption → Original Message
```

## 🛡️ Security Features

### Encryption Layer

- **Algorithm**: AES-256 in CBC mode
- **Key Size**: 256 bits (extremely secure)
- **Key Derivation**: PBKDF2 with SHA-256
- **Iterations**: 100,000 (prevents brute force)
- **Padding**: PKCS7 standard
- **Random Salt**: Unique 16-byte salt per encryption
- **Random IV**: Unique 16-byte IV per encryption

### Steganography Layer

- **Method**: LSB (Least Significant Bit) insertion
- **Visibility**: Changes are invisible to human eye
- **Capacity**: Up to (Width × Height × 3) / 8 bytes
- **Format**: PNG (lossless, preserves hidden data)

### Why Double Security?

1. **Encryption alone**: Encrypted data looks suspicious
2. **Steganography alone**: Hidden data can be extracted by anyone
3. **Combined**: Data is both hidden AND encrypted
   - Attacker must first know data exists
   - Then must break AES-256 encryption

## 📊 Image Capacity Examples

| Image Resolution | Approx. Capacity |
| ---------------- | ---------------- |
| 640 × 480        | ~115 KB          |
| 1280 × 720       | ~345 KB          |
| 1920 × 1080      | ~777 KB          |
| 3840 × 2160 (4K) | ~3.1 MB          |

**Formula**: Capacity = (Width × Height × 3) / 8 bytes

## ⚠️ Important Notes

### Do's ✅

- Use PNG format for stego images (lossless)
- Use strong passwords (8+ characters, mixed case, numbers, symbols)
- Keep backup of original cover images
- Test with small messages first
- Verify capacity before encoding large messages

### Don'ts ❌

- **Don't use JPEG** for stego images (lossy compression destroys hidden data)
- Don't share stego images on platforms that re-compress (Facebook, Instagram)
- Don't reuse the same password for multiple messages
- Don't edit stego images after encoding (will corrupt data)
- Don't compress stego images

## 🧪 Testing the Application

### Basic Test

1. Create a test message: "Hello, World! This is a secret message."
2. Use password: "TestPassword123"
3. Select any PNG image (recommend 1280×720 or larger)
4. Encode the message
5. Try decoding with correct password ✅
6. Try decoding with wrong password ❌ (should fail)

### Advanced Tests

```python
# Run built-in tests
python crypto_stego.py
```

Test scenarios:

- Small message in large image
- Large message (near capacity)
- Unicode characters (emoji, special symbols)
- Wrong password during decryption
- Very long messages
- Empty message handling

## 🐛 Troubleshooting

### "Message too large" error

- Solution: Use a larger cover image or shorter message
- Check capacity: Look at image info label after selecting

### "Decoding error" or wrong output

- Wrong password entered
- Image was compressed/edited after encoding
- Stego image format changed (e.g., PNG → JPEG)

### Image appears corrupted

- Ensure you're saving as PNG format
- Don't edit the stego image after encoding

### "Module not found" errors

```bash
pip install --upgrade cryptography Pillow numpy
```

## 📁 Project Structure

```
steganography_project/
│
├── crypto_stego.py       # Core encryption/steganography logic
├── gui.py                # GUI application (main entry point)
├── requirements.txt      # Python dependencies
├── README.md             # This file
│
├── test_images/          # Sample cover images (create this)
│   ├── sample1.png
│   └── sample2.png
│
└── output/               # Output stego images (create this)
    └── stego_output.png
```

## 🎓 Educational Value

This project demonstrates:

### Cryptography Concepts

- Symmetric encryption (AES)
- Block cipher modes (CBC)
- Key derivation functions (PBKDF2)
- Initialization vectors (IV)
- Salting
- Padding schemes (PKCS7)

### Steganography Concepts

- LSB encoding/decoding
- Digital image manipulation
- Capacity calculations
- Lossless vs lossy formats

### Security Best Practices

- Strong password requirements
- Random salt generation
- Multiple encryption layers
- Defense in depth

## 📝 Code Documentation

### CryptoStego Class Methods

```python
# Key derivation
derive_key(password: str, salt: bytes) -> bytes

# Encryption
encrypt_message(message: str, password: str) -> tuple

# Decryption
decrypt_message(encrypted_data: bytes, password: str, salt: bytes, iv: bytes) -> str

# Steganography
encode_message_in_image(image_path: str, message: str, password: str, output_path: str) -> bool

decode_message_from_image(image_path: str, password: str) -> str

# Utility
calculate_image_capacity(image_path: str) -> int
```

## 🚀 Future Enhancements (Optional)

- [ ] Support for hiding files (not just text)
- [ ] Multi-image message splitting
- [ ] Compression before encryption
- [ ] Metadata stripping from output
- [ ] Randomized pixel selection (more secure)
- [ ] Decoy message feature
- [ ] Command-line interface (CLI)
- [ ] Batch processing
- [ ] Progress bars for large files

## 📚 References

### Cryptography

- [AES Specification (FIPS 197)](https://csrc.nist.gov/publications/detail/fips/197/final)
- [PBKDF2 Specification (RFC 2898)](https://tools.ietf.org/html/rfc2898)
- Python Cryptography Library: https://cryptography.io/

### Steganography

- LSB Steganography: Hiding data in least significant bits
- PIL/Pillow Documentation: https://pillow.readthedocs.io/

## 📄 License

This project is for educational purposes. Use responsibly and ethically.

## 👨‍💻 Author

Created for CSS411 - Cryptography and Network Security

## 🤝 Contributing

Suggestions for improvements:

1. Fork the project
2. Create your feature branch
3. Test thoroughly
4. Submit a pull request

## ❓ FAQ

**Q: Can I use JPEG images?**
A: No. JPEG uses lossy compression which destroys hidden data. Always use PNG.

**Q: Is this encryption breakable?**
A: AES-256 with proper implementation is considered unbreakable with current technology. The weak point is password strength.

**Q: Can I hide any file type?**
A: Current version supports text only. File support can be added in future versions.

**Q: How do I know if an image contains hidden data?**
A: You can't easily tell by looking. That's the point of steganography! Statistical analysis can detect it, but visual inspection won't.

**Q: What happens if I edit the stego image?**
A: Any editing (crop, resize, filters) will likely corrupt the hidden data.

**Q: Can I share stego images on social media?**
A: Not recommended. Many platforms re-compress images, destroying hidden data.

## 🎯 Conclusion

This project successfully demonstrates the combination of modern cryptography (AES-256) with steganography (LSB method) to create a double-layer security system for hiding messages in images. The implementation covers key concepts from the CSS411 syllabus including:

- Block cipher encryption (AES)
- Key derivation (PBKDF2)
- Message authentication
- Security best practices

Perfect for understanding practical applications of cryptographic concepts!

"""
Steganography with Encryption - Core Module
Implements AES encryption and LSB steganography
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
from PIL import Image
import numpy as np


class CryptoStego:
    """Main class for encryption and steganography operations"""
    
    def __init__(self):
        self.backend = default_backend()
        self.salt_size = 16
        self.iv_size = 16
        self.pbkdf2_iterations = 100000
    
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive AES key from password using PBKDF2
        
        Args:
            password: User password
            salt: Random salt (16 bytes)
        
        Returns:
            32-byte key for AES-256
        """
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits for AES-256
            salt=salt,
            iterations=self.pbkdf2_iterations,
            backend=self.backend
        )
        key = kdf.derive(password.encode())
        return key
    
    def encrypt_message(self, message: str, password: str) -> tuple:
        """
        Encrypt message using AES-256-CBC
        
        Args:
            message: Plaintext message
            password: User password
        
        Returns:
            (encrypted_data, salt, iv)
        """
        # Generate random salt and IV
        salt = os.urandom(self.salt_size)
        iv = os.urandom(self.iv_size)
        
        # Derive key from password
        key = self.derive_key(password, salt)
        
        # Pad message to block size (16 bytes for AES)
        message_bytes = message.encode('utf-8')
        padded_message = self._pad(message_bytes)
        
        # Encrypt using AES-256-CBC
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_message) + encryptor.finalize()
        
        return encrypted_data, salt, iv
    
    def decrypt_message(self, encrypted_data: bytes, password: str, 
                       salt: bytes, iv: bytes) -> str:
        """
        Decrypt message using AES-256-CBC
        
        Args:
            encrypted_data: Encrypted bytes
            password: User password
            salt: Salt used during encryption
            iv: IV used during encryption
        
        Returns:
            Decrypted plaintext message
        """
        # Derive key from password
        key = self.derive_key(password, salt)
        
        # Decrypt using AES-256-CBC
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Remove padding
        decrypted_message = self._unpad(decrypted_padded)
        
        return decrypted_message.decode('utf-8')
    
    def _pad(self, data: bytes) -> bytes:
        """Apply PKCS7 padding"""
        padding_length = 16 - (len(data) % 16)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    def _unpad(self, data: bytes) -> bytes:
        """Remove PKCS7 padding"""
        padding_length = data[-1]
        return data[:-padding_length]
    
    def calculate_image_capacity(self, image_path: str) -> int:
        """
        Calculate maximum bytes that can be hidden in image
        
        Args:
            image_path: Path to cover image
        
        Returns:
            Maximum bytes capacity
        """
        img = Image.open(image_path)
        width, height = img.size
        # 3 color channels (RGB), 1 bit per channel, 8 bits per byte
        capacity = (width * height * 3) // 8
        return capacity
    
    def encode_message_in_image(self, image_path: str, message: str, 
                                password: str, output_path: str) -> bool:
        """
        Encode encrypted message in image using LSB steganography
        
        Args:
            image_path: Path to cover image
            message: Message to hide
            password: Encryption password
            output_path: Path to save stego-image
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Encrypt message
            encrypted_data, salt, iv = self.encrypt_message(message, password)
            
            # Prepare data to hide: [length(4)] + [salt(16)] + [iv(16)] + [encrypted_data]
            message_length = len(encrypted_data)
            data_to_hide = (
                message_length.to_bytes(4, byteorder='big') +
                salt +
                iv +
                encrypted_data
            )
            
            # Load image
            img = Image.open(image_path)
            img = img.convert('RGB')  # Ensure RGB mode
            img_array = np.array(img)
            
            # Check capacity
            max_bytes = (img_array.shape[0] * img_array.shape[1] * 3) // 8
            if len(data_to_hide) > max_bytes:
                print(f"Error: Message too large. Max: {max_bytes} bytes, Required: {len(data_to_hide)} bytes")
                return False
            
            # Convert data to binary
            binary_data = ''.join(format(byte, '08b') for byte in data_to_hide)
            data_index = 0
            data_len = len(binary_data)
            
            # Embed data in LSBs
            flat_img = img_array.flatten()
            for i in range(len(flat_img)):
                if data_index < data_len:
                    # Modify LSB
                    flat_img[i] = (flat_img[i] & 0xFE) | int(binary_data[data_index])
                    data_index += 1
                else:
                    break
            
            # Reshape and save
            stego_img_array = flat_img.reshape(img_array.shape)
            stego_img = Image.fromarray(stego_img_array.astype('uint8'), 'RGB')
            stego_img.save(output_path, 'PNG')
            
            print(f"Message successfully hidden in {output_path}")
            return True
            
        except Exception as e:
            print(f"Encoding error: {str(e)}")
            return False
    
    def decode_message_from_image(self, image_path: str, password: str) -> str:
        """
        Decode and decrypt message from stego-image
        
        Args:
            image_path: Path to stego-image
            password: Decryption password
        
        Returns:
            Decrypted message or error string
        """
        try:
            # Load stego-image
            img = Image.open(image_path)
            img = img.convert('RGB')
            img_array = np.array(img)
            
            # Extract bits from LSBs
            flat_img = img_array.flatten()
            
            # Extract length (first 32 bits = 4 bytes)
            length_bits = ''.join(str(flat_img[i] & 1) for i in range(32))
            message_length = int(length_bits, 2)
            
            # Calculate total bits needed
            total_bytes = 4 + self.salt_size + self.iv_size + message_length
            total_bits = total_bytes * 8
            
            # Extract all data bits
            binary_data = ''.join(str(flat_img[i] & 1) for i in range(total_bits))
            
            # Convert binary to bytes
            extracted_bytes = bytearray()
            for i in range(0, len(binary_data), 8):
                byte = binary_data[i:i+8]
                extracted_bytes.append(int(byte, 2))
            
            # Parse extracted data
            length = int.from_bytes(extracted_bytes[0:4], byteorder='big')
            salt = bytes(extracted_bytes[4:20])
            iv = bytes(extracted_bytes[20:36])
            encrypted_data = bytes(extracted_bytes[36:36+length])
            
            # Decrypt message
            decrypted_message = self.decrypt_message(encrypted_data, password, salt, iv)
            
            return decrypted_message
            
        except Exception as e:
            return f"Decoding error: {str(e)}"


# Testing function
def test_crypto_stego():
    """Test the CryptoStego class"""
    cs = CryptoStego()
    
    # Test encryption/decryption
    message = "This is a secret message! 🔐"
    password = "MySecurePassword123"
    
    print("Testing encryption...")
    encrypted, salt, iv = cs.encrypt_message(message, password)
    print(f"Encrypted data length: {len(encrypted)} bytes")
    
    print("\nTesting decryption...")
    decrypted = cs.decrypt_message(encrypted, password, salt, iv)
    print(f"Decrypted message: {decrypted}")
    print(f"Match: {message == decrypted}")


if __name__ == "__main__":
    test_crypto_stego()
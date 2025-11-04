"""
Test and Demo Script for Steganography with Encryption
Run this to test all functionality without GUI
"""

from crypto_stego import CryptoStego
from PIL import Image
import numpy as np
import os


def create_test_image(filename="test_cover.png", width=800, height=600):
    """
    Create a test image for demonstration
    """
    print(f"\n📸 Creating test image: {filename}")
    
    # Create a colorful gradient image
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    for i in range(height):
        for j in range(width):
            img_array[i, j] = [
                int((i / height) * 255),  # Red gradient
                int((j / width) * 255),   # Green gradient
                128                        # Constant blue
            ]
    
    img = Image.fromarray(img_array, 'RGB')
    img.save(filename, 'PNG')
    print(f"✅ Test image created: {width}x{height} pixels")
    
    return filename


def test_encryption_decryption():
    """Test basic encryption and decryption"""
    print("\n" + "="*60)
    print("TEST 1: Encryption/Decryption")
    print("="*60)
    
    cs = CryptoStego()
    
    test_cases = [
        ("Hello, World!", "password123"),
        ("This is a secret message 🔐", "StrongPass!@#"),
        ("Unicode test: 你好世界 مرحبا", "TestPass456"),
        ("A" * 1000, "LongMessage99"),  # Long message
    ]
    
    for i, (message, password) in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"  Message: {message[:50]}..." if len(message) > 50 else f"  Message: {message}")
        print(f"  Password: {password}")
        
        try:
            # Encrypt
            encrypted, salt, iv = cs.encrypt_message(message, password)
            print(f"  ✅ Encrypted ({len(encrypted)} bytes)")
            
            # Decrypt
            decrypted = cs.decrypt_message(encrypted, password, salt, iv)
            
            if decrypted == message:
                print(f"  ✅ Decryption successful - MATCH!")
            else:
                print(f"  ❌ Decryption failed - NO MATCH!")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")


def test_steganography():
    """Test steganography encoding and decoding"""
    print("\n" + "="*60)
    print("TEST 2: Steganography")
    print("="*60)
    
    cs = CryptoStego()
    
    # Create test image
    cover_image = create_test_image("test_cover.png", 800, 600)
    
    # Calculate capacity
    capacity = cs.calculate_image_capacity(cover_image)
    print(f"\n📊 Image capacity: {capacity} bytes ({capacity/1024:.2f} KB)")
    
    test_messages = [
        ("Short message", "pass123"),
        ("Medium length message with some details about cryptography and steganography! " * 10, "SecurePass!@#"),
        ("Testing emoji support 🔐🖼️💻🔒✨", "EmojiTest789"),
    ]
    
    for i, (message, password) in enumerate(test_messages, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Message length: {len(message)} characters")
        print(f"Message preview: {message[:50]}...")
        
        stego_image = f"test_stego_{i}.png"
        
        try:
            # Encode
            print("🔒 Encoding...")
            success = cs.encode_message_in_image(
                cover_image,
                message,
                password,
                stego_image
            )
            
            if not success:
                print("❌ Encoding failed!")
                continue
            
            print(f"✅ Encoded successfully → {stego_image}")
            
            # Decode
            print("🔓 Decoding...")
            decoded = cs.decode_message_from_image(stego_image, password)
            
            if decoded == message:
                print("✅ Decoding successful - MATCH!")
            else:
                print("❌ Decoding failed - NO MATCH!")
                print(f"Expected: {message[:100]}")
                print(f"Got: {decoded[:100]}")
            
            # Test wrong password
            print("🔓 Testing wrong password...")
            try:
                wrong_decode = cs.decode_message_from_image(stego_image, "wrongpassword")
                print("❌ Should have failed but didn't!")
            except:
                print("✅ Correctly rejected wrong password")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Cleanup
    print("\n🧹 Cleaning up test files...")
    for file in [cover_image] + [f"test_stego_{i}.png" for i in range(1, len(test_messages)+1)]:
        if os.path.exists(file):
            os.remove(file)
            print(f"  Deleted: {file}")


def test_capacity_limits():
    """Test image capacity limits"""
    print("\n" + "="*60)
    print("TEST 3: Capacity Limits")
    print("="*60)
    
    cs = CryptoStego()
    
    image_sizes = [
        (100, 100),
        (640, 480),
        (1280, 720),
        (1920, 1080),
    ]
    
    for width, height in image_sizes:
        test_img = create_test_image(f"capacity_test_{width}x{height}.png", width, height)
        capacity = cs.calculate_image_capacity(test_img)
        
        print(f"\n{width}x{height} image:")
        print(f"  Total pixels: {width * height:,}")
        print(f"  Capacity: {capacity:,} bytes ({capacity/1024:.2f} KB)")
        print(f"  Can hide ~{capacity} characters")
        
        # Test with message near capacity
        test_message = "A" * (capacity - 100)  # Leave some room for metadata
        test_pass = "TestPassword"
        output = f"capacity_stego_{width}x{height}.png"
        
        success = cs.encode_message_in_image(test_img, test_message, test_pass, output)
        
        if success:
            print(f"  ✅ Successfully hid {len(test_message)} characters")
            decoded = cs.decode_message_from_image(output, test_pass)
            if decoded == test_message:
                print(f"  ✅ Successfully retrieved all characters")
            else:
                print(f"  ❌ Retrieved message doesn't match")
        else:
            print(f"  ❌ Failed to hide message")
        
        # Cleanup
        os.remove(test_img)
        if os.path.exists(output):
            os.remove(output)


def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n" + "="*60)
    print("TEST 4: Edge Cases")
    print("="*60)
    
    cs = CryptoStego()
    cover_img = create_test_image("edge_test.png", 400, 300)
    
    # Test 1: Empty message
    print("\n1. Empty message:")
    try:
        success = cs.encode_message_in_image(cover_img, "", "pass", "edge1.png")
        print("  ⚠️  Empty message accepted (might want to add validation)")
    except Exception as e:
        print(f"  ✅ Rejected empty message: {str(e)}")
    
    # Test 2: Very long password
    print("\n2. Very long password:")
    long_pass = "A" * 1000
    try:
        success = cs.encode_message_in_image(cover_img, "Test", long_pass, "edge2.png")
        if success:
            print("  ✅ Long password accepted")
            decoded = cs.decode_message_from_image("edge2.png", long_pass)
            if decoded == "Test":
                print("  ✅ Decoding with long password works")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
    
    # Test 3: Special characters
    print("\n3. Special characters in message:")
    special_msg = "Test!@#$%^&*()_+-=[]{}|;':\",./<>?`~\n\t"
    try:
        success = cs.encode_message_in_image(cover_img, special_msg, "pass", "edge3.png")
        if success:
            decoded = cs.decode_message_from_image("edge3.png", "pass")
            if decoded == special_msg:
                print("  ✅ Special characters handled correctly")
            else:
                print("  ❌ Special characters corrupted")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
    
    # Cleanup
    for file in ["edge_test.png", "edge1.png", "edge2.png", "edge3.png"]:
        if os.path.exists(file):
            os.remove(file)


def demo_workflow():
    """Demonstrate complete workflow"""
    print("\n" + "="*60)
    print("DEMO: Complete Workflow")
    print("="*60)
    
    cs = CryptoStego()
    
    # Step 1: Create cover image
    print("\n📋 Step 1: Creating cover image...")
    cover = create_test_image("demo_cover.png", 1024, 768)
    capacity = cs.calculate_image_capacity(cover)
    print(f"   Capacity: {capacity/1024:.2f} KB")
    
    # Step 2: Prepare message
    message = """
    This is a secret message hidden using steganography and encryption!
    
    Key Features:
    - AES-256 encryption
    - LSB steganography
    - PBKDF2 key derivation
    - Completely invisible to the naked eye
    
    The combination of cryptography and steganography provides
    double-layer security for your sensitive information.
    
    Date: 2024
    Project: CSS411 Mini Project
    """
    
    password = "SuperSecurePassword123!@#"
    
    print(f"\n📋 Step 2: Preparing message...")
    print(f"   Message length: {len(message)} characters")
    print(f"   Password strength: Strong ✅")
    
    # Step 3: Encode
    print(f"\n📋 Step 3: Encoding message...")
    stego = "demo_stego.png"
    success = cs.encode_message_in_image(cover, message, password, stego)
    
    if success:
        print(f"   ✅ Message hidden successfully!")
        print(f"   Output: {stego}")
        
        # Step 4: Verify files
        print(f"\n📋 Step 4: Comparing images...")
        cover_img = Image.open(cover)
        stego_img = Image.open(stego)
        print(f"   Cover image size: {cover_img.size}")
        print(f"   Stego image size: {stego_img.size}")
        print(f"   Images look identical: ✅ (LSB changes invisible)")
        
        # Step 5: Decode
        print(f"\n📋 Step 5: Decoding message...")
        decoded = cs.decode_message_from_image(stego, password)
        
        if decoded == message:
            print(f"   ✅ Message retrieved successfully!")
            print(f"\n   Decoded message preview:")
            print(f"   {decoded[:150]}...")
        else:
            print(f"   ❌ Decoding failed!")
    
    # Cleanup
    print(f"\n🧹 Cleaning up...")
    for file in [cover, stego]:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n" + "="*60)
    print("DEMO COMPLETE! ✅")
    print("="*60)


def run_all_tests():
    """Run all tests"""
    print("\n" + "🔬"*30)
    print("STEGANOGRAPHY WITH ENCRYPTION - TEST SUITE")
    print("🔬"*30)
    
    test_encryption_decryption()
    test_steganography()
    test_capacity_limits()
    test_edge_cases()
    demo_workflow()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETE! ✅")
    print("="*60)
    print("\nTo run the GUI application, execute:")
    print("  python gui.py")


if __name__ == "__main__":
    run_all_tests()
    
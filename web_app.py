"""
Secure SMG - Web Application
Streamlit version for easy deployment
"""

import streamlit as st
from crypto_stego import CryptoStego
from PIL import Image
import io
import os

# Page configuration
st.set_page_config(
    page_title="Secure SMG",
    page_icon="🔐",
    layout="wide"
)

# Initialize CryptoStego
cs = CryptoStego()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px;
    }
    .success-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🔐 Secure SMG</h1>
    <h3>Steganography with AES-256 Encryption</h3>
    <p>Double-layer security: Hide encrypted messages in images</p>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["🔒 Encode Message", "🔓 Decode Message", "ℹ️ About"])

# ============= ENCODE TAB =============
with tab1:
    st.header("Hide Your Secret Message")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Message input
        message = st.text_area(
            "Enter Your Secret Message",
            height=150,
            placeholder="Type your message here...",
            help="This message will be encrypted and hidden in the image"
        )
        
        # Character count
        if message:
            st.caption(f"Characters: {len(message)}")
        
        # Password input
        password = st.text_input(
            "Enter Password",
            type="password",
            help="Choose a strong password (8+ characters recommended)"
        )
        
        # Password strength indicator
        if password:
            strength = 0
            if len(password) >= 8: strength += 1
            if any(c.isupper() for c in password): strength += 1
            if any(c.islower() for c in password): strength += 1
            if any(c.isdigit() for c in password): strength += 1
            if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password): strength += 1
            
            if strength <= 2:
                st.warning("⚠️ Weak password")
            elif strength <= 3:
                st.info("💡 Medium strength password")
            else:
                st.success("✅ Strong password!")
    
    with col2:
        # Image upload
        uploaded_file = st.file_uploader(
            "Choose Cover Image",
            type=['png', 'jpg', 'jpeg', 'bmp'],
            help="Select an image to hide your message in"
        )
        
        if uploaded_file:
            # Display image
            img = Image.open(uploaded_file)
            st.image(img, caption="Cover Image", use_column_width=True)
            
            # Calculate and show capacity
            img.save("temp_cover.png")
            capacity = cs.calculate_image_capacity("temp_cover.png")
            st.info(f"📊 **Capacity:** {capacity:,} bytes\n\n({capacity/1024:.2f} KB)")
    
    st.markdown("---")
    
    # Encode button
    if st.button("🔒 ENCODE & HIDE MESSAGE", key="encode_btn", use_container_width=True):
        if not message:
            st.error("❌ Please enter a message!")
        elif not password:
            st.error("❌ Please enter a password!")
        elif len(password) < 6:
            st.warning("⚠️ Password is too short! Use at least 6 characters.")
        elif not uploaded_file:
            st.error("❌ Please select a cover image!")
        else:
            try:
                # Save uploaded image
                img = Image.open(uploaded_file)
                img.save("temp_cover.png")
                
                # Encode message
                with st.spinner("Encoding message..."):
                    success = cs.encode_message_in_image(
                        "temp_cover.png",
                        message,
                        password,
                        "temp_stego.png"
                    )
                
                if success:
                    st.success("✅ Message successfully hidden and encrypted!")
                    
                    # Show success details
                    st.markdown("""
                    <div class="success-box">
                        <strong>Success!</strong><br>
                        ✓ Message encrypted with AES-256<br>
                        ✓ Hidden using LSB steganography<br>
                        ✓ Image looks identical to original
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Provide download button
                    with open("temp_stego.png", "rb") as f:
                        st.download_button(
                            label="⬇️ Download Stego Image",
                            data=f,
                            file_name="secure_smg_output.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    
                    # Show comparison
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image("temp_cover.png", caption="Original Image")
                    with col2:
                        st.image("temp_stego.png", caption="Stego Image (with hidden message)")
                    
                    st.info("💡 The images look identical, but the right one contains your encrypted message!")
                    
                else:
                    st.error("❌ Failed to encode message. Image may be too small for this message.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# ============= DECODE TAB =============
with tab2:
    st.header("Extract Hidden Message")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Password input
        decode_password = st.text_input(
            "Enter Password",
            type="password",
            key="decode_pwd",
            help="Enter the same password used to encode the message"
        )
    
    with col2:
        # Stego image upload
        stego_file = st.file_uploader(
            "Choose Stego Image",
            type=['png'],
            key="stego",
            help="Select the PNG image containing hidden message"
        )
        
        if stego_file:
            st.image(stego_file, caption="Stego Image", use_column_width=True)
    
    st.markdown("---")
    
    # Decode button
    if st.button("🔓 EXTRACT & DECRYPT MESSAGE", key="decode_btn", use_container_width=True):
        if not decode_password:
            st.error("❌ Please enter the password!")
        elif not stego_file:
            st.error("❌ Please select a stego image!")
        else:
            try:
                # Save uploaded image
                img = Image.open(stego_file)
                img.save("temp_decode.png")
                
                # Decode message
                with st.spinner("Extracting and decrypting message..."):
                    decoded_msg = cs.decode_message_from_image(
                        "temp_decode.png",
                        decode_password
                    )
                
                st.success("✅ Message successfully decrypted!")
                
                # Display decoded message
                st.markdown("### 📝 Decrypted Message:")
                st.text_area(
                    "Your Secret Message",
                    decoded_msg,
                    height=200,
                    key="decoded_output"
                )
                
                # Copy button simulation
                st.info("💡 Select the text above and copy it to clipboard")
                
                # Show statistics
                st.markdown("### 📊 Message Statistics:")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Characters", len(decoded_msg))
                with col2:
                    st.metric("Words", len(decoded_msg.split()))
                with col3:
                    st.metric("Bytes", len(decoded_msg.encode()))
                
            except Exception as e:
                st.error("❌ Failed to decode message!")
                st.warning("Possible reasons:\n- Wrong password\n- Image is corrupted\n- Not a valid stego image")
                st.caption(f"Technical error: {str(e)}")

# ============= ABOUT TAB =============
with tab3:
    st.header("About Secure SMG")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🛡️ Features
        
        **Encryption:**
        - 🔐 AES-256-CBC encryption
        - 🔑 PBKDF2 key derivation
        - 🔒 100,000 iterations
        - 🎲 Random salt & IV
        
        **Steganography:**
        - 🖼️ LSB (Least Significant Bit) method
        - 👁️ Invisible to human eye
        - 📏 Capacity calculator
        - 🔍 PNG format preservation
        
        **Security:**
        - 🛡️ Double-layer security
        - 🔐 Military-grade encryption
        - 🚫 No backdoors
        - ✅ Open source
        """)
    
    with col2:
        st.markdown("""
        ### 🎓 Project Information
        
        **Course:** CSS411 Cryptography and Network Security
        
        **Institution:** Indian Institute of Information Technology Kottayam
        
        **Team Members:**
        - Sujal Saraswat (2022BCS0015)
        - Gunj Joshi (2022BCS0024)
        - Suraj Rathor (2022BCS0051)
        - Manvith M (2022BCS0066)
        
        **Technologies:**
        - Python 3.8+
        - Cryptography library
        - Pillow (PIL)
        - NumPy
        - Streamlit
        
        **License:** MIT License
        """)
    
    st.markdown("---")
    
    # How it works
    st.markdown("""
    ### 🔍 How It Works
    
    #### Encoding Process:
    1. **Encryption**: Your message is encrypted using AES-256 with your password
    2. **Key Derivation**: Password → PBKDF2 (100,000 iterations) → 256-bit key
    3. **Steganography**: Encrypted data is hidden in image pixels using LSB method
    4. **Output**: Image looks identical but contains your encrypted message
    
    #### Decoding Process:
    1. **Extraction**: LSB data is extracted from image pixels
    2. **Key Derivation**: Your password generates the same encryption key
    3. **Decryption**: AES-256 decrypts the hidden message
    4. **Output**: Original message is revealed
    
    #### Why Double Security?
    - **Encryption alone**: Encrypted data is obvious
    - **Steganography alone**: Hidden but not encrypted
    - **Both together**: Hidden AND encrypted = Maximum security! 🔐
    """)
    
    st.markdown("---")
    
    # Usage tips
    with st.expander("💡 Usage Tips"):
        st.markdown("""
        **Best Practices:**
        - Use strong passwords (8+ characters, mixed case, numbers, symbols)
        - Choose larger images for longer messages
        - Always save stego images as PNG (not JPEG!)
        - Keep original cover images as backup
        - Don't edit stego images after creation
        
        **Security Notes:**
        - Never share your password
        - Use different passwords for different messages
        - Store stego images securely
        - Don't upload to platforms that compress images (Facebook, Instagram)
        
        **Image Requirements:**
        - **Input**: PNG, JPG, JPEG, or BMP
        - **Output**: Must be PNG (lossless compression)
        - **Minimum**: 640×480 pixels recommended
        - **Maximum message**: Depends on image size
        """)
    
    with st.expander("🔬 Technical Details"):
        st.markdown("""
        **Encryption Specifications:**
        - Algorithm: AES-256
        - Mode: CBC (Cipher Block Chaining)
        - Key Size: 256 bits (32 bytes)
        - Block Size: 128 bits (16 bytes)
        - Padding: PKCS7
        
        **Key Derivation:**
        - Function: PBKDF2-HMAC-SHA256
        - Iterations: 100,000
        - Salt: 16 bytes (random)
        - IV: 16 bytes (random)
        
        **Steganography:**
        - Method: LSB (Least Significant Bit)
        - Capacity: (Width × Height × 3) ÷ 8 bytes
        - Channels: RGB (3 channels)
        - Detection: Imperceptible to human eye
        """)
    
    with st.expander("📚 References & Resources"):
        st.markdown("""
        - [AES Specification (FIPS 197)](https://csrc.nist.gov/publications/detail/fips/197/final)
        - [PBKDF2 Specification (RFC 2898)](https://tools.ietf.org/html/rfc2898)
        - [Python Cryptography Library](https://cryptography.io/)
        - [Steganography Techniques](https://en.wikipedia.org/wiki/Steganography)
        """)

# Sidebar
with st.sidebar:
    st.markdown("### 🔐 Secure SMG")
    st.markdown("**Version:** 1.0.0")
    st.markdown("**Status:** 🟢 Active")
    
    st.markdown("---")
    
    st.markdown("### 📊 Quick Stats")
    st.markdown("""
    - **Encryption:** AES-256
    - **Iterations:** 100,000
    - **Key Size:** 256 bits
    - **Security:** Military-grade
    """)
    
    st.markdown("---")
    
    st.markdown("### 🔗 Links")
    st.markdown("""
    - [GitHub Repository](https://github.com/YOUR-USERNAME/steganography-encryption)
    - [Documentation](https://github.com/YOUR-USERNAME/steganography-encryption#readme)
    - [Report Issues](https://github.com/YOUR-USERNAME/steganography-encryption/issues)
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚠️ Disclaimer")
    st.caption("This tool is for educational purposes. Use responsibly and ethically. The developers are not responsible for misuse.")
    
    st.markdown("---")
    st.caption("© 2024 IIIT Kottayam | CSS411 Project")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p>Made with ❤️ by Team Secure SMG | IIIT Kottayam</p>
    <p>🔐 Double-layer security: Encryption + Steganography</p>
</div>
""", unsafe_allow_html=True)

"""
Project Setup Script
Creates all necessary files and folders for the Steganography project
"""

import os
import sys

def create_directory_structure():
    """Create project directory structure"""
    directories = [
        'test_images',
        'output',
        'docs',
        'screenshots'
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created: {directory}/")
        else:
            print(f"⚠️  Already exists: {directory}/")
    print()

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
output/*.png
test_images/*.png
screenshots/*.png
*.log

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ Created: .gitignore")

def create_requirements():
    """Create requirements.txt"""
    requirements = """cryptography==41.0.7
Pillow==10.1.0
numpy==1.24.3
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ Created: requirements.txt")

def create_readme():
    """Create README.md"""
    readme_content = """# Steganography with AES Encryption

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
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    print("✅ Created: README.md")

def create_license():
    """Create LICENSE file"""
    license_content = """MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    with open('LICENSE', 'w') as f:
        f.write(license_content)
    print("✅ Created: LICENSE")

def create_git_commands_file():
    """Create a file with Git commands to run"""
    git_commands = """# Git Commands to Initialize Repository

# 1. Initialize Git repository
git init

# 2. Add all files
git add .

# 3. Create initial commit
git commit -m "Initial commit: Steganography with AES Encryption project"

# 4. Create main branch (if needed)
git branch -M main

# 5. Add remote repository (replace with your GitHub repo URL)
git remote add origin https://github.com/yourusername/steganography-encryption.git

# 6. Push to GitHub
git push -u origin main

# Additional useful commands:

# Check status
git status

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-name

# Add specific files
git add filename.py

# Commit with message
git commit -m "Your commit message"

# Push changes
git push
"""
    
    with open('GIT_COMMANDS.txt', 'w') as f:
        f.write(git_commands)
    print("✅ Created: GIT_COMMANDS.txt")

def create_vscode_settings():
    """Create VS Code settings"""
    if not os.path.exists('.vscode'):
        os.makedirs('.vscode')
    
    settings = """{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "python.analysis.typeCheckingMode": "basic"
}
"""
    
    with open('.vscode/settings.json', 'w') as f:
        f.write(settings)
    print("✅ Created: .vscode/settings.json")
    
    # Create launch configuration for debugging
    launch_config = """{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: GUI Application",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/gui.py",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Test Suite",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/test_demo.py",
            "console": "integratedTerminal"
        }
    ]
}
"""
    
    with open('.vscode/launch.json', 'w') as f:
        f.write(launch_config)
    print("✅ Created: .vscode/launch.json")

def print_next_steps():
    """Print next steps for the user"""
    next_steps = """
╔════════════════════════════════════════════════════════════╗
║          PROJECT SETUP COMPLETED SUCCESSFULLY! ✅          ║
╚════════════════════════════════════════════════════════════╝

📁 Directory structure created
📄 Configuration files created
🔧 VS Code settings configured

NEXT STEPS:

1️⃣  CREATE GITHUB REPOSITORY
   - Go to https://github.com/new
   - Repository name: steganography-encryption
   - Description: AES Encryption + LSB Steganography Project
   - Make it Public or Private
   - DO NOT initialize with README (we already have one)
   - Click "Create repository"

2️⃣  OPEN PROJECT IN VS CODE
   - Open VS Code
   - File → Open Folder
   - Select this project folder

3️⃣  INITIALIZE GIT (in VS Code terminal)
   Run these commands one by one:
   
   git init
   git add .
   git commit -m "Initial commit: Steganography project"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/steganography-encryption.git
   git push -u origin main

4️⃣  INSTALL DEPENDENCIES
   pip install -r requirements.txt

5️⃣  CREATE PROJECT FILES
   - Copy crypto_stego.py code
   - Copy gui.py code
   - Copy test_demo.py code

6️⃣  TEST THE PROJECT
   python test_demo.py

7️⃣  RUN THE APPLICATION
   python gui.py

📝 NOTE: Replace YOUR-USERNAME with your actual GitHub username

💡 TIP: All Git commands are saved in GIT_COMMANDS.txt

═══════════════════════════════════════════════════════════════

Ready to start? Open VS Code and follow the steps above! 🚀
"""
    print(next_steps)

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  STEGANOGRAPHY PROJECT SETUP")
    print("="*60 + "\n")
    
    try:
        create_directory_structure()
        create_gitignore()
        create_requirements()
        create_readme()
        create_license()
        create_git_commands_file()
        create_vscode_settings()
        print()
        print_next_steps()
        
    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
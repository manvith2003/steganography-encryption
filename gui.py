"""
Steganography with Encryption - GUI Application
User interface for encoding and decoding messages
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from crypto_stego import CryptoStego
import os
from PIL import Image, ImageTk


class SteganographyGUI:
    """GUI Application for Steganography with Encryption"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography with AES Encryption")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        self.crypto_stego = CryptoStego()
        self.cover_image_path = None
        self.stego_image_path = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.encode_tab = ttk.Frame(self.notebook)
        self.decode_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.encode_tab, text='Encode Message')
        self.notebook.add(self.decode_tab, text='Decode Message')
        
        # Setup encode tab
        self.setup_encode_tab()
        
        # Setup decode tab
        self.setup_decode_tab()
        
        # Status bar
        self.status_bar = tk.Label(
            self.root, 
            text="Ready", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_encode_tab(self):
        """Setup the encode message tab"""
        
        # Message input section
        msg_frame = ttk.LabelFrame(self.encode_tab, text="Secret Message", padding=10)
        msg_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.encode_text = scrolledtext.ScrolledText(
            msg_frame, 
            height=8, 
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.encode_text.pack(fill='both', expand=True)
        
        # Character count
        self.char_count_label = tk.Label(msg_frame, text="Characters: 0", fg="gray")
        self.char_count_label.pack(anchor='e', pady=(5, 0))
        self.encode_text.bind('<KeyRelease>', self.update_char_count)
        
        # Password section
        pwd_frame = ttk.LabelFrame(self.encode_tab, text="Encryption Password", padding=10)
        pwd_frame.pack(fill='x', padx=10, pady=10)
        
        self.encode_password = tk.Entry(pwd_frame, show='*', font=('Arial', 10))
        self.encode_password.pack(fill='x', side='left', expand=True)
        self.encode_password.bind('<KeyRelease>', self.check_password_strength)
        
        self.show_pwd_encode = tk.Checkbutton(
            pwd_frame, 
            text="Show", 
            command=self.toggle_password_encode
        )
        self.show_pwd_encode.pack(side='left', padx=(10, 0))
        
        # Password strength indicator
        self.pwd_strength_label = tk.Label(pwd_frame, text="", fg="gray")
        self.pwd_strength_label.pack(side='left', padx=(10, 0))
        
        # Image section
        img_frame = ttk.LabelFrame(self.encode_tab, text="Cover Image", padding=10)
        img_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        btn_frame = tk.Frame(img_frame)
        btn_frame.pack(fill='x')
        
        self.select_image_btn = tk.Button(
            btn_frame,
            text="Select Cover Image",
            command=self.select_cover_image,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2'
        )
        self.select_image_btn.pack(side='left')
        
        self.image_info_label = tk.Label(btn_frame, text="No image selected", fg="gray")
        self.image_info_label.pack(side='left', padx=(10, 0))
        
        # Image preview
        self.image_preview_label = tk.Label(img_frame, text="Image preview will appear here")
        self.image_preview_label.pack(pady=10)
        
        # Encode button
        self.encode_btn = tk.Button(
            self.encode_tab,
            text="🔒 ENCODE & HIDE MESSAGE",
            command=self.encode_message,
            bg='#2196F3',
            fg='white',
            font=('Arial', 12, 'bold'),
            height=2,
            cursor='hand2'
        )
        self.encode_btn.pack(fill='x', padx=10, pady=10)
    
    def setup_decode_tab(self):
        """Setup the decode message tab"""
        
        # Stego image section
        img_frame = ttk.LabelFrame(self.decode_tab, text="Stego Image", padding=10)
        img_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        btn_frame = tk.Frame(img_frame)
        btn_frame.pack(fill='x')
        
        self.select_stego_btn = tk.Button(
            btn_frame,
            text="Select Stego Image",
            command=self.select_stego_image,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 10, 'bold'),
            cursor='hand2'
        )
        self.select_stego_btn.pack(side='left')
        
        self.stego_info_label = tk.Label(btn_frame, text="No image selected", fg="gray")
        self.stego_info_label.pack(side='left', padx=(10, 0))
        
        # Stego image preview
        self.stego_preview_label = tk.Label(img_frame, text="Image preview will appear here")
        self.stego_preview_label.pack(pady=10)
        
        # Password section
        pwd_frame = ttk.LabelFrame(self.decode_tab, text="Decryption Password", padding=10)
        pwd_frame.pack(fill='x', padx=10, pady=10)
        
        self.decode_password = tk.Entry(pwd_frame, show='*', font=('Arial', 10))
        self.decode_password.pack(fill='x', side='left', expand=True)
        
        self.show_pwd_decode = tk.Checkbutton(
            pwd_frame, 
            text="Show", 
            command=self.toggle_password_decode
        )
        self.show_pwd_decode.pack(side='left', padx=(10, 0))
        
        # Decode button
        self.decode_btn = tk.Button(
            self.decode_tab,
            text="🔓 EXTRACT & DECRYPT MESSAGE",
            command=self.decode_message,
            bg='#FF9800',
            fg='white',
            font=('Arial', 12, 'bold'),
            height=2,
            cursor='hand2'
        )
        self.decode_btn.pack(fill='x', padx=10, pady=10)
        
        # Decoded message section
        msg_frame = ttk.LabelFrame(self.decode_tab, text="Decrypted Message", padding=10)
        msg_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.decode_text = scrolledtext.ScrolledText(
            msg_frame, 
            height=8, 
            wrap=tk.WORD,
            font=('Arial', 10),
            state='disabled'
        )
        self.decode_text.pack(fill='both', expand=True)
        
        # Copy button
        self.copy_btn = tk.Button(
            msg_frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard,
            font=('Arial', 9)
        )
        self.copy_btn.pack(anchor='e', pady=(5, 0))
    
    def update_char_count(self, event=None):
        """Update character count label"""
        count = len(self.encode_text.get('1.0', 'end-1c'))
        self.char_count_label.config(text=f"Characters: {count}")
    
    def check_password_strength(self, event=None):
        """Check and display password strength"""
        password = self.encode_password.get()
        
        if len(password) == 0:
            self.pwd_strength_label.config(text="", fg="gray")
            return
        
        strength = 0
        if len(password) >= 8:
            strength += 1
        if any(c.isupper() for c in password):
            strength += 1
        if any(c.islower() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            strength += 1
        
        if strength <= 2:
            self.pwd_strength_label.config(text="Weak", fg="red")
        elif strength <= 3:
            self.pwd_strength_label.config(text="Medium", fg="orange")
        else:
            self.pwd_strength_label.config(text="Strong", fg="green")
    
    def toggle_password_encode(self):
        """Toggle password visibility for encode tab"""
        if self.encode_password.cget('show') == '*':
            self.encode_password.config(show='')
        else:
            self.encode_password.config(show='*')
    
    def toggle_password_decode(self):
        """Toggle password visibility for decode tab"""
        if self.decode_password.cget('show') == '*':
            self.decode_password.config(show='')
        else:
            self.decode_password.config(show='*')
    
    def select_cover_image(self):
        """Select cover image for encoding"""
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp"), ("All files", "*.*")]
        )
        
        if file_path:
            self.cover_image_path = file_path
            filename = os.path.basename(file_path)
            
            # Calculate capacity
            capacity = self.crypto_stego.calculate_image_capacity(file_path)
            
            self.image_info_label.config(
                text=f"{filename} (Capacity: {capacity} bytes)",
                fg="green"
            )
            
            # Show preview
            self.show_image_preview(file_path, self.image_preview_label)
            
            self.update_status(f"Cover image selected: {filename}")
    
    def select_stego_image(self):
        """Select stego image for decoding"""
        file_path = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            self.stego_image_path = file_path
            filename = os.path.basename(file_path)
            
            self.stego_info_label.config(text=filename, fg="green")
            
            # Show preview
            self.show_image_preview(file_path, self.stego_preview_label)
            
            self.update_status(f"Stego image selected: {filename}")
    
    def show_image_preview(self, image_path, label_widget):
        """Show image preview"""
        try:
            img = Image.open(image_path)
            img.thumbnail((300, 300))
            photo = ImageTk.PhotoImage(img)
            label_widget.config(image=photo, text="")
            label_widget.image = photo  # Keep reference
        except Exception as e:
            label_widget.config(text=f"Preview error: {str(e)}")
    
    def encode_message(self):
        """Encode message in image"""
        # Validate inputs
        message = self.encode_text.get('1.0', 'end-1c').strip()
        password = self.encode_password.get()
        
        if not message:
            messagebox.showerror("Error", "Please enter a message to hide!")
            return
        
        if not password:
            messagebox.showerror("Error", "Please enter a password!")
            return
        
        if len(password) < 6:
            messagebox.showwarning("Warning", "Password is too short! Recommended: 8+ characters")
        
        if not self.cover_image_path:
            messagebox.showerror("Error", "Please select a cover image!")
            return
        
        # Ask for output location
        output_path = filedialog.asksaveasfilename(
            title="Save Stego Image",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        
        if not output_path:
            return
        
        # Encode message
        self.update_status("Encoding message...")
        self.root.update()
        
        success = self.crypto_stego.encode_message_in_image(
            self.cover_image_path,
            message,
            password,
            output_path
        )
        
        if success:
            messagebox.showinfo(
                "Success", 
                f"Message successfully hidden!\n\nStego image saved to:\n{output_path}"
            )
            self.update_status("Encoding complete!")
        else:
            messagebox.showerror("Error", "Failed to encode message. Image may be too small.")
            self.update_status("Encoding failed")
    
    def decode_message(self):
        """Decode message from image"""
        # Validate inputs
        password = self.decode_password.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter the decryption password!")
            return
        
        if not self.stego_image_path:
            messagebox.showerror("Error", "Please select a stego image!")
            return
        
        # Decode message
        self.update_status("Decoding message...")
        self.root.update()
        
        decrypted_message = self.crypto_stego.decode_message_from_image(
            self.stego_image_path,
            password
        )
        
        # Display result
        self.decode_text.config(state='normal')
        self.decode_text.delete('1.0', tk.END)
        self.decode_text.insert('1.0', decrypted_message)
        self.decode_text.config(state='disabled')
        
        if "error" in decrypted_message.lower():
            messagebox.showerror("Error", "Failed to decode message. Wrong password or corrupted image.")
            self.update_status("Decoding failed")
        else:
            messagebox.showinfo("Success", "Message successfully decrypted!")
            self.update_status("Decoding complete!")
    
    def copy_to_clipboard(self):
        """Copy decoded message to clipboard"""
        message = self.decode_text.get('1.0', 'end-1c')
        if message:
            self.root.clipboard_clear()
            self.root.clipboard_append(message)
            messagebox.showinfo("Copied", "Message copied to clipboard!")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = SteganographyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
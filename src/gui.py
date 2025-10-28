"""
Graphical User Interface for the password generator.
Built with tkinter for cross-platform compatibility.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys

from .generator import PasswordGenerator
from .validator import PasswordCriteria


class PasswordGeneratorGUI:
    """
    Modern GUI for password generation with tkinter.
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.generator = PasswordGenerator()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("🔐 Secure Password Generator")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass  # Icon not available, continue without it
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Custom colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2196F3"
        self.success_color = "#4CAF50"
        self.danger_color = "#f44336"
        
        self.root.configure(bg=self.bg_color)
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Header
        self.create_header()
        
        # Configuration Frame
        self.create_config_frame()
        
        # Generation Buttons
        self.create_button_frame()
        
        # Result Display
        self.create_result_frame()
        
        # Strength Analysis
        self.create_strength_frame()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Create the header section."""
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔐 Secure Password Generator",
            font=("Arial", 20, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(pady=25)
    
    def create_config_frame(self):
        """Create the configuration options frame."""
        config_frame = tk.LabelFrame(
            self.root,
            text="Password Configuration",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            padx=20,
            pady=20
        )
        config_frame.pack(fill=tk.BOTH, padx=20, pady=20)
        
        # Password Length
        length_frame = tk.Frame(config_frame, bg=self.bg_color)
        length_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            length_frame,
            text="Password Length:",
            font=("Arial", 11),
            bg=self.bg_color
        ).pack(side=tk.LEFT)
        
        self.length_var = tk.IntVar(value=16)
        self.length_spinbox = tk.Spinbox(
            length_frame,
            from_=8,
            to=128,
            textvariable=self.length_var,
            width=10,
            font=("Arial", 11)
        )
        self.length_spinbox.pack(side=tk.LEFT, padx=10)
        
        self.length_label = tk.Label(
            length_frame,
            text="(8-128 characters)",
            font=("Arial", 9),
            fg="gray",
            bg=self.bg_color
        )
        self.length_label.pack(side=tk.LEFT)
        
        # Length slider
        self.length_scale = tk.Scale(
            config_frame,
            from_=8,
            to=128,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            bg=self.bg_color,
            highlightthickness=0,
            length=500
        )
        self.length_scale.pack(fill=tk.X, pady=5)
        
        # Checkboxes for character types
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_symbols = tk.BooleanVar(value=True)
        
        checkbox_frame = tk.Frame(config_frame, bg=self.bg_color)
        checkbox_frame.pack(fill=tk.X, pady=15)
        
        tk.Checkbutton(
            checkbox_frame,
            text="Include Numbers (0-9)",
            variable=self.include_numbers,
            font=("Arial", 11),
            bg=self.bg_color,
            activebackground=self.bg_color
        ).pack(anchor=tk.W, pady=5)
        
        tk.Checkbutton(
            checkbox_frame,
            text="Include Symbols (!@#$%^&*)",
            variable=self.include_symbols,
            font=("Arial", 11),
            bg=self.bg_color,
            activebackground=self.bg_color
        ).pack(anchor=tk.W, pady=5)
    
    def create_button_frame(self):
        """Create the action buttons frame."""
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Generate button
        self.generate_btn = tk.Button(
            button_frame,
            text="🔑 Generate Password",
            command=self.generate_password,
            font=("Arial", 12, "bold"),
            bg=self.success_color,
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            cursor="hand2",
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10
        )
        self.generate_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        # Copy button
        self.copy_btn = tk.Button(
            button_frame,
            text="📋 Copy to Clipboard",
            command=self.copy_to_clipboard,
            font=("Arial", 12, "bold"),
            bg=self.primary_color,
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            cursor="hand2",
            relief=tk.RAISED,
            bd=3,
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.copy_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
    def create_result_frame(self):
        """Create the password result display frame."""
        result_frame = tk.LabelFrame(
            self.root,
            text="Generated Password",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            padx=20,
            pady=20
        )
        result_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
        
        # Password display (read-only text widget)
        self.password_text = tk.Text(
            result_frame,
            height=3,
            font=("Courier New", 14, "bold"),
            wrap=tk.WORD,
            bg="white",
            fg="#333",
            relief=tk.SUNKEN,
            bd=2,
            padx=10,
            pady=10
        )
        self.password_text.pack(fill=tk.BOTH, expand=True)
        self.password_text.insert("1.0", "Click 'Generate Password' to create a secure password")
        self.password_text.config(state=tk.DISABLED)
    
    def create_strength_frame(self):
        """Create the password strength analysis frame."""
        self.strength_frame = tk.LabelFrame(
            self.root,
            text="Password Strength Analysis",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            padx=20,
            pady=20
        )
        self.strength_frame.pack(fill=tk.BOTH, padx=20, pady=10)
        
        # Strength indicators
        self.strength_level_label = tk.Label(
            self.strength_frame,
            text="Strength: -",
            font=("Arial", 11, "bold"),
            bg=self.bg_color
        )
        self.strength_level_label.pack(anchor=tk.W, pady=5)
        
        self.entropy_label = tk.Label(
            self.strength_frame,
            text="Entropy: - bits",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="gray"
        )
        self.entropy_label.pack(anchor=tk.W, pady=2)
        
        self.charset_label = tk.Label(
            self.strength_frame,
            text="Character Set Size: -",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="gray"
        )
        self.charset_label.pack(anchor=tk.W, pady=2)
        
        self.composition_label = tk.Label(
            self.strength_frame,
            text="Composition: -",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="gray"
        )
        self.composition_label.pack(anchor=tk.W, pady=2)
    
    def create_footer(self):
        """Create the footer section."""
        footer_frame = tk.Frame(self.root, bg=self.bg_color, height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=10)
        
        footer_label = tk.Label(
            footer_frame,
            text="Made with ❤️ and Python | Secure Password Generator v1.0",
            font=("Arial", 9),
            bg=self.bg_color,
            fg="gray"
        )
        footer_label.pack()
    
    def generate_password(self):
        """Generate a new password based on user settings."""
        try:
            # Get configuration
            length = self.length_var.get()
            include_numbers = self.include_numbers.get()
            include_symbols = self.include_symbols.get()
            
            # Validate length
            if length < 8 or length > 128:
                messagebox.showerror(
                    "Invalid Length",
                    "Password length must be between 8 and 128 characters."
                )
                return
            
            # Create criteria
            criteria = PasswordCriteria(
                length=length,
                include_numbers=include_numbers,
                include_symbols=include_symbols
            )
            
            # Generate password
            password = self.generator.generate(criteria)
            
            # Display password
            self.password_text.config(state=tk.NORMAL)
            self.password_text.delete("1.0", tk.END)
            self.password_text.insert("1.0", password)
            self.password_text.config(state=tk.DISABLED)
            
            # Enable copy button
            self.copy_btn.config(state=tk.NORMAL)
            
            # Analyze and display strength
            self.display_strength_analysis(password)
            
            # Show success message
            self.root.after(
                100,
                lambda: messagebox.showinfo(
                    "Success",
                    "Password generated successfully!\nClick 'Copy to Clipboard' to copy it."
                )
            )
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def display_strength_analysis(self, password):
        """
        Display password strength analysis.
        
        Args:
            password: The password to analyze
        """
        strength = self.generator.estimate_strength(password)
        
        # Update strength level with color
        level = strength['strength_level']
        color_map = {
            "Weak": self.danger_color,
            "Medium": "#FF9800",
            "Strong": "#2196F3",
            "Very Strong": self.success_color
        }
        
        self.strength_level_label.config(
            text=f"Strength: {level}",
            fg=color_map.get(level, "black")
        )
        
        # Update other metrics
        self.entropy_label.config(
            text=f"Entropy: {strength['entropy_bits']:.2f} bits"
        )
        
        self.charset_label.config(
            text=f"Character Set Size: {strength['charset_size']}"
        )
        
        # Build composition string
        composition = []
        if strength['has_lowercase']:
            composition.append("lowercase")
        if strength['has_uppercase']:
            composition.append("UPPERCASE")
        if strength['has_digits']:
            composition.append("digits")
        if strength['has_symbols']:
            composition.append("symbols")
        
        self.composition_label.config(
            text=f"Composition: {', '.join(composition)}"
        )
    
    def copy_to_clipboard(self):
        """Copy the generated password to clipboard."""
        password = self.password_text.get("1.0", tk.END).strip()
        
        if password and password != "Click 'Generate Password' to create a secure password":
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()  # Required for clipboard to work
            
            messagebox.showinfo(
                "Copied",
                "Password copied to clipboard!\n\nRemember to store it securely in a password manager."
            )
        else:
            messagebox.showwarning(
                "No Password",
                "Please generate a password first."
            )
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main():
    """Entry point for the GUI application."""
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    app.run()


if __name__ == "__main__":
    main()

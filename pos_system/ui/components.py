import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Optional
from PIL import Image
import os
import random


class LoginWindow(ctk.CTkToplevel):
    """Login window for user authentication"""
    
    def __init__(self, parent, auth_manager, on_success: Callable):
        super().__init__(parent)
        
        self.auth_manager = auth_manager
        self.on_success = on_success
        
        self.title("Shine Art Studio - Login")
        
        # Set window size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = int(screen_width * 0.75)
        window_height = int(screen_height * 0.8)
        
        # Center window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Prevent resize
        self.resizable(False, False)
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create login form widgets"""
        
        # Set window background
        self.configure(fg_color="#1a1a1a")
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="#1a1a1a")
        main_container.pack(fill="both", expand=True)
        
        # Left side - Image panel
        left_panel = ctk.CTkFrame(main_container, fg_color="#1a1a1a", corner_radius=0)
        left_panel.pack(side="left", fill="both", expand=True)
        
        # Random image selection
        self.display_image = None
        try:
            assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
            image_files = ["Image1.jpg", "image2.jpg", "image3.jpg"]
            available_images = [os.path.join(assets_path, img) for img in image_files if os.path.exists(os.path.join(assets_path, img))]
            
            if available_images:
                selected_image_path = random.choice(available_images)
                login_img = Image.open(selected_image_path)
                
                # Calculate image size
                window_height = int(self.winfo_screenheight() * 0.8)
                target_height = window_height - 100
                aspect_ratio = login_img.width / login_img.height
                target_width = int(target_height * aspect_ratio)
                
                self.display_image = ctk.CTkImage(
                    light_image=login_img,
                    dark_image=login_img,
                    size=(target_width, target_height)
                )
                
                img_label = ctk.CTkLabel(left_panel, image=self.display_image, text="")
                img_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"Could not load login image: {e}")
            fallback = ctk.CTkLabel(
                left_panel,
                text="Shine Art Studio",
                font=ctk.CTkFont(size=48, weight="bold"),
                text_color="white"
            )
            fallback.place(relx=0.5, rely=0.5, anchor="center")
        
        # Right side - Login form panel
        right_panel = ctk.CTkFrame(main_container, fg_color="#1a1a1a", width=520, corner_radius=0)
        right_panel.pack(side="right", fill="y")
        right_panel.pack_propagate(False)
        
        # Form container
        form_container = ctk.CTkFrame(right_panel, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo
        self.logo_image = None
        try:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo001.png")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                self.logo_image = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(110, 110))
                logo_label = ctk.CTkLabel(form_container, image=self.logo_image, text="")
                logo_label.pack(pady=(0, 25))
        except Exception as e:
            print(f"Could not load logo: {e}")
        
        # Title with hierarchy
        title_label = ctk.CTkLabel(
            form_container,
            text="Shine Art Studio",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=(0, 8))
        
        subtitle_label = ctk.CTkLabel(
            form_container,
            text="Photography POS System",
            font=ctk.CTkFont(size=15),
            text_color="#888888"
        )
        subtitle_label.pack(pady=(0, 50))
        
        # Username field
        username_label = ctk.CTkLabel(
            form_container,
            text="Username",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#cccccc",
            anchor="w"
        )
        username_label.pack(pady=(0, 10), anchor="w", padx=5)
        
        self.username_entry = ctk.CTkEntry(
            form_container,
            placeholder_text="Enter your username",
            height=48,
            width=420,
            font=ctk.CTkFont(size=15),
            border_width=2,
            corner_radius=8
        )
        self.username_entry.pack(pady=(0, 25))
        
        # Password field
        password_label = ctk.CTkLabel(
            form_container,
            text="Password",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#cccccc",
            anchor="w"
        )
        password_label.pack(pady=(0, 10), anchor="w", padx=5)
        
        self.password_entry = ctk.CTkEntry(
            form_container,
            placeholder_text="Enter your password",
            show="●",
            height=48,
            width=420,
            font=ctk.CTkFont(size=15),
            border_width=2,
            corner_radius=8
        )
        self.password_entry.pack(pady=(0, 35))
        
        # Login button with enhanced styling
        login_btn = ctk.CTkButton(
            form_container,
            text="LOGIN",
            command=self.handle_login,
            height=52,
            width=420,
            font=ctk.CTkFont(size=17, weight="bold"),
            fg_color="#1f538d",
            hover_color="#163d6b",
            corner_radius=8,
            border_width=0
        )
        login_btn.pack(pady=(0, 20))
        
        # Footer
        footer_label = ctk.CTkLabel(
            right_panel,
            text="Developed by Malinda Prabath\n© 2025 Photography Studio Management System. All rights reserved.",
            font=ctk.CTkFont(size=11),
            text_color="#555555",
            justify="center"
        )
        footer_label.pack(side="bottom", pady=25)
        
        # Keyboard bindings
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        
        # Set focus
        self.after(100, lambda: self.username_entry.focus())
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username:
            messagebox.showerror(
                "Login Error",
                "Please enter your username."
            )
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showerror(
                "Login Error",
                "Please enter your password."
            )
            self.password_entry.focus()
            return
        
        user = self.auth_manager.authenticate(username, password)
        
        if user:
            messagebox.showinfo(
                "Login Successful",
                f"Welcome back, {user['full_name']}!\n\nRole: {user['role'].title()}"
            )
            self.destroy()
            self.on_success(user)
        else:
            messagebox.showerror(
                "Authentication Failed",
                "Invalid username or password.\nPlease try again."
            )
            self.password_entry.delete(0, 'end')
            self.password_entry.focus()


class MessageDialog:
    """Utility class for showing messages"""
    
    @staticmethod
    def show_error(title: str, message: str):
        """Show error message"""
        messagebox.showerror(title, message)
    
    @staticmethod
    def show_success(title: str, message: str):
        """Show success message"""
        messagebox.showinfo(title, message)
    
    @staticmethod
    def show_warning(title: str, message: str):
        """Show warning message"""
        messagebox.showwarning(title, message)
    
    @staticmethod
    def show_confirm(title: str, message: str) -> bool:
        """Show confirmation dialog"""
        return messagebox.askyesno(title, message)


class BaseFrame(ctk.CTkFrame):
    """Base frame with common functionality"""
    
    def __init__(self, parent, auth_manager, db_manager):
        super().__init__(parent, fg_color="transparent")
        self.auth_manager = auth_manager
        self.db_manager = db_manager
        
    def validate_number(self, value: str, allow_decimal: bool = False) -> bool:
        """Validate if value is a number"""
        if not value:
            return False
        try:
            if allow_decimal:
                float(value)
            else:
                int(value)
            return True
        except ValueError:
            return False
    
    def validate_mobile(self, mobile: str) -> bool:
        """Validate mobile number (10 digits)"""
        return mobile.isdigit() and len(mobile) == 10
    
    def is_admin(self) -> bool:
        """Check if current user is admin"""
        return self.auth_manager.is_admin()

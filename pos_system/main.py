import customtkinter as ctk
from database import DatabaseManager
from auth import AuthManager
from ui.components import LoginWindow
from ui.customer_frame import CustomerManagementFrame
from ui.service_frame import ServiceManagementFrame
from ui.frame_frame import FrameManagementFrame
from ui.billing_frame import BillingFrame
from ui.booking_frame import BookingManagementFrame
from ui.invoice_history_frame import InvoiceHistoryFrame


class MainApplication(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Window setup
        self.title("Shine Art Studio - POS System")
        self.geometry("1400x800")
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 700
        y = (self.winfo_screenheight() // 2) - 400
        self.geometry(f"1400x800+{x}+{y}")
        
        # Initialize managers
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager()
        
        # Current user
        self.current_user = None
        
        # Create main container
        self.main_container = None
        self.content_frame = None
        
        # Show login
        self.show_login()
    
    def show_login(self):
        """Show login window"""
        login_window = LoginWindow(self, self.auth_manager, self.on_login_success)
    
    def on_login_success(self, user):
        """Handle successful login"""
        self.current_user = user
        self.create_main_interface()
    
    def create_main_interface(self):
        """Create main application interface"""
        
        # Main container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Top bar
        top_bar = ctk.CTkFrame(self.main_container, height=70, fg_color="#1f538d")
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)
        
        # Logo/Title
        title_label = ctk.CTkLabel(
            top_bar,
            text="Shine Art Studio - POS System",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left", padx=30, pady=15)
        
        # User info
        user_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        user_frame.pack(side="right", padx=30)
        
        user_label = ctk.CTkLabel(
            user_frame,
            text=f"User: {self.current_user['full_name']} ({self.current_user['role']})",
            font=ctk.CTkFont(size=13),
            text_color="white"
        )
        user_label.pack(side="left", padx=10)
        
        logout_btn = ctk.CTkButton(
            user_frame,
            text="Logout",
            command=self.logout,
            width=100,
            height=35,
            fg_color="red",
            hover_color="darkred"
        )
        logout_btn.pack(side="left", padx=10)
        
        # Sidebar
        sidebar = ctk.CTkFrame(self.main_container, width=220, fg_color="#2b2b2b")
        sidebar.pack(fill="y", side="left")
        sidebar.pack_propagate(False)
        
        # Navigation buttons
        nav_buttons = [
            ("💰 Billing", self.show_billing),
            ("👥 Customers", self.show_customers),
            ("📋 Services", self.show_services),
            ("🖼️ Photo Frames", self.show_frames),
            ("📅 Bookings", self.show_bookings),
            ("📄 Invoice History", self.show_invoice_history),
        ]
        
        ctk.CTkLabel(
            sidebar,
            text="Navigation",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 10))
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                width=180,
                height=45,
                font=ctk.CTkFont(size=14),
                anchor="w",
                fg_color="transparent",
                hover_color="#1f538d"
            )
            btn.pack(pady=5, padx=20)
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.pack(fill="both", expand=True, side="right", padx=10, pady=10)
        
        # Show default view (Billing)
        self.show_billing()
    
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_billing(self):
        """Show billing frame"""
        self.clear_content()
        frame = BillingFrame(self.content_frame, self.auth_manager, self.db_manager)
        frame.pack(fill="both", expand=True)
    
    def show_customers(self):
        """Show customer management frame"""
        self.clear_content()
        frame = CustomerManagementFrame(self.content_frame, self.auth_manager, self.db_manager)
        frame.pack(fill="both", expand=True)
    
    def show_services(self):
        """Show service management frame"""
        self.clear_content()
        frame = ServiceManagementFrame(self.content_frame, self.auth_manager, self.db_manager)
        frame.pack(fill="both", expand=True)
    
    def show_frames(self):
        """Show photo frame management frame"""
        self.clear_content()
        frame = FrameManagementFrame(self.content_frame, self.auth_manager, self.db_manager)
        frame.pack(fill="both", expand=True)
    
    def show_bookings(self):
        """Show booking management frame"""
        self.clear_content()
        frame = BookingManagementFrame(self.content_frame, self.auth_manager, self.db_manager)
        frame.pack(fill="both", expand=True)
    
    def show_invoice_history(self):
        """Show invoice history frame"""
        self.clear_content()
        frame = InvoiceHistoryFrame(self.content_frame, self.auth_manager, self.db_manager)
        frame.pack(fill="both", expand=True)
    
    def logout(self):
        """Logout and return to login screen"""
        self.auth_manager.logout()
        self.current_user = None
        
        # Clear main container
        if self.main_container:
            self.main_container.destroy()
            self.main_container = None
        
        # Show login
        self.show_login()


def main():
    """Main entry point"""
    # Initialize database
    from database import initialize_database
    initialize_database()
    
    # Start application
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    main()

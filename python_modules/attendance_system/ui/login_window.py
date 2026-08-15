"""
Future Mall - Attendance System Login Window
"""

import tkinter as tk
from tkinter import messagebox
from typing import Optional, Callable

from .base import (Theme, ModernButton, ModernEntry, ModernLabel, Card, StyledWidget)


class LoginWindow:
    """Login window for the attendance system."""

    def __init__(self, root: tk.Tk, on_login_success: Callable[[str], None]):
        self.root = root
        self.on_login_success = on_login_success

        # Import here to avoid circular imports
        from ..models import Employee

        self.Employee = Employee

        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Configure the login window."""
        self.root.title("Future Mall - Attendance System")
        self.root.geometry("420x520")
        self.root.minsize(400, 500)
        self.root.configure(bg=Theme.BG)
        self.root.resizable(False, False)

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 210
        y = (self.root.winfo_screenheight() // 2) - 260
        self.root.geometry(f"+{x}+{y}")

        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        """Create login form widgets."""
        # Main container
        main_frame = tk.Frame(self.root, bg=Theme.BG)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=Theme.SPACING_XL, pady=Theme.SPACING_XL)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Login card
        self.login_card = Card(main_frame, padding=Theme.SPACING_XL)
        self.login_card.grid(row=0, column=0, sticky="nsew")

        # Logo and title
        self.create_header()

        # Form fields
        self.create_form()

        # Login button
        self.create_login_button()

        # Footer
        self.create_footer()

    def create_header(self):
        """Create login header with logo."""
        header_frame = tk.Frame(self.login_card.content, bg=Theme.SURFACE)
        header_frame.pack(fill="x", pady=(0, Theme.SPACING_LG))

        # Logo
        logo_text = ModernLabel(header_frame, text="🏢", style="display")
        logo_text.config(fg=Theme.PRIMARY)
        logo_text.pack()

        # Title
        title = ModernLabel(header_frame, text="Future Mall", style="display")
        title.pack(pady=(Theme.SPACING_SM, 0))

        # Subtitle
        subtitle = ModernLabel(header_frame, text="Attendance System", style="muted")
        subtitle.pack()

        # Divider
        divider = tk.Frame(self.login_card.content, height=2, bg=Theme.PRIMARY_LIGHT)
        divider.pack(fill="x", pady=Theme.SPACING_MD)

    def create_form(self):
        """Create login form fields."""
        form_frame = tk.Frame(self.login_card.content, bg=Theme.SURFACE)
        form_frame.pack(fill="x")

        # Employee ID
        ModernLabel(form_frame, text="Employee ID", style="subheading").pack(anchor="w", pady=(0, Theme.SPACING_XS))

        self.employee_id_entry = ModernEntry(form_frame, placeholder="EMP001")
        self.employee_id_entry.pack(fill="x", pady=(0, Theme.SPACING_MD), ipady=8)

        # Password
        ModernLabel(form_frame, text="Password", style="subheading").pack(anchor="w", pady=(0, Theme.SPACING_XS))

        self.password_entry = ModernEntry(form_frame, placeholder="Enter password", show="•")
        self.password_entry.pack(fill="x", pady=(0, Theme.SPACING_MD), ipady=8)

        # Remember me / Forgot password
        bottom_frame = tk.Frame(form_frame, bg=Theme.SURFACE)
        bottom_frame.pack(fill="x", pady=(0, Theme.SPACING_MD))

        self.remember_var = tk.BooleanVar()
        remember_cb = tk.Checkbutton(bottom_frame, text="Remember me",
                                     variable=self.remember_var,
                                     bg=Theme.SURFACE, fg=Theme.TEXT,
                                     font=Theme.FONT_SMALL,
                                     activebackground=Theme.SURFACE,
                                     activeforeground=Theme.TEXT,
                                     selectcolor=Theme.SURFACE)
        remember_cb.pack(side="left")

        forgot_btn = ModernButton(bottom_frame, text="Forgot Password?",
                                  style="ghost", command=self.on_forgot_password)
        forgot_btn.pack(side="right")

    def create_login_button(self):
        """Create login button."""
        btn_frame = tk.Frame(self.login_card.content, bg=Theme.SURFACE)
        btn_frame.pack(fill="x", pady=Theme.SPACING_MD)

        self.login_btn = ModernButton(
            btn_frame,
            text="Sign In",
            style="primary",
            command=self.on_login,
            height=2
        )
        self.login_btn.pack(fill="x", ipady=8)

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self.on_login())

    def create_footer(self):
        """Create footer with demo credentials."""
        footer_frame = tk.Frame(self.login_card.content, bg=Theme.SURFACE)
        footer_frame.pack(fill="x", pady=(Theme.SPACING_LG, 0))

        # Divider
        divider = tk.Frame(footer_frame, height=1, bg=Theme.BORDER_LIGHT)
        divider.pack(fill="x", pady=(0, Theme.SPACING_MD))

        # Demo credentials
        demo_text = ModernLabel(
            footer_frame,
            text="Demo Credentials:",
            style="small"
        )
        demo_text.pack()

        credentials = [
            ("Admin", "EMP003 / password123"),
            ("Supervisor", "EMP002 / password123"),
            ("Employee", "EMP001 / password123"),
        ]

        for role, creds in credentials:
            cred_frame = tk.Frame(footer_frame, bg=Theme.SURFACE)
            cred_frame.pack(fill="x", pady=1)

            ModernLabel(cred_frame, text=f"{role}:", style="small").pack(side="left")
            ModernLabel(cred_frame, text=creds, style="muted").pack(side="left", padx=(Theme.SPACING_XS, 0))

    def on_login(self):
        """Handle login attempt."""
        employee_id = self.employee_id_entry.get_value().strip().upper()
        password = self.password_entry.get()

        if not employee_id:
            self.show_error("Please enter your Employee ID")
            return

        if not password:
            self.show_error("Please enter your password")
            return

        # Disable button during authentication
        self.login_btn.set_state("disabled")
        self.login_btn.config(text="Signing in...")
        self.root.update()

        # Authenticate
        employee = self.Employee.authenticate(employee_id, password)

        # Re-enable button
        self.login_btn.set_state("normal")
        self.login_btn.config(text="Sign In")

        if employee:
            # Success
            self.on_login_success(employee.role)
        else:
            self.show_error("Invalid Employee ID or password")

    def on_forgot_password(self):
        """Handle forgot password."""
        messagebox.showinfo(
            "Reset Password",
            "Please contact your administrator to reset your password.\n\n"
            "Demo passwords:\n"
            "• Admin: EMP003 / password123\n"
            "• Supervisor: EMP002 / password123\n"
            "• Employee: EMP001 / password123"
        )

    def show_error(self, message: str):
        """Show error message."""
        messagebox.showerror("Login Error", message)
        self.password_entry.delete(0, tk.END)
        self.password_entry.focus()
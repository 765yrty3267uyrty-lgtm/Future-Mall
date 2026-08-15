#!/usr/bin/env python3
"""
Future Mall - Attendance System Main Entry Point
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
sys.path.insert(0, os.path.dirname(__file__))

from ui.login_window import LoginWindow
from ui.employee_dashboard import EmployeeDashboard
from ui.supervisor_dashboard import SupervisorDashboard
from ui.admin_dashboard import AdminDashboard
from models import get_db


class AttendanceApp:
    """Main application controller."""

    def __init__(self):
        self.root = tk.Tk()
        self.current_window = None
        self.current_user = None

        # Initialize database and seed data
        self.init_database()

    def init_database(self):
        """Initialize database with sample data."""
        db = get_db()
        db.seed_sample_data()

    def run(self):
        """Start the application."""
        self.show_login()
        self.root.mainloop()

    def show_login(self):
        """Show login window."""
        self.clear_window()

        # Configure root for login
        self.root.title("Future Mall - Attendance System")
        self.root.geometry("420x520")
        self.root.minsize(400, 500)
        self.root.configure(bg="#F8FAFC")

        # Create login window
        self.current_window = LoginWindow(self.root, self.on_login_success)

    def on_login_success(self, role: str):
        """Handle successful login."""
        self.current_user_role = role
        self.show_dashboard(role)

    def show_dashboard(self, role: str):
        """Show appropriate dashboard based on role."""
        self.clear_window()

        # Maximize window for dashboards
        self.root.state('zoomed')
        self.root.title(f"Future Mall - Attendance System ({role.title()})")
        self.root.configure(bg="#F8FAFC")

        # Create main container
        main_frame = tk.Frame(self.root, bg="#F8FAFC")
        main_frame.pack(fill="both", expand=True)

        if role == "admin":
            self.current_window = AdminDashboard(main_frame, self.current_user_id, self.show_login)
        elif role == "supervisor":
            self.current_window = SupervisorDashboard(main_frame, self.current_user_id, self.show_login)
        else:
            self.current_window = EmployeeDashboard(main_frame, self.current_user_id, self.show_login)

    def clear_window(self):
        """Clear all widgets from root."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def set_current_user(self, employee_id: int):
        """Set current user ID."""
        self.current_user_id = employee_id


def main():
    """Entry point."""
    try:
        app = AttendanceApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
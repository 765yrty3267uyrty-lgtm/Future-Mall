"""
Future Mall - Attendance System UI Package
"""

from .base import Theme, StyledWidget, ModernButton, Card, ModernEntry, ModernLabel
from .login_window import LoginWindow
from .employee_dashboard import EmployeeDashboard
from .supervisor_dashboard import SupervisorDashboard
from .admin_dashboard import AdminDashboard

__all__ = [
    'Theme', 'StyledWidget', 'ModernButton', 'Card', 'ModernEntry', 'ModernLabel',
    'LoginWindow', 'EmployeeDashboard', 'SupervisorDashboard', 'AdminDashboard'
]
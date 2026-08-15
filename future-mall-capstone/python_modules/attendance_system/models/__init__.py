"""
Future Mall - Attendance System Models Package
"""

from .database import Database, get_db
from .employee import Employee
from .attendance import Attendance

__all__ = ['Database', 'get_db', 'Employee', 'Attendance']
"""
Future Mall - Attendance System Database Module
Handles SQLite database connection, migrations, and schema.
"""

import sqlite3
import os
from contextlib import contextmanager
from typing import Optional

# Add shared constants to path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'shared'))
from constants import ATTENDANCE


class Database:
    """SQLite database manager with connection pooling and migrations."""

    def __init__(self, db_path: str = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, 'data', 'attendance.db')
        self.db_path = db_path
        self._ensure_db_dir()
        self._init_schema()

    def _ensure_db_dir(self) -> None:
        """Ensure database directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a query and return cursor."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Fetch a single row."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()) -> list:
        """Fetch all rows."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def _init_schema(self) -> None:
        """Initialize database schema with migrations."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Employees table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    position TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    date_joined DATE NOT NULL,
                    role TEXT NOT NULL DEFAULT 'employee',
                    password_hash TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Attendance records table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER NOT NULL,
                    date DATE NOT NULL,
                    check_in TIMESTAMP,
                    check_out TIMESTAMP,
                    status TEXT NOT NULL DEFAULT 'absent',
                    working_hours REAL DEFAULT 0,
                    overtime_hours REAL DEFAULT 0,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (employee_id) REFERENCES employees(id),
                    UNIQUE(employee_id, date)
                )
            """)

            # Leave requests table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS leaves (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    leave_type TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    reason TEXT,
                    FOREIGN KEY (employee_id) REFERENCES employees(id)
                )
            """)

            # Settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)

            # Insert default settings
            defaults = {
                'work_start': ATTENDANCE['work_start'],
                'work_end': ATTENDANCE['work_end'],
                'late_threshold': ATTENDANCE['late_threshold'],
            }
            for key, value in defaults.items():
                cursor.execute(
                    "INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)",
                    (key, value)
                )

            conn.commit()

    def seed_sample_data(self) -> None:
        """Seed database with sample employees for testing."""
        import hashlib

        sample_employees = [
            {
                'employee_id': 'EMP001',
                'full_name': 'Ahmed Hassan',
                'department': 'IT',
                'position': 'Developer',
                'email': 'ahmed@futuremall.com',
                'phone': '+201000000001',
                'date_joined': '2024-01-15',
                'role': 'employee',
                'password': 'password123',
            },
            {
                'employee_id': 'EMP002',
                'full_name': 'Sara Ali',
                'department': 'HR',
                'position': 'HR Manager',
                'email': 'sara@futuremall.com',
                'phone': '+201000000002',
                'date_joined': '2023-11-01',
                'role': 'supervisor',
                'password': 'password123',
            },
            {
                'employee_id': 'EMP003',
                'full_name': 'Mohamed Omar',
                'department': 'Operations',
                'position': 'Store Manager',
                'email': 'mohamed@futuremall.com',
                'phone': '+201000000003',
                'date_joined': '2023-06-10',
                'role': 'admin',
                'password': 'password123',
            },
            {
                'employee_id': 'EMP004',
                'full_name': 'Fatima Mahmoud',
                'department': 'Finance',
                'position': 'Accountant',
                'email': 'fatima@futuremall.com',
                'phone': '+201000000004',
                'date_joined': '2024-03-01',
                'role': 'employee',
                'password': 'password123',
            },
            {
                'employee_id': 'EMP005',
                'full_name': 'Omar Khalid',
                'department': 'Marketing',
                'position': 'Marketing Specialist',
                'email': 'omar@futuremall.com',
                'phone': '+201000000005',
                'date_joined': '2024-02-15',
                'role': 'employee',
                'password': 'password123',
            },
        ]

        with self.get_connection() as conn:
            cursor = conn.cursor()
            for emp in sample_employees:
                password_hash = hashlib.sha256(emp['password'].encode()).hexdigest()
                cursor.execute("""
                    INSERT OR IGNORE INTO employees
                    (employee_id, full_name, department, position, email, phone,
                     date_joined, role, password_hash, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                """, (
                    emp['employee_id'], emp['full_name'], emp['department'],
                    emp['position'], emp['email'], emp['phone'],
                    emp['date_joined'], emp['role'], password_hash
                ))
            conn.commit()


# Global database instance
db = Database()


def get_db() -> Database:
    """Get the global database instance."""
    return db
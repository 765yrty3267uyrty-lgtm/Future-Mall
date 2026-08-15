"""
Future Mall - Attendance System Employee Model
Handles employee data operations.
"""

import hashlib
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from .database import get_db


@dataclass
class Employee:
    """Employee data model."""
    id: int
    employee_id: str
    full_name: str
    department: str
    position: str
    email: Optional[str]
    phone: Optional[str]
    date_joined: str
    role: str
    is_active: bool
    created_at: str

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Employee':
        """Create Employee from database row."""
        return cls(
            id=row['id'],
            employee_id=row['employee_id'],
            full_name=row['full_name'],
            department=row['department'],
            position=row['position'],
            email=row['email'],
            phone=row['phone'],
            date_joined=row['date_joined'],
            role=row['role'],
            is_active=bool(row['is_active']),
            created_at=row['created_at'],
        )

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def create(cls, data: Dict[str, Any]) -> 'Employee':
        """Create a new employee."""
        db = get_db()
        password_hash = cls.hash_password(data['password'])

        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO employees
                (employee_id, full_name, department, position, email, phone,
                 date_joined, role, password_hash, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """, (
                data['employee_id'], data['full_name'], data['department'],
                data['position'], data.get('email'), data.get('phone'),
                data['date_joined'], data.get('role', 'employee'), password_hash
            ))
            conn.commit()
            emp_id = cursor.lastrowid

        return cls.get_by_id(emp_id)

    @classmethod
    def get_by_id(cls, emp_id: int) -> Optional['Employee']:
        """Get employee by internal ID."""
        db = get_db()
        row = db.fetch_one("SELECT * FROM employees WHERE id = ?", (emp_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_by_employee_id(cls, employee_id: str) -> Optional['Employee']:
        """Get employee by employee_id (EMP001 format)."""
        db = get_db()
        row = db.fetch_one("SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_all(cls, filters: Dict[str, Any] = None) -> List['Employee']:
        """Get all employees with optional filters."""
        db = get_db()
        query = "SELECT * FROM employees WHERE 1=1"
        params = []

        if filters:
            if filters.get('department'):
                query += " AND department = ?"
                params.append(filters['department'])
            if filters.get('role'):
                query += " AND role = ?"
                params.append(filters['role'])
            if filters.get('is_active') is not None:
                query += " AND is_active = ?"
                params.append(1 if filters['is_active'] else 0)

        query += " ORDER BY employee_id"
        rows = db.fetch_all(query, tuple(params))
        return [cls.from_row(row) for row in rows]

    @classmethod
    def get_by_role(cls, role: str) -> List['Employee']:
        """Get employees by role."""
        return cls.get_all({'role': role})

    @classmethod
    def authenticate(cls, employee_id: str, password: str) -> Optional['Employee']:
        """Authenticate employee with employee_id and password."""
        emp = cls.get_by_employee_id(employee_id)
        if emp and emp.is_active:
            password_hash = cls.hash_password(password)
            db = get_db()
            row = db.fetch_one(
                "SELECT * FROM employees WHERE employee_id = ? AND password_hash = ?",
                (employee_id, password_hash)
            )
            return cls.from_row(row) if row else None
        return None

    @classmethod
    def update(cls, emp_id: int, data: Dict[str, Any]) -> Optional['Employee']:
        """Update employee data."""
        db = get_db()
        allowed_fields = ['full_name', 'department', 'position', 'email',
                          'phone', 'role', 'is_active']
        updates = []
        params = []

        for field in allowed_fields:
            if field in data:
                updates.append(f"{field} = ?")
                params.append(data[field])

        if not updates:
            return cls.get_by_id(emp_id)

        params.append(emp_id)
        query = f"UPDATE employees SET {', '.join(updates)} WHERE id = ?"

        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

        return cls.get_by_id(emp_id)

    @classmethod
    def update_password(cls, emp_id: int, new_password: str) -> bool:
        """Update employee password."""
        db = get_db()
        password_hash = cls.hash_password(new_password)

        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE employees SET password_hash = ? WHERE id = ?",
                (password_hash, emp_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @classmethod
    def delete(cls, emp_id: int) -> bool:
        """Delete an employee (soft delete - set inactive)."""
        return cls.update(emp_id, {'is_active': False}) is not None

    @classmethod
    def hard_delete(cls, emp_id: int) -> bool:
        """Permanently delete an employee."""
        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
            conn.commit()
            return cursor.rowcount > 0

    @classmethod
    def count_by_role(cls) -> Dict[str, int]:
        """Count employees by role."""
        db = get_db()
        rows = db.fetch_all("""
            SELECT role, COUNT(*) as count
            FROM employees
            WHERE is_active = 1
            GROUP BY role
        """)
        return {row['role']: row['count'] for row in rows}

    @classmethod
    def count_by_department(cls) -> Dict[str, int]:
        """Count employees by department."""
        db = get_db()
        rows = db.fetch_all("""
            SELECT department, COUNT(*) as count
            FROM employees
            WHERE is_active = 1
            GROUP BY department
        """)
        return {row['department']: row['count'] for row in rows}
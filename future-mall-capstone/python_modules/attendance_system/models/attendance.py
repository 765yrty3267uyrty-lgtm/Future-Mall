"""
Future Mall - Attendance System Attendance Model
Handles attendance records, check-in/out, and reports.
"""

import sqlite3
from datetime import datetime, date, time, timedelta
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from .database import get_db
from .employee import Employee


@dataclass
class Attendance:
    """Attendance record data model."""
    id: int
    employee_id: int
    date: str
    check_in: Optional[str]
    check_out: Optional[str]
    status: str
    working_hours: float
    overtime_hours: float
    notes: Optional[str]
    created_at: str

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Attendance':
        """Create Attendance from database row."""
        return cls(
            id=row['id'],
            employee_id=row['employee_id'],
            date=row['date'],
            check_in=row['check_in'],
            check_out=row['check_out'],
            status=row['status'],
            working_hours=row['working_hours'] or 0.0,
            overtime_hours=row['overtime_hours'] or 0.0,
            notes=row['notes'],
            created_at=row['created_at'],
        )

    @classmethod
    def get_today(cls, employee_id: int) -> Optional['Attendance']:
        """Get today's attendance record for an employee."""
        db = get_db()
        today = date.today().isoformat()
        row = db.fetch_one(
            "SELECT * FROM attendance WHERE employee_id = ? AND date = ?",
            (employee_id, today)
        )
        return cls.from_row(row) if row else None

    @classmethod
    def get_by_id(cls, attendance_id: int) -> Optional['Attendance']:
        """Get attendance by ID."""
        db = get_db()
        row = db.fetch_one("SELECT * FROM attendance WHERE id = ?", (attendance_id,))
        return cls.from_row(row) if row else None

    @classmethod
    def get_history(cls, employee_id: int, start_date: str, end_date: str) -> List['Attendance']:
        """Get attendance history for an employee within date range."""
        db = get_db()
        rows = db.fetch_all("""
            SELECT * FROM attendance
            WHERE employee_id = ? AND date BETWEEN ? AND ?
            ORDER BY date DESC
        """, (employee_id, start_date, end_date))
        return [cls.from_row(row) for row in rows]

    @classmethod
    def get_daily_report(cls, target_date: str = None) -> List[Dict[str, Any]]:
        """Get daily attendance report for all employees."""
        db = get_db()
        if target_date is None:
            target_date = date.today().isoformat()

        rows = db.fetch_all("""
            SELECT
                e.employee_id,
                e.full_name,
                e.department,
                e.position,
                a.check_in,
                a.check_out,
                a.status,
                a.working_hours,
                a.overtime_hours
            FROM employees e
            LEFT JOIN attendance a ON e.id = a.employee_id AND a.date = ?
            WHERE e.is_active = 1
            ORDER BY e.employee_id
        """, (target_date,))

        return [dict(row) for row in rows]

    @classmethod
    def get_weekly_report(cls, employee_id: int, week_start: str) -> List[Dict[str, Any]]:
        """Get weekly attendance report for an employee."""
        db = get_db()
        start = datetime.fromisoformat(week_start).date()
        end = start + timedelta(days=6)

        rows = db.fetch_all("""
            SELECT * FROM attendance
            WHERE employee_id = ? AND date BETWEEN ? AND ?
            ORDER BY date
        """, (employee_id, start.isoformat(), end.isoformat()))

        return [dict(row) for row in rows]

    @classmethod
    def get_monthly_report(cls, employee_id: int, year: int, month: int) -> List[Dict[str, Any]]:
        """Get monthly attendance report for an employee."""
        db = get_db()
        start = date(year, month, 1)
        if month == 12:
            end = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end = date(year, month + 1, 1) - timedelta(days=1)

        rows = db.fetch_all("""
            SELECT * FROM attendance
            WHERE employee_id = ? AND date BETWEEN ? AND ?
            ORDER BY date
        """, (employee_id, start.isoformat(), end.isoformat()))

        return [dict(row) for row in rows]

    @classmethod
    def get_department_report(cls, department: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get attendance report for a department."""
        db = get_db()
        rows = db.fetch_all("""
            SELECT
                e.employee_id,
                e.full_name,
                a.date,
                a.check_in,
                a.check_out,
                a.status,
                a.working_hours,
                a.overtime_hours
            FROM employees e
            LEFT JOIN attendance a ON e.id = a.employee_id
                AND a.date BETWEEN ? AND ?
            WHERE e.department = ? AND e.is_active = 1
            ORDER BY e.employee_id, a.date
        """, (start_date, end_date, department))

        return [dict(row) for row in rows]

    @classmethod
    def do_check_in(cls, employee_id: int) -> Dict[str, Any]:
        """Process employee check-in."""
        db = get_db()
        today = date.today().isoformat()
        now = datetime.now()

        # Get settings
        work_start = cls._get_setting('work_start', '08:00')
        late_threshold = cls._get_setting('late_threshold', '08:15')

        # Check if already checked in
        existing = cls.get_today(employee_id)
        if existing and existing.check_in:
            return {
                'success': False,
                'message': 'Already checked in today',
                'record': existing
            }

        # Determine status based on check-in time
        check_in_time = now.time()
        late_time = time.fromisoformat(late_threshold)
        status = 'late' if check_in_time > late_time else 'present'

        # Create or update record
        if existing:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE attendance
                    SET check_in = ?, status = ?, notes = ?
                    WHERE id = ?
                """, (now.isoformat(), status, f"Checked in at {now.strftime('%H:%M')}", existing.id))
                conn.commit()
            record = cls.get_by_id(existing.id)
        else:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO attendance (employee_id, date, check_in, status, notes)
                    VALUES (?, ?, ?, ?, ?)
                """, (employee_id, today, now.isoformat(), status,
                      f"Checked in at {now.strftime('%H:%M')}"))
                conn.commit()
                record_id = cursor.lastrowid
            record = cls.get_by_id(record_id)

        return {
            'success': True,
            'message': f'Checked in successfully at {now.strftime("%H:%M")}',
            'status': status,
            'record': record
        }

    @classmethod
    def do_check_out(cls, employee_id: int) -> Dict[str, Any]:
        """Process employee check-out."""
        db = get_db()
        today = date.today().isoformat()
        now = datetime.now()

        # Get today's record
        existing = cls.get_today(employee_id)
        if not existing:
            return {
                'success': False,
                'message': 'No check-in record found for today'
            }

        if existing.check_out:
            return {
                'success': False,
                'message': 'Already checked out today',
                'record': existing
            }

        if not existing.check_in:
            return {
                'success': False,
                'message': 'Cannot check out without checking in first'
            }

        # Calculate working hours
        check_in_dt = datetime.fromisoformat(existing.check_in)
        check_out_dt = now
        working_seconds = (check_out_dt - check_in_dt).total_seconds()
        working_hours = round(working_seconds / 3600, 2)

        # Calculate overtime
        standard_hours = 8.0
        overtime_hours = max(0, round(working_hours - standard_hours, 2))

        # Update record
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE attendance
                SET check_out = ?, working_hours = ?, overtime_hours = ?,
                    notes = COALESCE(notes || '; ', '') || ?
                WHERE id = ?
            """, (now.isoformat(), working_hours, overtime_hours,
                  f"Checked out at {now.strftime('%H:%M')}", existing.id))
            conn.commit()

        updated = cls.get_by_id(existing.id)

        return {
            'success': True,
            'message': f'Checked out successfully at {now.strftime("%H:%M")}',
            'working_hours': working_hours,
            'overtime_hours': overtime_hours,
            'record': updated
        }

    @classmethod
    def mark_absent_employees(cls, target_date: str = None) -> int:
        """Mark employees as absent for a given date (run at end of day)."""
        db = get_db()
        if target_date is None:
            target_date = date.today().isoformat()

        # Get all active employees
        employees = Employee.get_all({'is_active': True})
        count = 0

        for emp in employees:
            existing = cls.get_today(emp.id)
            if not existing:
                # Create absent record
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO attendance (employee_id, date, status)
                        VALUES (?, ?, 'absent')
                    """, (emp.id, target_date))
                    conn.commit()
                count += 1
            elif existing and not existing.check_in:
                # Update to absent if no check-in
                with db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE attendance SET status = 'absent'
                        WHERE id = ?
                    """, (existing.id,))
                    conn.commit()
                count += 1

        return count

    @classmethod
    def _get_setting(cls, key: str, default: str) -> str:
        """Get a setting value from database."""
        db = get_db()
        row = db.fetch_one("SELECT value FROM settings WHERE key = ?", (key,))
        return row['value'] if row else default

    @classmethod
    def calculate_dashboard_stats(cls) -> Dict[str, int]:
        """Calculate dashboard statistics for today."""
        db = get_db()
        today = date.today().isoformat()

        stats = {}
        stats['total_employees'] = db.fetch_one(
            "SELECT COUNT(*) as c FROM employees WHERE is_active = 1"
        )['c']

        stats['present_today'] = db.fetch_one("""
            SELECT COUNT(*) as c FROM attendance
            WHERE date = ? AND status IN ('present', 'late')
        """, (today,))['c']

        stats['late_today'] = db.fetch_one("""
            SELECT COUNT(*) as c FROM attendance
            WHERE date = ? AND status = 'late'
        """, (today,))['c']

        stats['absent_today'] = db.fetch_one("""
            SELECT COUNT(*) as c FROM attendance
            WHERE date = ? AND status = 'absent'
        """, (today,))['c']

        stats['on_leave_today'] = db.fetch_one("""
            SELECT COUNT(*) as c FROM attendance
            WHERE date = ? AND status = 'on_leave'
        """, (today,))['c']

        stats['checked_in'] = db.fetch_one("""
            SELECT COUNT(*) as c FROM attendance
            WHERE date = ? AND check_in IS NOT NULL
        """, (today,))['c']

        stats['checked_out'] = db.fetch_one("""
            SELECT COUNT(*) as c FROM attendance
            WHERE date = ? AND check_out IS NOT NULL
        """, (today,))['c']

        return stats
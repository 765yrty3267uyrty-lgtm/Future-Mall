"""
Future Mall - Attendance System Services
Business logic layer for attendance operations.
"""

from datetime import date, datetime
from typing import List, Dict, Any, Optional
import csv
import os

from ..models import Employee, Attendance


class AttendanceService:
    """Business logic for attendance operations."""

    @staticmethod
    def perform_check_in(employee_id: int) -> Dict[str, Any]:
        """Process employee check-in with validation."""
        # Validate employee exists and is active
        emp = Employee.get_by_id(employee_id)
        if not emp:
            return {'success': False, 'message': 'Employee not found'}
        if not emp.is_active:
            return {'success': False, 'message': 'Employee account is inactive'}

        # Process check-in
        return Attendance.do_check_in(employee_id)

    @staticmethod
    def perform_check_out(employee_id: int) -> Dict[str, Any]:
        """Process employee check-out with validation."""
        emp = Employee.get_by_id(employee_id)
        if not emp:
            return {'success': False, 'message': 'Employee not found'}

        return Attendance.do_check_out(employee_id)

    @staticmethod
    def get_employee_today_status(employee_id: int) -> Dict[str, Any]:
        """Get current status for employee dashboard."""
        emp = Employee.get_by_id(employee_id)
        if not emp:
            return {'success': False, 'message': 'Employee not found'}

        record = Attendance.get_today(employee_id)
        today = date.today().isoformat()

        return {
            'success': True,
            'employee': {
                'id': emp.id,
                'employee_id': emp.employee_id,
                'full_name': emp.full_name,
                'department': emp.department,
            },
            'today': today,
            'record': record,
        }

    @staticmethod
    def get_dashboard_stats() -> Dict[str, Any]:
        """Get dashboard statistics."""
        return Attendance.calculate_dashboard_stats()

    @staticmethod
    def get_all_employees_today_status() -> List[Dict[str, Any]]:
        """Get today's status for all employees (supervisor/admin view)."""
        employees = Employee.get_all({'is_active': True})
        today = date.today().isoformat()

        results = []
        for emp in employees:
            record = Attendance.get_today(emp.id)
            results.append({
                'employee_id': emp.employee_id,
                'full_name': emp.full_name,
                'department': emp.department,
                'position': emp.position,
                'status': record.status if record else 'not_recorded',
                'check_in': record.check_in if record else None,
                'check_out': record.check_out if record else None,
                'working_hours': record.working_hours if record else 0,
            })
        return results

    @staticmethod
    def mark_all_absent() -> Dict[str, Any]:
        """Mark all employees without check-in as absent (end of day)."""
        count = Attendance.mark_absent_employees()
        return {
            'success': True,
            'message': f'Marked {count} employees as absent',
            'count': count
        }


class ReportService:
    """Business logic for report generation."""

    @staticmethod
    def generate_daily_report(target_date: str = None) -> List[Dict[str, Any]]:
        """Generate daily attendance report."""
        if target_date is None:
            target_date = date.today().isoformat()
        return Attendance.get_daily_report(target_date)

    @staticmethod
    def generate_weekly_report(employee_id: int, week_start: str = None) -> List[Dict[str, Any]]:
        """Generate weekly attendance report."""
        if week_start is None:
            # Get Monday of current week
            today = date.today()
            week_start = (today - timedelta(days=today.weekday())).isoformat()
        return Attendance.get_weekly_report(employee_id, week_start)

    @staticmethod
    def generate_monthly_report(employee_id: int, year: int = None, month: int = None) -> List[Dict[str, Any]]:
        """Generate monthly attendance report."""
        if year is None:
            year = date.today().year
        if month is None:
            month = date.today().month
        return Attendance.get_monthly_report(employee_id, year, month)

    @staticmethod
    def generate_department_report(department: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Generate department attendance report."""
        return Attendance.get_department_report(department, start_date, end_date)

    @staticmethod
    def export_to_csv(report_data: List[Dict[str, Any]], filename: str) -> str:
        """Export report data to CSV file."""
        if not report_data:
            raise ValueError("No data to export")

        # Ensure directory exists
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)

        fieldnames = list(report_data[0].keys())
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(report_data)

        return filename

    @staticmethod
    def export_to_excel(report_data: List[Dict[str, Any]], filename: str) -> str:
        """Export report data to Excel file (requires openpyxl)."""
        try:
            from openpyxl import Workbook
        except ImportError:
            raise ImportError("openpyxl is required for Excel export. Install with: pip install openpyxl")

        if not report_data:
            raise ValueError("No data to export")

        wb = Workbook()
        ws = wb.active
        ws.title = "Attendance Report"

        # Headers
        fieldnames = list(report_data[0].keys())
        ws.append(fieldnames)

        # Data
        for row in report_data:
            ws.append([row.get(field) for field in fieldnames])

        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        wb.save(filename)
        return filename


class StatsService:
    """Business logic for statistics and analytics."""

    @staticmethod
    def get_attendance_rate(employee_id: int, start_date: str, end_date: str) -> float:
        """Calculate attendance rate for an employee in date range."""
        records = Attendance.get_history(employee_id, start_date, end_date)
        if not records:
            return 0.0

        total_days = len(records)
        present_days = sum(1 for r in records if r.status in ('present', 'late'))
        return round((present_days / total_days) * 100, 2) if total_days > 0 else 0.0

    @staticmethod
    def get_average_working_hours(employee_id: int, start_date: str, end_date: str) -> float:
        """Calculate average working hours for an employee in date range."""
        records = Attendance.get_history(employee_id, start_date, end_date)
        if not records:
            return 0.0

        total_hours = sum(r.working_hours for r in records if r.working_hours)
        days_with_hours = sum(1 for r in records if r.working_hours > 0)
        return round(total_hours / days_with_hours, 2) if days_with_hours > 0 else 0.0

    @staticmethod
    def get_most_punctual_employee(start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
        """Find most punctual employee in date range."""
        db = get_db()
        rows = db.fetch_all("""
            SELECT
                e.id, e.employee_id, e.full_name,
                COUNT(CASE WHEN a.status = 'present' THEN 1 END) as present_count,
                COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late_count,
                COUNT(*) as total_days
            FROM employees e
            LEFT JOIN attendance a ON e.id = a.employee_id
                AND a.date BETWEEN ? AND ?
            WHERE e.is_active = 1
            GROUP BY e.id
            HAVING total_days > 0
            ORDER BY late_count ASC, present_count DESC
            LIMIT 1
        """, (start_date, end_date))

        if rows:
            row = rows[0]
            return {
                'employee_id': row['employee_id'],
                'full_name': row['full_name'],
                'late_count': row['late_count'],
                'present_count': row['present_count'],
                'punctuality_rate': round((row['present_count'] / row['total_days']) * 100, 2)
            }
        return None

    @staticmethod
    def get_most_late_employee(start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
        """Find most late employee in date range."""
        db = get_db()
        rows = db.fetch_all("""
            SELECT
                e.id, e.employee_id, e.full_name,
                COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late_count,
                COUNT(*) as total_days
            FROM employees e
            LEFT JOIN attendance a ON e.id = a.employee_id
                AND a.date BETWEEN ? AND ?
            WHERE e.is_active = 1
            GROUP BY e.id
            HAVING late_count > 0
            ORDER BY late_count DESC
            LIMIT 1
        """, (start_date, end_date))

        if rows:
            row = rows[0]
            return {
                'employee_id': row['employee_id'],
                'full_name': row['full_name'],
                'late_count': row['late_count'],
                'total_days': row['total_days'],
            }
        return None

    @staticmethod
    def get_attendance_trend(months: int = 6) -> List[Dict[str, Any]]:
        """Get attendance trend over last N months."""
        db = get_db()
        rows = db.fetch_all("""
            SELECT
                strftime('%Y-%m', date) as month,
                COUNT(*) as total_records,
                COUNT(CASE WHEN status = 'present' THEN 1 END) as present_count,
                COUNT(CASE WHEN status = 'late' THEN 1 END) as late_count,
                COUNT(CASE WHEN status = 'absent' THEN 1 END) as absent_count
            FROM attendance
            WHERE date >= date('now', '-' || ? || ' months')
            GROUP BY strftime('%Y-%m', date)
            ORDER BY month
        """, (months,))

        return [dict(row) for row in rows]


# Import timedelta for ReportService
from datetime import timedelta
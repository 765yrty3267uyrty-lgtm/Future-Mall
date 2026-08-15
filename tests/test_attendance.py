import pytest
import sys
import os
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python_modules', 'attendance_system'))

from models import Employee, Attendance, get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Clean database before each test."""
    db = get_db()
    with db.get_connection() as conn:
        conn.execute("DELETE FROM attendance")
        conn.execute("DELETE FROM employees")
        conn.commit()
    yield
    with db.get_connection() as conn:
        conn.execute("DELETE FROM attendance")
        conn.execute("DELETE FROM employees")
        conn.commit()


class TestEmployeeModel:
    def test_create_employee(self):
        emp = Employee.create({
            'employee_id': 'TEST001',
            'full_name': 'Test User',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        assert emp is not None
        assert emp.employee_id == 'TEST001'
        assert emp.full_name == 'Test User'
        assert emp.department == 'IT'
        assert emp.is_active is True

    def test_get_by_id(self):
        emp = Employee.create({
            'employee_id': 'TEST002',
            'full_name': 'Test User 2',
            'department': 'HR',
            'position': 'Manager',
            'email': 'test2@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        fetched = Employee.get_by_id(emp.id)
        assert fetched is not None
        assert fetched.employee_id == 'TEST002'

    def test_get_by_employee_id(self):
        Employee.create({
            'employee_id': 'TEST003',
            'full_name': 'Test User 3',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test3@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        emp = Employee.get_by_employee_id('TEST003')
        assert emp is not None
        assert emp.employee_id == 'TEST003'

    def test_get_all_employees(self):
        Employee.create({
            'employee_id': 'TEST004',
            'full_name': 'Test User 4',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test4@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        Employee.create({
            'employee_id': 'TEST005',
            'full_name': 'Test User 5',
            'department': 'HR',
            'position': 'Manager',
            'email': 'test5@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'supervisor',
            'password': 'password123'
        })
        employees = Employee.get_all()
        assert len(employees) >= 2

    def test_authenticate_valid(self):
        Employee.create({
            'employee_id': 'TEST006',
            'full_name': 'Test User 6',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test6@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        emp = Employee.authenticate('TEST006', 'password123')
        assert emp is not None
        assert emp.employee_id == 'TEST006'

    def test_authenticate_invalid_password(self):
        Employee.create({
            'employee_id': 'TEST007',
            'full_name': 'Test User 7',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test7@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        emp = Employee.authenticate('TEST007', 'wrongpassword')
        assert emp is None

    def test_authenticate_nonexistent(self):
        emp = Employee.authenticate('NONEXISTENT', 'password123')
        assert emp is None

    def test_update_employee(self):
        emp = Employee.create({
            'employee_id': 'TEST008',
            'full_name': 'Test User 8',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test8@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        updated = Employee.update(emp.id, {'full_name': 'Updated Name', 'department': 'HR'})
        assert updated is not None
        assert updated.full_name == 'Updated Name'
        assert updated.department == 'HR'

    def test_deactivate_employee(self):
        emp = Employee.create({
            'employee_id': 'TEST009',
            'full_name': 'Test User 9',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test9@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        Employee.update(emp.id, {'is_active': False})
        emp = Employee.get_by_id(emp.id)
        assert emp.is_active is False


class TestAttendanceModel:
    def test_check_in(self):
        emp = Employee.create({
            'employee_id': 'TEST010',
            'full_name': 'Test User 10',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test10@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        result = Attendance.do_check_in(emp.id)
        assert result['success'] is True
        assert result['status'] in ('present', 'late')
        assert result['record'] is not None
        assert result['record'].check_in is not None

    def test_check_in_duplicate(self):
        emp = Employee.create({
            'employee_id': 'TEST011',
            'full_name': 'Test User 11',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test11@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        Attendance.do_check_in(emp.id)
        result = Attendance.do_check_in(emp.id)
        assert result['success'] is False
        assert 'Already checked in' in result['message']

    def test_check_out(self):
        emp = Employee.create({
            'employee_id': 'TEST012',
            'full_name': 'Test User 12',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test12@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        Attendance.do_check_in(emp.id)
        result = Attendance.do_check_out(emp.id)
        assert result['success'] is True
        assert result['working_hours'] >= 0
        assert result['record'].check_out is not None

    def test_check_out_without_check_in(self):
        emp = Employee.create({
            'employee_id': 'TEST013',
            'full_name': 'Test User 13',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test13@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        result = Attendance.do_check_out(emp.id)
        assert result['success'] is False
        assert 'No check-in record' in result['message']

    def test_check_out_duplicate(self):
        emp = Employee.create({
            'employee_id': 'TEST014',
            'full_name': 'Test User 14',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test14@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        Attendance.do_check_in(emp.id)
        Attendance.do_check_out(emp.id)
        result = Attendance.do_check_out(emp.id)
        assert result['success'] is False
        assert 'Already checked out' in result['message']

    def test_get_today_attendance(self):
        emp = Employee.create({
            'employee_id': 'TEST015',
            'full_name': 'Test User 15',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test15@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        Attendance.do_check_in(emp.id)
        record = Attendance.get_today(emp.id)
        assert record is not None
        assert record.employee_id == emp.id

    def test_get_history(self):
        emp = Employee.create({
            'employee_id': 'TEST016',
            'full_name': 'Test User 16',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test16@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        today = date.today().isoformat()
        yesterday = (date.today() - timedelta(days=1)).isoformat()

        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO attendance (employee_id, date, check_in, check_out, status, working_hours, overtime_hours)
                VALUES (?, ?, ?, ?, 'present', 8.0, 0.0)
            """, (emp.id, yesterday, '2024-01-01 08:00:00', '2024-01-01 17:00:00'))
            cursor.execute("""
                INSERT INTO attendance (employee_id, date, check_in, check_out, status, working_hours, overtime_hours)
                VALUES (?, ?, ?, ?, 'late', 7.5, 0.0)
            """, (emp.id, today, '2024-01-02 08:20:00', '2024-01-02 16:50:00'))
            conn.commit()

        history = Attendance.get_history(emp.id, yesterday, today)
        assert len(history) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
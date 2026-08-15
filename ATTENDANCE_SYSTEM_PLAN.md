# Employee Attendance System - Implementation Plan

## Project Overview
Build a complete Employee Attendance Management System for Future Mall with check-in/out, working hours calculation, history tracking, and daily/weekly/monthly reports.

## Tech Stack Options
| Option | Best For | Complexity |
|--------|----------|------------|
| Python + SQLite + Tkinter | Desktop app, offline, beginner-friendly | Medium |
| Python Console + SQLite | Learning fundamentals, simple deployment | Low |
| HTML/CSS/JS + LocalStorage/IndexedDB | Web-based, no backend needed | Medium |
| React + TypeScript + Supabase/Firebase | Production web app, real-time, scalable | High |

Recommendation: Python + SQLite + Tkinter - balances functionality, learning value, and Future Mall branding integration.

## Project Structure
employee-attendance-system/
|-- main.py
|-- models/
|   |-- __init__.py
|   |-- employee.py
|   |-- attendance.py
|   |-- database.py
|-- services/
|   |-- __init__.py
|   |-- auth_service.py
|   |-- attendance_service.py
|   |-- report_service.py
|   |-- stats_service.py
|-- ui/
|   |-- __init__.py
|   |-- base.py
|   |-- login_window.py
|   |-- employee_dashboard.py
|   |-- supervisor_dashboard.py
|   |-- admin_dashboard.py
|   |-- attendance_window.py
|   |-- history_window.py
|   |-- reports_window.py
|   |-- components/
|-- utils/
|   |-- __init__.py
|   |-- validators.py
|   |-- date_time.py
|   |-- export.py
|   |-- constants.py
|-- data/
|   |-- attendance.db
|   |-- sample_data.sql
|-- tests/
|   |-- test_attendance.py
|   |-- test_reports.py
|   |-- test_validators.py
|-- requirements.txt
|-- README.md
|-- .gitignore
---

## Core Modules

### 1. Database Schema (SQLite)

-- Employees table
CREATE TABLE employees (
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
);

-- Attendance records
CREATE TABLE attendance (
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
);

-- Leave requests (optional)
CREATE TABLE leaves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    leave_type TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    reason TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

-- Settings
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

### 2. Constants (utils/constants.py)
WORK_START = '08:00'
WORK_END = '17:00'
LATE_THRESHOLD = '08:15'
STANDARD_HOURS = 8.0
MAX_OVERTIME = 2.0

ROLES = ['employee', 'supervisor', 'admin']
STATUSES = ['present', 'late', 'absent', 'on_leave', 'holiday']
DEPARTMENTS = ['IT', 'HR', 'Finance', 'Operations', 'Marketing', 'Customer Service']

### 3. Employee Model (models/employee.py)
class Employee:
    def __init__(self, id, employee_id, full_name, department, position, 
                 email, phone, date_joined, role, is_active):
        ...

    @classmethod
    def create(cls, data): ...
    @classmethod
    def get_by_id(cls, id): ...
    @classmethod
    def get_by_employee_id(cls, emp_id): ...
    @classmethod
    def get_all(cls, filters=None): ...
    @classmethod
    def update(cls, id, data): ...
    @classmethod
    def delete(cls, id): ...
    @classmethod
    def authenticate(cls, employee_id, password): ...
    def check_password(self, password): ...
    def set_password(self, password): ...

### 4. Attendance Model (models/attendance.py)
class Attendance:
    def __init__(self, id, employee_id, date, check_in, check_out, 
                 status, working_hours, overtime_hours, notes):
        ...

    @classmethod
    def check_in(cls, employee_id): ...
    @classmethod
    def check_out(cls, employee_id): ...
    @classmethod
    def get_today(cls, employee_id): ...
    @classmethod
    def get_history(cls, employee_id, start_date, end_date): ...
    @classmethod
    def get_daily_report(cls, date): ...
    @classmethod
    def get_weekly_report(cls, employee_id, week_start): ...
    @classmethod
    def get_monthly_report(cls, employee_id, year, month): ...
    @classmethod
    def calculate_status(cls, check_in_time): ...
    @classmethod
    def calculate_hours(cls, check_in, check_out): ...

### 5. Services

#### Attendance Service
- perform_check_in(employee_id)
- perform_check_out(employee_id)
- get_dashboard_stats()
- mark_absent_employees(date)
- validate_check_in(employee_id)
- validate_check_out(employee_id)

#### Report Service
- generate_daily_report(date, format='table')
- generate_weekly_report(employee_id, week_start)
- generate_monthly_report(employee_id, year, month)
- generate_department_report(department, start_date, end_date)
- export_to_csv/report_data, filename)
- export_to_excel(report_data, filename)
- export_to_pdf(report_data, filename)

#### Stats Service
- average_attendance_rate(period)
- average_working_hours(period)
- most_punctual_employee(period)
- most_late_employee(period)
- attendance_trend(months=6)

---

## UI Design (Tkinter)

### Theme System (ui/base.py)
COLORS = {
    'primary': '#2563EB',
    'primary_hover': '#1D4ED8',
    'secondary': '#0D9488',
    'accent': '#F97316',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'bg': '#F8FAFC',
    'surface': '#FFFFFF',
    'text': '#1E293B',
    'text_muted': '#64748B',
    'border': '#E2E8F0',
}

FONTS = {
    'heading': ('Space Grotesk', 18, 'bold'),
    'subheading': ('Space Grotesk', 14, 'bold'),
    'body': ('Inter', 11),
    'small': ('Inter', 9),
    'mono': ('JetBrains Mono', 10),
}

### Windows
1. Login Window - Centered card, Future Mall logo, Employee ID + Password, Role-based redirect
2. Employee Dashboard - Welcome header, Check-In/Out buttons, Today status, Working hours, Quick stats
3. Supervisor Dashboard - Stats cards, Employee list with filters, Report buttons
4. Admin Dashboard - All supervisor + Employee CRUD, Settings, Data export
5. Attendance History - Calendar picker, Table with summary, Export
6. Reports Window - Tabs for Daily/Weekly/Monthly, Preview + Export

---

## Implementation Phases

### Phase 1: Foundation (Day 1)
- Project setup, virtual environment, requirements.txt
- Database module with migrations
- Models: Employee, Attendance with CRUD
- Constants, validators, date/time utils
- Basic authentication service

### Phase 2: Core Logic (Day 1-2)
- Attendance service: check-in, check-out, status calculation
- Business rules: late threshold, duplicate prevention
- Report service: daily, weekly, monthly queries
- Stats service: aggregates, trends
- Export utilities (CSV, Excel via openpyxl)

### Phase 3: UI - Base & Login (Day 2)
- Theme system, custom widgets (Card, Button, Table, Form)
- Login window with validation
- Role-based window routing
- Session management

### Phase 4: UI - Employee Features (Day 2-3)
- Employee dashboard with check-in/out
- Attendance history view
- Profile view (read-only)

### Phase 5: UI - Supervisor Features (Day 3)
- Supervisor dashboard with stats cards
- Employee list with filters
- Daily report generation

### Phase 6: UI - Admin Features (Day 3-4)
- Admin dashboard
- Employee CRUD modals
- Settings management
- Data export

### Phase 7: Polish (Day 4)
- Dark mode toggle
- Keyboard shortcuts
- Tooltips, help text
- Error handling, logging
- Sample data seeder
- README.md with screenshots

---

## Data Storage

### SQLite (Recommended)
- File-based, zero config
- ACID compliant
- Easy backup (copy .db file)
- SQL queries for reports

### Alternative: JSON Files (Beginner)
data/
|-- employees.json
|-- attendance.json
|-- settings.json
- Simpler for learning
- No SQL knowledge needed
- Not concurrent-safe

---

## Validation Rules

| Operation | Validations |
|-----------|-------------|
| Check-In | Employee exists, active, not already checked in today, within work hours |
| Check-Out | Check-in exists today, not already checked out, after check-in time |
| Add Employee | Unique employee_id, email, valid department/position, strong password |
| Date Input | Valid format (YYYY-MM-DD), not future (for history), not before hire date |
| Time Input | Valid 24hr format (HH:MM) |

---

## Sample Data (for testing)
EMPLOYEES = [
    {'employee_id': 'EMP001', 'full_name': 'Ahmed Hassan', 'department': 'IT', 
     'position': 'Developer', 'email': 'ahmed@futuremall.com', 'role': 'employee'},
    {'employee_id': 'EMP002', 'full_name': 'Sara Ali', 'department': 'HR', 
     'position': 'HR Manager', 'email': 'sara@futuremall.com', 'role': 'supervisor'},
    {'employee_id': 'EMP003', 'full_name': 'Mohamed Omar', 'department': 'Operations', 
     'position': 'Store Manager', 'email': 'mohamed@futuremall.com', 'role': 'admin'},
]

---

## Optional Features Priority

| Feature | Effort | Value |
|---------|--------|-------|
| Dark Mode | Low | High |
| CSV/Excel Export | Medium | High |
| PDF Reports (reportlab) | Medium | Medium |
| QR Code Check-in (simulation) | Low | High |
| Attendance Calendar View | Medium | Medium |
| Email Notifications | High | Low |
| Multi-language (i18n) | High | Low |
| Biometric Simulation | Low | Fun |

---

## Clarifying Questions

1. **Tech Stack**: Python+Tkinter (recommended), Console, Web (HTML/JS), or React?
2. **Database**: SQLite (recommended), JSON files, or in-memory?
3. **Work Hours**: 08:00-17:00 with 08:15 late threshold, or different?
4. **Departments/Positions**: Use example list or provide custom?
5. **Sample Data**: Seed with 10-15 employees across roles?
6. **Export Formats**: CSV required, Excel (openpyxl), PDF (reportlab)?
7. **Dark Mode**: Include from start?
8. **Login**: Simple employee_id + password, or PIN/QR simulation?
9. **Calendar**: Visual calendar widget for history?
10. **Packaging**: PyInstaller executable for distribution?

---

## Success Criteria
- [ ] Employee checks in/out successfully
- [ ] Late/present/absent status calculated correctly
- [ ] Working hours and overtime computed accurately
- [ ] Daily/weekly/monthly reports generate correct data
- [ ] Search/filter works on all criteria
- [ ] Admin can CRUD employees
- [ ] Data persists in SQLite
- [ ] Input validation prevents invalid operations
- [ ] UI is responsive, themed (Future Mall colors)
- [ ] Code is modular, typed, documented
- [ ] README with run instructions

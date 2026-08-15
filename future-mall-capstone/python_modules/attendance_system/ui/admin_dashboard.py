"""
Future Mall - Attendance System Admin Dashboard
Full admin panel with employee management, settings, and data export.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, timedelta
from typing import Optional, Callable

from .base import (Theme, ModernButton, ModernLabel, Card, ModernEntry,
                   StatusBadge, ModernButton)
from ..services import AttendanceService, ReportService, StatsService
from ..models import Employee, Attendance


class AdminDashboard:
    """Admin dashboard with full system management."""

    def __init__(self, parent: tk.Widget, employee_id: int,
                 on_logout: Callable[[], None]):
        self.parent = parent
        self.employee_id = employee_id
        self.on_logout = on_logout

        from ..models import Employee
        self.employee = Employee.get_by_id(employee_id)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """Setup the admin dashboard UI."""
        self.main_frame = tk.Frame(self.parent, bg=Theme.BG)
        self.main_frame.pack(fill="both", expand=True)

        # Header
        self.create_header()

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        # Tab 1: Dashboard
        self.create_dashboard_tab()

        # Tab 2: Employee Management
        self.create_employee_tab()

        # Tab 3: Attendance Management
        self.create_attendance_tab()

        # Tab 4: Reports
        self.create_reports_tab()

        # Tab 5: Settings
        self.create_settings_tab()

    def create_header(self):
        """Create dashboard header."""
        header = tk.Frame(self.main_frame, bg=Theme.SURFACE,
                          highlightbackground=Theme.BORDER,
                          highlightthickness=1)
        header.pack(fill="x", padx=Theme.SPACING_LG, pady=(Theme.SPACING_LG, 0))

        header_content = tk.Frame(header, bg=Theme.SURFACE)
        header_content.pack(fill="x", padx=Theme.SPACING_LG, pady=Theme.SPACING_MD)

        # Title
        title_frame = tk.Frame(header_content, bg=Theme.SURFACE)
        title_frame.pack(side="left")

        ModernLabel(title_frame, text="🏢 Future Mall", style="heading").pack(anchor="w")
        ModernLabel(title_frame, text="Admin Panel", style="muted").pack(anchor="w")

        # User info
        user_frame = tk.Frame(header_content, bg=Theme.SURFACE)
        user_frame.pack(side="right")

        ModernLabel(header_content, text=f"Admin: {self.employee.full_name}",
                    style="body").pack(side="right", padx=Theme.SPACING_LG)

        ModernButton(header_content, text="Logout", style="outline",
                     command=self.on_logout, width=10).pack(side="right")

    def create_dashboard_tab(self):
        """Create main dashboard tab."""
        dash_frame = tk.Frame(self.notebook, bg=Theme.BG)
        self.notebook.add(dash_frame, text="  Dashboard  ")

        # Stats cards
        stats_frame = tk.Frame(dash_frame, bg=Theme.BG)
        stats_frame.pack(fill="x", padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        self.dash_stats = {}
        stats = [
            ("total", "Total Employees", "0", Theme.PRIMARY, "👥"),
            ("present", "Present Today", "0", Theme.SUCCESS, "✅"),
            ("late", "Late Today", "0", Theme.WARNING, "⏰"),
            ("absent", "Absent Today", "0", Theme.DANGER, "❌"),
            ("on_leave", "On Leave", "0", Theme.INFO, "🏖️"),
            ("departments", "Departments", "0", Theme.ACCENT, "🏢"),
        ]

        for i, (key, title, value, color, icon) in enumerate(stats):
            card = self._create_stat_card(stats_frame, title, value, color, icon)
            card.grid(row=0, column=i, padx=Theme.SPACING_SM, pady=Theme.SPACING_SM, sticky="ew")
            stats_frame.grid_columnconfigure(i, weight=1)
            self.dash_stats[key] = card

        # Quick actions
        actions_card = Card(self.main_frame, padding=Theme.SPACING_LG)
        actions_card.pack(fill="x", padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        ModernLabel(actions_card.content, text="Quick Actions", style="heading").pack(anchor="w", pady=(0, Theme.SPACING_MD))

        btn_frame = tk.Frame(actions_card.content, bg=Theme.SURFACE)
        btn_frame.pack(fill="x")

        actions = [
            ("Add Employee", "primary", self.show_add_employee),
            ("Generate Daily Report", "secondary", self.generate_daily_report),
            ("Export All Data", "accent", self.export_all_data),
            ("Mark All Absent", "danger", self.mark_all_absent),
            ("Backup Database", "secondary", self.backup_database),
        ]

        for text, style, cmd in actions:
            ModernButton(btn_frame, text=text, style=style, command=text.lower().replace(" ", "_")).pack(
                side="left", padx=Theme.SPACING_SM)

        # Recent activity
        activity_card = Card(self.main_frame, padding=Theme.SPACING_LG)
        activity_card.pack(fill="both", expand=True, padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        ModernLabel(activity_card.content, text="System Overview", style="heading").pack(anchor="w", pady=(0, Theme.SPACING_MD))

        # Department stats
        dept_frame = tk.Frame(activity_card.content, bg=Theme.SURFACE)
        dept_frame.pack(fill="x")

        ModernLabel(activity_card.content, text="Employees by Department", style="subheading").pack(anchor="w", pady=(Theme.SPACING_MD, Theme.SPACING_SM))

        self.dept_tree = ttk.Treeview(self.main_frame, columns=("dept", "count"), show="headings", height=6)
        self.dept_tree.heading("dept", text="Department")
        self.dept_tree.heading("count", text="Employees")
        self.dept_tree.column("dept", width=200)
        self.dept_tree.column("count", width=100, anchor="center")

    def _create_stat_card(self, parent, title, value, color, icon):
        """Create a stat card."""
        from .base import StatCard
        card = StatCard(parent, title, value, icon, color)
        return card

    def create_employee_tab(self):
        """Create employee management tab."""
        emp_frame = tk.Frame(self.notebook, bg=Theme.BG)
        self.notebook.add(emp_frame, text="  Employees  ")

        # Toolbar
        toolbar = tk.Frame(emp_frame, bg=Theme.BG)
        toolbar.pack(fill="x", padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        ModernButton(toolbar, text="➕ Add Employee", style="primary",
                     command=self.show_add_employee).pack(side="left")
        ModernButton(toolbar, text="📥 Import CSV", style="secondary",
                     command=self.import_employees).pack(side="left", padx=Theme.SPACING_SM)
        ModernButton(toolbar, text="📤 Export CSV", style="secondary",
                     command=self.export_employees).pack(side="left")

        # Search
        search_frame = tk.Frame(toolbar, bg=Theme.BG)
        search_frame.pack(side="right")

        ModernLabel(search_frame, text="Search:", style="muted").pack(side="left", padx=(0, Theme.SPACING_SM))
        self.emp_search_var = tk.StringVar()
        search_entry = ModernEntry(search_frame, placeholder="Search by name, ID, dept...")
        search_entry.pack(side="left", padx=Theme.SPACING_SM)
        search_entry.bind("<KeyRelease>", self.filter_employees)

        # Employee table
        table_card = Card(self.main_frame, padding=Theme.SPACING_LG)
        table_card.pack(fill="both", expand=True, padx=Theme.SPACING_LG, pady=(0, Theme.SPACING_LG))

        columns = ("emp_id", "name", "email", "department", "position", "role", "status", "joined")
        self.emp_tree = ttk.Treeview(self.main_frame, columns=("emp_id", "name", "email", "dept", "pos", "role", "status", "joined"),
                                     show="headings", height=15)

        for col, heading in [("emp_id", "ID"), ("name", "Name"), ("email", "Email"),
                             ("dept", "Department"), ("pos", "Position"), ("role", "Role"),
                             ("status", "Status"), ("joined", "Joined")]:
            self.emp_tree.heading(col, text=heading)
            self.emp_tree.column(col, width=120, anchor="center" if col != "name" else "w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.emp_tree.yview)
        self.emp_tree.configure(yscrollcommand=scrollbar.set)

        # Pack in a frame
        table_frame = tk.Frame(self.main_frame, bg=Theme.BG)
        table_frame.pack(fill="both", expand=True, padx=Theme.SPACING_LG, pady=(0, Theme.SPACING_LG))

        self.emp_tree = ttk.Treeview(table_frame, columns=("emp_id", "name", "email", "dept", "pos", "role", "status", "joined"),
                                     show="headings", height=15)

        for col in ["emp_id", "name", "email", "dept", "pos", "role", "status", "joined"]:
            self.emp_tree.heading(col, text=col.replace("_", " ").title())
            self.emp_tree.column(col, width=120, anchor="center" if col != "name" else "w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.emp_tree.yview)
        self.emp_tree.configure(yscrollcommand=scrollbar.set)

        self.emp_tree.pack(side="left", fill="both", expand=True)
        ttk.Scrollbar(table_frame, orient="vertical", command=self.emp_tree.yview).pack(side="right", fill="y")

        # Context menu
        self.create_emp_context_menu()

    def create_attendance_tab(self):
        """Create attendance management tab."""
        att_frame = tk.Frame(self.notebook, bg=Theme.BG)
        self.notebook.add(att_frame, text="  Attendance  ")

        # This would include attendance records management, manual corrections, etc.
        ModernLabel(att_frame, text="Attendance Management", style="heading").pack(pady=Theme.SPACING_LG)
        ModernLabel(att_frame, text="Full attendance records management coming soon...", style="muted").pack()

    def create_reports_tab(self):
        """Create reports tab."""
        rep_frame = tk.Frame(self.notebook, bg=Theme.BG)
        self.notebook.add(rep_frame, text="  Reports  ")

        ModernLabel(rep_frame, text="System Reports", style="heading").pack(pady=Theme.SPACING_LG)

        # Report buttons
        btn_frame = tk.Frame(rep_frame, bg=Theme.BG)
        btn_frame.pack(pady=Theme.SPACING_MD)

        reports = [
            ("Daily Report", lambda: self.quick_report("daily")),
            ("Weekly Report", lambda: self.quick_report("weekly")),
            ("Monthly Report", lambda: self.quick_report("monthly")),
            ("Department Report", lambda: self.quick_report("department")),
            ("Trend Analysis", lambda: self.quick_report("trend")),
            ("Export All Data", self.export_all_data),
        ]

        for label, cmd in reports:
            ModernButton(btn_frame, text=label, style="secondary", command=cmd).pack(
                side="left", padx=Theme.SPACING_SM, pady=Theme.SPACING_SM)

    def create_settings_tab(self):
        """Create settings tab."""
        settings_frame = tk.Frame(self.notebook, bg=Theme.BG)
        self.notebook.add(settings_frame, text="  Settings  ")

        ModernLabel(settings_frame, text="System Settings", style="heading").pack(
            anchor="w", padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        # Work hours settings
        hours_card = Card(settings_frame, padding=Theme.SPACING_LG)
        hours_card.pack(fill="x", padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        ModernLabel(hours_card.content, text="Work Hours Configuration", style="heading").pack(anchor="w", pady=(0, Theme.SPACING_MD))

        # Work start
        start_frame = tk.Frame(hours_card.content, bg=Theme.SURFACE)
        start_frame.pack(fill="x", pady=Theme.SPACING_SM)

        ModernLabel(start_frame, text="Work Start Time:", style="subheading").pack(side="left", padx=(0, Theme.SPACING_MD))
        self.work_start_var = tk.StringVar(value="08:00")
        ModernEntry(start_frame, placeholder="HH:MM").pack(side="left", padx=Theme.SPACING_MD)
        self.start_entry = hours_card.content.winfo_children()[-1]

        # Work end
        end_frame = tk.Frame(hours_card.content, bg=Theme.SURFACE)
        end_frame.pack(fill="x", pady=Theme.SPACING_SM)

        ModernLabel(end_frame, text="Work End Time:", style="subheading").pack(side="left", padx=(0, Theme.SPACING_MD))
        self.work_end_var = tk.StringVar(value="17:00")
        ModernEntry(end_frame, placeholder="HH:MM").pack(side="left", padx=Theme.SPACING_MD)
        self.end_entry = hours_card.content.winfo_children()[-1]

        # Late threshold
        late_frame = tk.Frame(hours_card.content, bg=Theme.SURFACE)
        late_frame.pack(fill="x", pady=Theme.SPACING_SM)

        ModernLabel(late_frame, text="Late Threshold:", style="subheading").pack(side="left", padx=(0, Theme.SPACING_MD))
        self.late_threshold_var = tk.StringVar(value="08:15")
        ModernEntry(late_frame, placeholder="HH:MM").pack(side="left", padx=Theme.SPACING_MD)
        self.late_entry = hours_card.content.winfo_children()[-1]

        ModernButton(hours_card.content, text="Save Settings", style="primary",
                     command=self.save_settings).pack(anchor="w", pady=(Theme.SPACING_MD, 0))

        # Data management
        data_card = Card(settings_frame, padding=Theme.SPACING_LG)
        data_card.pack(fill="x", padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        ModernLabel(data_card.content, text="Data Management", style="heading").pack(anchor="w", pady=(0, Theme.SPACING_MD))

        data_btns = tk.Frame(data_card.content, bg=Theme.SURFACE)
        data_btns.pack(fill="x")

        ModernButton(data_btns, text="Backup Database", style="secondary",
                     command=self.backup_database).pack(side="left", padx=Theme.SPACING_SM)
        ModernButton(data_btns, text="Clear Old Records", style="warning",
                     command=self.clear_old_records).pack(side="left", padx=Theme.SPACING_SM)
        ModernButton(data_btns, text="Reset to Defaults", style="danger",
                     command=self.reset_defaults).pack(side="left", padx=Theme.SPACING_SM)

    def load_data(self):
        """Load all admin dashboard data."""
        self.load_dashboard_stats()
        self.load_employee_table()
        self.load_department_stats()

    def load_dashboard_stats(self):
        """Load dashboard statistics."""
        from ..services import AttendanceService
        from ..models import Employee

        stats = AttendanceService.get_dashboard_stats()

        # Update stat cards
        if 'total' in self.dash_stats:
            self.dash_stats['total'].value_label.config(text=str(stats['total_employees']))
        if 'present' in self.dash_stats:
            self.dash_stats['present'].value_label.config(text=str(stats['present_today']))
        if 'late' in self.dash_stats:
            self.dash_stats['late'].value_label.config(text=str(stats['late_today']))
        if 'absent' in self.dash_stats:
            self.dash_stats['absent'].value_label.config(text=str(stats['absent_today']))
        if 'on_leave' in self.dash_stats:
            self.dash_stats['on_leave'].value_label.config(text=str(stats.get('on_leave_today', 0)))

        # Departments
        dept_counts = Employee.count_by_department()
        if 'departments' in self.dash_stats:
            self.dash_stats['departments'].value_label.config(text=str(len(dept_counts)))

    def load_employee_table(self):
        """Load employee table."""
        from ..models import Employee

        employees = Employee.get_all()

        # Clear
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)

        for emp in employees:
            status = "Active" if emp.is_active else "Inactive"
            self.emp_tree.insert("", "end", values=(
                emp.employee_id,
                emp.full_name,
                emp.email or "—",
                emp.department,
                emp.position,
                emp.role.title(),
                status,
                emp.date_joined
            ), tags=("active" if emp.is_active else "inactive",))

    def load_department_stats(self):
        """Load department statistics."""
        from ..models import Employee

        dept_counts = Employee.count_by_department()

        # Clear
        for item in self.dept_tree.get_children():
            self.dept_tree.delete(item)

        for dept, count in dept_counts.items():
            self.dept_tree.insert("", "end", values=(dept, count))

    def filter_employees(self, event=None):
        """Filter employee table by search."""
        query = self.emp_search_var.get().lower()

        # Clear
        for item in self.emp_tree.get_children():
            self.emp_tree.delete(item)

        from ..models import Employee
        employees = Employee.get_all()

        for emp in employees:
            if (query in emp.full_name.lower() or
                query in emp.employee_id.lower() or
                query in emp.department.lower() or
                query in (emp.email or "").lower()):
                status = "Active" if emp.is_active else "Inactive"
                self.emp_tree.insert("", "end", values=(
                    emp.employee_id,
                    emp.full_name,
                    emp.email or "—",
                    emp.department,
                    emp.position,
                    emp.role.title(),
                    status,
                    emp.date_joined
                ))

    def show_add_employee(self):
        """Show add employee dialog."""
        self.show_employee_dialog()

    def show_employee_dialog(self, employee=None):
        """Show add/edit employee dialog."""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Employee" if employee is None else "Edit Employee")
        dialog.geometry("500x600")
        dialog.configure(bg=Theme.BG)
        dialog.transient(self.parent)
        dialog.grab_set()

        # Center
        dialog.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() // 2) - 250
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() // 2) - 300
        dialog.geometry(f"+{x}+{y}")

        # Form
        form_frame = tk.Frame(dialog, bg=Theme.BG, padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)
        form_frame.pack(fill="both", expand=True)

        ModernLabel(form_frame, text="Employee Information", style="heading").pack(anchor="w", pady=(0, Theme.SPACING_LG))

        fields = [
            ("employee_id", "Employee ID", True),
            ("full_name", "Full Name", True),
            ("email", "Email", False),
            ("phone", "Phone", False),
            ("department", "Department", True),
            ("position", "Position", True),
            ("role", "Role", True),
            ("date_joined", "Date Joined (YYYY-MM-DD)", True),
            ("password", "Password", True),
        ]

        entries = {}
        for field_name, label, required in fields:
            frame = tk.Frame(form_frame, bg=Theme.BG)
            frame.pack(fill="x", pady=Theme.SPACING_SM)

            ModernLabel(frame, text=f"{label}{' *' if required else ''}", style="subheading").pack(anchor="w")
            entry = ModernEntry(frame, placeholder=label)
            entry.pack(fill="x", pady=(Theme.SPACING_XS, 0), ipady=4)
            entries[field_name] = entry

        if employee:
            # Pre-fill
            entries['employee_id'].insert(0, employee.employee_id)
            entries['employee_id'].config(state='disabled')
            entries['full_name'].insert(0, employee.full_name)
            entries['email'].insert(0, employee.email or "")
            entries['phone'].insert(0, employee.phone or "")
            entries['department'].insert(0, employee.department)
            entries['position'].insert(0, employee.position)
            entries['role'].insert(0, employee.role)
            entries['date_joined'].insert(0, employee.date_joined)
            entries['password'].insert(0, "")

        def save():
            data = {k: v.get().strip() for k, v in entries.items()}
            # Validate required
            for field_name, label, required in fields:
                if required and not data[field_name]:
                    messagebox.showerror("Error", f"{label} is required")
                    return

            # Validate date
            try:
                date.fromisoformat(data['date_joined'])
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return

            # Validate role
            if data['role'] not in ['employee', 'supervisor', 'admin']:
                messagebox.showerror("Error", "Role must be: employee, supervisor, or admin")
                return

            try:
                if employee:
                    # Update
                    Employee.update(employee.id, {k: v for k, v in data.items() if k != 'password'})
                    if data['password']:
                        Employee.update_password(employee.id, data['password'])
                else:
                    # Create
                    Employee.create(data)
                dialog.destroy()
                self.load_employee_table()
                self.load_dashboard_stats()
                messagebox.showinfo("Success", "Employee saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {e}")

        btn_frame = tk.Frame(form_frame, bg=Theme.BG)
        btn_frame.pack(fill="x", pady=(Theme.SPACING_LG, 0))

        ModernButton(btn_frame, text="Save", style="primary", command=save).pack(side="right", padx=Theme.SPACING_SM)
        ModernButton(btn_frame, text="Cancel", style="ghost", command=dialog.destroy).pack(side="right")

    def create_emp_context_menu(self):
        """Create context menu for employee table."""
        self.emp_context_menu = tk.Menu(self.parent, tearoff=0)
        self.emp_context_menu.add_command(label="Edit", command=self.edit_selected_employee)
        self.emp_context_menu.add_command(label="Toggle Active/Inactive", command=self.toggle_employee_status)
        self.emp_context_menu.add_separator()
        self.emp_context_menu.add_command(label="Reset Password", command=self.reset_employee_password)
        self.emp_context_menu.add_command(label="View History", command=self.view_employee_history)

        def show_context(event):
            item = self.emp_tree.identify_row(event.y)
            if item:
                self.emp_tree.selection_set(item)
                self.emp_context_menu.post(event.x_root, event.y_root)

        self.emp_tree.bind("<Button-3>", show_context)

    def edit_selected_employee(self):
        """Edit selected employee."""
        selection = self.emp_tree.selection()
        if selection:
            item = self.emp_tree.item(selection[0])
            emp_id = item['values'][0]
            from ..models import Employee
            emp = Employee.get_by_employee_id(emp_id)
            if emp:
                self.show_employee_dialog(emp)

    def toggle_employee_status(self):
        """Toggle employee active status."""
        selection = self.emp_tree.selection()
        if selection:
            item = self.emp_tree.item(selection[0])
            emp_id = item['values'][0]
            from ..models import Employee
            emp = Employee.get_by_employee_id(emp_id)
            if emp:
                Employee.update(emp.id, {'is_active': not emp.is_active})
                self.load_employee_table()
                messagebox.showinfo("Success", "Employee status updated")

    def reset_employee_password(self):
        """Reset employee password."""
        selection = self.emp_tree.selection()
        if selection:
            item = self.emp_tree.item(selection[0])
            emp_id = item['values'][0]
            new_password = "password123"
            from ..models import Employee
            emp = Employee.get_by_employee_id(emp_id)
            if emp:
                Employee.update_password(emp.id, new_password)
                messagebox.showinfo("Success", f"Password reset to: {new_password}")

    def view_employee_history(self):
        """View employee attendance history."""
        selection = self.emp_tree.selection()
        if selection:
            item = self.emp_tree.item(selection[0])
            emp_id = item['values'][0]
            messagebox.showinfo("Info", f"History view for {emp_id} - Feature coming soon")

    def generate_daily_report(self):
        """Generate daily report."""
        from ..services import ReportService
        from ..models import Attendance
        import csv
        from tkinter import filedialog

        today = date.today().isoformat()
        data = ReportService.generate_daily_report(today)

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"daily_report_{today}.csv"
        )

        if filename:
            try:
                ReportService.export_to_csv(data, filename)
                messagebox.showinfo("Success", f"Report exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")

    def export_employees(self):
        """Export employees to CSV."""
        import csv
        from tkinter import filedialog
        from ..models import Employee

        employees = Employee.get_all()

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=f"employees_{date.today().isoformat()}.csv"
        )

        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Employee ID", "Name", "Email", "Phone",
                                     "Department", "Position", "Role", "Date Joined", "Status"])
                    for emp in employees:
                        writer.writerow([emp.id, emp.employee_id, emp.full_name,
                                         emp.email, emp.phone, emp.department,
                                         emp.position, emp.role, emp.date_joined,
                                         "Active" if emp.is_active else "Inactive"])
                messagebox.showinfo("Success", f"Exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")

    def import_employees(self):
        """Import employees from CSV."""
        messagebox.showinfo("Info", "CSV import feature coming soon")

    def export_all_data(self):
        """Export all system data."""
        import csv
        from tkinter import filedialog
        from ..models import Employee, Attendance

        filename = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP files", "*.zip")],
            initialfile=f"future_mall_backup_{date.today().isoformat()}.zip"
        )

        if filename:
            messagebox.showinfo("Info", "Full backup feature coming soon")

    def backup_database(self):
        """Backup database."""
        import shutil
        from ..models import get_db
        from tkinter import filedialog

        db = get_db()
        filename = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db")],
            initialfile=f"attendance_backup_{date.today().isoformat()}.db"
        )

        if filename:
            try:
                shutil.copy2(db.db_path, filename)
                messagebox.showinfo("Success", f"Database backed up to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Backup failed: {e}")

    def mark_all_absent(self):
        """Mark all absent."""
        from ..services import AttendanceService

        result = AttendanceService.mark_all_absent()
        messagebox.showinfo("Success", result['message'])
        self.load_dashboard_stats()

    def backup_database(self):
        """Backup database."""
        import shutil
        from ..models import get_db
        from tkinter import filedialog

        db = get_db()
        filename = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db")],
            initialfile=f"attendance_backup_{date.today().isoformat()}.db"
        )

        if filename:
            try:
                shutil.copy2(db.db_path, filename)
                messagebox.showinfo("Success", f"Database backed up to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Backup failed: {e}")

    def clear_old_records(self):
        """Clear old attendance records."""
        if messagebox.askyesno("Confirm", "Delete attendance records older than 1 year? This cannot be undone."):
            messagebox.showinfo("Info", "Feature coming soon")

    def reset_defaults(self):
        """Reset settings to defaults."""
        if messagebox.askyesno("Confirm", "Reset all settings to defaults? This cannot be undone."):
            from ..models import get_db
            db = get_db()
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE settings SET value = '08:00' WHERE key = 'work_start'")
                cursor.execute("UPDATE settings SET value = '17:00' WHERE key = 'work_end'")
                cursor.execute("UPDATE settings SET value = '08:15' WHERE key = 'late_threshold'")
                conn.commit()
            messagebox.showinfo("Success", "Settings reset to defaults")

    def quick_report(self, report_type: str):
        """Quick report generation."""
        messagebox.showinfo("Info", f"{report_type.title()} report generation - Feature coming soon")

    def save_settings(self):
        """Save system settings."""
        from ..models import get_db

        db = get_db()
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE settings SET value = ? WHERE key = 'work_start'",
                           (self.work_start_var.get(),))
            cursor.execute("UPDATE settings SET value = ? WHERE key = 'work_end'",
                           (self.work_end_var.get(),))
            cursor.execute("UPDATE settings SET value = ? WHERE key = 'late_threshold'",
                           (self.late_threshold_var.get(),))
            conn.commit()

        messagebox.showinfo("Success", "Settings saved successfully")

    def on_logout(self):
        """Handle logout."""
        self.on_logout()
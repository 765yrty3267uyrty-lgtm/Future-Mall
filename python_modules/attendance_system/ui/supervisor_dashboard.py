"""
Future Mall - Attendance System Supervisor Dashboard
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, timedelta
from typing import Optional, Callable

from .base import (Theme, ModernButton, ModernLabel, Card, StatCard, StatusBadge,
                   ModernEntry, ScrollableFrame)
from ..services import AttendanceService, ReportService
from ..models import Employee, Attendance


class SupervisorDashboard:
    """Supervisor dashboard with team oversight and reports."""

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
        """Setup the supervisor dashboard UI."""
        self.main_frame = tk.Frame(self.parent, bg=Theme.BG)
        self.main_frame.pack(fill="both", expand=True)

        # Header
        self.create_header()

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill="both", expand=True, padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        # Tab 1: Team Overview
        self.create_team_tab()

        # Tab 2: Daily Report
        self.create_daily_report_tab()

        # Tab 3: Weekly/Monthly Reports
        self.create_reports_tab()

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
        ModernLabel(title_frame, text="Supervisor Dashboard", style="muted").pack(anchor="w")

        # User info
        user_frame = tk.Frame(header_content, bg=Theme.SURFACE)
        user_frame.pack(side="right")

        ModernLabel(user_frame, text=self.employee.full_name, style="body").pack(anchor="e")
        ModernLabel(user_frame, text=f"Supervisor • {self.employee.department}", style="muted").pack(anchor="e")

        ModernButton(user_frame, text="Logout", style="outline",
                     command=self.on_logout, width=10).pack(anchor="e", pady=(Theme.SPACING_SM, 0))

    def create_team_tab(self):
        """Create team overview tab."""
        team_frame = tk.Frame(self.notebook, bg=Theme.BG)
        self.notebook.add(team_frame, text="  Team Overview  ")

        # Stats cards
        stats_frame = tk.Frame(team_frame, bg=Theme.BG)
        stats_frame.pack(fill="x", padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        self.stat_cards = {}
        stats = [
            ("total", "Total Employees", "0", Theme.PRIMARY, "👥"),
            ("present", "Present Today", "0", Theme.SUCCESS, "✅"),
            ("late", "Late Today", "0", Theme.WARNING, "⏰"),
            ("absent", "Absent Today", "0", Theme.DANGER, "❌"),
        ]

        for i, (key, title, value, color, icon) in enumerate(stats):
            card = StatCard(stats_frame, title, value, icon, color)
            card.grid(row=0, column=i, padx=Theme.SPACING_SM, pady=Theme.SPACING_SM, sticky="ew")
            stats_frame.grid_columnconfigure(i, weight=1)
            self.stat_cards[key] = card

        # Team table
        table_card = Card(team_frame, padding=Theme.SPACING_LG)
        table_card.pack(fill="both", expand=True, padx=Theme.SPACING_LG, pady=(0, Theme.SPACING_LG))

        # Table header
        table_header = tk.Frame(table_card.content, bg=Theme.SURFACE)
        table_header.pack(fill="x", pady=(0, Theme.SPACING_MD))

        ModernLabel(table_header, text="Team Attendance Today", style="heading").pack(side="left")

        ModernButton(table_header, text="↻ Refresh", style="ghost",
                     command=self.load_team_data, width=10).pack(side="right")

        # Team table
        self.create_team_table(table_card.content)

        # Action buttons
        action_frame = tk.Frame(table_card.content, bg=Theme.SURFACE)
        action_frame.pack(fill="x", pady=(Theme.SPACING_MD, 0))

        ModernButton(action_frame, text="Mark All Absent (End of Day)", style="danger",
                     command=self.mark_all_absent).pack(side="left")
        ModernButton(action_frame, text="Export Daily Report", style="secondary",
                     command=self.export_daily_report).pack(side="right")

    def create_team_table(self, parent):
        """Create team attendance table."""
        table_frame = tk.Frame(parent, bg=Theme.SURFACE)
        table_frame.pack(fill="both", expand=True)

        columns = ("emp_id", "name", "department", "status", "check_in", "check_out", "hours")
        self.team_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        self.team_tree.heading("emp_id", text="ID")
        self.team_tree.heading("name", text="Name")
        self.team_tree.heading("department", text="Department")
        self.team_tree.heading("status", text="Status")
        self.team_tree.heading("check_in", text="Check In")
        self.team_tree.heading("check_out", text="Check Out")
        self.team_tree.heading("hours", text="Hours")

        self.team_tree.column("emp_id", width=70, anchor="center")
        self.team_tree.column("name", width=150, anchor="w")
        self.team_tree.column("department", width=120, anchor="center")
        self.team_tree.column("status", width=100, anchor="center")
        self.team_tree.column("check_in", width=100, anchor="center")
        self.team_tree.column("check_out", width=100, anchor="center")
        self.team_tree.column("hours", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.team_tree.yview)
        self.team_tree.configure(yscrollcommand=scrollbar.set)

        self.team_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Tag configurations
        self.team_tree.tag_configure("present", background="#D1FAE5")
        self.team_tree.tag_configure("late", background="#FEF3C7")
        self.team_tree.tag_configure("absent", background="#FEE2E2")
        self.team_tree.tag_configure("on_leave", background="#DBEAFE")

    def create_daily_report_tab(self):
        """Create daily report tab."""
        report_frame = tk.Frame(self.notebook, bg=Theme.BG)
        self.notebook.add(report_frame, text="  Daily Report  ")

        # Date selector
        date_card = Card(report_frame, padding=Theme.SPACING_MD)
        date_card.pack(fill="x", padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        date_frame = tk.Frame(date_card.content, bg=Theme.SURFACE)
        date_frame.pack(fill="x")

        ModernLabel(date_frame, text="Select Date:", style="subheading").pack(side="left", padx=(0, Theme.SPACING_MD))

        self.report_date_var = tk.StringVar(value=date.today().isoformat())
        self.date_entry = ModernEntry(date_frame, placeholder="YYYY-MM-DD")
        self.date_entry.insert(0, date.today().isoformat())
        self.date_entry.pack(side="left", padx=(0, Theme.SPACING_MD), ipady=4, ipadx=10)

        ModernButton(date_frame, text="Generate Report", style="primary",
                     command=self.generate_daily_report).pack(side="left", padx=Theme.SPACING_MD)

        ModernButton(date_frame, text="Export CSV", style="secondary",
                     command=lambda: self.export_report('daily')).pack(side="left")

        # Report table
        table_card = Card(report_frame, padding=Theme.SPACING_LG)
        table_card.pack(fill="both", expand=True, padx=Theme.SPACING_LG, pady=(0, Theme.SPACING_LG))

        self.create_report_table(table_card.content)

    def create_report_table(self, parent):
        """Create report table."""
        table_frame = tk.Frame(parent, bg=Theme.SURFACE)
        table_frame.pack(fill="both", expand=True)

        columns = ("emp_id", "name", "department", "check_in", "check_out", "hours", "status")
        self.report_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.report_tree.heading("emp_id", text="ID")
        self.report_tree.heading("name", text="Name")
        self.report_tree.heading("department", text="Department")
        self.report_tree.heading("check_in", text="Check In")
        self.report_tree.heading("check_out", text="Check Out")
        self.report_tree.heading("hours", text="Hours")
        self.report_tree.heading("status", text="Status")

        for col in columns:
            self.report_tree.column(col, width=120, anchor="center" if col != "name" else "w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=scrollbar.set)

        self.report_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_reports_tab(self):
        """Create weekly/monthly reports tab."""
        reports_frame = tk.Frame(self.notebook, bg=Theme.BG)
        self.notebook.add(reports_frame, text="  Reports  ")

        # Report type selector
        selector_card = Card(reports_frame, padding=Theme.SPACING_MD)
        selector_card.pack(fill="x", padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        selector_frame = tk.Frame(selector_card.content, bg=Theme.SURFACE)
        selector_frame.pack(fill="x")

        ModernLabel(selector_frame, text="Report Type:", style="subheading").pack(side="left", padx=(0, Theme.SPACING_MD))

        self.report_type_var = tk.StringVar(value="weekly")
        for value, label in [("weekly", "Weekly"), ("monthly", "Monthly"), ("department", "By Department")]:
            rb = tk.Radiobutton(selector_frame, text=label, variable=self.report_type_var,
                                value=value, bg=Theme.SURFACE, font=Theme.FONT_BODY,
                                fg=Theme.TEXT, selectcolor=Theme.SURFACE,
                                activebackground=Theme.SURFACE)
            rb.pack(side="left", padx=Theme.SPACING_MD)

        # Parameters frame
        self.params_frame = tk.Frame(selector_card.content, bg=Theme.SURFACE)
        self.params_frame.pack(fill="x", pady=(Theme.SPACING_MD, 0))

        self.create_report_params()

        ModernButton(selector_frame, text="Generate", style="primary",
                     command=self.generate_custom_report).pack(side="left", padx=Theme.SPACING_LG)
        ModernButton(selector_frame, text="Export CSV", style="secondary",
                     command=lambda: self.export_report('custom')).pack(side="left")

        # Report results
        results_card = Card(reports_frame, padding=Theme.SPACING_LG)
        results_card.pack(fill="both", expand=True, padx=Theme.SPACING_LG, pady=(0, Theme.SPACING_LG))

        self.create_custom_report_table(results_card.content)

        # Bind report type change
        self.report_type_var.trace("w", self.on_report_type_change)

    def create_report_params(self):
        """Create dynamic report parameters based on type."""
        # Clear existing
        for widget in self.params_frame.winfo_children():
            widget.destroy()

        report_type = self.report_type_var.get()
        today = date.today()

        if report_type == "weekly":
            ModernLabel(self.params_frame, text="Week Start (Monday):", style="muted").pack(side="left", padx=(0, Theme.SPACING_MD))
            self.week_start_var = tk.StringVar(value=(today - timedelta(days=today.weekday())).isoformat())
            ModernEntry(self.params_frame, placeholder="YYYY-MM-DD").pack(side="left", padx=(0, Theme.SPACING_MD))
            self.params_frame.children['!entry'].insert(0, self.week_start_var.get())

        elif report_type == "monthly":
            ModernLabel(self.params_frame, text="Month:", style="muted").pack(side="left", padx=(0, Theme.SPACING_MD))
            self.month_var = tk.StringVar(value=today.strftime("%Y-%m"))
            ModernEntry(self.params_frame, placeholder="YYYY-MM").pack(side="left", padx=(0, Theme.SPACING_MD))
            self.params_frame.children['!entry'].insert(0, self.month_var.get())

        elif report_type == "department":
            ModernLabel(self.params_frame, text="Department:", style="muted").pack(side="left", padx=(0, Theme.SPACING_MD))
            self.dept_var = tk.StringVar(value="IT")
            dept_combo = ttk.Combobox(self.params_frame, textvariable=self.dept_var,
                                      values=["IT", "HR", "Finance", "Operations", "Marketing", "Customer Service"],
                                      state="readonly", width=20)
            dept_combo.pack(side="left", padx=(0, Theme.SPACING_MD))

            ModernLabel(self.params_frame, text="Start Date:", style="muted").pack(side="left", padx=(Theme.SPACING_MD, Theme.SPACING_MD))
            self.start_date_var = tk.StringVar(value=(today - timedelta(days=30)).isoformat())
            ModernEntry(self.params_frame, placeholder="YYYY-MM-DD").pack(side="left", padx=(0, Theme.SPACING_MD))
            self.params_frame.children['!entry'].insert(0, self.start_date_var.get())

            ModernLabel(self.params_frame, text="End Date:", style="muted").pack(side="left", padx=(Theme.SPACING_MD, Theme.SPACING_MD))
            self.end_date_var = tk.StringVar(value=today.isoformat())
            ModernEntry(self.params_frame, placeholder="YYYY-MM-DD").pack(side="left", padx=(0, Theme.SPACING_MD))
            self.params_frame.children['!entry'].insert(0, self.end_date_var.get())

    def on_report_type_change(self, *args):
        """Handle report type change."""
        self.create_report_params()

    def create_custom_report_table(self, parent):
        """Create custom report table."""
        table_frame = tk.Frame(parent, bg=Theme.SURFACE)
        table_frame.pack(fill="both", expand=True)

        self.custom_tree = ttk.Treeview(table_frame, show="headings", height=12)
        self.custom_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.custom_tree.yview)
        self.custom_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def load_data(self):
        """Load all dashboard data."""
        self.load_team_overview()
        self.load_team_table()

    def load_team_overview(self):
        """Load team overview stats."""
        from ..services import AttendanceService

        stats = AttendanceService.get_dashboard_stats()

        self.stat_cards['total'].value_label.config(text=str(stats['total_employees']))
        self.stat_cards['present'].value_label.config(text=str(stats['present_today']))
        self.stat_cards['late'].value_label.config(text=str(stats['late_today']))
        self.stat_cards['absent'].value_label.config(text=str(stats['absent_today']))

    def load_team_table(self):
        """Load team attendance table."""
        from ..services import AttendanceService

        data = AttendanceService.get_all_employees_today_status()

        # Clear
        for item in self.team_tree.get_children():
            self.team_tree.delete(item)

        for emp in data:
            check_in = emp['check_in']
            check_out = emp['check_out']

            if check_in:
                check_in_str = datetime.fromisoformat(check_in).strftime("%H:%M")
            else:
                check_in_str = "--:--"

            if check_out:
                check_out_str = datetime.fromisoformat(check_out).strftime("%H:%M")
            else:
                check_out_str = "--:--"

            self.team_tree.insert("", "end", values=(
                emp['employee_id'],
                emp['full_name'],
                emp['department'],
                emp['status'].replace("_", " ").title(),
                datetime.fromisoformat(emp['check_in']).strftime("%H:%M") if emp['check_in'] else "--:--",
                datetime.fromisoformat(emp['check_out']).strftime("%H:%M") if emp['check_out'] else "--:--",
                f"{emp['working_hours']:.2f}"
            ), tags=(emp['status'],))

    def generate_daily_report(self):
        """Generate daily report for selected date."""
        from ..services import ReportService

        report_date = self.date_entry.get()
        try:
            datetime.strptime(report_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return

        data = ReportService.generate_daily_report(report_date)

        # Clear
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)

        for row in data:
            check_in = row['check_in']
            check_out = row['check_out']

            check_in_str = datetime.fromisoformat(check_in).strftime("%H:%M") if check_in else "--:--"
            check_out_str = datetime.fromisoformat(check_out).strftime("%H:%M") if check_out else "--:--"

            self.report_tree.insert("", "end", values=(
                row['employee_id'],
                row['full_name'],
                row['department'],
                check_in_str,
                check_out_str,
                f"{row['working_hours']:.2f}",
                row['status'].replace("_", " ").title()
            ), tags=(row['status'],))

    def generate_custom_report(self):
        """Generate custom report based on selected type."""
        from ..services import ReportService
        from ..models import Attendance

        report_type = self.report_type_var.get()

        try:
            if report_type == "weekly":
                # For demo, use first employee
                employees = Employee.get_all({'is_active': True})
                if not employees:
                    return
                emp = employees[0]
                week_start = self.week_start_var.get()
                data = ReportService.generate_weekly_report(emp.id, week_start)

            elif report_type == "monthly":
                employees = Employee.get_all({'is_active': True})
                if not employees:
                    return
                emp = employees[0]
                year = int(self.month_var.get()[:4])
                month = int(self.month_var.get()[5:])
                data = ReportService.generate_monthly_report(emp.id, year, month)

            elif report_type == "department":
                data = ReportService.generate_department_report(
                    self.dept_var.get(),
                    self.start_date_var.get(),
                    self.end_date_var.get()
                )
            else:
                return

            # Clear and update custom tree
            for item in self.custom_tree.get_children():
                self.custom_tree.delete(item)

            if data:
                # Configure columns dynamically
                cols = list(data[0].keys())
                self.custom_tree["columns"] = cols
                for col in cols:
                    self.custom_tree.heading(col, text=col.replace("_", " ").title())
                    self.custom_tree.column(col, width=120, anchor="center")

                for row in data:
                    vals = []
                    for col in data[0].keys():
                        val = row[col]
                        if isinstance(val, datetime):
                            vals.append(val.strftime("%H:%M"))
                        elif isinstance(val, date):
                            vals.append(val.isoformat())
                        else:
                            vals.append(str(val) if val is not None else "")
                    self.custom_tree.insert("", "end", values=vals)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    def export_report(self, report_type: str):
        """Export report to CSV."""
        from ..services import ReportService
        import csv
        from tkinter import filedialog

        try:
            if report_type == 'daily':
                report_date = self.date_entry.get()
                data = ReportService.generate_daily_report(report_date)
            elif report_type == 'custom':
                # Use last generated data
                messagebox.showinfo("Info", "Please generate report first")
                return
            else:
                return

            if not data:
                messagebox.showinfo("Info", "No data to export")
                return

            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"attendance_report_{date.today().isoformat()}.csv"
            )

            if filename:
                ReportService.export_to_csv(data, filename)
                messagebox.showinfo("Success", f"Report exported to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {e}")

    def load_data(self):
        """Load all dashboard data."""
        self.load_team_overview()
        self.load_team_table()
        self.generate_daily_report()

    def load_team_data(self):
        """Refresh team data."""
        self.load_team_overview()
        self.load_team_table()

    def mark_all_absent(self):
        """Mark all employees without check-in as absent."""
        from ..services import AttendanceService

        result = AttendanceService.mark_all_absent()
        messagebox.showinfo("Success", result['message'])
        self.load_team_data()

    def on_logout(self):
        """Handle logout."""
        self.on_logout()
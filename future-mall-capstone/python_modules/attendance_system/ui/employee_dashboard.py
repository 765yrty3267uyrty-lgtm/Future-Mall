"""
Future Mall - Attendance System Employee Dashboard
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from typing import Optional, Callable

from .base import (Theme, ModernButton, ModernLabel, Card, StatCard, StatusBadge,
                   ScrollableFrame, ModernEntry)
from ..services import AttendanceService


class EmployeeDashboard:
    """Employee dashboard with check-in/out and history."""

    def __init__(self, parent: tk.Widget, employee_id: int,
                 on_logout: Callable[[], None]):
        self.parent = parent
        self.employee_id = employee_id
        self.on_logout = on_logout

        # Load employee data
        from ..models import Employee
        self.employee = Employee.get_by_id(employee_id)

        self.setup_ui()
        self.load_data()
        self.start_clock()

    def setup_ui(self):
        """Setup the dashboard UI."""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg=Theme.BG)
        self.main_frame.pack(fill="both", expand=True)

        # Header
        self.create_header()

        # Content area with sidebar
        content_frame = tk.Frame(self.main_frame, bg=Theme.BG)
        content_frame.pack(fill="both", expand=True, padx=Theme.SPACING_LG, pady=Theme.SPACING_LG)

        # Left column - Main content
        left_column = tk.Frame(content_frame, bg=Theme.BG)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, Theme.SPACING_MD))

        # Right column - Stats (for wider screens)
        right_column = tk.Frame(content_frame, bg=Theme.BG, width=280)
        right_column.pack(side="right", fill="y", padx=(Theme.SPACING_MD, 0))
        right_column.pack_propagate(False)

        # Today's status card
        self.create_today_status(left_column)

        # Check-in/out buttons
        self.create_action_buttons(left_column)

        # Quick stats
        self.create_quick_stats(right_column)

        # History section
        self.create_history_section(left_column)

    def create_header(self):
        """Create dashboard header."""
        header = tk.Frame(self.main_frame, bg=Theme.SURFACE,
                          highlightbackground=Theme.BORDER,
                          highlightthickness=1)
        header.pack(fill="x", padx=Theme.SPACING_LG, pady=(Theme.SPACING_LG, 0))

        header_content = tk.Frame(header, bg=Theme.SURFACE)
        header_content.pack(fill="x", padx=Theme.SPACING_LG, pady=Theme.SPACING_MD)

        # Logo and title
        title_frame = tk.Frame(header_content, bg=Theme.SURFACE)
        title_frame.pack(side="left")

        ModernLabel(title_frame, text="🏢 Future Mall", style="heading").pack(anchor="w")
        ModernLabel(title_frame, text="Employee Dashboard", style="muted").pack(anchor="w")

        # User info and logout
        user_frame = tk.Frame(header_content, bg=Theme.SURFACE)
        user_frame.pack(side="right")

        # Current time
        self.time_label = ModernLabel(user_frame, text="", style="muted")
        self.time_label.pack(anchor="e")

        # User name and role
        user_info = tk.Frame(user_frame, bg=Theme.SURFACE)
        user_info.pack(anchor="e", pady=(Theme.SPACING_XS, 0))

        ModernLabel(user_info, text=self.employee.full_name, style="body").pack(anchor="e")
        ModernLabel(user_info, text=f"{self.employee.employee_id} • {self.employee.department}",
                    style="muted").pack(anchor="e")

        # Logout button
        ModernButton(user_info, text="Logout", style="outline",
                     command=self.on_logout, width=10).pack(anchor="e", pady=(Theme.SPACING_SM, 0))

    def create_today_status(self, parent):
        """Create today's attendance status card."""
        self.status_card = Card(parent, padding=Theme.SPACING_LG)
        self.status_card.pack(fill="x", pady=(0, Theme.SPACING_LG))

        # Title
        ModernLabel(self.status_card.content, text="Today's Status", style="heading").pack(anchor="w")

        # Status display
        self.status_frame = tk.Frame(self.status_card.content, bg=Theme.SURFACE)
        self.status_frame.pack(fill="x", pady=Theme.SPACING_MD)

        # Status badge
        self.status_badge = StatusBadge(self.status_frame, "not_recorded")
        self.status_badge.pack(side="left", padx=(0, Theme.SPACING_MD))

        # Check-in/out times
        self.time_info_frame = tk.Frame(self.status_frame, bg=Theme.SURFACE)
        self.time_info_frame.pack(side="left", fill="x", expand=True)

        self.check_in_label = ModernLabel(self.time_info_frame, text="Check-in: --:--", style="body")
        self.check_in_label.pack(anchor="w")

        self.check_out_label = ModernLabel(self.time_info_frame, text="Check-out: --:--", style="muted")
        self.check_out_label.pack(anchor="w")

        # Working hours
        self.hours_label = ModernLabel(self.status_frame, text="Hours: 0.00h", style="subheading")
        self.hours_label.config(fg=Theme.PRIMARY)
        self.hours_label.pack(side="right")

    def create_action_buttons(self, parent):
        """Create check-in/out action buttons."""
        btn_card = Card(parent, padding=Theme.SPACING_LG)
        btn_card.pack(fill="x", pady=(0, Theme.SPACING_LG))

        ModernLabel(btn_card.content, text="Actions", style="heading").pack(anchor="w", pady=(0, Theme.SPACING_MD))

        btn_frame = tk.Frame(btn_card.content, bg=Theme.SURFACE)
        btn_frame.pack(fill="x")

        # Check-in button
        self.check_in_btn = ModernButton(
            btn_frame, text="⏰ Check In", style="primary",
            command=self.on_check_in, height=2
        )
        self.check_in_btn.pack(side="left", fill="x", expand=True, padx=(0, Theme.SPACING_SM))

        # Check-out button
        self.check_out_btn = ModernButton(
            btn_frame, text="🏁 Check Out", style="accent",
            command=self.on_check_out, height=2
        )
        self.check_out_btn.pack(side="left", fill="x", expand=True, padx=(Theme.SPACING_SM, 0))

    def create_quick_stats(self, parent):
        """Create quick stats cards."""
        stats_card = Card(parent, padding=Theme.SPACING_MD)
        stats_card.pack(fill="x", pady=(0, Theme.SPACING_LG))

        ModernLabel(stats_card.content, text="This Month", style="heading").pack(anchor="w", pady=(0, Theme.SPACING_MD))

        # Stats grid
        stats_grid = tk.Frame(stats_card.content, bg=Theme.SURFACE)
        stats_grid.pack(fill="x")

        self.stat_present = self._create_mini_stat(stats_grid, "Present", "0", Theme.SUCCESS, 0, 0)
        self.stat_late = self._create_mini_stat(stats_grid, "Late", "0", Theme.WARNING, 0, 1)
        self.stat_absent = self._create_mini_stat(stats_grid, "Absent", "0", Theme.DANGER, 1, 0)
        self.stat_hours = self._create_mini_stat(stats_grid, "Hours", "0.0h", Theme.PRIMARY, 1, 1)

        # Attendance rate
        rate_frame = tk.Frame(stats_card.content, bg=Theme.SURFACE)
        rate_frame.pack(fill="x", pady=(Theme.SPACING_MD, 0))

        ModernLabel(rate_frame, text="Attendance Rate", style="muted").pack(anchor="w")
        self.rate_label = ModernLabel(rate_frame, text="0%", style="heading")
        self.rate_label.config(fg=Theme.PRIMARY)
        self.rate_label.pack(anchor="w")

    def _create_mini_stat(self, parent, label: str, value: str, color: str, row: int, col: int) -> ModernLabel:
        """Create a mini stat display."""
        frame = tk.Frame(parent, bg=Theme.SURFACE)
        frame.grid(row=row, column=col, padx=Theme.SPACING_SM, pady=Theme.SPACING_SM, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)

        color_indicator = tk.Frame(frame, width=4, height=24, bg=color)
        color_indicator.pack(side="left", padx=(0, Theme.SPACING_SM))

        text_frame = tk.Frame(frame, bg=Theme.SURFACE)
        text_frame.pack(side="left", fill="x", expand=True)

        ModernLabel(text_frame, text=label, style="small").pack(anchor="w")
        value_label = ModernLabel(text_frame, text=value, style="subheading")
        value_label.config(fg=color)
        value_label.pack(anchor="w")

        return value_label

    def create_history_section(self, parent):
        """Create attendance history section."""
        history_card = Card(parent, padding=Theme.SPACING_LG)
        history_card.pack(fill="both", expand=True)

        # Header with title and refresh
        header_frame = tk.Frame(history_card.content, bg=Theme.SURFACE)
        header_frame.pack(fill="x", pady=(0, Theme.SPACING_MD))

        ModernLabel(header_frame, text="Attendance History", style="heading").pack(side="left")

        ModernButton(header_frame, text="↻ Refresh", style="ghost",
                     command=self.load_history, width=10).pack(side="right")

        # History table
        self.create_history_table(history_card.content)

    def create_history_table(self, parent):
        """Create attendance history table."""
        # Table frame with scrollbar
        table_frame = tk.Frame(parent, bg=Theme.SURFACE)
        table_frame.pack(fill="both", expand=True)

        # Treeview
        columns = ("date", "check_in", "check_out", "hours", "overtime", "status")
        self.history_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        # Configure columns
        self.history_tree.heading("date", text="Date")
        self.history_tree.heading("check_in", text="Check In")
        self.history_tree.heading("check_out", text="Check Out")
        self.history_tree.heading("hours", text="Hours")
        self.history_tree.heading("overtime", text="OT")
        self.history_tree.heading("status", text="Status")

        self.history_tree.column("date", width=100, anchor="center")
        self.history_tree.column("check_in", width=100, anchor="center")
        self.history_tree.column("check_out", width=100, anchor="center")
        self.history_tree.column("hours", width=70, anchor="center")
        self.history_tree.column("overtime", width=60, anchor="center")
        self.history_tree.column("status", width=100, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Style
        style = ttk.Style()
        style.configure("Treeview", font=Theme.FONT_BODY, rowheight=32)
        style.configure("Treeview.Heading", font=Theme.FONT_SUBHEADING)
        style.map("Treeview", background=[("selected", Theme.PRIMARY_LIGHT)])

        # Tag configurations for status colors
        self.history_tree.tag_configure("present", background="#D1FAE5")
        self.history_tree.tag_configure("late", background="#FEF3C7")
        self.history_tree.tag_configure("absent", background="#FEE2E2")
        self.history_tree.tag_configure("on_leave", background="#DBEAFE")

    def load_data(self):
        """Load all dashboard data."""
        self.load_today_status()
        self.load_quick_stats()
        self.load_history()

    def load_today_status(self):
        """Load today's attendance status."""
        from ..models import Attendance

        record = Attendance.get_today(self.employee_id)

        if record:
            self.update_status_display(record)
        else:
            self.update_status_display(None)

        # Update button states
        self.update_button_states(record)

    def update_status_display(self, record):
        """Update status display with record data."""
        if record:
            self.status_badge.config(text=record.status.replace("_", " ").title())
            # Update badge color
            self.status_badge.destroy()
            self.status_badge = StatusBadge(self.status_frame, record.status)
            self.status_badge.pack(side="left", padx=(0, Theme.SPACING_MD))

            check_in_str = "--:--"
            check_out_str = "--:--"

            if record.check_in:
                dt = datetime.fromisoformat(record.check_in)
                check_in_str = dt.strftime("%H:%M")
            if record.check_out:
                dt = datetime.fromisoformat(record.check_out)
                check_out_str = dt.strftime("%H:%M")

            self.check_in_label.config(text=f"Check-in: {check_in_str}")
            self.check_out_label.config(text=f"Check-out: {check_out_str}")
            self.hours_label.config(text=f"Hours: {record.working_hours:.2f}h")
        else:
            self.status_badge.config(text="Not Recorded")
            self.check_in_label.config(text="Check-in: --:--")
            self.check_out_label.config(text="Check-out: --:--")
            self.hours_label.config(text="Hours: 0.00h")

    def update_button_states(self, record):
        """Update check-in/out button states based on record."""
        if record is None:
            # No record - can check in
            self.check_in_btn.set_state("normal")
            self.check_out_btn.set_state("disabled")
        elif record.check_in and not record.check_out:
            # Checked in, not out - can check out
            self.check_in_btn.set_state("disabled")
            self.check_out_btn.set_state("normal")
        else:
            # Both done - both disabled
            self.check_in_btn.set_state("disabled")
            self.check_out_btn.set_state("disabled")

    def load_quick_stats(self):
        """Load monthly quick stats."""
        from ..models import Attendance
        from ..services import StatsService

        today = date.today()
        start_of_month = today.replace(day=1).isoformat()
        end_of_month = today.isoformat()

        records = Attendance.get_history(self.employee_id, start_of_month, end_of_month)

        present = sum(1 for r in records if r.status == 'present')
        late = sum(1 for r in records if r.status == 'late')
        absent = sum(1 for r in records if r.status == 'absent')
        total_hours = sum(r.working_hours for r in records)
        total_days = len(records)

        self.stat_present.config(text=str(present))
        self.stat_late.config(text=str(late))
        self.stat_absent.config(text=str(absent))
        self.stat_hours.config(text=f"{total_hours:.1f}h")

        if total_days > 0:
            rate = round(((present + late) / total_days) * 100)
        else:
            rate = 0
        self.rate_label.config(text=f"{rate}%")

    def load_history(self):
        """Load attendance history."""
        from ..models import Attendance

        # Clear existing
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Get last 30 days
        end_date = date.today().isoformat()
        start_date = (date.today() - timedelta(days=30)).isoformat()

        records = Attendance.get_history(self.employee_id, start_date, end_date)

        for record in records:
            check_in_str = "--:--"
            check_out_str = "--:--"
            if record.check_in:
                check_in_str = datetime.fromisoformat(record.check_in).strftime("%H:%M")
            if record.check_out:
                check_out_str = datetime.fromisoformat(record.check_out).strftime("%H:%M")

            overtime_str = f"{record.overtime_hours:.2f}" if record.overtime_hours > 0 else "0.00"

            self.history_tree.insert("", "end", values=(
                record.date,
                check_in_str,
                check_out_str,
                f"{record.working_hours:.2f}",
                overtime_str,
                record.status.replace("_", " ").title()
            ), tags=(record.status,))

    def start_clock(self):
        """Start the clock update loop."""
        self.update_clock()

    def update_clock(self):
        """Update the clock display."""
        now = datetime.now()
        self.time_label.config(text=now.strftime("%A, %B %d, %Y • %H:%M:%S"))
        self.parent.after(1000, self.update_clock)

    def on_check_in(self):
        """Handle check-in button click."""
        result = AttendanceService.perform_check_in(self.employee_id)

        if result['success']:
            messagebox.showinfo("Success", result['message'])
            self.load_today_status()
        else:
            messagebox.showerror("Error", result['message'])

    def on_check_out(self):
        """Handle check-out button click."""
        result = AttendanceService.perform_check_out(self.employee_id)

        if result['success']:
            messagebox.showinfo("Success",
                f"{result['message']}\nHours worked: {result['working_hours']:.2f}h\nOvertime: {result['overtime_hours']:.2f}h")
            self.load_today_status()
        else:
            messagebox.showerror("Error", result['message'])

    def on_logout(self):
        """Handle logout."""
        self.on_logout()
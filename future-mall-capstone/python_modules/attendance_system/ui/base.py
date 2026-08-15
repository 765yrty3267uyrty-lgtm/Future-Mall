"""
Future Mall - Attendance System Base UI Components
Theme system and reusable styled widgets.
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Any

# Theme colors matching Future Mall brand
class Theme:
    """Future Mall color theme for the attendance system."""
    # Primary - Future Blue
    PRIMARY = "#2563EB"
    PRIMARY_HOVER = "#1D4ED8"
    PRIMARY_LIGHT = "#DBEAFE"

    # Secondary - Innovation Teal
    SECONDARY = "#0D9488"
    SECONDARY_HOVER = "#0F766E"
    SECONDARY_LIGHT = "#CCFBF1"

    # Accent - Energy Orange
    ACCENT = "#F97316"
    ACCENT_HOVER = "#EA580C"
    ACCENT_LIGHT = "#FFEDD5"

    # Semantic
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    INFO = "#3B82F6"

    # Neutral
    BG = "#F8FAFC"
    SURFACE = "#FFFFFF"
    TEXT = "#1E293B"
    TEXT_MUTED = "#64748B"
    BORDER = "#E2E8F0"
    BORDER_LIGHT = "#F1F5F9"

    # Fonts
    FONT_DISPLAY = ("Space Grotesk", 24, "bold")
    FONT_HEADING = ("Space Grotesk", 16, "bold")
    FONT_SUBHEADING = ("Space Grotesk", 13, "bold")
    FONT_BODY = ("Inter", 11)
    FONT_SMALL = ("Inter", 9)
    FONT_MONO = ("JetBrains Mono", 10)

    # Spacing
    SPACING_XS = 4
    SPACING_SM = 8
    SPACING_MD = 16
    SPACING_LG = 24
    SPACING_XL = 32

    # Radius
    RADIUS_SM = 4
    RADIUS_MD = 8
    RADIUS_LG = 12
    RADIUS_XL = 16

    # Shadows (simulated with borders)
    SHADOW_LIGHT = "#E2E8F0"
    SHADOW_MEDIUM = "#CBD5E1"


class StyledWidget:
    """Base class for styled widgets with theme support."""

    def __init__(self, parent: tk.Widget, **kwargs):
        self.parent = parent
        self.widget = None

    def apply_style(self):
        """Apply theme styles to the widget."""
        pass


class ModernButton(tk.Button):
    """Modern styled button with hover effects."""

    def __init__(self, parent, text="", command=None, style="primary",
                 width=None, height=None, **kwargs):
        # Remove style from kwargs to avoid conflicts
        kwargs.pop('style', None)

        # Configure base button
        super().__init__(parent, text=text, command=command,
                         font=Theme.FONT_BODY, cursor="hand2",
                         relief="flat", borderwidth=0, **kwargs)

        self.style_type = style
        self._setup_style(style)

        if width:
            self.config(width=width)
        if height:
            self.config(height=height)

        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _setup_style(self, style: str):
        """Setup button style based on type."""
        styles = {
            "primary": {
                "bg": Theme.PRIMARY, "fg": "white",
                "active_bg": Theme.PRIMARY_HOVER, "active_fg": "white",
                "hover_bg": Theme.PRIMARY_HOVER,
            },
            "secondary": {
                "bg": Theme.SECONDARY, "fg": "white",
                "active_bg": Theme.SECONDARY_HOVER, "active_fg": "white",
                "hover_bg": Theme.SECONDARY_HOVER,
            },
            "accent": {
                "bg": Theme.ACCENT, "fg": "white",
                "active_bg": Theme.ACCENT_HOVER, "active_fg": "white",
                "hover_bg": Theme.ACCENT_HOVER,
            },
            "success": {
                "bg": Theme.SUCCESS, "fg": "white",
                "active_bg": "#059669", "active_fg": "white",
                "hover_bg": "#059669",
            },
            "danger": {
                "bg": Theme.DANGER, "fg": "white",
                "active_bg": "#DC2626", "active_fg": "white",
                "hover_bg": "#DC2626",
            },
            "outline": {
                "bg": Theme.SURFACE, "fg": Theme.PRIMARY,
                "active_bg": Theme.PRIMARY_LIGHT, "active_fg": Theme.PRIMARY,
                "hover_bg": Theme.PRIMARY_LIGHT,
            },
            "ghost": {
                "bg": "transparent", "fg": Theme.PRIMARY,
                "active_bg": Theme.PRIMARY_LIGHT, "active_fg": Theme.PRIMARY,
                "hover_bg": Theme.PRIMARY_LIGHT,
            },
        }

        s = styles.get(style, styles["primary"])
        self.style_config = s
        self.config(bg=s["bg"], fg=s["fg"],
                    activebackground=s["active_bg"], activeforeground=s["active_fg"])

        # Handle transparent background
        if s["bg"] == "transparent":
            self.config(bg=Theme.BG)

    def _on_enter(self, e):
        if self["state"] != "disabled":
            self.config(bg=self.style_config.get("hover_bg", self.style_config["active_bg"]))

    def _on_leave(self, e):
        if self["state"] != "disabled":
            self.config(bg=self.style_config["bg"])

    def _on_press(self, e):
        if self["state"] != "disabled":
            self.config(bg=self.style_config["active_bg"])

    def _on_release(self, e):
        if self["state"] != "disabled":
            self.config(bg=self.style_config.get("hover_bg", self.style_config["bg"]))

    def set_state(self, state: str):
        """Set button state and update appearance."""
        self.config(state=state)
        if state == "disabled":
            self.config(bg=Theme.BORDER, fg=Theme.TEXT_MUTED)
        else:
            self.config(bg=self.style_config["bg"], fg=self.style_config["fg"])


class Card(tk.Frame):
    """Card container with border and optional shadow effect."""

    def __init__(self, parent, padding=Theme.SPACING_MD, **kwargs):
        super().__init__(parent, bg=Theme.SURFACE,
                         highlightbackground=Theme.BORDER,
                         highlightthickness=1, **kwargs)
        self.padding = padding
        self.pack_propagate(False)
        self._create_inner_frame()

    def _create_inner_frame(self):
        """Create inner content frame with padding."""
        self.content = tk.Frame(self, bg=Theme.SURFACE)
        self.content.pack(fill="both", expand=True,
                          padx=self.padding, pady=self.padding)

    def add(self, widget, **pack_kwargs):
        """Add widget to card content."""
        widget.pack(in_=self.content, **pack_kwargs)
        return widget


class ModernEntry(tk.Entry):
    """Modern styled entry field with focus effects."""

    def __init__(self, parent, placeholder="", show=None, **kwargs):
        super().__init__(parent, font=Theme.FONT_BODY,
                         relief="flat", borderwidth=1,
                         highlightthickness=1,
                         highlightbackground=Theme.BORDER,
                         highlightcolor=Theme.PRIMARY,
                         **kwargs)

        self.placeholder = placeholder
        self.show_char = show
        self._has_placeholder = False

        if placeholder:
            self._show_placeholder()

        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

    def _show_placeholder(self):
        """Show placeholder text."""
        self.config(fg=Theme.TEXT_MUTED, show="")
        self.delete(0, tk.END)
        self.insert(0, self.placeholder)
        self._has_placeholder = True

    def _hide_placeholder(self):
        """Hide placeholder text."""
        if self._has_placeholder:
            self.delete(0, tk.END)
            self.config(fg=Theme.TEXT, show=self.show_char if self.show_char else "")
            self._has_placeholder = False

    def _on_focus_in(self, e):
        self.config(highlightbackground=Theme.PRIMARY, highlightcolor=Theme.PRIMARY)
        self._hide_placeholder()

    def _on_focus_out(self, e):
        self.config(highlightbackground=Theme.BORDER)
        if not self.get():
            self._show_placeholder()

    def get_value(self) -> str:
        """Get actual value (empty if placeholder is showing)."""
        if self._has_placeholder:
            return ""
        return self.get()


class ModernLabel(tk.Label):
    """Modern styled label with theme support."""

    def __init__(self, parent, text="", style="body", **kwargs):
        styles = {
            "display": {"font": Theme.FONT_DISPLAY, "fg": Theme.TEXT},
            "heading": {"font": Theme.FONT_HEADING, "fg": Theme.TEXT},
            "subheading": {"font": Theme.FONT_SUBHEADING, "fg": Theme.TEXT},
            "body": {"font": Theme.FONT_BODY, "fg": Theme.TEXT},
            "muted": {"font": Theme.FONT_BODY, "fg": Theme.TEXT_MUTED},
            "small": {"font": Theme.FONT_SMALL, "fg": Theme.TEXT_MUTED},
            "success": {"font": Theme.FONT_BODY, "fg": Theme.SUCCESS},
            "warning": {"font": Theme.FONT_BODY, "fg": Theme.WARNING},
            "danger": {"font": Theme.FONT_BODY, "fg": Theme.DANGER},
            "primary": {"font": Theme.FONT_BODY, "fg": Theme.PRIMARY},
        }

        style_config = styles.get(style, styles["body"])
        super().__init__(parent, text=text, bg=Theme.SURFACE, **style_config, **kwargs)


class StatusBadge(tk.Label):
    """Status indicator badge."""

    STATUS_COLORS = {
        "present": (Theme.SUCCESS, "#D1FAE5"),
        "late": (Theme.WARNING, "#FEF3C7"),
        "absent": (Theme.DANGER, "#FEE2E2"),
        "on_leave": (Theme.INFO, "#DBEAFE"),
        "holiday": (Theme.SECONDARY, "#CCFBF1"),
        "not_recorded": (Theme.TEXT_MUTED, "#F1F5F9"),
    }

    def __init__(self, parent, status="not_recorded", **kwargs):
        fg_color, bg_color = self.STATUS_COLORS.get(status, self.STATUS_COLORS["not_recorded"])
        super().__init__(parent, text=status.replace("_", " ").title(),
                         font=Theme.FONT_SMALL, fg=fg_color, bg=bg_color,
                         padx=Theme.SPACING_SM, pady=2, **kwargs)


class StatCard(tk.Frame):
    """Dashboard statistic card."""

    def __init__(self, parent, title: str, value: str, icon: str = "",
                 color: str = Theme.PRIMARY, trend: str = "", **kwargs):
        super().__init__(parent, bg=Theme.SURFACE,
                         highlightbackground=Theme.BORDER,
                         highlightthickness=1, **kwargs)

        self.config(padx=Theme.SPACING_MD, pady=Theme.SPACING_MD)

        # Header with icon and title
        header = tk.Frame(self, bg=Theme.SURFACE)
        header.pack(fill="x", pady=(0, Theme.SPACING_SM))

        if icon:
            icon_label = tk.Label(header, text=icon, font=("Segoe UI Emoji", 16),
                                  fg=color, bg=Theme.SURFACE)
            icon_label.pack(side="left", padx=(0, Theme.SPACING_SM))

        title_label = ModernLabel(header, text=title, style="muted")
        title_label.pack(side="left")

        # Value
        value_label = tk.Label(self, text=value, font=("Space Grotesk", 28, "bold"),
                               fg=Theme.TEXT, bg=Theme.SURFACE)
        value_label.pack(anchor="w")

        # Trend
        if trend:
            trend_color = Theme.SUCCESS if trend.startswith("+") else Theme.DANGER
            trend_label = ModernLabel(self, text=trend, style="small")
            trend_label.config(fg=trend_color)
            trend_label.pack(anchor="w")


class ScrollableFrame(tk.Frame):
    """Scrollable frame container."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.canvas = tk.Canvas(self, bg=Theme.BG, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=Theme.BG)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, e):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_leave(self, e):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, e):
        self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")


class ToolTip:
    """Tooltip for widgets."""

    def __init__(self, widget, text: str):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, e=None):
        if self.tooltip:
            return

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, font=Theme.FONT_SMALL,
                         bg=Theme.TEXT, fg=Theme.SURFACE,
                         padx=Theme.SPACING_SM, pady=Theme.SPACING_XS)
        label.pack()

    def hide(self, e=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
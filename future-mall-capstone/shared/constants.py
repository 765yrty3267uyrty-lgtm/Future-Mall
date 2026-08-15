"""
Future Mall - Shared Brand Constants (Python)
Used by all Python modules for consistent branding.
"""

BRAND = {
    "name": "Future Mall",
    "slogan": "Shopping for Tomorrow",
    "colors": {
        "primary": "#2563EB",
        "primary_hover": "#1D4ED8",
        "primary_light": "#DBEAFE",
        "secondary": "#0D9488",
        "secondary_hover": "#0F766E",
        "secondary_light": "#CCFBF1",
        "accent": "#F97316",
        "accent_hover": "#EA580C",
        "accent_light": "#FFEDD5",
        "success": "#10B981",
        "warning": "#F59E0B",
        "danger": "#EF4444",
        "bg": "#F8FAFC",
        "surface": "#FFFFFF",
        "text": "#1E293B",
        "text_muted": "#64748B",
        "border": "#E2E8F0",
    },
    "fonts": {
        "display": "Space Grotesk",
        "heading": "Space Grotesk",
        "body": "Inter",
        "mono": "JetBrains Mono",
    },
    "spacing": {
        "xs": "4px",
        "sm": "8px",
        "md": "16px",
        "lg": "24px",
        "xl": "32px",
    },
    "radius": {
        "sm": "4px",
        "md": "8px",
        "lg": "12px",
        "xl": "16px",
        "full": "9999px",
    },
    "shadows": {
        "sm": "0 1px 2px rgba(15, 23, 42, 0.05)",
        "md": "0 4px 6px rgba(15, 23, 42, 0.07)",
        "lg": "0 10px 15px rgba(15, 23, 42, 0.1)",
        "xl": "0 20px 25px rgba(15, 23, 42, 0.15)",
    },
}

# Attendance System Constants
ATTENDANCE = {
    "work_start": "08:00",
    "work_end": "17:00",
    "late_threshold": "08:15",
    "standard_hours": 8.0,
    "max_overtime": 2.0,
    "roles": ["employee", "supervisor", "admin"],
    "statuses": ["present", "late", "absent", "on_leave", "holiday"],
    "departments": ["IT", "HR", "Finance", "Operations", "Marketing", "Customer Service"],
}

# Cashier Program Constants
CASHIER = {
    "store_name": "Future Mall",
    "tax_rate": 0.10,
    "currency": "EGP",
    "discount_threshold": 500.00,
    "discount_rate": 0.10,
    "products": [
        {"name": "Milk", "price": 25.00},
        {"name": "Bread", "price": 15.00},
        {"name": "Rice", "price": 80.00},
        {"name": "Eggs", "price": 45.00},
        {"name": "Sugar", "price": 30.00},
        {"name": "Tea", "price": 60.00},
        {"name": "Coffee", "price": 120.00},
        {"name": "Juice", "price": 35.00},
        {"name": "Water", "price": 10.00},
        {"name": "Chocolate", "price": 50.00},
    ],
}

# Visitors Analysis Constants
VISITORS = {
    "days_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "min_days": 1,
}

# Product Classifier Constants
CLASSIFIER = {
    "price_tiers": {
        "Premium": (1000, float("inf")),
        "Standard": (300, 1000),
        "Budget": (0, 300),
    },
    "weight_tiers": {
        "Light": (0, 1),
        "Medium": (1, 10),
        "Heavy": (10, float("inf")),
    },
    "stock_tiers": {
        "In Stock": (11, float("inf")),
        "Low Stock": (1, 10),
        "Out of Stock": (0, 0),
    },
}

# Digital Awareness Constants
DIGITAL_AWARENESS = {
    "threats": [
        "Phishing",
        "Malware",
        "Viruses",
        "Ransomware",
        "Spyware",
        "Identity Theft",
        "Data Breaches",
        "Social Engineering",
    ],
    "password_rules": [
        "At least 12 characters",
        "Uppercase letters",
        "Lowercase letters",
        "Numbers",
        "Special symbols",
        "Avoid personal information",
        "Never reuse passwords",
        "Use a password manager",
        "Enable Multi-Factor Authentication (MFA)",
    ],
}

def get_color(name: str) -> str:
    """Get a color from the brand palette."""
    return BRAND["colors"].get(name, "#000000")

def format_currency(amount: float, symbol: str = "$") -> str:
    """Format amount as currency."""
    return f"{symbol}{amount:,.2f}"

def format_number(value: float, decimals: int = 0) -> str:
    """Format a number with thousands separators."""
    return f"{value:,.{decimals}f}"

def print_header(title: str) -> None:
    """Print a formatted header."""
    width = 60
    print("\n" + "=" * width)
    print(f"{title.center(width)}")
    print("=" * width)

def print_section(title: str) -> None:
    """Print a section divider."""
    print(f"\n{title}")
    print("-" * len(title))
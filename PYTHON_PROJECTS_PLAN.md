# Python Console Applications - Implementation Plan

## Project Overview
Build three independent Python console applications demonstrating programming fundamentals, data processing, and clean software design.

## Tech Stack
- **Language**: Python 3.12+
- **Architecture**: Modular, function-based design
- **No external dependencies** (stdlib only for core functionality)
- **Optional**: colorama for colored output, tabulate for tables

## Project Structure
project/
├── cashier_program.py      # Task 1.1 - Shop cashier system
├── visitors_analysis.py    # Task 1.2 - Visitor statistics analyzer
├── product_classifier.py   # Task 1.3 - Product classification system
├── README.md               # Documentation
└── utils/                  # Shared utilities (optional)
    ├── __init__.py
    ├── validators.py       # Input validation helpers
    ├── formatters.py       # Output formatting helpers
    └── constants.py        # Shared constants

---

## Task 1.1: Cashier Program (cashier_program.py)

### Core Features
- Predefined product catalog (10 items: Milk, Bread, Rice, Eggs, Sugar, Tea, Coffee, Juice, Water, Chocolate)
- Shopping cart management (add, remove, update quantity, clear, cancel)
- Multiple purchases in one session
- Discount tiers: 5% (>200), 10% (>500), 15% (>1000)
- Tax calculation (configurable, e.g., 10%)
- Professional receipt generation with all details
- Save receipts to text file (bonus)
- Input validation & error handling

### Module Structure
cashier_program.py
├── Constants
│   ├── PRODUCTS: List[Dict] - Product catalog
│   ├── DISCOUNT_TIERS: List[Tuple] - (threshold, percentage)
│   └── TAX_RATE: float
├── Classes
│   ├── Product - name, price
│   ├── CartItem - product, quantity, line_total
│   └── Receipt - store info, items, totals, number, date
├── Functions
│   ├── display_products()
│   ├── get_user_choice()
│   ├── get_quantity()
│   ├── add_to_cart()
│   ├── remove_from_cart()
│   ├── update_quantity()
│   ├── view_cart()
│   ├── calculate_subtotal()
│   ├── calculate_discount()
│   ├── calculate_tax()
│   ├── generate_receipt()
│   ├── save_receipt_to_file()
│   ├── print_receipt()
│   └── main_menu()
└── Main Loop
    ├── Initialize cart
    ├── Show menu
    ├── Process actions
    └── On confirm: generate receipt, ask for another purchase

### Menu Options
1. View Products
2. Add to Cart
3. View Cart
4. Update Quantity
5. Remove Item
6. Clear Cart
7. Checkout / Confirm Purchase
8. Cancel Purchase
9. Exit

---

## Task 1.2: Visitors Analysis (visitors_analysis.py)

### Core Features
- Input visitor counts for 7 days (Mon-Sun) or dynamic N days
- Store in list with day labels
- Calculate: Total, Average, Max, Min, Max Day, Min Day, Day Count
- Optional: Median, Range, Difference, % Increase/Decrease
- Clean table output
- Save to CSV (bonus)
- Input validation (positive integers only)

### Module Structure
visitors_analysis.py
├── Constants
│   ├── DAYS: List[str] = [Monday, Tuesday, ...]
│   └── MIN_DAYS: int = 1
├── Functions
│   ├── get_visitor_input()
│   ├── validate_visitor_count()
│   ├── calculate_total()
│   ├── calculate_average()
│   ├── calculate_max()
│   ├── calculate_min()
│   ├── find_max_day()
│   ├── find_min_day()
│   ├── calculate_median()
│   ├── calculate_range()
│   ├── calculate_percentage_change()
│   ├── display_results_table()
│   ├── save_to_csv()
│   └── main()
└── Main Flow
    ├── Show title/instructions
    ├── Collect data (loop through days)
    ├── Process statistics
    ├── Display formatted table
    ├── Ask to save CSV
    └── Ask to restart

### Output Table Format
Total Visitors      | 1,234
Average Daily       | 176
Maximum             | 350 (Saturday)
Minimum             | 80 (Monday)
Days Recorded       | 7
Median              | 165
Range               | 270
% Change (Max/Min)  | 337.5%

---

## Task 1.3: Product Classifier (product_classifier.py)

### Core Features
- Input: Product Name, Price, Weight, Category (optional), Stock Quantity
- Price Classification: Premium (>1000), Standard (300-1000), Budget (<300)
- Weight Classification: Light (<1kg), Medium (1-10kg), Heavy (>10kg)
- Stock Classification: In Stock (>10), Low Stock (1-10), Out of Stock (0)
- Display formatted results
- Search/Sort products (bonus)
- Load from JSON (bonus)
- Multiple product entries in one session

### Module Structure
product_classifier.py
├── Constants
│   ├── PRICE_TIERS: Dict[str, Tuple] - {Premium: (1000, inf), ...}
│   ├── WEIGHT_TIERS: Dict[str, Tuple] - {Light: (0, 1), ...}
│   └── STOCK_TIERS: Dict[str, Tuple] - {In Stock: (11, inf), ...}
├── Classes
│   └── Product - name, price, weight, category, stock, classifications
├── Functions
│   ├── get_product_input()
│   ├── validate_price()
│   ├── validate_weight()
│   ├── validate_stock()
│   ├── classify_price()
│   ├── classify_weight()
│   ├── classify_stock()
│   ├── classify_product()
│   ├── display_classification()
│   ├── display_all_products()
│   ├── save_to_json()
│   ├── load_from_json()
│   └── main()
└── Main Flow
    ├── Show title/instructions
    ├── Loop: Input product data
    ├── Classify each dimension
    ├── Display results
    ├── Ask to add another / view all / save / exit

### Classification Rules
| Dimension | Criteria | Classification |
|-----------|----------|----------------|
| Price     | > 1000   | Premium        |
|           | 300-1000 | Standard       |
|           | < 300    | Budget         |
| Weight    | < 1 kg   | Light          |
|           | 1-10 kg  | Medium         |
|           | > 10 kg  | Heavy          |
| Stock     | > 10     | In Stock       |
|           | 1-10     | Low Stock      |
|           | 0        | Out of Stock   |

---

## Shared Utilities (utils/)

### validators.py
def get_positive_int(prompt: str, min_val: int = 1) -> int
def get_positive_float(prompt: str, min_val: float = 0.0) -> float
def get_non_empty_string(prompt: str) -> str
def get_menu_choice(options: List[str]) -> int
def confirm_action(prompt: str) -> bool

### formatters.py
def format_currency(amount: float, symbol: str = $) -> str
def format_number(num: int) -> str  # with commas
def print_header(title: str)
def print_table(headers: List[str], rows: List[List[str]])
def print_success(msg: str)
def print_error(msg: str)
def print_info(msg: str)

### constants.py
STORE_NAME = Future Mall
TAX_RATE = 0.10
DISCOUNT_TIERS = [(200, 0.05), (500, 0.10), (1000, 0.15)]
DAYS_OF_WEEK = [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]

---

## Implementation Order

### Phase 1: Core Utilities & Cashier Program (Day 1)
1. Create utils/ module with validators, formatters, constants
2. Implement cashier_program.py with all core features
3. Test cashier program thoroughly

### Phase 2: Visitors Analysis (Day 1-2)
1. Implement visitors_analysis.py using shared utilities
2. Add CSV export functionality
3. Test with various inputs

### Phase 3: Product Classifier (Day 2)
1. Implement product_classifier.py using shared utilities
2. Add JSON save/load (bonus)
3. Test classification logic

### Phase 4: Polish & Documentation (Day 2-3)
1. Create comprehensive README.md
2. Add colored output (colorama)
3. Cross-test all three programs
4. Verify error handling edge cases

---

## Coding Standards
- PEP 8 compliance
- Type hints on all functions
- Docstrings for all public functions/classes
- Single responsibility - each function does one thing
- No global mutable state - pass data explicitly
- Defensive programming - validate all inputs
- Clear error messages - user-friendly, actionable
- Consistent naming - snake_case for functions/variables, PascalCase for classes

---

## Testing Checklist
- [ ] Cashier: Empty cart checkout handled
- [ ] Cashier: Discount tiers calculate correctly
- [ ] Cashier: Receipt saves to file
- [ ] Cashier: Invalid input rejected gracefully
- [ ] Visitors: All 7 days accepted
- [ ] Visitors: Statistics calculate correctly
- [ ] Visitors: CSV exports valid data
- [ ] Classifier: All 3 classifications work
- [ ] Classifier: Edge cases (boundary values)
- [ ] Classifier: JSON round-trip works
- [ ] All: KeyboardInterrupt handled (Ctrl+C)
- [ ] All: Restart option works

---

## README.md Structure
# Python Console Applications

Three independent programs demonstrating Python fundamentals.

## Programs
1. **Cashier Program** - Shop simulation with cart, discounts, receipts
2. **Visitors Analysis** - Weekly visitor statistics calculator
3. **Product Classifier** - Multi-dimensional product categorization

## Requirements
- Python 3.12+

## Installation
bash
# Optional dependencies for enhanced output
pip install colorama tabulate

## Usage
bash
python cashier_program.py
python visitors_analysis.py
python product_classifier.py

## Features
[Detailed feature list per program]

## Project Structure
[Directory tree]

## Code Quality
- Type hints throughout
- Comprehensive error handling
- Modular, reusable design
- Clean, documented code

---

## Clarifying Questions

1. **Currency**: What currency symbol? ($, Euro, Pound, or configurable?)
2. **Tax Rate**: Fixed 10% or configurable per region?
3. **Discount Tiers**: Use the example tiers (200/500/1000) or different values?
4. **Visitors Days**: Fixed 7 days (Mon-Sun) or user-defined number of days?
5. **Classification Thresholds**: Use example values or customize?
6. **Dependencies**: Allow colorama + tabulate for better UX, or stdlib only?
7. **Persistence**: JSON/CSV saving required or just bonus?
8. **Language**: English only, or multi-language support needed?

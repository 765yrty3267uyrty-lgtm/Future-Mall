# Future Mall - Testing Guide

## Overview

This guide covers testing strategies for all Future Mall modules.

## Test Structure

```
tests/
├── test_cashier.py          # Cashier program tests
├── test_visitors.py         # Visitors analysis tests
├── test_classifier.py       # Product classifier tests
├── test_attendance.py       # Attendance system tests
├── test_website.py          # Website tests
└── test_digital_awareness.py # Digital awareness tests
```

## Python Module Testing

### Running Tests

```bash
cd python_modules

# Run all tests
pytest tests/ -v

# Run specific module
pytest tests/test_cashier.py -v

# With coverage
pytest tests/ --cov=../python_modules --cov-report=html

# Run with specific marker
pytest tests/ -m "not slow" -v
```

### Test Configuration (`pytest.ini`)
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
```

### Cashier Tests (`test_cashier.py`)

```python
import pytest
from cashier_program import CashierSystem, Product, CartItem, Receipt

class TestCashierSystem:
    def setup_method(self):
        self.system = CashierSystem()

    def test_add_to_cart(self):
        self.system.add_to_cart(1, 2)  # Milk x2
        assert len(self.system.cart) == 1
        assert self.system.cart[0].quantity == 2

    def test_calculate_subtotal(self):
        self.system.cart = [CartItem(Product("Milk", 25.00), 2)]
        assert self.system.calculate_subtotal() == 50.00

    def test_calculate_discount(self):
        # No discount under 200
        assert self.system.calculate_discount(150) == (0.0, "0%")
        # 5% discount over 200
        assert self.system.calculate_discount(250) == (12.5, "5%")
        # 10% discount over 500
        assert self.system.calculate_discount(600) == (60.0, "10%")
        # 15% discount over 1000
        assert self.system.calculate_discount(1200) == (180.0, "15%")

    def test_calculate_tax(self):
        assert self.system.calculate_tax(100) == 10.00

    def test_generate_receipt(self):
        self.system.cart = [CartItem(Product("Milk", 25.00), 2)]
        receipt = self.system.checkout()
        assert receipt is not None
        assert receipt.subtotal == 50.00
        assert "GRAND TOTAL" in str(receipt)
```

### Visitors Analysis Tests (`test_visitors.py`)

```python
import pytest
from visitors_analysis import VisitorsAnalyzer

class TestVisitorsAnalyzer:
    def setup_method(self):
        self.analyzer = VisitorsAnalyzer()

    def test_collect_data_valid(self):
        # Mock input
        pass

    def test_calculate_statistics(self):
        self.analyzer.visitor_data = [100, 150, 200, 180, 220, 300, 160]
        results = self.analyzer.calculate_statistics()
        
        assert results['total'] == 1310
        assert results['average'] == 187.14
        assert results['maximum'] == 300
        assert results['minimum'] == 100
        assert results['max_day'] == 'Saturday'
        assert results['min_day'] == 'Monday'

    def test_save_csv(self):
        self.analyzer.visitor_data = [100, 200, 300]
        self.analyzer.calculate_statistics()
        filename = self.analyzer.save_to_csv()
        assert filename.endswith('.csv')
```

### Product Classifier Tests (`test_classifier.py`)

```python
import pytest
from product_classifier import ProductClassifier, Product

class TestProductClassifier:
    def setup_method(self):
        self.classifier = ProductClassifier()

    def test_classify_price(self):
        assert self.classifier.classify_price(1500) == "Premium"
        assert self.classifier.classify_price(500) == "Standard"
        assert self.classifier.classify_price(100) == "Budget"

    def test_classify_weight(self):
        assert self.classifier.classify_weight(0.5) == "Light"
        assert self.classifier.classify_weight(5) == "Medium"
        assert self.classifier.classify_weight(15) == "Heavy"

    def test_classify_stock(self):
        assert self.classifier.classify_stock(20) == "In Stock"
        assert self.classifier.classify_stock(5) == "Low Stock"
        assert self.classifier.classify_stock(0) == "Out of Stock"

    def test_classify_product(self):
        product = Product("Test", 500, 2, 10)
        product = self.classifier.classify_product(product)
        assert product.price_class == "Standard"
        assert product.weight_class == "Light"
        assert product.stock_class == "In Stock"
```

### Attendance System Tests (`test_attendance.py`)

```python
import pytest
from datetime import date, datetime
from attendance_system.models import Employee, Attendance, get_db

class TestAttendanceSystem:
    @pytest.fixture(autouse=True)
    def setup_database(self):
        db = get_db()
        # Clean up test data
        with db.get_connection() as conn:
            conn.execute("DELETE FROM attendance")
            conn.execute("DELETE FROM employees")
            conn.commit()

    def test_employee_creation(self):
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

    def test_employee_authentication(self):
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
        
        auth = Employee.authenticate('TEST002', 'password123')
        assert auth is not None
        assert auth.employee_id == 'TEST002'
        
        # Wrong password
        auth = Employee.authenticate('TEST002', 'wrong')
        assert auth is None

    def test_check_in_out(self):
        emp = Employee.create({
            'employee_id': 'TEST003',
            'full_name': 'Test User 3',
            'department': 'IT',
            'position': 'Developer',
            'email': 'test3@test.com',
            'date_joined': date.today().isoformat(),
            'role': 'employee',
            'password': 'password123'
        })
        
        # Check in
        result = Attendance.check_in(emp.id)
        assert result['success'] is True
        assert result['status'] in ('present', 'late')
        
        # Check out
        result = Attendance.check_out(emp.id)
        assert result['success'] is True
        assert result['working_hours'] > 0
```

## Web Module Testing

### Website Tests (`test_website.py`)

```python
import pytest
from bs4 import BeautifulSoup

class TestWebsite:
    def test_html_structure(self):
        with open('../website/index.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Check semantic structure
        assert soup.find('header') is not None
        assert soup.find('nav') is not None
        assert soup.find('main') is not None
        assert soup.find('footer') is not None
        
        # Check semantic sections
        assert soup.find('section', id='home') is not None
        assert soup.find('section', id='about') is not None
        assert soup.find('section', id='modules') is not None

    def test_accessibility(self):
        with open('../website/index.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Skip link
        skip_link = soup.find('a', class_='skip-link')
        assert skip_link is not None
        assert skip_link['href'] == '#main'
        
        # ARIA labels
        nav = soup.find('nav')
        assert nav.get('aria-label') == 'Main navigation'
        
        # Alt text for images
        for img in soup.find_all('img'):
            assert img.get('alt') is not None

    def test_responsive_meta(self):
        with open('../website/index.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        assert viewport is not None
        assert 'width=device-width' in viewport['content']

    def test_css_linked(self):
        with open('../website/index.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        css_link = soup.find('link', rel='stylesheet')
        assert css_link is not None
        assert css_link['href'] == 'style.css'
```

### Digital Awareness Tests (`test_digital_awareness.py`)

```python
import pytest
from bs4 import BeautifulSoup

class TestDigitalAwareness:
    def test_threats_page_structure(self):
        with open('../digital_awareness/threats.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        # Check threat cards
        threats = soup.find_all('article', class_='threat-card')
        assert len(threats) == 8
        
        # Check each has required elements
        for threat in threats:
            assert threat.find('h3', class_='threat-title') is not None
            assert threat.find('span', class_='threat-severity') is not None

    def test_password_checker_elements(self):
        with open('../digital_awareness/password.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        assert soup.find('input', id='password-input') is not None
        assert soup.find('button', id='toggle-visibility') is not None
        assert soup.find('button', id='generate-btn') is not None
        assert soup.find('div', id='meter-fill') is not None

    def test_quiz_page_structure(self):
        with open('../digital_awareness/quiz.html') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        assert soup.find('button', id='start-quiz') is not None
        assert soup.find('div', id='quiz-area') is not None
        assert soup.find('button', id='next-btn') is not None
```

## JavaScript Testing

### Manual Testing Checklist

#### Password Checker (`password.html`)
- [ ] Empty input shows "Enter a password"
- [ ] Weak password (< 8 chars) shows "Very Weak"
- [ ] Fair password (8-11 chars) shows "Fair"
- [ ] Strong password (12+ chars, mixed) shows "Strong"
- [ ] Very strong (16+ chars, all types) shows "Very Strong"
- [ ] Toggle visibility works
- [ ] Generate password creates valid password
- [ ] Requirements checklist updates in real-time
- [ ] Suggestions appear for weak passwords
- [ ] Warnings appear for common patterns
- [ ] Entropy calculation accurate
- [ ] Crack time estimates reasonable

#### Quiz (`quiz.html`)
- [ ] Start button begins quiz
- [ ] 15 questions load sequentially
- [ ] Progress bar updates
- [ ] Score updates on correct answers
- [ ] Immediate feedback on selection
- [ ] Explanation shows after answer
- [ ] Next button advances
- [ ] Final score calculated correctly
- [ ] Category breakdown shown
- [ ] Personalized tips displayed
- [ ] Retry button works
- [ ] Share button copies to clipboard

#### Threats Page (`threats.html`)
- [ ] All 8 threat cards render
- [ ] Each card has title, severity, description
- [ ] Accordion expand/collapse works
- [ ] Summary table at bottom
- [ ] Checklist section complete

#### Posters Page (`posters.html`)
- [ ] 6 poster cards display
- [ ] Preview modal opens
- [ ] Download buttons work
- [ ] Download all buttons work
- [ ] Download bundle works
- [ ] Notification toast appears

## Browser Testing Matrix

| Browser | Versions | Status |
|---------|----------|--------|
| Chrome | Latest 2 | ✅ Test |
| Firefox | Latest 2 | ✅ Test |
| Safari | Latest 2 | ✅ Test |
| Edge | Latest 2 | ✅ Test |
| Mobile Chrome | Latest | ✅ Test |
| Mobile Safari | Latest | ✅ Test |

## Responsive Testing

### Breakpoints to Test
- 320px (Mobile)
- 375px (iPhone SE)
- 428px (iPhone 14 Pro)
- 768px (Tablet)
- 1024px (Desktop)
- 1440px (Large Desktop)

### Test Checklist per Breakpoint
- [ ] Navigation collapses/expands correctly
- [ ] Hero section stacks properly
- [ ] Module cards stack/grid correctly
- [ ] Tables scroll horizontally
- [ ] Forms usable
- [ ] Modals fit screen
- [ ] Text readable (no horizontal scroll)

## Accessibility Testing (WCAG 2.1 AA)

### Automated (axe-core)
```bash
# Install
npm install -g @axe-core/cli

# Run
axe http://localhost:8000
```

### Manual Checklist
- [ ] Skip link works
- [ ] Tab order logical
- [ ] Focus visible on all interactive elements
- [ ] Color contrast ≥ 4.5:1 (text), 3:1 (UI)
- [ ] No color-only information
- [ ] Alt text on all images
- [ ] ARIA labels on icon buttons
- [ ] Form labels associated
- [ ] Error messages announced
- [ ] Language declared (`lang="en"`)
- [ ] Page titles unique
- [ ] Headings hierarchical (h1→h2→h3)
- [ ] Reduced motion respected
- [ ] Zoom to 200% works

## Performance Testing

### Lighthouse Targets
```bash
# Install
npm install -g lighthouse

# Run
lighthouse http://localhost:8000 --output=json --output-path=./lighthouse-report.json
```

### Targets
| Metric | Target |
|--------|--------|
| Performance | ≥ 90 |
| Accessibility | ≥ 95 |
| Best Practices | ≥ 90 |
| SEO | ≥ 90 |

### Core Web Vitals
| Metric | Target |
|--------|--------|
| LCP | < 2.5s |
| FID | < 100ms |
| CLS | < 0.1 |

## Continuous Integration

### GitHub Actions (`.github/workflows/test.yml`)
```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  python-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install pytest pytest-cov
      - run: cd python_modules && pytest tests/ --cov=../python_modules

  web-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install -g stylelint
      - run: npx stylelint website/style.css digital_awareness/style.css
```

## Test Data Management

### Attendance System
- Use in-memory SQLite for tests
- Seed with known data in `setup_method`
- Clean up in `teardown_method`
- Never test against production database

### Web Modules
- Static files only, no test database needed
- Mock user interactions where needed
- Use `BeautifulSoup` for HTML parsing

## Reporting

### Coverage Reports
```bash
# Python
pytest tests/ --cov=python_modules --cov-report=html --cov-report=term

# JavaScript (if using bundler)
# npx jest --coverage
```

### Reports Location
- Python: `htmlcov/index.html`
- View in browser for detailed coverage

## Troubleshooting Tests

### Common Issues

**Import Errors**:
- Ensure `sys.path` includes project root
- Check `__init__.py` files exist

**Database Locked**:
- Use separate test database
- Close connections in teardown

**Flaky Tests**:
- Add `pytest-rerunfailures`
- Use `pytest-timeout`

**Slow Tests**:
- Mark with `@pytest.mark.slow`
- Run with `pytest -m "not slow"`
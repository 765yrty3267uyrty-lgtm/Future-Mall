# Future Mall - Capstone Project

A comprehensive educational capstone project demonstrating full-stack development, branding, cybersecurity education, and data management skills through seven integrated modules.

## 🌟 Live Demos

| Module | Type | Live Demo |
|--------|------|-----------|
| **Website** | HTML/CSS/JS | [https://username.github.io/future-mall-capstone/](https://username.github.io/future-mall-capstone/) |
| **Digital Awareness** | HTML/CSS/JS | [https://username.github.io/future-mall-capstone/digital-awareness/](https://username.github.io/future-mall-capstone/digital-awareness/) |

## 📦 Project Structure

```
future-mall-capstone/
├── python_modules/
│   ├── cashier_program.py          # Console shop simulator
│   ├── visitors_analysis.py        # Visitor statistics analyzer
│   ├── product_classifier.py       # Product classification system
│   └── attendance_system/          # Tkinter + SQLite desktop app
│       ├── main.py                 # Entry point
│       ├── models/                 # Database models
│       ├── services/               # Business logic
│       ├── ui/                     # Tkinter UI components
│       └── requirements.txt
├── website/                        # GitHub Pages website
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── package.json
├── digital_awareness/              # Cybersecurity education platform
│   ├── index.html                  # Home page
│   ├── threats.html                # Threat library
│   ├── password.html               # Password strength checker
│   ├── quiz.html                   # Phishing identification quiz
│   ├── posters.html                # Safety posters
│   ├── style.css
│   ├── script.js
│   ├── password.js
│   ├── quiz.js
│   ├── posters.js
│   └── package.json
├── branding/                       # Brand identity assets
│   ├── logo/
│   │   ├── concepts/               # 3 initial concepts
│   │   └── final/                  # 6 logo variations (SVG/PNG)
│   ├── colors/
│   ├── typography/
│   ├── advertisement/              # 5 ad formats
│   ├── mockups/                    # Business card, app icon, social
│   └── BRAND_GUIDELINES.md
├── shared/                         # Shared design tokens
│   ├── constants.py                # Python constants
│   ├── constants.css               # CSS custom properties
│   └── constants.js                # JavaScript constants
├── docs/                           # Documentation
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── TESTING.md
├── tests/                          # Test suites
│   ├── test_cashier.py
│   ├── test_visitors.py
│   ├── test_classifier.py
│   ├── test_attendance.py
│   ├── test_website.py
│   └── test_digital_awareness.py
├── .github/workflows/              # CI/CD pipelines
│   └── deploy-pages.yml            # Single site build + deploy
├── requirements.txt                # Python dependencies
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## 🚀 Quick Start

### Python Modules (Console Apps)

```bash
cd python_modules

# Cashier Program
python cashier_program.py

# Visitors Analysis
python visitors_analysis.py

# Product Classifier
python product_classifier.py
```

### Attendance System (Desktop GUI)

```bash
cd python_modules/attendance_system

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Web Modules (Local Development)

```bash
# Main Website
cd website
npx serve .

# Digital Awareness
cd digital_awareness
npx serve .
```

## 🎯 Module Overview

### 1. Cashier Program (`python_modules/cashier_program.py`)
Console-based shop simulator with:
- Product catalog (10 items)
- Shopping cart management (add/remove/update)
- Tiered discounts (5% > $200, 10% > $500, 15% > $1000)
- Tax calculation (10%)
- Professional receipt generation with file export
- Transaction history

### 2. Visitors Analysis (`python_modules/visitors_analysis.py`)
Statistical analysis of weekly visitor data:
- Daily visitor input (7 days)
- Total, average, min, max visitors
- Peak/low day identification
- Median, range, percentage change
- Daily trend analysis
- CSV/JSON export

### 3. Product Classifier (`python_modules/product_classifier.py`)
Multi-dimensional product classification:
- **Price**: Premium (>$1000), Standard ($300-1000), Budget (<$300)
- **Weight**: Light (<1kg), Medium (1-10kg), Heavy (>10kg)
- **Stock**: In Stock (>10), Low Stock (1-10), Out of Stock (0)
- JSON persistence with search and sort

### 4. Attendance System (`python_modules/attendance_system/`)
Full-featured desktop GUI (Tkinter + SQLite):
- **3 Roles**: Employee, Supervisor, Admin
- Check-in/out with validation
- Role-based dashboards
- Daily/weekly/monthly reports
- CSV/Excel export
- CSV/Excel export
- Dark mode support

### 5. GitHub Pages Website (`website/`)
Responsive portfolio website:
- Semantic HTML5 with accessibility
- Modern CSS3 (custom properties, Grid/Flexbox)
- Dark mode support
- Responsive design (320px - 1440px)
- Auto-deploy via GitHub Actions
- Smooth scroll navigation

### 6. Digital Awareness (`digital_awareness/`)
Interactive cybersecurity education:
- **Threat Library**: 8 threat categories with examples
- **Password Checker**: Real-time entropy-based strength meter
- **Phishing Quiz**: 15 questions with instant feedback
- **Safety Posters**: 6 downloadable posters
- Interactive tips and checklists

### 7. Brand Identity (`branding/`)
Complete visual identity system:
- **Logo**: 6 variations (primary, stacked, icon, mono, white, responsive)
- **Colors**: Primary (#2563EB), Secondary (#0D9488), Accent (#F97316)
- **Typography**: Space Grotesk (display) + Inter (body)
- **Ads**: 5 formats (hero, square, story, print, Telegram)
- **Mockups**: Business card, app icon, social, website header
- **Guidelines**: Complete usage documentation

## 🎨 Design System

All modules share a unified design system via `shared/` constants:

### Colors
```css
--color-primary: #2563EB;      /* Future Blue */
--color-secondary: #0D9488;    /* Innovation Teal */
--color-accent: #F97316;       /* Energy Orange */
--color-success: #10B981;
--color-warning: #F59E0B;
--color-danger: #EF4444;
```

### Typography
- **Display/Headings**: Space Grotesk (500-700)
- **Body**: Inter (400-600)
- **Mono**: JetBrains Mono

### Spacing (4px base)
- xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Python** | 3.12+, Tkinter, SQLite3 |
| **Web** | HTML5, CSS3, Vanilla JS (ES6+) |
| **Design** | CSS Custom Properties, Grid, Flexbox |
| **Fonts** | Google Fonts (Space Grotesk, Inter, JetBrains Mono) |
| **Icons** | Inline SVG |
| **Deploy** | GitHub Pages + GitHub Actions |
| **Python Packaging** | PyInstaller |
| **Testing** | pytest, manual testing |

## 🚀 Deployment

### GitHub Pages (Automatic)
1. Push to `main` branch
2. GitHub Actions (`deploy-pages.yml`) builds a single site from all web modules:
   - `website/` → `https://username.github.io/future-mall-capstone/`
   - `digital_awareness/` → `https://username.github.io/future-mall-capstone/digital-awareness/`
   - `branding/` → `https://username.github.io/future-mall-capstone/branding/`

### Python Executables
```bash
# Install PyInstaller
pip install pyinstaller

# Build executables
cd python_modules
pyinstaller --onefile --windowed cashier_program.py
pyinstaller --onefile --windowed visitors_analysis.py
pyinstaller --onefile --windowed product_classifier.py

# Attendance system
cd attendance_system
pyinstaller --onefile --windowed --add-data "data;data" main.py
```

## 🧪 Testing

```bash
# Python tests
cd python_modules
pytest tests/ -v

# Web tests (manual)
# Open website/index.html and digital_awareness/index.html in browser
# Test responsive design at 320px, 768px, 1024px, 1440px
# Test dark mode (OS preference)
# Test keyboard navigation
```

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and module interactions
- [Deployment](docs/DEPLOYMENT.md) - Deployment guides for all platforms
- [Testing](docs/TESTING.md) - Testing strategies and checklists
- [Brand Guidelines](branding/BRAND_GUIDELINES.md) - Complete brand usage guide

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Fonts**: Space Grotesk, Inter, JetBrains Mono (Google Fonts)
- **Icons**: Inline SVG, Unicode emoji
- **Inspiration**: Modern cybersecurity education platforms

---

**Future Mall** - Shopping for Tomorrow 🛒✨

*Built as an educational capstone project demonstrating full-stack development, branding, cybersecurity education, and data management skills.*
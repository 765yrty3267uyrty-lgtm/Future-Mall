# Future Mall - Architecture Documentation

## System Overview

The Future Mall capstone project consists of 7 integrated modules sharing a unified design system. The architecture follows a modular, loosely-coupled approach with shared constants enabling visual consistency across all modules.

## Module Architecture

### Shared Design System (`shared/`)
Centralized design tokens used across all modules:
- `constants.py` - Python design tokens (colors, spacing, typography, brand info)
- `constants.css` - CSS custom properties for web modules
- `constants.js` - JavaScript constants for interactive features

### Python Modules (Console Apps)

#### 1. Cashier Program (`cashier_program.py`)
**Architecture**: Single-file MVC pattern
- **Model**: `Product`, `CartItem`, `Receipt` dataclasses
- **View**: Console-based menu system with formatted output
- **Controller**: `CashierSystem` class managing state and business logic

**Data Flow**:
```
User Input → CashierSystem → Product/CartItem/Receipt Models → Console Output
```

#### 2. Visitors Analysis (`visitors_analysis.py`)
**Architecture**: Single-file procedural with class-based analysis
- **Model**: `VisitorsAnalyzer` class
- **View**: Console tables and formatted output
- **Controller**: `VisitorsAnalyzer` methods

**Data Flow**:
```
User Input → VisitorsAnalyzer → Statistics Calculation → Formatted Output → File Export
```

#### 3. Product Classifier (`product_classifier.py`)
**Architecture**: Single-file OOP with dataclass model
- **Model**: `Product` dataclass with classification fields
- **View**: Console formatted output with tables
- **Controller**: `ProductClassifier` class

**Data Flow**:
```
User Input → ProductClassifier → Product Model → Classification → Output/JSON Export
```

### Attendance System (Desktop GUI)

#### Architecture: Layered Architecture (Models → Services → UI)

```
┌─────────────────────────────────────┐
│           UI Layer (Tkinter)        │
│  Login → Dashboard (Role-based)     │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Service Layer               │
│  AttendanceService | ReportService  │
│  StatsService | AuthService         │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Model Layer                 │
│  Employee | Attendance | Database   │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│         Data Layer (SQLite)         │
│  employees | attendance | settings  │
└─────────────────────────────────────┘
```

#### Components

**Models** (`models/`):
- `database.py` - SQLite connection manager with context managers
- `employee.py` - Employee CRUD, authentication
- `attendance.py` - Check-in/out, reports, statistics

**Services** (`services/`):
- `attendance_service.py` - Check-in/out validation, business rules
- `report_service.py` - Daily/weekly/monthly/department reports
- `stats_service.py` - Analytics, trends, leaderboards

**UI** (`ui/`):
- `base.py` - Theme system, styled widgets (ModernButton, Card, etc.)
- `login_window.py` - Role-based authentication
- `employee_dashboard.py` - Employee check-in/out, history
- `supervisor_dashboard.py` - Team oversight, daily reports
- `admin_dashboard.py` - Full management, settings, exports

### Web Modules

#### GitHub Pages Website (`website/`)
**Architecture**: Static site with progressive enhancement
- `index.html` - Semantic HTML5 with accessibility
- `style.css` - CSS custom properties, responsive Grid/Flexbox
- `script.js` - Progressive enhancement (navigation, scroll effects, animations)

**Features**:
- Semantic HTML5 (header, nav, main, section, footer)
- CSS Custom Properties for theming
- Mobile-first responsive (320px - 1440px)
- Dark mode via `prefers-color-scheme`
- Smooth scroll, intersection observer animations
- Skip links, ARIA labels, focus management

#### Digital Awareness (`digital_awareness/`)
**Architecture**: Multi-page SPA-like static site
- `index.html` - Home with module cards
- `threats.html` - Accordion-style threat cards
- `password.html` - Real-time password checker
- `quiz.html` - 15-question phishing quiz with state management
- `posters.html` - Poster gallery with preview/download
- Shared `style.css` and `script.js` + page-specific JS

**Interactive Features**:
- Password checker: Real-time entropy calculation
- Quiz: 15 questions, shuffle, instant feedback, scoring
- Posters: Preview modal, download (text-based), bundle download

### Branding (`branding/`)
**Asset Pipeline**:
- Source: Figma/SVG
- Export: SVG (vector), PNG @1x/2x/3x, ICO, PDF (print)
- Formats: Logo (6 variations), Ads (5 formats), Mockups (5 types)

## Data Flow Diagram

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Shared     │────▶│   Python     │     │   Web        │
│   Constants  │     │   Modules    │     │   Modules    │
└──────────────┘     └──────────────┘     └──────────────┘
                           │                       │
                    ┌──────▼──────┐          ┌──────▼──────┐
                    │ Attendance  │          │  GitHub     │
                    │   System    │          │   Pages     │
                    │  (SQLite)   │          │  Deploy     │
                    └─────────────┘          └─────────────┘
```

## Deployment Architecture

### GitHub Actions CI/CD
```
Push to main
    │
    ├─▶ Website workflow ──▶ Build (no-op) ──▶ Deploy to gh-pages (root)
    │
    └─▶ Digital Awareness workflow ──▶ Build (no-op) ──▶ Deploy to gh-pages/digital-awareness
```

### Python Packaging
```
Source Code
    │
    ▼
PyInstaller ──▶ Executable (.exe)
    │
    ▼
Distribution
```

## Security Considerations

### Attendance System
- Password hashing: SHA-256 (demo) - production should use bcrypt/argon2
- Role-based access control (Employee/Supervisor/Admin)
- SQL parameterization prevents injection
- Session management via Tkinter window state

### Web Modules
- No server-side processing (static sites)
- CSP-ready (no inline scripts/styles)
- HTTPS enforced via GitHub Pages
- No sensitive data in client-side code

### Digital Awareness
- All processing client-side
- No password transmission
- Quiz answers not stored
- Password checker runs entirely in browser

## Performance Considerations

### Python Modules
- Lightweight: stdlib only (optional: colorama, tabulate)
- Fast startup (< 100ms)
- Low memory footprint (< 50MB)

### Web Modules
- Critical CSS inlined
- No external dependencies (except Google Fonts)
- Optimized SVG icons inline
- Lazy-loadable images (if added)
- Total bundle < 100KB (gzipped)

### Attendance System
- SQLite with connection pooling via context managers
- Indexed queries on employee_id, date
- Lazy-loaded UI components
- Efficient Tkinter widget reuse

## Scalability Notes

### Current Limitations
- Attendance system: Single-user SQLite, local-only
- Python modules: Console-based, no network
- Web modules: Static only, no backend

### Future Enhancements
- Attendance: PostgreSQL + REST API + React frontend
- Python modules: FastAPI backend + web UI
- Web modules: Progressive Web App (PWA)
- Analytics: Privacy-respecting usage metrics

## Technology Decisions

| Decision | Rationale |
|----------|-----------|
| Tkinter for GUI | Stdlib, no dependencies, cross-platform |
| SQLite | Zero-config, file-based, ACID compliant |
| Vanilla JS | No build step, minimal bundle, educational |
| CSS Custom Props | Native theming, no preprocessor needed |
| GitHub Pages | Free, HTTPS, CDN, custom domains |
| SHA-256 for demo | Simplicity; production needs bcrypt |
| Dataclasses | Python 3.7+, clean model definitions |
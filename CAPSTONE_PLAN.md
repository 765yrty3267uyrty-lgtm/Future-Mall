# Future Mall - Capstone Project Master Implementation Plan

## Project Overview
Unify all 7 educational modules into a single cohesive Future Mall capstone project demonstrating full-stack development, branding, cybersecurity education, and data management skills.

## Master Project Structure
future-mall-capstone/
|-- python_modules/
|   |-- cashier_program.py
|   |-- visitors_analysis.py
|   |-- product_classifier.py
|   |-- attendance_system/
|       |-- main.py
|       |-- models/
|       |-- services/
|       |-- ui/
|       |-- utils/
|       |-- data/
|-- website/
|   |-- index.html
|   |-- style.css
|   |-- script.js
|   |-- images/
|   |-- assets/
|-- branding/
|   |-- logo/
|   |   |-- concepts/
|   |   |-- final/
|   |   |-- usage-guidelines.md
|   |-- colors/
|   |-- typography/
|   |-- advertisement/
|   |-- mockups/
|   |-- BRAND_GUIDELINES.md
|-- digital_awareness/
|   |-- index.html
|   |-- style.css
|   |-- script.js
|   |-- data/
|   |-- assets/
|-- shared/
|   |-- constants.py
|   |-- constants.css
|   |-- constants.js
|   |-- utils/
|-- docs/
|   |-- ARCHITECTURE.md
|   |-- API.md
|   |-- DEPLOYMENT.md
|   |-- TESTING.md
|-- tests/
|   |-- test_cashier.py
|   |-- test_visitors.py
|   |-- test_classifier.py
|   |-- test_attendance.py
|   |-- test_website.py
|   |-- test_digital_awareness.py
|-- .github/
|   |-- workflows/
|       |-- deploy-website.yml
|       |-- deploy-digital-awareness.yml
|-- .gitignore
|-- requirements.txt
|-- package.json (optional)
|-- Makefile (optional)
|-- LICENSE
|-- CONTRIBUTING.md
|-- README.md (Master)
## Module Integration Strategy

### Shared Design System
| Asset | Location | Used By |
|-------|----------|---------|
| Color Palette | shared/constants.css, shared/constants.py | All modules |
| Typography | shared/constants.css, shared/constants.py | All modules |
| Logo | branding/logo/final/future-mall-logo.svg | All modules |
| Icons | shared/assets/icons/ | All modules |
| Components | shared/components/ | Web modules |

### Shared Constants (shared/constants.py)
`python
BRAND = {
    "name": "Future Mall",
    "slogan": "Shopping for Tomorrow",
    "colors": {
        "primary": "#2563EB",
        "secondary": "#0D9488",
        "accent": "#F97316",
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
    "spacing": {"xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px"},
    "radius": {"sm": "4px", "md": "8px", "lg": "12px", "xl": "16px", "full": "9999px"},
    "shadows": {"sm": "0 1px 2px", "md": "0 4px 6px", "lg": "0 10px 15px", "xl": "0 20px 25px"},
}
`

---

## Module Specifications

### Module 1: Cashier Program (python_modules/cashier_program.py)
**Type**: Console Application
**Status**: Planned in PYTHON_PROJECTS_PLAN.md
**Integration**: Uses shared/constants.py for branding colors in terminal output

### Module 2: Visitors Analysis (python_modules/visitors_analysis.py)
**Type**: Console Application
**Status**: Planned in PYTHON_PROJECTS_PLAN.md
**Integration**: Uses shared/constants.py for formatted output

### Module 3: Product Classifier (python_modules/product_classifier.py)
**Type**: Console Application
**Status**: Planned in PYTHON_PROJECTS_PLAN.md
**Integration**: Uses shared/constants.py for formatted output

### Module 4: GitHub Pages Website (website/)
**Type**: Static Website (HTML/CSS/JS)
**Status**: Planned in GITHUB_PAGES_PLAN.md
**Deployment**: GitHub Pages at username.github.io/future-mall-capstone/
**Integration**: Loads brand constants from shared/constants.css, Links to Digital Awareness, Showcases all modules

### Module 5: Logo & Branding (branding/)
**Status**: Planned in LOGO_BRANDING_PLAN.md
**Deliverables**: Final logo (SVG, PNG, favicon), Brand guidelines (PDF/MD), Advertisement assets (5 formats), Mockups

### Module 6: Digital Awareness (digital_awareness/)
**Type**: Interactive Web Application
**Status**: Planned in DIGITAL_AWARENESS_PLAN.md (needs creation)
**Deployment**: GitHub Pages at username.github.io/future-mall-capstone/digital-awareness/
**Integration**: Loads brand constants from shared/constants.css, Links from main website, Password checker, quiz, posters

### Module 7: Employee Attendance System (python_modules/attendance_system/)
**Type**: Desktop GUI (Python + Tkinter + SQLite)
**Status**: Planned in ATTENDANCE_SYSTEM_PLAN.md
**Integration**: Uses shared/constants.py for UI theming, Future Mall branded UI

---

## Implementation Timeline (4-5 Weeks)

### Week 1: Foundation & Branding (Days 1-3)
| Day | Tasks |
|-----|-------|
| 1 | Create shared/ constants (Python, CSS, JS), Set up repo structure |
| 2 | Branding: 3 logo concepts to final logo (6 variations) |
| 3 | Brand guidelines, color palette, typography, advertisement assets |

### Week 2: Python Console Modules (Days 4-6)
| Day | Tasks |
|-----|-------|
| 4 | Cashier, Visitors Analysis, Product Classifier core logic |
| 5 | Polish all 3, validation, error handling, README |
| 5 | Shared constants integration (colors in output) |

### Week 3: Attendance System & Digital Awareness (Days 7-10)
| Day | Tasks |
|-----|-------|
| 7-8 | Attendance System: Models, Services, UI (Tkinter), Reports |
| 8 | Digital Awareness: Plan content, HTML structure |
| 9 | Digital Awareness: CSS/JS, interactive features (quiz, checker) |
| 10 | Polish both, integrate brand constants |

### Week 4: Website & Integration (Days 11-14)
| Day | Tasks |
|-----|-------|
| 11 | Main website: HTML structure, semantic HTML |
| 12 | Main website: CSS (shared constants), JS, responsive |
| 13 | Digital Awareness: Quiz, password checker, posters |
| 14 | Integration: Cross-linking, shared constants, favicon |

### Week 5: Polish, Docs, Deploy (Days 15-17)
| Day | Tasks |
|-----|-------|
| 15 | Cross-module integration testing |
| 16 | Master README.md, docs/, CONTRIBUTING.md |
| 16 | GitHub Pages deployment (website + digital-awareness) |
| 16 | PyInstaller packaging for Python modules |
| 16 | Final testing, bug fixes |
| 17 | Final README.md, final testing, submission |

---

## Cross-Module Integration Points

### 1. Visual Consistency
- All modules use Future Mall color palette
- Logo appears in all GUIs and web pages
- Consistent typography (Space Grotesk/Inter)
- Consistent spacing, shadows, radius

### 2. Shared Data (Future Enhancement)
- Attendance system could share employee data with website admin
- Digital Awareness quiz scores could be stored
- Cashier transactions could feed visitor analysis

### 3. Navigation Flow
Website (Home) -> About Future Mall, Modules Showcase (Cashier, Visitors, Classifier, Attendance, Digital Awareness), Digital Awareness (Live Link), Brand Assets, Contact

### 4. GitHub Repository Structure
.github/workflows/deploy-website.yml and deploy-digital-awareness.yml for auto-deployment

---

## GitHub Pages Deployment Strategy

- **Main branch**: Source code
- **gh-pages branch**: Auto-deployed by GitHub Actions
- Two workflows: one for website/, one for digital_awareness/

---

## Documentation Structure

Master README.md with live demo links, module table, quick start, architecture/deployment links

---

## Testing Strategy

Unit tests for all Python modules (pytest), Integration tests for attendance flow, Digital Awareness quiz, Website navigation, Manual testing checklist

---

## Clarifying Questions

1. **Capstone Scope**: All 7 modules or subset?
2. **Timeline**: 4-5 weeks acceptable?
3. **Team**: Solo or team?
4. **Hosting**: GitHub Pages or Netlify/Vercel?
5. **Python Packaging**: PyInstaller executables?
6. **Digital Awareness**: Create DIGITAL_AWARENESS_PLAN.md first?
7. **Attendance GUI**: Tkinter or React?
8. **Database**: SQLite or cloud (Supabase)?
9. **Digital Awareness Content**: Standard or custom?
10. **Branding**: Use existing LOGO_BRANDING_PLAN.md colors?
11. **Portfolio**: Optimize for GitHub portfolio?
12. **Evaluation**: Grading rubric?
13. **Extras**: QR check-in, PDF reports, PWA, multi-language?

---

## Success Criteria (Capstone Level)

**Technical**: All 7 modules functional, zero critical bugs, clean typed documented code, meaningful Git history, CI/CD passing
**Design**: Consistent branding across ALL modules, responsive 320-1440px, WCAG AA accessible, dark mode, logo scales 16px-3m
**Architecture**: Modular shared/ constants, clean Models/Services/UI separation, component-based CSS/JS
**Documentation**: Master README with live links, module READMEs, ARCHITECTURE.md, DEPLOYMENT.md, BRAND_GUIDELINES.pdf, CONTRIBUTING.md, LICENSE
**Portfolio**: Live GitHub Pages URLs, screenshots/GIFs, professional Git history, professional repo structure

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Scope creep | Strict 4-week sprint, freeze scope Week 1 |
| Branding inconsistency | Single shared/ source of truth, design review |
| Time overflow | Prioritize Core Python -> Attendance -> Website -> Digital Awareness |
| Integration bugs | Shared constants from Day 1, integration test Week 4 |
| Deployment issues | Test GitHub Actions locally (act) Week 1 |

---

## Next Steps

1. **Confirm scope** - All 7 modules or prioritized subset?
2. **Create DIGITAL_AWARENESS_PLAN.md** (missing from current plans)
3. **Initialize repo** with master structure
4. **Create shared/ constants** (Python, CSS, JS)
5. **Begin Phase 1**: Branding + Shared Constants
6. **Weekly checkpoints** with milestone demos

---

**Ready to proceed?** Confirm:
1. **Scope**: All 7 modules or subset?
2. **Timeline**: 4-5 weeks acceptable?
3. **Digital Awareness**: Create plan first?
4. **Priority order** for implementation?
5. **Team**: Solo or collaborators?
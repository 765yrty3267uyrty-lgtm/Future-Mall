# Future Mall - Project Specification Document

High-fidelity recreation of the FUTURE MALL capstone project specification as a professional academic-style PDF.

## Preview

Open `index.html` in a browser to view the two-page document. Use browser "Print to PDF" (Ctrl+P / Cmd+P) with these settings:
- **Paper size**: A4
- **Margins**: None / Default
- **Background graphics**: Enabled
- **Scale**: 100%

## Automated PDF Generation

```bash
# Install Puppeteer
npm install puppeteer

# Generate PDF
node generate-pdf.js
```

Output: `FUTURE-MALL-Specification.pdf`

## Structure

```
future-mall-document/
├── index.html          # Main document (2 pages)
├── styles.css          # All styles with print media queries
├── generate-pdf.js     # Puppeteer script for automated PDF
├── assets/
│   ├── mall-icon.svg   # Header shopping mall line art
│   ├── folder.svg      # Folder icon for zip diagram
│   ├── file.svg        # File icon for zip diagram
│   ├── check.svg       # Checkmark for rules card
│   ├── success.svg     # Green check for validation card
│   └── warning-icon.svg # Warning triangle for note boxes
└── README.md
```

## Design System

- **Colors**: Navy (`#0f172a`), Blue (`#3b82f6`), Amber (`#fffbeb`), Green (`#22c55e`)
- **Fonts**: Space Grotesk (display) + Inter (body) via Google Fonts
- **Spacing**: 4px base unit, strict vertical rhythm
- **Components**: Cards, tables, lists, diagrams, note boxes
- **Print-ready**: `@page` rules, page-break control, `@media print`

## Document Contents

### Page 1
1. Header: "FUTURE MALL" + mall icon
2. **1. The Complete Picture** - overview with numbered list
3. **What You Submit for Each Task** - info card + deliverables table
4. Warning note
5. **The Form of the Files** - naming conventions
6. **The Three Rules** - bordered card with blue check icons
6. Small note
7. **File Naming Convention Table** - 16-row reference table

### Page 2
1. File naming table continuation note
2. **4. The Zip Structure** - folder tree diagram card
3. **5. Project Validation** - validation illustration card (device + green check + "Open successfully")
4. Success callout
5. **6. Timing** - deadlines, penalties, extensions
6. **7. The Final Checklist** - 15-item verification list
7. **8. Summary** - concluding paragraph

## Customization

Edit `index.html` to update text content. Modify `styles.css` for visual adjustments. The CSS uses CSS custom properties for easy theming.

## Requirements

- Modern browser (Chrome, Firefox, Safari, Edge) for HTML viewing
- Node.js 18+ and Puppeteer for automated PDF generation

## License

Part of the Future Mall capstone project. See root LICENSE.
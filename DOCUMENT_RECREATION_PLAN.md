# Future Mall Document Recreation - Implementation Plan

## Project Overview
Create a pixel-perfect, high-fidelity recreation of the FUTURE MALL project specification document as a professional academic-style PDF. Two-page layout with exact visual matching to reference design.

## Approach: HTML/CSS to PDF (Print Media)
**Why HTML/CSS**: Maximum control over typography, spacing, borders, tables, cards, and exact visual reproduction. Print media queries enable precise page breaks and PDF generation.

## Tech Stack
- HTML5 - Semantic structure
- CSS3 - Custom properties, Grid/Flexbox, print media queries, @page rules
- No JS required - Pure document layout
- Generation: Browser Print to PDF or headless Chrome (Puppeteer/Playwright)
- Fonts: System UI stack (Inter, Space Grotesk) or embedded Google Fonts

---

## Color Palette (Exact from Reference)
:root {
  /* Primary Navy */
  --navy-900: #0f172a;      /* Section headings, table headers, dark text */
  --navy-800: #1e293b;      /* Body text, borders */
  --navy-700: #334155;      /* Subtle text */

  /* Light Blue Accents */
  --blue-50:  #eff6ff;       /* Page background tint, alternating rows */
  --blue-100: #dbeafe;       /* Card backgrounds, light borders */
  --blue-200: #bfdbfe;       /* Dividers, table borders */
  --blue-500: #3b82f6;       /* Icons, numbered circles, check icons */
  --blue-600: #2563eb;       /* Primary buttons/links if any */

  /* Warning/Note Colors */
  --amber-50:  #fffbeb;      /* Note card background */
  --amber-100: #fef3c7;      /* Note card border */
  --amber-700: #b45309;      /* Note card text/icon */

  /* Success */
  --green-500: #22c55e;      /* Success check icon only */

  /* Neutrals */
  --white:     #ffffff;
  --gray-50:   #f8fafc;      /* Alternating table rows */
  --gray-100:  #f1f5f9;      /* Canvas background */
  --gray-200:  #e2e8f0;      /* Light borders */
  --gray-400:  #94a3b8;      /* Muted text */

  /* Canvas */
  --canvas-bg: #f1f5f9;      /* Surrounding page canvas */
  --page-bg:   #ffffff;      /* Document page background */
}

---

## Typography Scale
:root {
  /* Font Families */
  --font-sans: Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;
  --font-display: Space Grotesk, var(--font-sans);

  /* Font Sizes (compact, academic) */
  --text-xs:    0.6875rem;  /* 11px - footnotes, table cells */
  --text-sm:    0.75rem;    /* 12px - body, list items */
  --text-base:  0.8125rem;  /* 13px - comfortable body */
  --text-lg:    0.875rem;   /* 14px - subheadings */
  --text-xl:    1rem;       /* 16px - section titles */
  --text-2xl:   1.25rem;    /* 20px - page title */

  /* Line Heights */
  --leading-tight:   1.3;
  --leading-normal:  1.5;
  --leading-relaxed: 1.6;

  /* Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}

---

## Spacing System (Strict Vertical Rhythm)
:root {
  --space-1:  0.25rem;  /* 4px  */
  --space-2:  0.5rem;   /* 8px  */
  --space-3:  0.75rem;  /* 12px */
  --space-4:  1rem;     /* 16px */
  --space-5:  1.25rem;  /* 20px */
  --space-6:  1.5rem;   /* 24px */
  --space-8:  2rem;     /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
}

---

## Document Dimensions (A4 Portrait)
@page {
  size: A4;
  margin: 0;
  padding: 0;
}

.document-page {
  width: 210mm;
  height: 297mm;
  background: var(--page-bg);
  box-sizing: border-box;
  /* Content area with margins */
  padding: 20mm 18mm 25mm 18mm;  /* Top, Right, Bottom, Left */
}

---

## Component Specifications

### 1. Page Container & Canvas
.canvas {
  min-height: 100vh;
  background: var(--canvas-bg);
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

.page {
  width: 210mm;
  min-height: 297mm;
  background: var(--page-bg);
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

### 2. Header/Logo Area (Page 1 Top)
- Centered FUTURE MALL in Space Grotesk, 28px, navy-900, tracking-wide
- Simple line-art shopping mall icon (SVG, 60x40px, blue-500 stroke)
- Spacing: 16px below title, 24px below icon before first section

### 3. Section Headings
.section-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  color: var(--navy-900);
  margin-bottom: var(--space-2);
}

.section-divider {
  height: 1.5px;
  background: linear-gradient(90deg, transparent, var(--blue-300), transparent);
  border: none;
  margin-bottom: var(--space-4);
  width: 60px;  /* Short divider under title */
}

### 4. Body Text
.body-text {
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  color: var(--navy-700);
  margin-bottom: var(--space-3);
  text-align: justify;
  hyphens: auto;
}

### 5. Numbered/Bullet Lists
.numbered-list {
  list-style: none;
  counter-reset: item;
  margin: var(--space-3) 0;
  padding-left: var(--space-6);
}

.numbered-list li {
  position: relative;
  padding-left: var(--space-4);
  margin-bottom: var(--space-2);
  font-size: var(--text-sm);
  line-height: var(--leading-normal);
  color: var(--navy-700);
}

.numbered-list li::before {
  counter-increment: item;
  content: counter(item);
  position: absolute;
  left: 0;
  top: 0;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--blue-500);
  color: white;
  font-size: 10px;
  font-weight: var(--font-bold);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

### 6. Info Card: What You Submit for Each Task
.info-card {
  border: 1.5px solid var(--blue-200);
  border-radius: 8px;
  background: var(--white);
  padding: var(--space-4) var(--space-5);
  margin: var(--space-4) 0;
}

.info-card-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--navy-900);
  margin-bottom: var(--space-3);
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

### 7. Data Tables
.spec-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-xs);
  line-height: var(--leading-normal);
  margin: var(--space-4) 0;
}

.spec-table thead th {
  background: var(--navy-900);
  color: var(--white);
  font-weight: var(--font-semibold);
  padding: var(--space-2) var(--space-3);
  text-align: left;
  border: none;
}

.spec-table tbody td {
  padding: var(--space-2) var(--space-3);
  border-bottom: 1px solid var(--blue-100);
  color: var(--navy-700);
}

.spec-table tbody tr:nth-child(even) td {
  background: var(--blue-50);
}

.spec-table tbody tr:last-child td {
  border-bottom: none;
}

.spec-table td:first-child {
  width: 18%;
  font-weight: var(--font-medium);
  color: var(--navy-800);
}

### 8. Note/Callout Boxes
.note-box {
  border: 1px solid var(--amber-200);
  border-radius: 6px;
  background: var(--amber-50);
  padding: var(--space-3) var(--space-4);
  margin: var(--space-4) 0;
  font-size: var(--text-xs);
  color: var(--amber-800);
  display: flex;
  gap: var(--space-3);
  align-items: flex-start;
}

.note-box.warning { border-color: var(--amber-300); }
.note-box.success { 
  border-color: var(--green-200); 
  background: #f0fdf4; 
  color: #166534; 
}

### 9. The Three Rules Card
.rules-card {
  border: 1.5px solid var(--blue-200);
  border-radius: 8px;
  background: var(--white);
  padding: var(--space-5);
  margin: var(--space-5) 0;
}

.rule-item {
  display: flex;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
  align-items: flex-start;
}

.rule-item:last-child { margin-bottom: 0; }

.rule-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--blue-500);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
  flex-shrink: 0;
  margin-top: 2px;
}

.rule-text {
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  color: var(--navy-700);
}

### 10. Zip Structure Diagram Card
.diagram-card {
  border: 1.5px solid var(--blue-200);
  border-radius: 8px;
  background: var(--white);
  padding: var(--space-5);
  margin: var(--space-4) 0;
}

.diagram-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--navy-900);
  text-align: center;
  margin-bottom: var(--space-5);
}

.folder-tree {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--navy-700);
}

.folder-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-3);
  background: var(--blue-50);
  border-radius: 4px;
  border: 1px solid var(--blue-100);
}

.folder-icon {
  color: var(--blue-500);
  width: 16px;
  flex-shrink: 0;
}

### 11. Validation Illustration Card
.validation-card {
  border: 1.5px solid var(--blue-200);
  border-radius: 8px;
  background: var(--white);
  padding: var(--space-6);
  margin: var(--space-5) 0;
  text-align: center;
}

.validation-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-6);
  margin-top: var(--space-4);
}

.device-mockup {
  width: 120px;
  height: 80px;
  border: 2px solid var(--blue-200);
  border-radius: 8px;
  background: var(--blue-50);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: var(--text-xs);
  color: var(--navy-600);
}

.success-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--green-500);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.success-text {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  color: var(--navy-900);
}

### 12. Final Checklist
.checklist {
  list-style: none;
  padding: 0;
  margin: var(--space-3) 0;
}

.checklist li {
  position: relative;
  padding-left: var(--space-6);
  margin-bottom: var(--space-2);
  font-size: var(--text-sm);
  line-height: var(--leading-normal);
  color: var(--navy-700);
}

.checklist li::before {
  content: check;
  position: absolute;
  left: 0;
  top: 0;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid var(--blue-500);
  color: var(--blue-500);
  font-size: 11px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

---

## Page Break Strategy
@media print {
  @page {
    size: A4;
    margin: 0;
  }
  
  .page-break {
    page-break-after: always;
    break-after: page;
  }
  
  /* Prevent breaking inside components */
  .info-card, .rules-card, .diagram-card, .validation-card, table {
    page-break-inside: avoid;
    break-inside: avoid;
  }
}

---

## File Structure
future-mall-document/
|-- index.html          # Main document (2 pages)
|-- styles.css          # All styles
|-- assets/
|   |-- mall-icon.svg   # Header shopping mall line art
|   |-- folder.svg      # Folder icon for zip diagram
|   |-- file.svg        # File icon for zip diagram
|   |-- check.svg       # Checkmark for rules
|   |-- success.svg     # Green check for validation
|-- generate-pdf.js     # Optional: Puppeteer script for automated PDF
|-- README.md

---

## SVG Icons Needed (Simple, Light Blue Stroke)
1. mall-icon.svg - Shopping mall line art (building with windows, entrance)
2. folder.svg - Standard folder outline
3. file.svg - Document outline
4. check.svg - Checkmark for The Three Rules
5. success.svg - Large checkmark for validation card
5. warning-icon.svg - Small warning triangle for note boxes
6. numbered-circles - CSS-generated (no SVG needed)

---

## Implementation Phases

### Phase 1: HTML Structure & Content (2-3 hours)
- Build semantic HTML matching exact section order
- Insert all text content from specification
- Create table structures with correct row/column counts
- Place all cards, lists, diagrams in correct positions
- Add page-break marker between pages

### Phase 2: CSS Styling & Visual Matching (3-4 hours)
- Implement design system (colors, typography, spacing)
- Style all components to match reference exactly
- Fine-tune borders, radii, shadows
- Adjust table alternating rows, header styling
- Perfect card borders, padding, icon alignment
- Match vertical rhythm and spacing

### Phase 3: Print Optimization & PDF Generation (1-2 hours)
- Add @page rules, print media queries
- Test page breaks fall correctly
- Verify no content cut off at page boundaries
- Generate PDF via browser print or headless Chrome
- Verify PDF output matches reference

### Phase 4: Polish & Verification (1 hour)
- Side-by-side comparison with reference
- Check all measurements: margins, font sizes, spacing
- Verify color accuracy
- Test at different zoom levels
- Final PDF output

---

## Content Requirements (From User Spec)

### Page 1 Sections (in order):
1. Header: FUTURE MALL + mall icon
2. 1. The Complete Picture - heading, divider, paragraphs, numbered list
3. What You Submit for Each Task - info card with numbered list
4. Table - task submission requirements (navy header, alternating rows)
5. Note box - pale yellow/orange callout
6. The Form of the Files - heading, divider, paragraphs, subsection, warning box
7. The Three Rules - bordered card with 3 rules + blue check icons
8. Note - small note under rules card
9. File Naming Convention Table - long table with dark navy header

### Page 2 Sections (continuing):
1. File naming table continued (from page 1)
2. Short explanatory paragraph
3. 4. The Zip Structure - heading, paragraphs, diagram card
4. 5. Project Validation - heading, explanation, validation illustration card
5. Success callout - pale green box
6. 6. Timing - heading, paragraphs about deadlines
7. 7. The Final Checklist - heading, numbered checklist with blue circles
8. 8. Summary - heading, concluding paragraph

---

## Clarifying Questions

1. **Content Source**: Do you have the exact text content for all sections, or should I use placeholder lorem ipsum matching the structure?

2. **Reference Images**: You mentioned attached reference images - can you share them, or should I work from your detailed description only?

3. **Table Data**: Exact row/column counts and content for:
   - What You Submit table
   - File Naming Convention table (how many rows?)
   - Zip structure diagram items

4. **Icons**: Should I create the SVG icons, or do you have specific icon assets?

5. **Output Format**: 
   - HTML file only (you print to PDF)?
   - HTML + automated PDF generation script?
   - Just the PDF?

6. **Fonts**: Use system fonts (Inter/Space Grotesk via Google Fonts CDN) or local font files?

7. **Page Size**: A4 (210x297mm) or US Letter (8.5x11in)?

8. **Language**: English only, or any localization needed?

---

## Success Criteria
- [ ] Visual match >= 95% to reference design
- [ ] Correct two-page flow with natural page break
- [ ] All components: tables, cards, lists, diagrams, icons
- [ ] Exact color palette: navy/blue/white/amber/green
- [ ] Typography: Inter/Space Grotesk, correct sizes/weights
- [ ] Spacing: Consistent vertical rhythm, proper margins
- [ ] Tables: Navy headers, alternating rows, thin borders
- [ ] Cards: Thin blue borders, 8px radius, proper padding
- [ ] Icons: Blue circular numbers, checkmarks, folder/file icons
- [ ] Print-ready: No content cut off, clean PDF output
- [ ] Professional academic document appearance (not web dashboard)

---

## Estimated Effort: 7-11 hours

| Phase | Hours |
|-------|-------|
| HTML Structure | 2-3 |
| CSS Styling | 3-4 |
| Print/PDF | 1-2 |
| Polish | 1 |
| **Total** | **7-11** |

---

## Next Steps
1. **Provide exact text content** for all sections (or confirm placeholder text is OK)
2. **Share reference images** if available
3. **Confirm table data** (row counts, content)
4. **Choose output preference** (HTML only vs HTML+PDF script)
5. **Confirm page size** (A4 vs Letter)
6. Then I will implement Phase 1 -> 2 -> 3 -> 4
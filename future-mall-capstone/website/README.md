# Future Mall Website

Responsive portfolio website for the capstone project. Deploys automatically to
GitHub Pages via `.github/workflows/deploy-website.yml`.

## Run Locally

```bash
npm install   # optional; npx serve is enough
npx serve .
```

Open `http://localhost:3000`.

## Structure

- `index.html` — semantic HTML5, accessible, responsive
- `style.css` — CSS custom properties, Grid, Flexbox, dark mode
- `script.js` — nav, scroll, dark mode, interactivity
- `assets/` — SVG logos, favicon, hero illustration
- `package.json` — scripts (`npm run serve`, `npm run format`)

## Features

- Skip-link and ARIA labels
- Responsive from 320px to 1440px+
- Dark mode via OS preference
- Sections: Home, About, Modules, Digital Awareness, Brand, Contact
- Inline SVG icons (no external icon library)

## Tests

See `../tests/test_website.py` (run from repo root with `pytest tests/ -v`).

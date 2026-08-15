# Digital Awareness

Interactive cybersecurity education platform for the Future Mall capstone project.
Deploys to GitHub Pages under `/digital-awareness/`.

## Pages

| Page | Purpose |
|------|---------|
| `index.html` | Home with module cards and quick tips |
| `threats.html` | Threat library — 8 categories with severity, description, prevention |
| `password.html` | Real-time password strength checker + generator |
| `quiz.html` | 15-question phishing identification quiz |
| `posters.html` | 6 downloadable safety posters with preview modal |

## Run Locally

```bash
npx serve .
```

Open `http://localhost:3000`.

## Key Files

- `style.css` — shared styling (imports `../shared/constants.css` tokens)
- `script.js` — shared shell behavior (nav, dark mode)
- `password.js` — entropy calculation, strength meter, generator
- `quiz.js` — quiz engine, scoring, category breakdown, tips
- `posters.js` — poster data, preview, download/bundle logic
- `assets/` — poster artwork and illustrations

## Tests

See `../tests/test_digital_awareness.py` (run with `pytest tests/ -v`).

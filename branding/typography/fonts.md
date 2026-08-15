# Typography

Future Mall type system. Fonts are loaded from Google Fonts.

## Families

| Role | Font | Weights | Fallbacks |
|------|------|---------|-----------|
| Display / Headings | Space Grotesk | 500, 600, 700 | `system-ui`, sans-serif |
| Body | Inter | 400, 500, 600 | `system-ui`, sans-serif |
| Mono / Code | JetBrains Mono | 400, 500 | `monospace` |

## Recommended CSS

```css
:root {
  --font-display: 'Space Grotesk', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

## Type Scale (desktop)

| Token | Rem | Px | Family | Weight | Letter-spacing |
|-------|-----|----|--------|--------|----------------|
| display | 3rem | 48 | Space Grotesk | 700 | -0.02em |
| h1 | 2.25rem | 36 | Space Grotesk | 700 | -0.02em |
| h2 | 1.875rem | 30 | Space Grotesk | 600 | -0.01em |
| h3 | 1.5rem | 24 | Space Grotesk | 600 | 0 |
| h4 | 1.25rem | 20 | Inter | 600 | 0 |
| body-lg | 1.125rem | 18 | Inter | 400 | 0 |
| body | 1rem | 16 | Inter | 400 | 0 |
| small | 0.875rem | 14 | Inter | 400 | 0 |
| label | 0.8125rem | 13 | Inter | 600 | 0.02em |
| caption | 0.75rem | 12 | Inter | 400 | 0.03em |
| code | 0.875rem | 14 | JetBrains Mono | 400 | 0 |

## Guidelines

- **Headings** use Space Grotesk with tight (negative) letter-spacing for display.
- **Body copy** uses Inter; keep line-height at 1.5–1.6 for readability.
- **Code/technical values** (receipts, passwords, numbers) use JetBrains Mono.
- Mobile type scale: reduce `display` and `h1` by ~25% (e.g., `clamp()`).
- Maximum readable line length: ~72 characters (body).

## Accessible Type

- Never set body text below 14px.
- Recommended paragraph contrast ≥ 4.5:1.
- Use `rem` units so users can scale text from browser settings.

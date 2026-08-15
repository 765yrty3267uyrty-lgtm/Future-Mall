# Brand Guidelines

Future Mall — comprehensive usage guidelines for the visual identity system.

## 1. Brand Overview

**Future Mall** is a forward-thinking retail concept: *"Shopping for Tomorrow."*
The identity blends future-blue technology, innovation teal, and energy orange
with a modern geometric wordmark.

## 2. Logo

### Primary Logo
The horizontal lockup (mark + wordmark) is the default. Use most of the time.

### Stacked Logo
For square, avatar, or social contexts where horizontal space is limited.

### Icon Only
For app icons, favicons, and small UI footprints where the wordmark cannot be read.

### Variations
Six versions are provided in `logo/final/`:
1. **Primary** — full color, horizontal
2. **Stacked** — full color, stacked
3. **Icon Only** — mark only
4. **Black** — single-color black (light backgrounds)
5. **White** — single-color white (dark/photographic backgrounds)
6. **Responsive** — adapts between stacked and horizontal

### Logo Usage Rules
- **Clear space:** keep a margin of at least the height of the `F` around the logo.
- **Minimum size:** never render below 32px wide (icon) / 80px wide (horizontal).
- **Do not:** stretch, rotate, recolor, add drop shadows, place on busy backgrounds,
  or combine with other logos.
- **Backgrounds:** use the primary or black version on light backgrounds; use the
  white version on the dark primary (`#1E293B`) or dark photographic backgrounds.

## 3. Color

See [`colors/palette.md`](colors/palette.md) for the full palette.

### Brand Colors
| Token | Value | Usage |
|-------|-------|-------|
| Future Blue | `#2563EB` | Primary actions, links, focal points |
| Innovation Teal | `#0D9488` | Secondary highlights, success accents |
| Energy Orange | `#F97316` | Calls-to-action, attention elements |
| Ink / Slate-900 | `#1E293B` | Text and dark surfaces |
| Canvas / Slate-50 | `#F8FAFC` | Page backgrounds |

### Contrast & Accessibility
- Body text must maintain a minimum WCAG AA contrast ratio (4.5:1 for text,
  3:1 for large text and UI components).
- Never place orange text on white for small text.
- Color is decorative, never the sole carrier of meaning.

## 4. Typography

See [`typography/fonts.md`](typography/fonts.md) for the full type system.

- **Display / Headings:** Space Grotesk (500–700)
- **Body:** Inter (400–600)
- **Mono / Code:** JetBrains Mono

## 5. Spacing & Layout

Base unit is **4px** (`--space-xs`). Scale: xs (4), sm (8), md (16), lg (24), xl (32).

## 6. Imagery & Illustration

- Use the geometric storefront mark and simple line illustrations.
- Tone: clean, minimal, forward-looking, optimistic.
- Avoid stock-photo clichés and heavy gradients that fight the flat identity.

## 7. Icons

- Inline SVG only, 1.5–2 stroke weight, rounded caps.
- Match `currentColor` so icons inherit nearby text color.

## 8. Writing & Voice

- Short, direct, optimistic. Avoid excessive jargon.
- Reference the tagline: *"Shopping for Tomorrow"*.
- Use title case for headings.

## 9. Do's & Don'ts

### Do
- Use primary blue for primary actions.
- Use white variation on dark surfaces.
- Keep generous clear space.

### Don't
- Change brand colors without approval.
- Use the logo on clashing backgrounds.
- Stretch or distort the logo.
- Add effects (glows, shadows, gradients) to the logo.

## 10. File Formats

- **SVG** (default, scalable, web/screen)
- **PNG** (raster distribution, exports)
- Deliverables live in `logo/final/`, mockups in `mockups/`, ads in `advertisement/`.

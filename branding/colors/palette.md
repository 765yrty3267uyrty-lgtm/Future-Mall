# Color Palette

Future Mall brand color system. All values are mirrored in `shared/constants.css`
and `shared/constants.js`.

## Brand Colors

| Token | Hex | CMYK | RGB |
|-------|-----|------|-----|
| Future Blue | `#2563EB` | 84/58/0/8 | 37, 99, 235 |
| Innovation Teal | `#0D9488` | 91/0/8/42 | 13, 148, 136 |
| Energy Orange | `#F97316` | 0/53/91/2 | 249, 115, 22 |

## Neutrals

| Token | Hex | Usage |
|-------|-----|-------|
| Ink-900 | `#0F172A` | Darkest text |
| Slate-900 | `#1E293B` | Headings, dark surfaces |
| Slate-600 | `#475569` | Muted text |
| Slate-400 | `#94A3B8` | Disabled, placeholders |
| Slate-100 | `#F1F5F9` | Card backgrounds |
| Slate-50 | `#F8FAFC` | Page background (light mode) |

## Functional Colors

| Token | Hex | Usage |
|-------|-----|-------|
| Success | `#10B981` | Positive states, check-in success |
| Warning | `#F59E0B` | Warnings, low stock |
| Danger | `#EF4444` | Errors, high-severity threats |
| Info | `#3B82F6` | Informational accents |

## Dark Mode

| Token | Hex | Usage |
|-------|-----|-------|
| Background | `#0F172A` | Page background (dark mode) |
| Surface | `#1E293B` | Cards, inputs |
| Border | `#334155` | Dividers, outlines |
| Text | `#F8FAFC` | Primary text (dark mode) |

## Color Roles in Modules

- **Digital Awareness:** severity badges use success/warning/danger scales.
- **Attendance System:** check-in = success, check-out = info, overtime = warning.
- **Cashier/Classifier:** discount tiers and stock states use functional colors.
- **Website:** primary blue for CTAs, orange for the highlight accent.

## Ratios

- Primary : Secondary : Accent = **60 : 25 : 15** (approximate, visual balance).
- Accent orange should never exceed ~15% of a surface.

## Accessibility

- Meet WCAG AA: 4.5:1 for normal text, 3:1 for large text/UI components.
- When using functional colors, pair with an icon or text label (never color alone).

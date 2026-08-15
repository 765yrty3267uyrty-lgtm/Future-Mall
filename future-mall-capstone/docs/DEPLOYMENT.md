# Future Mall - Deployment Guide

## Overview

This guide covers deployment of all Future Mall modules across different platforms.

## GitHub Pages Deployment (Automatic)

### Prerequisites
- GitHub repository with GitHub Pages enabled
- `main` branch as default branch
- GitHub Actions enabled

### Setup

1. **Enable GitHub Pages**:
   - Go to Repository Settings → Pages
   - Source: "GitHub Actions"
   - Save

2. **Repository Structure** (must match):
   ```
   future-mall-capstone/
   ├── website/           # Main website (deploys to site root)
   ├── digital_awareness/ # Cybersecurity education (deploys to /digital-awareness/)
   ├── branding/          # Brand assets (deploys to /branding/)
   └── .github/workflows/
       └── deploy-pages.yml
   ```

3. **Automatic Deployment**:
   - Push to `main` branch triggers the single `deploy-pages.yml` workflow
   - Website deploys to: `https://username.github.io/future-mall-capstone/`
   - Digital Awareness deploys to: `https://username.github.io/future-mall-capstone/digital-awareness/`
   - Brand assets deploy to: `https://username.github.io/future-mall-capstone/branding/`

### Workflow Details

#### Pages Deployment (`.github/workflows/deploy-pages.yml`)
```yaml
on:
  push:
    branches: [main]
```
- Single workflow assembles one site so modules never overwrite each other:
  - `website/` → site root (`/`)
  - `digital_awareness/` → `/digital-awareness/`
  - `branding/` → `/branding/`
- Uploads the assembled `_site/` as a single Pages artifact and deploys

### Custom Domain (Optional)

1. Add `CNAME` file to `website/`:
   ```
   futuremall.example.com
   ```

2. Configure DNS:
   - CNAME: `futuremall.example.com` → `username.github.io`
   - Or A records: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`

3. Enable "Enforce HTTPS" in Pages settings

## Python Module Deployment

### Executable Creation (PyInstaller)

#### Prerequisites
```bash
pip install pyinstaller
```

#### Build Commands

**Console Apps (Windowed)**:
```bash
cd python_modules

# Cashier
pyinstaller --onefile --windowed --name "FutureMall-Cashier" \
  --icon=../branding/logo/final/favicon.ico \
  cashier_program.py

# Visitors Analysis
pyinstaller --onefile --windowed --name "FutureMall-Visitors" \
  --icon=../branding/logo/final/favicon.ico \
  visitors_analysis.py

# Product Classifier
pyinstaller --onefile --windowed --name "FutureMall-Classifier" \
  --icon=../branding/logo/final/favicon.ico \
  product_classifier.py
```

**Attendance System (with data)**:
```bash
cd python_modules/attendance_system

pyinstaller --onefile --windowed --name "FutureMall-Attendance" \
  --icon=../../branding/logo/final/favicon.ico \
  --add-data "data;data" \
  --hidden-import=tkinter \
  --hidden-import=sqlite3 \
  main.py
```

#### Output
- Executables in `dist/`
- Single `.exe` files (Windows) or binaries (Linux/macOS)
- Include `branding/logo/final/favicon.ico` for app icon

#### Distribution
- Zip each executable with its README
- Distribute via GitHub Releases
- Consider code signing for Windows (avoid SmartScreen warnings)

## Development Server

### Local Web Development
```bash
# Main Website
cd website
npx serve .

# Digital Awareness
cd digital_awareness
npx serve .

# Or use Python
python -m http.server 8000
```

### Live Reload (Optional)
```bash
# Install browser-sync
npm install -g browser-sync

# Run with live reload
browser-sync start --server --files "**/*.html, **/*.css, **/*.js"
```

## Docker Deployment (Optional)

### Dockerfile for Web Modules
```dockerfile
# website/Dockerfile
FROM nginx:alpine
COPY . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'
services:
  website:
    build: ./website
    ports:
      - "8080:80"
  
  digital-awareness:
    build: ./digital_awareness
    ports:
      - "8081:80"
```

## Environment Configuration

### Production Variables
```bash
# .env.production (not committed)
# Attendance System (if using external DB)
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-secret-key
DEBUG=false
```

### GitHub Secrets (for Actions)
```
# Repository Settings → Secrets → Actions
CUSTOM_DOMAIN=futuremall.example.com  # Optional
```

## Verification Checklist

### Pre-Deployment
- [ ] All tests pass (`pytest tests/`)
- [ ] Linting passes (`flake8`, `stylelint`)
- [ ] Build succeeds locally
- [ ] No console errors in browser
- [ ] Responsive at 320px, 768px, 1024px, 1440px
- [ ] Dark mode works
- [ ] Keyboard navigation works
- [ ] Skip links functional
- [ ] ARIA labels present

### Post-Deployment
- [ ] Live URLs accessible
- [ ] HTTPS enforced
- [ ] Custom domain works (if applicable)
- [ ] GitHub Actions show green
- [ ] No mixed content warnings
- [ ] Performance acceptable (Lighthouse > 90)

## Rollback Procedure

### GitHub Pages
1. Go to Actions tab
2. Find previous successful deployment
3. Click "Re-run" or manually trigger with previous commit

### Python Executables
- Keep previous `dist/` versions
- Revert to previous release on GitHub Releases

## Monitoring

### GitHub Actions
- Monitor workflow runs in Actions tab
- Set up notifications for failures
- Review deployment logs

### GitHub Pages
- Check Pages settings for build status
- Monitor 404s in repository insights
- Use Lighthouse CI for performance regression

## Troubleshooting

### Common Issues

**GitHub Pages not updating**:
- Check Actions tab for workflow status
- Verify `paths:` filter in workflow matches changed files
- Check `gh-pages` branch exists

**PyInstaller fails**:
- Ensure all imports are detected (`--hidden-import`)
- Check for missing data files (`--add-data`)
- Use `--debug` for verbose output

**CSS/JS not loading on Pages**:
- Check paths are relative (not absolute)
- Verify `base` href not needed
- Check browser console for 404s

**Dark mode not working**:
- Verify `prefers-color-scheme` media query
- Check CSS custom properties defined
- Test in browser dev tools

## Performance Optimization

### Before Deploy
- Minify CSS/JS (optional for static sites)
- Optimize images (WebP, appropriate sizes)
- Enable gzip/brotli (automatic on GitHub Pages)
- Use `Cache-Control` headers (automatic on GitHub Pages)

### Lighthouse Targets
- Performance: > 90
- Accessibility: > 95
- Best Practices: > 90
- SEO: > 90

## Security

### Headers (via GitHub Pages)
- HTTPS enforced
- HSTS enabled
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff

### Content Security Policy (if needed)
```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' fonts.googleapis.com; font-src 'self' fonts.gstatic.com;">
```

## Support

For deployment issues:
1. Check GitHub Actions logs
2. Review GitHub Pages documentation
3. Open issue in repository
# Contributing to Future Mall

Thank you for your interest in contributing to the Future Mall capstone project! This document provides guidelines for contributing.

## Code of Conduct

By participating, you agree to uphold our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- No harassment, discrimination, or offensive behavior

## How to Contribute

### Reporting Bugs
1. Check existing issues first
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment (OS, Python version, browser)
   - Screenshots if applicable

### Suggesting Features
1. Check existing issues/discussions
2. Create a feature request with:
   - Clear use case
   - Proposed solution
   - Alternatives considered
   - Impact assessment

### Pull Requests

#### Before Submitting
- [ ] Fork the repository
- [ ] Create a feature branch: `git checkout -b feature/your-feature`
- [ ] Make your changes
- [ ] Run tests locally
- [ ] Update documentation if needed
- [ ] Ensure code passes linting

#### PR Requirements
- Clear title and description
- Reference related issues (`Fixes #123`)
- Single logical change per PR
- Tests pass
- Code follows style guide
- Documentation updated

## Development Setup

### Prerequisites
- Python 3.12+
- Node.js 20+ (for web tooling)
- Git

### Clone and Setup
```bash
git clone https://github.com/username/future-mall-capstone.git
cd future-mall-capstone

# Python dependencies
cd python_modules
pip install -r requirements.txt
cd ../attendance_system
pip install -r requirements.txt

# Web tooling (optional)
cd ../../website
npm install
cd ../digital_awareness
npm install
```

### Running Tests
```bash
# Python tests
cd python_modules
pytest tests/ -v

# Web linting
cd ../website
npx stylelint style.css
cd ../digital_awareness
npx stylelint style.css
```

## Code Style Guide

### Python
- Follow PEP 8
- Use type hints on all functions
- Docstrings for public functions/classes (Google style)
- Line length: 100 chars
- Use `black` for formatting: `black .`
- Use `isort` for imports: `isort .`

### CSS
- Use CSS custom properties from `shared/constants.css`
- BEM-ish naming: `.component__element--modifier`
- Mobile-first responsive
- 4px spacing scale
- Nesting max 3 levels

### JavaScript
- ES6+ features
- Single responsibility functions
- JSDoc comments for public functions
- `const`/`let` only (no `var`)
- Arrow functions for callbacks

### HTML
- Semantic HTML5 elements
- ARIA labels for accessibility
- `lang="en"` on `<html>`
- Skip link at top
- Proper heading hierarchy

### Git Commit Messages
```
type(scope): brief description

Longer description if needed.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

## Project Structure Guidelines

### Adding New Python Module
1. Create `python_modules/new_module.py`
2. Follow existing patterns (constants, models, main loop)
2. Add tests in `tests/test_new_module.py`
3. Update `README.md` module list

### Adding New Web Page
1. Create HTML in appropriate folder
2. Link shared CSS/JS
3. Add navigation link
4. Test responsive/accessibility
5. Update sitemap if needed

### Adding New Brand Asset
1. Create in `branding/` following structure
2. Export SVG, PNG @1x/2x/3x
3. Update `BRAND_GUIDELINES.md`
4. Add to `branding/README.md`

## Code Review Process

### For Reviewers
- Be constructive and specific
- Focus on code, not person
- Suggest improvements with examples
- Approve when ready
- Request changes with clear reasons

### For Authors
- Respond to all comments
- Make requested changes
- Push updates to same branch
- Re-request review when ready

## Release Process

### Versioning
Semantic Versioning: `MAJOR.MINOR.PATCH`
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Steps
1. Update version in relevant files
2. Update `CHANGELOG.md`
3. Create release tag: `git tag v1.2.3`
4. Push tag: `git push origin v1.2.3`
5. GitHub Actions creates release
6. Upload Python executables as release assets

## Getting Help

- Open a GitHub Discussion for questions
- Check existing documentation in `docs/`
- Review code comments for context
- Ask in PR comments

## Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Project README

Thank you for contributing to Future Mall! 🛒✨
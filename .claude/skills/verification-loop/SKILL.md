---
name: verification-loop
description: Systematic quality verification for ARDIA PRECISION HEALTH. Run after completing a feature or before pushing. Checks build, types, lint, tests, security scan, and diff review.
---

Run a full verification pass on the current changes before pushing.

## Phase 1: HTML/CSS Validation (current static site)

```bash
# Check all 20 HTML files parse cleanly
for f in /home/user/ardiaprecisionhealth/*.html; do
  python3 -c "
from html.parser import HTMLParser
p = HTMLParser()
p.feed(open('$f').read())
print('OK: $f')
"
done

# Verify logo/branding CSS is consistent across all pages
grep -l "logo-icon\|logo-mark\|nav-brand-icon" /home/user/ardiaprecisionhealth/*.html
```

## Phase 2: Branding Consistency Check

```bash
# Verify all pages have correct teal color
grep -c "#1d9bd1\|14b8a6" /home/user/ardiaprecisionhealth/*.html

# Verify no pages are empty (>0 bytes)
for f in /home/user/ardiaprecisionhealth/*.html; do
  size=$(wc -c < "$f")
  [ "$size" -lt 1000 ] && echo "WARNING: $f is suspiciously small ($size bytes)"
done

# Check Ardia_Logo.png is referenced everywhere
grep -L "Ardia_Logo.png" /home/user/ardiaprecisionhealth/*.html
```

## Phase 3: Git Diff Review

```bash
git diff --stat HEAD
git diff HEAD | head -200
```

Review changed files for:
- Accidental deletions of large content blocks
- CSS overrides that break the navbar
- Missing closing tags
- Hardcoded paths that won't work on Vercel

## Phase 4: Security Scan (static site)

```bash
# Check for accidental secrets in HTML
grep -rn "api_key\|secret\|password\|token" /home/user/ardiaprecisionhealth/*.html --include="*.html"

# Check for development artifacts
grep -rn "localhost\|127.0.0.1\|TODO\|FIXME\|console.log" /home/user/ardiaprecisionhealth/*.html
```

## Phase 5: Backend Code (when applicable)

```bash
# Python
pip install bandit safety
bandit -r src/ -ll                  # Security scan
safety check                         # Vulnerability check
python -m pytest tests/ --cov=src   # Tests with coverage
mypy src/                            # Type checking
```

## Verification Report Template

```
## Verification Report — [date]

### Phase 1: HTML Validation    [PASS/FAIL]
### Phase 2: Branding Check     [PASS/FAIL]
  - Pages with correct branding: X/20
  - Pages missing logo: [list]
### Phase 3: Diff Review        [PASS/FAIL]
  - Files changed: X
  - Suspicious changes: [list]
### Phase 4: Security Scan      [PASS/FAIL]
  - Secrets found: [none / list]
  - Dev artifacts: [none / list]

### Overall: READY / NOT READY
Issues requiring attention:
1. [issue]
2. [issue]
```

Re-run verification every time a new batch of files is updated.

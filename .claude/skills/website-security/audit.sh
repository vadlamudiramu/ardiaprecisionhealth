#!/usr/bin/env bash
# Website Security Audit — ARDIA PRECISION HEALTH
# Run from repo root: bash .claude/skills/website-security/audit.sh

set -euo pipefail

BASE="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$BASE"

HTML_FILES=$(ls *.html 2>/dev/null)
PASS=0
WARN=0
FAIL=0

_pass() { echo "  [PASS] $1"; ((PASS++)) || true; }
_warn() { echo "  [WARN] $1"; ((WARN++)) || true; }
_fail() { echo "  [FAIL] $1"; ((FAIL++)) || true; }
_head() { echo; echo "=== $1 ==="; }

# ─── 1. VERCEL SECURITY HEADERS ───────────────────────────────────────────────
_head "1. Vercel Security Headers (vercel.json)"

check_header() {
  local key="$1" label="$2"
  if grep -q "$key" vercel.json 2>/dev/null; then
    _pass "$label present"
  else
    _fail "$label MISSING — add to vercel.json"
  fi
}

check_header "X-Frame-Options"              "X-Frame-Options (clickjacking)"
check_header "Content-Security-Policy"      "Content-Security-Policy"
check_header "Strict-Transport-Security"    "HSTS"
check_header "X-Content-Type-Options"       "X-Content-Type-Options"
check_header "Referrer-Policy"              "Referrer-Policy"
check_header "Permissions-Policy"           "Permissions-Policy"

# ─── 2. EXPOSED INTERNAL PAGES ────────────────────────────────────────────────
_head "2. Exposed Internal / Sensitive Pages"

INTERNAL_PAGES=$(ls _*.html 2>/dev/null || true)
if [ -n "$INTERNAL_PAGES" ]; then
  for f in $INTERNAL_PAGES; do
    _fail "Internal page publicly accessible: $f — add to vercel.json rewrites with auth or move outside web root"
  done
else
  _pass "No _prefixed internal pages found"
fi

# ─── 3. SECRETS IN HTML SOURCE ────────────────────────────────────────────────
_head "3. Secrets / API Keys in HTML Source"

SECRET_HITS=$(grep -rn "api_key\s*=\|apikey\s*=\|secret\s*=\|password\s*=\|bearer\s\|sk-ant\|sk-proj\|AIza" \
  $HTML_FILES 2>/dev/null | grep -v "<!--" || true)
if [ -n "$SECRET_HITS" ]; then
  echo "$SECRET_HITS" | head -10
  _fail "Potential secrets found in HTML (see above)"
else
  _pass "No hardcoded secrets detected"
fi

# ─── 4. SUBRESOURCE INTEGRITY (SRI) ───────────────────────────────────────────
_head "4. Subresource Integrity (SRI) for CDN Resources"

CDN_NO_SRI=$(grep -rn 'src="https://\|href="https://' $HTML_FILES 2>/dev/null \
  | grep -v 'integrity=' | grep -E 'cdn|fonts\.google|cdnjs|jsdelivr|unpkg' || true)
if [ -n "$CDN_NO_SRI" ]; then
  echo "$CDN_NO_SRI" | head -10
  _warn "CDN resources loaded without SRI integrity= attribute (supply-chain risk)"
else
  _pass "All CDN resources have SRI or no external CDNs used"
fi

SRI_COUNT=$(grep -rn 'integrity=' $HTML_FILES 2>/dev/null | wc -l | tr -d ' ')
echo "  (SRI tags found: ${SRI_COUNT:-0})"

# ─── 5. HTML COMMENTS WITH SENSITIVE INFO ─────────────────────────────────────
_head "5. HTML Comments — Sensitive Information"

SENSITIVE_COMMENTS=$(grep -rn "<!--" $HTML_FILES 2>/dev/null \
  | grep -iE "password|secret|key|token|ssn|dob|patient|internal|private|todo|fixme|hack" || true)
if [ -n "$SENSITIVE_COMMENTS" ]; then
  echo "$SENSITIVE_COMMENTS" | head -10
  _warn "HTML comments may contain sensitive info (review manually)"
else
  _pass "No obviously sensitive HTML comments"
fi

# ─── 6. DEV ARTIFACTS ─────────────────────────────────────────────────────────
_head "6. Dev Artifacts"

for pattern in "console\.log" "console\.error" "console\.warn" "debugger;" "alert(" "TODO" "FIXME" "localhost" "127\.0\.0\.1"; do
  HITS=$(grep -rn "$pattern" $HTML_FILES 2>/dev/null | grep -v "_internal\|\.min\." | wc -l | tr -d ' ')
  if [ "${HITS:-0}" -gt 0 ]; then
    _warn "'$pattern' found in $HITS location(s)"
  else
    _pass "No '$pattern' in production pages"
  fi
done

# ─── 7. localStorage / sessionStorage USAGE ───────────────────────────────────
_head "7. Browser Storage (HIPAA — no PHI in localStorage/sessionStorage)"

STORAGE_HITS=$(grep -rn "localStorage\|sessionStorage" $HTML_FILES 2>/dev/null || true)
if [ -n "$STORAGE_HITS" ]; then
  echo "$STORAGE_HITS" | head -10
  _warn "localStorage/sessionStorage usage found — ensure no PHI is stored"
else
  _pass "No localStorage/sessionStorage usage"
fi

# ─── 8. PHI IN URLS / QUERY STRINGS ──────────────────────────────────────────
_head "8. PHI in URLs / Query Strings (HIPAA)"

PHI_URL=$(grep -rn 'href.*?\|action.*?\|src.*?' $HTML_FILES 2>/dev/null \
  | grep -iE 'patient|ssn|dob|name=|email=|mrn=' || true)
if [ -n "$PHI_URL" ]; then
  echo "$PHI_URL" | head -10
  _fail "Potential PHI in URL parameters — PHI must never appear in URLs"
else
  _pass "No PHI detected in URL parameters"
fi

# ─── 9. THIRD-PARTY SCRIPTS (BAA RISK) ────────────────────────────────────────
_head "9. Third-Party Scripts (HIPAA BAA Risk)"

THIRD_PARTY=$(grep -rn '<script.*src="https://' $HTML_FILES 2>/dev/null \
  | grep -v "cdn.jsdelivr\|cdnjs.cloudflare\|fonts.googleapis" || true)
if [ -n "$THIRD_PARTY" ]; then
  echo "$THIRD_PARTY" | head -10
  _warn "Third-party scripts present — verify BAA coverage for any handling PHI"
else
  _pass "No unexpected third-party scripts (known CDNs only)"
fi

# ─── 10. FORM SECURITY ────────────────────────────────────────────────────────
_head "10. Form Security"

FORMS=$(grep -rn '<form' $HTML_FILES 2>/dev/null || true)
if [ -n "$FORMS" ]; then
  echo "$FORMS" | head -5
  _warn "Forms present — ensure CSRF protection when backend is added"
  # Check for method=GET on forms (bad for any sensitive data)
  GET_FORMS=$(echo "$FORMS" | grep -i 'method.*get\|method="get"' || true)
  if [ -n "$GET_FORMS" ]; then
    _fail "Forms using GET method — PHI could leak into server/proxy logs"
  fi
else
  _pass "No HTML forms detected in static pages"
fi

# ─── SUMMARY ──────────────────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════"
echo "  ARDIA SECURITY AUDIT SUMMARY"
echo "════════════════════════════════════════"
echo "  PASS: $PASS"
echo "  WARN: $WARN"
echo "  FAIL: $FAIL"
echo

if [ "$FAIL" -gt 0 ]; then
  echo "  VERDICT: BLOCKED — $FAIL critical issue(s) must be fixed before deploy"
  exit 1
elif [ "$WARN" -gt 0 ]; then
  echo "  VERDICT: CONDITIONAL — $WARN warning(s) require review"
  exit 0
else
  echo "  VERDICT: APPROVED — all checks passed"
  exit 0
fi

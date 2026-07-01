# Security Rules — ARDIA PRECISION HEALTH

These rules apply to ALL code in this repository.

## Mandatory Checks Before Every Commit

1. **No hardcoded secrets** — API keys, tokens, passwords must be in environment variables
2. **No PHI in logs** — Patient names, SSNs, DOBs, diagnoses must never appear in log output
3. **No SQL concatenation** — All queries must use parameterized statements
4. **No XSS vectors** — All user-provided content must be sanitized before rendering
5. **No unvalidated input** — All external inputs validated with Pydantic/Zod schemas
6. **No localStorage for tokens** — Auth tokens must use httpOnly cookies
7. **No verbose errors to client** — Stack traces and internal details stay server-side
8. **No direct PHI in AI prompts** — De-identify patient data before sending to Claude API

## When You Find a Security Issue

1. **Stop current work**
2. **Invoke the `security-reviewer` agent**
3. **Fix CRITICAL and HIGH issues before continuing**
4. **Scan the rest of the codebase** for the same pattern

## HIPAA Requirements (Non-Negotiable)

- Every PHI access must generate an audit log entry
- PHI fields must be encrypted at rest (AES-256)
- All PHI transmitted via TLS 1.3+
- Access follows minimum necessary principle
- Business Associate Agreements (BAA) required for all vendors touching PHI

## Secret Management

Always use:
```python
api_key = os.environ["ANTHROPIC_API_KEY"]  # raises KeyError if missing
```

Never use:
```python
api_key = os.environ.get("ANTHROPIC_API_KEY", "sk-ant-fallback")  # dangerous default
```

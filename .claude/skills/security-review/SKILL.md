---
name: security-review
description: Run a full HIPAA + OWASP security audit on changed files. Invoke before any PR or deployment, after adding auth/PHI handling, or when asked to check security.
---

Run a complete security review of the current changes. Delegate to the `security-reviewer` agent and produce a prioritized findings report.

## Trigger Conditions

Automatically invoke this skill when:
- Implementing authentication or authorization
- Adding any endpoint that touches PHI (patient data, medical records, diagnoses)
- Integrating third-party APIs (payment, EHR, lab systems)
- Creating file upload handlers
- Working with environment variables or secrets
- Before any production deployment

## Review Scope

1. **HIPAA Compliance**
   - PHI never logged or exposed in error messages
   - Audit trail for every PHI access (who/what/when/where/why)
   - Minimum necessary access enforced
   - Column-level encryption for PHI fields
   - BAA requirements met for third-party services

2. **OWASP Top 10**
   - Injection (SQL, command, LDAP)
   - Broken authentication
   - Sensitive data exposure
   - XML External Entities
   - Broken access control
   - Security misconfiguration
   - XSS
   - Insecure deserialization
   - Using components with known vulnerabilities
   - Insufficient logging & monitoring

3. **Secrets & Config**
   - No hardcoded API keys, tokens, or passwords
   - `.env` files in `.gitignore`
   - Production secrets in platform environment (Vercel/AWS)

4. **Input Validation**
   - All user inputs validated with schemas (Zod / Pydantic)
   - File uploads restricted by type, size, extension
   - No raw user input in database queries

## Output Format

Produce a report with:

```
## Security Review Report
Date: [date]
Files Reviewed: [list]

### CRITICAL Issues (block deployment)
[findings]

### HIGH Issues (fix before merge)
[findings]

### MEDIUM Issues (fix within sprint)
[findings]

### LOW Issues (fix in next release)
[findings]

### HIPAA Compliance Status
[ ] PHI audit logging implemented
[ ] Minimum necessary access enforced
[ ] Encryption at rest verified
[ ] Encryption in transit verified

### Verdict
APPROVED / BLOCKED — [reason]
```

## Healthcare-Specific Notes

This platform will be subject to HIPAA audit. Every PHI exposure is a potential $100–$50,000 fine per violation. Treat security findings with the same urgency as clinical accuracy.

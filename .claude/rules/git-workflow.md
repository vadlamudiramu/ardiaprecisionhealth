# Git Workflow — ARDIA PRECISION HEALTH

## Branch Strategy

- `main` — production (auto-deploys to Vercel on push)
- `claude/loving-goldberg-ualodr` — Claude Code development branch
- Feature branches: `feature/[description]`

## Commit Messages

Format: `[type]: [what changed and why]`

Types:
- `feat:` — new feature or page
- `fix:` — bug fix
- `style:` — CSS/branding changes
- `refactor:` — code restructure (no behavior change)
- `security:` — security fix
- `docs:` — documentation only

Examples:
```
feat: add investor CRM dashboard with lead tracking
fix: restore ardia-profile.html (accidentally pushed empty)
style: apply teal-to-amber gradient underline to all 20 nav bars
security: add HIPAA audit logging to patient data endpoints
```

## Pushing Rules

1. **Never force-push to main** without explicit user approval
2. **Verify file size before pushing** — `wc -c filename.html` should be >5000 bytes
3. **Large files (>30KB) must be pushed from main context** using `mcp__github__push_files`
4. **Never push empty files** — double-check content exists before calling push tool
5. **Always set git author** before committing: `git config user.email noreply@anthropic.com`

## Pre-Push Checklist

- [ ] Files are not empty (wc -c check)
- [ ] Branding is consistent with all 20 pages
- [ ] No secrets or dev artifacts in HTML files
- [ ] Commit message follows format above
- [ ] git config user.email is noreply@anthropic.com

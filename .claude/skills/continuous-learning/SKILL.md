---
name: continuous-learning
description: Extract and save reusable patterns from ARDIA PRECISION HEALTH sessions. Runs at session end to capture project-specific conventions, bug patterns, and workflow improvements.
---

At the end of each productive session, extract patterns worth remembering for future sessions.

## Patterns to Capture

| Type | Description | Example |
|------|-------------|---------|
| `bug_pattern` | Recurring mistakes and their fixes | "Agents can't push >30KB files — always push from main context" |
| `css_convention` | Project-specific CSS patterns | "All 20 pages use inline styles — no shared stylesheet" |
| `hipaa_reminder` | Compliance rules discovered in practice | "PHI audit logs must be written before data is retrieved" |
| `git_workflow` | Git patterns specific to this repo | "MCP push_files is the only way to push from remote session" |
| `tool_limitation` | Known tool constraints | "mcp__github__get_file_contents times out on files >50KB" |
| `branding_rule` | Design decisions | "ardia-profile.html uses .nav-brand-icon not .logo-icon" |

## Session Evaluation

After a session with 10+ messages, review:

1. Were there any errors that required multiple attempts?
2. Did the user correct any approach or output?
3. Were there workarounds for tool limitations?
4. Were any project conventions clarified?
5. Were HIPAA or security issues discovered?

## Output Format

Save insights to CLAUDE.md under a `## Learned Patterns` section:

```markdown
## Learned Patterns

### [Date] — [Session Topic]
- **[pattern_type]**: [What was learned] — [Why it matters]
```

## Current Known Patterns (bootstrap)

- **tool_limitation**: Agents hit 32K output token limit when returning large file contents — always use `mcp__github__push_files` from main context for files >30KB
- **css_convention**: No shared stylesheet — all CSS is inline per-file `<style>` blocks; changes require editing each of 20 HTML files individually
- **branding_rule**: `ardia-profile.html` uses `.nav-brand-icon` CSS class; `mobile-app.html` uses `.logo-mark`; all other 16 pages use `.logo-icon`
- **git_workflow**: Development branch is `claude/loving-goldberg-ualodr`; production is `main` (auto-deploys to Vercel)
- **bug_pattern**: Accidental empty file push happened once — always verify `wc -c` on files before pushing

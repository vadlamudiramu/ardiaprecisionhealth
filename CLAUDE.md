# ARDIA PRECISION HEALTH — Claude Code Project Guide

## Project Overview

ARDIA PRECISION HEALTH is a next-generation AI healthcare infrastructure platform. The codebase is a static HTML/CSS website (20 pages) deployed via Vercel. Future development includes backend APIs, a mobile app, and AI-powered clinical decision support.

## Repository

- **Repo**: `vadlamudiramu/ardiaprecisionhealth`
- **Branch**: `claude/loving-goldberg-ualodr` (development), `main` (production)
- **Deployed via**: Vercel (auto-deploy on push to main)

## Tech Stack

- **Frontend**: Static HTML5 + inline CSS (no shared stylesheet — all styles are per-file `<style>` blocks)
- **Assets**: `Ardia_Logo.png` (1344×768 RGBA PNG, transparent background), `favicon.svg`, `logo.svg`
- **Future**: Next.js / FastAPI backend, Claude API integration, PostgreSQL, Redis

## Branding Standards

### Logo / Navbar (applied across all 20 pages)
- `.logo-icon`: dark navy box — `background:linear-gradient(135deg,#0a1628,#0e2040)`, `border:1.5px solid rgba(20,184,166,0.5)`, `box-shadow:0 0 12px rgba(20,184,166,0.25)`, `52×52px`, `border-radius:10px`, `padding:6px`
- "ARDIA" in `var(--navy)` (dark navy), "PRECISION HEALTH" in `#1d9bd1` (light blue)
- Gradient underline: `linear-gradient(to right,#14b8a6,#f59e0b)` (teal → amber), `height:2px`
- Tagline: "Next-Generation Intelligence for Healthcare Infrastructure." in `#5a6e87`, normal-case, 10px

### Brand Colors
- Navy: `#0a1628`
- Teal: `#14b8a6` / `rgba(20,184,166,...)`
- Blue: `#1d9bd1`
- Amber: `#f59e0b`
- Gray: `#5a6e87`

## File Map (20 HTML pages)
- `index.html` — Homepage
- `about.html` — About Ardia
- `architecture.html` — Technical architecture
- `ardia-profile.html` — Company profile (uses `.nav-brand-icon` CSS class)
- `case-studies.html` — Clinical case studies
- `contact.html` — Contact page
- `dashboard.html` — Analytics dashboard
- `how-it-works.html` — How the platform works
- `how-software-works.html` — Technical deep-dive
- `investors.html` — Investor relations
- `mobile-app.html` — Mobile app page (uses `.logo-mark` CSS class)
- `our-product.html` — Product overview
- `pama.html` — PAMA compliance
- `plg-sandbox.html` — PLG sandbox
- `precision-medicine.html` — Precision medicine
- `research.html` — Research & publications
- `roadmap.html` — Product roadmap
- `security.html` — Security & compliance
- `solutions.html` — Solutions
- `vision.html` — Company vision

## Development Rules

1. **Never push empty files** — always verify file content before pushing via `mcp__github__push_files`
2. **Large files (>30KB) must be pushed directly from main context** — agents hit 32K output token limit
3. **CSS changes require per-file edits** — no shared stylesheet exists
4. **All 20 pages must maintain consistent navbar branding** per standards above

## Healthcare Compliance (HIPAA)

This platform will handle Protected Health Information (PHI). All future backend code must:
- Encrypt PHI at rest (AES-256) and in transit (TLS 1.3)
- Implement audit logging for all PHI access
- Use role-based access control (RBAC)
- Never log PHI to console or error messages
- Follow minimum necessary access principle

## Active Skills

- `/security-review` — HIPAA + OWASP security audit
- `/verify` — Build verification loop
- `/code-review` — Code quality review
- `/deep-research` — Multi-source research synthesis

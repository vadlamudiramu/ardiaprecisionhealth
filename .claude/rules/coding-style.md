# Coding Style — ARDIA PRECISION HEALTH

## HTML/CSS (Current Static Site)

- **No shared stylesheet** — all styles are inline `<style>` blocks per file
- **Branding variables** — always use the exact brand colors (never approximate):
  - Navy: `#0a1628`
  - Teal: `#14b8a6`
  - Blue (Precision Health): `#1d9bd1`
  - Amber: `#f59e0b`
  - Gray (tagline): `#5a6e87`
- **Logo box** — `.logo-icon` always: 52×52px, dark navy gradient, teal border, 6px padding
- **Gradient underline** — always 2px, `linear-gradient(to right,#14b8a6,#f59e0b)`
- **Tagline** — always normal-case (not uppercase), 10px, `#5a6e87`
- **Font** — Sora for brand text, system-ui for body

## Python (Future Backend)

- Type hints on all function signatures
- Pydantic models for all API request/response schemas
- Async/await for all I/O operations
- No bare `except:` — always catch specific exceptions
- Docstrings only where the WHY is non-obvious

## TypeScript/Next.js (Future Frontend)

- Strict mode enabled
- Zod schemas for all external inputs
- No `any` type — use `unknown` and narrow properly
- Components: function declarations, not arrow functions
- CSS: Tailwind utility classes preferred over custom CSS

## General Rules

- No TODO/FIXME comments in committed code — open a GitHub issue instead
- No `console.log` in production code — use structured logger
- No dead code — remove unused functions, variables, imports
- Comments explain WHY, not WHAT — code should be self-documenting

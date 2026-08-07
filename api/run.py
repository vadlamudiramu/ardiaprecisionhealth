"""Vercel serverless function: POST /api/run — the public Studio engine.

Same-origin endpoint so the deployed Studio page (ardiahealthlabs.com/studio) can
reach it under the site's `default-src 'self'` CSP with no mixed-content problem.

It reuses the EXACT tested pipeline from ardia-studio-app/server.py:
  Sentinel de-identify (before any model sees the text)
    -> live PubMed / ClinicalTrials.gov grounding (cite-or-abstain)
      -> the model (Gemini or Claude, key read from a Vercel env var)
        -> Crucible guardrail gates on the output.

Deps are pure stdlib + the repo's own `models/` (regex + pure functions), so this
function needs no pip packages.

REQUIRED for live answers (set in the Vercel project → Settings → Environment Variables):
  GEMINI_API_KEY=...        (free: aistudio.google.com/app/apikey)   -- or --
  ANTHROPIC_API_KEY=sk-ant-...
OPTIONAL gate (recommended so the endpoint isn't open to the whole internet):
  ARDIA_DEMO_CODE=some-shared-code   -> callers must send {"code": "..."} to run.

Until a key is set, the function returns {"error":"no_key"} and the Studio page shows
its honest "engine offline" state — it never fabricates an answer.

Note: this is a SYNTHETIC-CASE DEMO. Do not send real PHI: the model providers are
third parties and require a signed BAA before any real patient data.
"""
import hmac
import json
import os
import pathlib
import sys
from http.server import BaseHTTPRequestHandler

# Make the repo root and the studio-app package importable from the serverless bundle.
_ROOT = pathlib.Path(__file__).resolve().parents[1]
for _p in (str(_ROOT), str(_ROOT / "ardia-studio-app")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

MAX_INPUT = 6000  # hard input cap for a public endpoint
_ALLOWED_ORIGIN = os.environ.get("ARDIA_ALLOWED_ORIGIN", "https://www.ardiahealthlabs.com")


def _run(body):
    """Run the tested engine pipeline. Returns (json_obj, http_code)."""
    # Optional shared-code gate: if ARDIA_DEMO_CODE is set on the server, require it.
    # Constant-time compare to avoid a timing side-channel on the code.
    gate = os.environ.get("ARDIA_DEMO_CODE")
    code_ok = (not gate) or hmac.compare_digest(str(body.get("code") or ""), str(gate))
    if gate and not code_ok:
        return {"error": "forbidden", "message": "This demo endpoint requires an access code."}, 403

    text = (body.get("text") or "").strip()[:MAX_INPUT]
    atts = body.get("attachments") or []
    if not text and not atts:
        return {"error": "bad_request", "message": "Enter a case or attach a file."}, 400

    import server as engine  # ardia-studio-app/server.py — reuses call_model as-is
    # Public endpoint: file uploads require the operator opt-in (a BAA / gated synthetic
    # demo) AND a configured + matched access code — so anonymous internet clients can
    # never POST raw binary (image/PDF/DICOM) to a non-BAA third-party model.
    uploads_enabled = os.environ.get("ARDIA_ALLOW_UPLOADS") == "1" or os.environ.get("ARDIA_BAA_VERIFIED") == "1"
    attachments_ok = uploads_enabled and bool(gate) and code_ok
    res = engine.call_model(
        body.get("model", "tara"), text, atts,
        body.get("engine", ""), body.get("ground", True),
        attest=bool(body.get("attest_synthetic")), attachments_ok=attachments_ok,
    )
    if not isinstance(res, dict):
        return {"error": "server", "message": "Unexpected engine response."}, 502
    code = 200 if ("text" in res) else (400 if res.get("error") in (
        "no_key", "bad_model", "bad_request", "attest_required", "uploads_disabled",
        "guard_unavailable", "kernel_unavailable") else 502)
    return res, code


class handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass   # never emit per-request logs (client IP / path) — keep the endpoint PHI-safe

    def _send(self, obj, code=200):
        b = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", _ALLOWED_ORIGIN)
        self.send_header("Vary", "Origin")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", _ALLOWED_ORIGIN)
        self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.end_headers()

    def do_GET(self):
        # health check
        provider = None
        if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
            provider = "gemini"
        elif os.environ.get("ANTHROPIC_API_KEY"):
            provider = "anthropic"
        self._send({"ok": True, "provider": provider, "gated": bool(os.environ.get("ARDIA_DEMO_CODE"))})

    def do_POST(self):
        try:
            n = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
        except Exception:
            return self._send({"error": "bad_request", "message": "Invalid JSON."}, 400)
        try:
            res, code = _run(body)
        except Exception:
            # never leak internals; the page degrades to its honest "engine offline" state
            return self._send({"error": "server", "message": "Engine error — check the function logs."}, 500)
        self._send(res, code)

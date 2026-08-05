#!/usr/bin/env python3
"""
Ardia Studio — real-time model server (zero dependencies, Python 3.8+).

Every response is generated live by a real model from the user's own text +
uploaded image/report. Nothing is hard-coded.

Supports TWO providers — pick whichever key you have (Gemini is checked first):
  • Google Gemini   ->  export GEMINI_API_KEY=...      (free key: aistudio.google.com/app/apikey)
  • Anthropic Claude->  export ANTHROPIC_API_KEY=sk-ant-...

Security: the key is read from the environment (never stored in the page, never logged).
Run:  python3 server.py   then open  http://localhost:8787
"""
import os, json, http.server, socketserver, pathlib, sys, urllib.request, urllib.error

HERE = pathlib.Path(__file__).parent

def _load_dotenv():
    """Read KEY=VALUE lines from a .env file next to this script so the key survives restarts
    (env vars already set always win; the file never overrides them)."""
    p = HERE / ".env"
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v
_load_dotenv()

PORT = int(os.environ.get("ARDIA_PORT", "8787"))
CLAUDE_MODEL = os.environ.get("ARDIA_MODEL", "claude-sonnet-5")
GEMINI_MODEL = os.environ.get("ARDIA_GEMINI_MODEL", "gemini-2.0-flash")

# ---- Hard safety guardrail applied to EVERY model (non-negotiable) ----
GUARDRAIL = """You are Ardia, an AI health assistant — you are NOT a doctor and you do NOT diagnose.
Absolute rules, in priority order:
1. SAFETY FIRST. If the input describes any possible emergency — chest pain or pressure, trouble breathing,
   fainting, sudden weakness/numbness, slurred speech, the "worst headache of my life", severe bleeding,
   thoughts of self-harm — your FIRST sentence must tell the person to call 911 / emergency services now.
   Never downplay or delay these.
2. BE GENUINELY, FULLY USEFUL — do not hedge into uselessness. When given a report/image/symptoms:
   - Flag what STANDS OUT (out-of-range, abnormal, concerning) and name the likely POSSIBILITIES in plain
     language (as possibilities to confirm with a clinician — never a confirmed diagnosis).
   - Explain WHAT CAN BE DONE: sensible next steps, self-care that is safe, lifestyle measures, and the KINDS of
     treatment or medication commonly used for such situations — describe them by category/approach (e.g. "often
     managed with a class of medicine called ...") while making clear the clinician chooses and prescribes the
     specific drug and dose.
   - Say WHAT CANNOT be told from the input and what only an in-person clinician can decide.
   - Give urgency: how soon to seek care, and when to call 911.
   You never state a diagnosis as fact, give a specific drug + dose as an instruction, or write a treatment order.
   The clinician makes the final call and writes any prescription.
3. Do NOT invent specific findings you cannot actually see or verify. If you cannot read an attached file or a
   value confidently, say so plainly instead of guessing. Ground every flag in what is actually there.
4. Recommend consulting a licensed clinician for anything that matters.
5. Keep it warm, clear, and concise. Use short markdown sections with '## ' headings and '- ' bullets.
6. End EVERY response with exactly this line on its own:
   *Not a diagnosis — talk to a licensed clinician. In an emergency, call 911.*
"""

MODELS = {
 "lumen": {"name": "Lumen", "role": "Report & Scan Explainer", "system": """You are Lumen, Ardia's report & scan explainer. Explain like an experienced, thorough clinician walking a patient through their results — specific and substantive, never generic or padded. The user may paste report text or attach ONE OR MORE images/PDFs (labs, MRI/X-ray/CT, discharge summaries). Read them ALL, together.
Write these sections with real depth, and FINISH every section (never trail off):
- '## What stands out' — for EACH abnormal or notable finding give: (a) what it is in plain language; (b) the likely POSSIBILITIES / causes (as possibilities to confirm with a clinician, NOT a diagnosis); (c) what is typically DONE about it — the specific follow-up tests, the lifestyle measures, and the CLASS of medication commonly used with a common example (e.g. "a statin such as atorvastatin", "a biguanide such as metformin"), always making clear the clinician chooses and prescribes the specific drug and dose; (d) red flags that mean seek care sooner; and (e) how soon to follow up.
- '## What can be done' — a concrete, prioritised action list: what to do now, what to ask for, what is safely self-managed vs what needs the clinician, and what CANNOT be determined from this input alone.
- '## Plain-language summary' — 2-3 sentences on what the document(s) say overall.
- '## Terms' — define the key jargon simply.
- '## Questions for your clinician' — specific, high-yield questions.
If you cannot read a value or impression confidently, say so instead of guessing. Never give a definitive diagnosis, a specific dose as an instruction, or a treatment order — the clinician decides and prescribes. When several files are attached, reason across them (e.g. compare a prior vs a current report)."""},
 "aria": {"name": "Aria", "role": "Elder Companion", "system": """You are Aria, Ardia's voice-first companion for older adults.
Be warm, patient, and reassuring, in plain short sentences. FIRST, silently run a safety red-flag check and act
on rule 1 if needed. Then give gentle, practical guidance. Offer to remind about medications and to notify the
listed emergency contact. Never name a disease and never tell them to start/stop/change a medication."""},
 "molec": {"name": "MolecuIQ", "role": "Lab Denial Recovery (administrative)", "system": """You are MolecuIQ, Ardia's
molecular/toxicology denial-recovery assistant. This is ADMINISTRATIVE revenue-cycle work, not clinical care.
The user may paste/attach a denial letter / EOB / claim. Classify the denial and root cause; if appealable,
outline a cited appeal (name the relevant guideline/policy at a high level; do NOT fabricate exact citation IDs
— say 'verify against the payer LCD/NCD'). HONESTY GATE: if the record does not support the service (e.g.,
comprehensive tumour profiling on a benign nodule with no cancer diagnosis), REFUSE to appeal and say why."""},
 "cadence": {"name": "Cadence", "role": "Movement & Wellbeing", "system": """You are Cadence, Ardia's movement & wellbeing
assistant. The user describes a day/week of activity or pastes step/activity data. Summarise the pattern and flag
whether there is a reviewable functional-decline TREND. Be explicit about honest limits: the trained model was
validated on adults aged 19-48 (public UCI HAR data) and re-validated on the target cohort before clinical use;
it is non-diagnostic and NOT a fall detector. Signals prompt a human review; they never name a disease."""},
 "tara": {"name": "TARA", "role": "Clinical Reasoning core", "system": """You are TARA, Ardia's reasoning core, answering
clinical/coding questions for professionals. Give the answer, then a short '## How I got there' section naming the
rule/guideline each step relies on, so it is auditable. Flag that codes/thresholds change and must be verified
against current CMS/payer policy. Educational reference, not advice for a specific patient."""},
}

NO_KEY = {"error": "no_key", "message":
          "No model key found. Use EITHER a free Google Gemini key OR an Anthropic key, then restart the server:\n"
          "  • Free (Google): make a key at aistudio.google.com/app/apikey  ->  export GEMINI_API_KEY=...\n"
          "  • Anthropic:  export ANTHROPIC_API_KEY=sk-ant-...\n"
          "Then:  python3 server.py"}


def active_provider():
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        return "gemini"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    return None


def active_model_id():
    p = active_provider()
    return GEMINI_MODEL if p == "gemini" else (CLAUDE_MODEL if p == "anthropic" else None)


def _post(url, headers, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=90) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _http_err(e):
    body = e.read().decode("utf-8", "replace")
    try:
        detail = json.loads(body).get("error", {}).get("message", body)
    except Exception:
        detail = body
    return {"error": "api_error", "status": e.code, "message": detail}


_GEMINI_CUR = {"model": None}

def _gemini_list(key):
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models",
                                 headers={"x-goog-api-key": key}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    return [m.get("name", "").replace("models/", "") for m in data.get("models", [])
            if "generateContent" in m.get("supportedGenerationMethods", [])]

def _pick_gemini(models):
    import re
    bad = ("vision", "tts", "image", "embedding", "aqa", "learnlm", "gemma", "exp")
    cand = [m for m in models if not any(b in m for b in bad)]
    flash = [m for m in cand if "flash" in m and "thinking" not in m]
    pool = flash or cand
    lat = [m for m in pool if m.endswith("-latest")]
    if lat:
        return lat[0]
    def ver(m):
        ns = re.findall(r"\d+\.?\d*", m)
        return [float(x) for x in ns] or [0.0]
    pool.sort(key=ver, reverse=True)
    return pool[0] if pool else None

def resolve_gemini_model(key):
    """Pick a model the key can actually use, so we never hard-code a retired id."""
    if _GEMINI_CUR["model"]:
        return _GEMINI_CUR["model"]
    try:
        models = _gemini_list(key)
    except Exception:
        models = []
    if GEMINI_MODEL in models:               # honour an explicit choice only if it's really available
        _GEMINI_CUR["model"] = GEMINI_MODEL
    else:
        _GEMINI_CUR["model"] = _pick_gemini(models) or GEMINI_MODEL
    return _GEMINI_CUR["model"]

def call_gemini(model_key, text, attachments, engine=""):
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    m = MODELS[model_key]
    parts = []
    for a in (attachments or []):
        if a.get("b64") and a.get("media_type"):
            parts.append({"inline_data": {"mime_type": a["media_type"], "data": a["b64"]}})
    parts.append({"text": text or "(No text provided — please analyse the attached file(s).)"})
    payload = {
        "systemInstruction": {"parts": [{"text": GUARDRAIL + "\n\n---\n" + m["system"]}]},
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.4},
    }
    try:
        avail = set(_gemini_list(key))
    except Exception:
        avail = set()
    if engine == "deep":   # Deep thinking → prefer Pro models first
        order = ["gemini-pro-latest", "gemini-2.5-pro", "gemini-flash-latest",
                 "gemini-2.5-flash-lite", "gemini-2.0-flash-001", "gemini-2.5-flash"]
    else:                  # Ultrafast → Flash models
        order = ["gemini-flash-latest", "gemini-2.5-flash-lite", "gemini-2.0-flash-lite",
                 "gemini-2.0-flash-001", "gemini-flash-lite-latest", "gemini-2.5-flash",
                 "gemini-pro-latest", "gemini-2.5-pro"]
    cand = [x for x in order if (not avail or x in avail)] or ["gemini-flash-latest"]
    ekey = "deep" if engine == "deep" else "fast"
    prev = _GEMINI_CUR.get(ekey)
    if prev and prev in cand:                                      # stick with one that worked before (per mode)
        cand = [prev] + [x for x in cand if x != prev]
    last = None
    for use_model in cand:                                         # try each until one actually answers
        url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % use_model
        try:
            data = _post(url, {"x-goog-api-key": key, "content-type": "application/json"}, payload)
            cands = data.get("candidates", [])
            if not cands:
                last = {"error": "api_error", "message": "No text returned (possible safety block)."}
                continue
            out = "".join(p.get("text", "") for p in cands[0].get("content", {}).get("parts", []))
            _GEMINI_CUR[ekey] = use_model
            return {"text": out, "model_id": use_model, "provider": "gemini"}
        except urllib.error.HTTPError as e:
            last = _http_err(e); last["tried_model"] = use_model
            continue
        except Exception as e:
            last = {"error": "network", "message": str(e)}
            break
    return last or {"error": "api_error", "message": "No Gemini model could be reached."}


def call_anthropic(model_key, text, attachments, engine=""):
    key = os.environ.get("ANTHROPIC_API_KEY")
    m = MODELS[model_key]
    claude_id = engine if (engine or "").startswith("claude") else CLAUDE_MODEL
    content = []
    for a in (attachments or []):
        mt = a.get("media_type"); b = a.get("b64")
        if not (b and mt):
            continue
        if mt == "application/pdf":
            content.append({"type": "document", "source": {"type": "base64", "media_type": mt, "data": b}})
        elif mt.startswith("image/"):
            content.append({"type": "image", "source": {"type": "base64", "media_type": mt, "data": b}})
    content.append({"type": "text", "text": text or "(No text provided — please analyse the attached file(s).)"})
    payload = {"model": claude_id, "max_tokens": 4096,
               "system": GUARDRAIL + "\n\n---\n" + m["system"],
               "messages": [{"role": "user", "content": content}]}
    try:
        data = _post("https://api.anthropic.com/v1/messages",
                     {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"}, payload)
        out = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
        return {"text": out, "model_id": data.get("model", claude_id), "provider": "anthropic"}
    except urllib.error.HTTPError as e:
        return _http_err(e)
    except Exception as e:
        return {"error": "network", "message": str(e)}


# ---- Real guardrails + research grounding ----
try:
    from guardrails import deid_input, gate_output, summarize
    _GUARDS_OK = True
except Exception:
    _GUARDS_OK = False
try:
    from research import gather_sources, grounding_block
    _RESEARCH_OK = True
except Exception:
    _RESEARCH_OK = False


def call_model(model_key, text, attachments, engine="", ground=True):
    if model_key not in MODELS:
        return {"error": "bad_model", "message": "Unknown model."}
    p = active_provider()
    if p is None:
        return NO_KEY
    # Sentinel: strip HIPAA Safe-Harbor identifiers from the text BEFORE the model sees it.
    sentinel = None
    if _GUARDS_OK:
        text, sentinel = deid_input(text)
    # Research grounding: retrieve real PubMed / ClinicalTrials sources from the
    # de-identified query and give them to the model to cite (best-effort).
    sources = []
    if ground and _RESEARCH_OK and text:
        sources = gather_sources(text, n=3)
        if sources:
            text = text + grounding_block(sources)
    if p == "gemini":
        res = call_gemini(model_key, text, attachments, engine)
    elif p == "anthropic":
        res = call_anthropic(model_key, text, attachments, engine)
    else:
        res = NO_KEY
    if isinstance(res, dict) and "text" in res:
        # Crucible: run the guardrail gates on the model OUTPUT and attach verdicts.
        if _GUARDS_OK:
            res["sentinel"] = sentinel
            res["crucible"] = gate_output(res["text"])
            res["crucible_summary"] = summarize(res["crucible"])
        res["sources"] = sources
    return res


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(HERE), **k)

    def log_message(self, *a):
        pass  # keep console quiet & PHI-free

    def _json(self, obj, code=200):
        b = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Access-Control-Allow-Origin", "*")  # allow the website Studio page to call the local engine
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        # CORS preflight for cross-origin /api/run calls from the marketing Studio page
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.end_headers()

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.path = "/index.html"
        if self.path == "/api/health":
            return self._json({"ok": True, "provider": active_provider(), "model": active_model_id(),
                               "key_set": active_provider() is not None,
                               "models": [{"k": k, "name": v["name"], "role": v["role"]} for k, v in MODELS.items()]})
        if self.path == "/api/models":   # diagnostic: which Gemini models can this key use?
            key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if not key:
                return self._json({"error": "no_gemini_key"})
            try:
                avail = _gemini_list(key)
                return self._json({"available": avail, "picked": _pick_gemini(avail)})
            except urllib.error.HTTPError as e:
                return self._json(_http_err(e))
            except Exception as e:
                return self._json({"error": "network", "message": str(e)})
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/run":
            return self._json({"error": "not_found"}, 404)
        try:
            n = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(n).decode("utf-8")) if n else {}
        except Exception:
            return self._json({"error": "bad_request", "message": "Invalid JSON."}, 400)
        atts = body.get("attachments") or []
        if not atts and body.get("image_b64"):   # backward compat with single-file clients
            atts = [{"b64": body.get("image_b64"), "media_type": body.get("image_media_type")}]
        res = call_model(body.get("model", "lumen"), (body.get("text") or "").strip(), atts,
                         body.get("engine", ""), body.get("ground", True))
        code = 200 if "text" in res else (400 if res.get("error") in ("no_key", "bad_model", "bad_request") else 502)
        return self._json(res, code)


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    p = active_provider()
    print("\n  Ardia Studio  ·  real-time model server")
    print("  " + "-" * 44)
    if p == "gemini":
        print(f"  provider : Google Gemini   model: {GEMINI_MODEL}   key: set ✓")
    elif p == "anthropic":
        print(f"  provider : Anthropic Claude model: {CLAUDE_MODEL}   key: set ✓")
    else:
        print("  provider : NONE — no key set. Runs will error until you set one:")
        print("             export GEMINI_API_KEY=...        (free: aistudio.google.com/app/apikey)")
        print("             export ANTHROPIC_API_KEY=sk-ant-...")
    print(f"  open  : http://localhost:{PORT}\n")
    try:
        Server(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\n  stopped.\n")
        sys.exit(0)

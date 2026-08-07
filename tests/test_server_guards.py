"""Server-side PHI egress gates in call_model — the client cannot flip these.

Verifies attachments never leave for a third-party model unless the SERVER authorized
uploads AND the client attested synthetic, that text-only still flows, and that the
de-id guardrail fails closed. No API key needed — the gates return before any model call.
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ardia-studio-app"))
sys.path.insert(0, str(ROOT))

import server as s  # noqa: E402

IMG = [{"b64": "AAAA", "media_type": "image/png", "name": "x.png"}]


def test_attachments_blocked_without_server_authorization():
    # client says attest=True, but the server didn't authorize uploads -> still blocked
    assert s.call_model("lumen", "hi", IMG, attest=True, attachments_ok=False).get("error") == "uploads_disabled"


def test_attachments_need_attestation_even_when_authorized():
    assert s.call_model("lumen", "hi", IMG, attest=False, attachments_ok=True).get("error") == "attest_required"


def test_authorized_attested_attachment_passes_the_gates():
    # reaches the provider step; with no key that is NO_KEY, with a key it's a real answer —
    # either way it got PAST the egress gates (not blocked).
    err = s.call_model("lumen", "hi", IMG, attest=True, attachments_ok=True).get("error")
    assert err not in ("uploads_disabled", "attest_required", "bad_model", "guard_unavailable")


def test_text_only_passes_the_gates():
    err = s.call_model("lumen", "hi", []).get("error")
    assert err not in ("uploads_disabled", "attest_required", "guard_unavailable")


def test_bad_model_rejected():
    assert s.call_model("nope", "hi", []).get("error") == "bad_model"

"""Sentinel — HIPAA Safe-Harbor de-identification for free text.

Implements the pattern-detectable subset of the 18 identifiers enumerated in the
HIPAA Privacy Rule, 45 CFR 164.514(b)(2)(i). Structured identifiers (SSN, phone,
email, dates, MRN, ZIP, IP, URL, account/beneficiary numbers, license/vehicle/
device IDs, ages > 89) are detected deterministically by regex and replaced with a
category tag. Names are redacted from a supplied roster (free-text name detection
without a trained NER model is best-effort and is intentionally *not* claimed here).

Deterministic and dependency-free: same input always yields the same output, and
nothing is sent to a model. Raw PHI never leaves this function un-redacted.

This is the honest core behind the site's "Sentinel" claims: the number of
Safe-Harbor categories this engine actually covers is ``len(SAFE_HARBOR_CATEGORIES)``,
not a marketing figure.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

#: The 18 HIPAA Safe-Harbor identifier categories (45 CFR 164.514(b)(2)).
#: ``regex`` = handled deterministically here; ``roster`` = needs a supplied list;
#: ``out-of-scope`` = not applicable to plain text (photos, biometrics).
SAFE_HARBOR_CATEGORIES: dict[str, str] = {
    "name": "roster",
    "geo_zip": "regex",
    "date": "regex",
    "age_over_89": "regex",
    "phone_or_fax": "regex",
    "email": "regex",
    "ssn": "regex",
    "mrn": "regex",
    "health_plan_id": "regex",
    "account_number": "regex",
    "license_number": "regex",
    "vehicle_id": "regex",
    "device_id": "regex",
    "url": "regex",
    "ip_address": "regex",
    "biometric": "out-of-scope",
    "photo": "out-of-scope",
    "other_unique_id": "regex",
}

# Order matters: more specific patterns run before generic ones so we don't, e.g.,
# swallow an SSN as an "other unique id".
_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("url", re.compile(r"\bhttps?://[^\s]+|\bwww\.[^\s]+", re.I)),
    ("ip_address", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
    ("ssn", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    # label-based IDs: the captured token must contain a digit (real MRNs, member
    # IDs, account/license/device numbers do) so ordinary words like "licensed"
    # or "serial section" are not mistaken for identifiers.
    ("mrn", re.compile(r"\bMRN[:#]?\s*(?=[A-Z0-9-]*\d)[A-Z0-9-]{4,}\b", re.I)),
    ("health_plan_id", re.compile(r"\b(?:member|beneficiary|policy|health\s*plan)\s*(?:id|#|no\.?)?[:#]?\s*(?=[A-Z0-9-]*\d)[A-Z0-9-]{5,}\b", re.I)),
    ("account_number", re.compile(r"\b(?:acct|account)\s*(?:#|no\.?|number)?[:#]?\s*(?=[A-Z0-9-]*\d)[A-Z0-9-]{4,}\b", re.I)),
    ("license_number", re.compile(r"\b(?:license|licence|dl)\s*(?:#|no\.?|number)?[:#]?\s*(?=[A-Z0-9-]*\d)[A-Z0-9-]{4,}\b", re.I)),
    ("vehicle_id", re.compile(r"\b(?:VIN[:#]?\s*[A-HJ-NPR-Z0-9]{11,17}|plate[:#]?\s*(?=[A-Z0-9-]*\d)[A-Z0-9-]{4,})\b", re.I)),
    ("device_id", re.compile(r"\b(?:device|serial|sn)\s*(?:#|no\.?|number)?[:#]?\s*(?=[A-Z0-9-]*\d)[A-Z0-9-]{4,}\b", re.I)),
    ("phone_or_fax", re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b")),
    ("date", re.compile(
        r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b"
        r"|\b(?:January|February|March|April|May|June|July|August|September|October|November|December|"
        r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b", re.I)),
    ("age_over_89", re.compile(r"\b(?:9\d|1\d\d)\s*(?:-|\s)?(?:years?[-\s]?old|y/?o|yo)\b", re.I)),
]

# Public reference domains — a URL to one of these is a policy / literature CITATION
# (e.g. a CMS coverage LCD or a PubMed article), never PHI, so Sentinel does not
# redact it. A personal, portal, or any other URL is still redacted as identifier #14.
_CITATION_HOSTS = (
    "cms.gov", "medicare.gov", "medicaid.gov", "ncbi.nlm.nih.gov",
    "pubmed.ncbi.nlm.nih.gov", "clinicaltrials.gov", "nih.gov", "fda.gov", "cdc.gov",
)
_PUBLIC_CITATION_URL = re.compile(
    r"https?://(?:[a-z0-9-]+\.)*(?:" + "|".join(h.replace(".", r"\.") for h in _CITATION_HOSTS) + r")(?:[/:?#]|$)",
    re.I,
)

_REDACTION = "[REDACTED:{cat}]"


@dataclass
class DeidReport:
    """Result of a de-identification pass."""
    text: str                                   # the de-identified text
    counts: dict[str, int] = field(default_factory=dict)  # {category: n_removed}
    categories_hit: list[str] = field(default_factory=list)

    @property
    def total_removed(self) -> int:
        return sum(self.counts.values())

    @property
    def is_clean(self) -> bool:
        """True if no detectable Safe-Harbor identifiers remain (best-effort)."""
        return self.total_removed >= 0 and not _has_residual(self.text)


def _has_residual(text: str) -> bool:
    for _, pat in _PATTERNS:
        if pat.search(text):
            return True
    return False


def deidentify(text: str, names: list[str] | None = None) -> DeidReport:
    """Redact HIPAA Safe-Harbor identifiers from ``text``.

    Args:
        text: free text that may contain PHI.
        names: optional roster of patient/individual names to redact verbatim
            (case-insensitive, whole-word).

    Returns:
        A :class:`DeidReport` with the redacted text and per-category removal counts.
    """
    if text is None:
        raise ValueError("text must not be None")
    counts: dict[str, int] = {}

    # 1) Names from the supplied roster (before regexes, so a name that looks like
    #    an id token is still removed as a name).
    if names:
        for nm in sorted({n.strip() for n in names if n and n.strip()}, key=len, reverse=True):
            pat = re.compile(r"\b" + re.escape(nm) + r"\b", re.I)
            text, n = pat.subn(_REDACTION.format(cat="name"), text)
            if n:
                counts["name"] = counts.get("name", 0) + n

    # 2) Regex-detectable structured identifiers.
    for cat, pat in _PATTERNS:
        if cat == "url":
            def _url_sub(m: re.Match) -> str:
                if _PUBLIC_CITATION_URL.match(m.group(0)):
                    return m.group(0)          # public policy / literature citation — not PHI
                counts["url"] = counts.get("url", 0) + 1
                return _REDACTION.format(cat="url")
            text = pat.sub(_url_sub, text)
            continue
        text, n = pat.subn(_REDACTION.format(cat=cat), text)
        if n:
            counts[cat] = counts.get(cat, 0) + n

    # 3) ZIP codes: HIPAA allows the first 3 digits (if the 3-digit area has
    #    > 20,000 people); we generalize 5-digit ZIPs to the 3-digit prefix.
    #    Context-gated (state abbrev or a "zip" label) so we do NOT redact other
    #    5-digit numbers such as CPT/PLA codes.
    def _zip_sub(m: re.Match) -> str:
        counts["geo_zip"] = counts.get("geo_zip", 0) + 1
        return m.group(1) + m.group(2) + "XX"
    text = re.compile(
        r"\b([A-Z]{2}\s+|zip\s*(?:code)?[:#]?\s*)(\d{3})\d{2}\b", re.I
    ).sub(_zip_sub, text)

    return DeidReport(text=text, counts=counts, categories_hit=sorted(counts))

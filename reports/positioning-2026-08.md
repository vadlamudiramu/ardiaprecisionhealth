# Positioning — rewrite proposal

**1 August 2026** · Internal · ARDIA PRECISION HEALTH

> Rewrites the company narrative around one claim: *Ardia is not a precision medicine company;
> it is the reimbursement infrastructure that determines whether precision medicine is
> economically deliverable.* Smaller claim, far more defensible, and it sits on the layer where
> the constraint has actually moved. Copy blocks below are drafts to paste, not descriptions of
> copy to write. **No live page has been changed** — see §7 for the change list awaiting approval.

---

## 1. The problem with the current positioning

| Current | Why it fails |
|---|---|
| "AI-Native Revenue Recovery" | Rock Health stopped tracking AI as a distinguishing category because it is now universal. This differentiates against nobody in 2026. |
| "The first AI-native platform built exclusively for independent labs" | XiFin claims >half of all molecular lab claims and shipped an AI Appeals Agent in spring 2026. "First" and "exclusively" both fail on inspection. |
| "MolecuIQ™ **Precision Medicine** Intelligence" | Implies clinical intelligence. Ardia does not sequence, interpret variants, or influence treatment. This borrows clinical credibility for billing infrastructure — a clinician on the cap table will notice. |
| "Where Genomics Meets Revenue Certainty" | Closest to right of anything on the site. Keep the instinct, sharpen the claim. |

The through-line: the current story claims a **clinical** identity and an **AI** differentiator.
Neither survives contact with a knowledgeable reader. The real differentiator — molecular
reimbursement domain depth — is currently buried below the fold.

---

## 2. The core positioning statement

> **Ardia is reimbursement infrastructure for precision medicine — the layer that lets the
> independent laboratories running molecular tests actually collect on them.**

Everything else derives from this. Three tests it passes that the current line does not: it is
checkable, it is not claimed by any incumbent, and it stays true whether or not PAMA cuts land.

**The thesis in one paragraph** (use verbatim in deck, memo, and About):

> Sequencing got roughly five times cheaper and the industry's largest platform posted two
> consecutive flat years. The binding constraint in precision medicine has moved from reading
> the genome to getting paid for reading it. Medicare now spends $3.6 billion a year on genetic
> testing — 43% of all Part B lab spend on 5% of the volume — and molecular diagnostics is the
> most-denied category in American healthcare. Ardia builds the infrastructure that closes that gap.

---

## 3. The structural insight — lead with this, it is the moat

This is the single most valuable sentence in the company's story and it is not currently on the site:

> **Molecular coverage is conditional on clinical facts the laboratory cannot see.**

Unpack it in exactly this order — it explains the whole business in four beats:

1. A CBC has been billed identically for forty years: stable code, stable price, unconditional
   coverage. A new molecular test often has no permanent CPT code. It gets a PLA code — around
   700 issued in eight years, 39 added in the July 2026 release alone — which carries no
   established price, so it goes to gapfill. In the 2026 cycle three MACs proposed **$1,160,
   $1,324 and $325 for the same test**. The lab does not know what it will be paid.
2. Medicare's NGS coverage is not "this test is covered." It is covered *if* the cancer is
   recurrent, metastatic or advanced, *if* the patient has not been tested with the same assay
   before, and so on. **Whether an identical laboratory procedure is payable depends on what is
   written in the ordering physician's notes.**
3. A hospital lab sits inside the same medical record as the encounter that generated the order.
   When a payer demands proof of medical necessity, it has the chart. An independent reference
   lab receives a specimen and a requisition — it must go *ask someone else* to justify a test
   it has already performed and already paid for.
4. That asymmetry is why independent labs face **2.76× higher odds of denial** than hospital labs
   (*JAMA Netw Open*, April 2025). It is not that they bill worse. It is that they are
   structurally separated from the evidence that makes the claim payable.

**Why this is the moat:** it is not transferable domain knowledge. Hospital-RCM tooling — Waystar,
R1, Ensemble — is architected around encounters, charge capture and DRGs. None of it is built
around MolDX technical assessments, DEX Z-codes, gapfill variance, ADLT rate decay, or a PLA code
set that churns every quarter.

---

## 4. Copy blocks — paste-ready

### 4.1 Homepage hero

**Recommended:**

> # The genome got cheap. The billing didn't.
> Ardia is reimbursement infrastructure for precision medicine — built for the independent
> laboratories that run molecular tests, where coverage depends on clinical facts the lab
> never sees.

**Alternate, if you want the problem stated before the company:**

> # Precision medicine works. Getting paid for it doesn't.
> Ardia builds the layer that closes the gap — reimbursement infrastructure for the independent
> laboratories running molecular diagnostics.

Both are in the existing site voice (the "honest zero" register on `market-validation.html`),
which is a genuine asset and should govern everything below.

### 4.2 Boilerplate — email signature, deck footer, LinkedIn, press

> Ardia builds reimbursement infrastructure for precision medicine: the systems that let
> independent laboratories collect on molecular testing. Dallas–Fort Worth, founded January 2026.

### 4.3 The "what we are not" block — trust builder, put it high on the site

> ## What Ardia is not
>
> We are not a precision medicine company. We don't sequence anything, we don't interpret
> variants, and we don't influence anyone's treatment.
>
> We're the layer underneath — the reason a lab can afford to keep running the test.
>
> That distinction matters to us. A denied claim isn't a neutral financial event: labs that
> can't collect stop offering tests, or bill the patient, or close. We work on the economics so
> the medicine stays available.

This does more for credibility than any capability claim on the site. It also inoculates against
the exact objection a clinical advisor would raise.

### 4.4 Product descriptor — one-word fix

| Current | Change to |
|---|---|
| MolecuIQ™ **Precision Medicine** Intelligence | MolecuIQ™ **Molecular Reimbursement** Intelligence |

Cheapest high-value change on the list. It removes the clinical-credibility borrow without
touching the brand, the mark, or the product.

### 4.5 Investor deck — first three slides

**Slide 1 — the shift.**
> Sequencing cost fell ~5×. Illumina posted two flat years.
> The constraint moved from reading the genome to getting paid for it.

**Slide 2 — why molecular breaks specifically.**
> Coverage is conditional on clinical facts the lab cannot see.
> *(the four beats from §3)*

**Slide 3 — why independent labs specifically.**
> 2.76× higher **odds** of denial vs hospital labs — *JAMA Netw Open*, Apr 2025, n=29,919.
> Not because they bill worse. Because they don't hold the chart.

Note the wording: **odds**, not "rate." See the audit in
`reports/precision-health-market-analysis-2026-08.md` §7 item 1.

### 4.6 "Why now" — the accelerant, not the foundation

> PAMA private-payor reporting closed 31 July 2026. CY2027 Medicare lab rates will be the first
> since 2018 built on current data, with reductions of up to 15% a year through 2029.
>
> The denial problem is structural and predates PAMA. The 2027 rates decide how fast labs have
> to solve it.

**Do not build the narrative on the cliff.** Congress has deferred these cuts seven times; the
RESULTS Act has 97 cosponsors and no markup. If an eighth delay lands in December, a
cliff-dependent story dies with it. A structural story survives.

---

## 5. Message hierarchy

| Layer | Message |
|---|---|
| **Category** | Reimbursement infrastructure for molecular diagnostics |
| **Problem** | Coverage is conditional on clinical facts the lab cannot see |
| **Who hurts** | Independent labs — 2.76× the odds of denial, no access to the chart |
| **Wedge** | Appeal recovery: success fee, no upfront cost, no workflow change |
| **Expansion** | Prevention — Z-code registration, medical-necessity capture at order time, LCD/NCD mapping |
| **Why now** | CY2027 rates, first built on current data since 2018 |
| **Proof** | Pilots, stated honestly — keep the "honest zero" posture |

The wedge/expansion split matters commercially: Waystar's subscription revenue grew **38% to 55%
of total** while volume-based grew **7%**. The category's value is migrating from transaction to
subscription. Appeals get you in the door; prevention is the business.

---

## 6. Words to retire

| Retire | Because |
|---|---|
| "AI-native" as the differentiator | Table stakes in 2026; differentiates against nobody |
| "First" / "only" / "exclusively" | XiFin is incumbent in molecular lab RCM. These claims fail on inspection |
| "Entirely ignored by the AI RCM wave" | Directly contradicted by XiFin's Empower AI launch, Mar/Apr 2026 |
| "Precision Medicine Intelligence" (as product descriptor) | Implies clinical function Ardia does not perform |
| "Denial **rates** 2.76× higher" | Misstates an odds ratio; overstates your own best statistic |

Keep AI everywhere it describes *how* the product works. Just stop using it to describe *why
Ardia wins*.

---

## 7. Page-by-page change list — awaiting approval

Nothing below has been applied.

| Page | Change |
|---|---|
| `index.html` | Hero → §4.1. Correct the stats block per audit §7 (odds not rate; JAMA 2025; ACLA attribution on $3.8B; pick one PAMA window) |
| `our-product.html` | "AI-Native Revenue Recovery for Healthcare Labs & Clinics" → §4.1/§4.2 |
| `precision-medicine.html` | Keep "Where Genomics Meets Revenue Certainty"; add §3 structural insight; MolecuIQ descriptor → §4.4 |
| `market-validation.html` | Voice is right — keep it. Fix the XiFin 23–31% vs 35.3% conflict and the 2.76 odds/rate wording |
| `ardia-profile.html` | Resolve the 35%/35.3% vs 23–31% contradiction and the "$3.8B from 2018–2020 alone" vs "since 2018" conflict |
| `investors.html` | Narrative → §4.5. Name XiFin, Epic and Infinx as comps rather than claiming white space |
| `about.html`, `vision.html` | Category language → §2. Add the §4.3 "what we are not" block |
| White paper (`.docx`) | Remove "entirely ignored"; update SALSA → RESULTS Act; reconcile appeal win rate (83% / 50–83% / 89%) |

**Brand constraints hold throughout** — navbar, `.logo-icon`, gradient underline and the
page-category tag system are untouched by any change above. This is copy only.

---

## 8. On the company name

Keep it. "ARDIA PRECISION HEALTH" is fine *provided* the positioning line sits immediately
beneath it — the name then reads as the domain served, not the function performed. The problem
was never the name; it was the product descriptor claiming clinical intelligence (§4.4) and the
absence of an explicit "what we are not" (§4.3). Fix those two and the name stops being a
liability and starts being an asset.

---

*Draft for review · ARDIA PRECISION HEALTH internal · not for external distribution*

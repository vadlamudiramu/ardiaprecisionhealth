# Precision Health & Precision Medicine — Market Analysis

**As of 1 August 2026** · Internal market intelligence · ARDIA PRECISION HEALTH

> **Scope.** Who leads precision health/medicine right now, why the field is (and is not) a
> genuine step change, and what both mean for ARDIA. Every figure is dated and attributed.
> Where a widely-repeated number has no auditable primary source, it is labelled as such
> rather than laundered into a claim. Confidence ratings appear in §8.

---

## 1. Bottom line

Three findings, in order of how much they should change your thinking.

**1. There is no single leader, and anyone who names one is selling something.** Precision
medicine is not one market — it is six stacked layers with different winners, different
economics, and almost no overlap in who dominates each. Illumina still owns the substrate.
Abbott now owns the largest screening revenue pool. Natera owns clinical volume. Tempus owns
data monetisation. Epic owns the workflow everything must pass through. Nobody owns two layers.
The honest answer to "who is leading" is §2's scoreboard, not a name.

**2. The technology stopped being the bottleneck; payment became the bottleneck.** This is the
single most important structural fact in the field as of mid-2026, and it is the one most
market reports miss. Sequencing cost fell roughly fivefold with NovaSeq X and Illumina posted
two consecutive flat years — revenue elasticity to its own price cuts is below one. Meanwhile
Medicare Part B genetic-testing spend hit **$3.6B in 2024, 43% of all Part B lab spend on 5%
of test volume, up 20% year over year** (HHS OIG, 28 Jan 2026). Volume is not the constraint.
Yield is. Molecular diagnostics is the highest-denial category in US healthcare, and
independent labs are denied at **2.76× the odds of hospital labs** (*JAMA Netw Open*, Apr 2025).
The value is migrating from "can we read the genome" to "can we get paid for reading it."

**3. The "game changer" claim is true in four specific places and oversold everywhere else.**
The evidence in §3 is tiered deliberately. Pharmacogenomics, rare-disease rapid genome
sequencing, targeted oncology in biomarker-defined subsets, and AI-assisted imaging now have
randomised or near-randomised evidence of patient benefit. Population-wide multi-cancer blood
screening does not — GRAIL's NHS-Galleri trial, the only randomised MCED trial ever run,
**missed its primary endpoint** in May 2026. Treat those two categories differently in every
investor conversation.

**For ARDIA specifically:** the thesis is directionally right and better-timed than the
business plan realises. The PAMA private-payor reporting window **closed 31 July 2026 — one day
before this report** — which means CY2027 rates will be the first since 2018 built on current
data, with cuts of up to 15%/year landing 2027–2029. The window between "labs learn what 2027
pays" and "labs need every claimable dollar" opens now.

But **two claims in the current materials will not survive diligence.** The white paper says
independent labs have been "entirely ignored by the AI RCM wave" — XiFin claims more than half
of all molecular-diagnostics lab claims and shipped an AI Appeals Agent in spring 2026. And the
site restates an *odds ratio* as a *rate ratio*, which overstates its own headline 2.76×
statistic. Section 6 works through the strategic implications; **§7 is the one to action first**
— it audits every statistic currently published on the site and lists five contradictions
between ARDIA's own pages.

---

## 2. Who is leading — the scoreboard

### Layer 0 — Reading biology (sequencing platforms)

**Leader: Illumina, but for the first time with a real challenger.**

| Company | Position | Key 2026 figures |
|---|---|---|
| **Illumina** | Incumbent standard for clinical NGS | FY2025 ~$4.34B (−0.66%); Q2 2026 $1.159B, +9.5% reported / +6.5% organic; FY26 guide raised to $4.60–4.64B; non-GAAP GM 68.2% |
| **Roche (AXELIOS 1)** | First architecturally novel high-throughput platform to launch | Launched 29 Jun 2026 (research-use-only); $750K list vs NovaSeq X $985K–$1.25M; 1.8–2.7 Tb duplex in 4 hours; claimed $150 genome |
| **Oxford Nanopore** | Leading long-read / non-optical modality | FY2025 £223.9M, +22.2%; clinical +60%; H1 2026 ~£116.5M, +10% — below management expectations |
| **Ultima Genomics** | Lowest cost/read at extreme scale | UG200 from $850K, UG200 Ultra $1.25M (AGBT, 25 Feb 2026); >60,000 30× genomes/year per Ultra |
| **Element Biosciences** | Best-funded private short-read challenger | ~200 AVITI installs; Series E >$175M led by Samsung (9 Jun 2026), making Samsung largest shareholder |
| **MGI / Complete Genomics** | Dominant inside China, excluded from US | ~70% domestic China share (company claim, 4 consecutive years); 1,470 sequencers sold globally 2025 |
| **PacBio** | HiFi long-read accuracy, sub-scale | Q1 2026 $37.2M, flat; FY26 guidance *cut* to $165–175M |

**The insight that matters.** Illumina's NovaSeq X install base reached ~1,000 units by Q1 2026
and now carries **83% of Illumina's sequencing volume but only 59% of its sequencing revenue**.
That gap *is* the deflation Illumina caused to itself. Its growth in 2026 comes from clinical
conversion — clinical is now ~65% of sequencing consumables, growing ~20% ex-China — not from
cheaper sequencing driving more revenue. Cheaper reading of DNA has not produced a
proportionally larger business for the company doing the reading. That is a warning about where
value accrues in this field generally.

Roche's AXELIOS is a genuine threat to *margin*, not yet to *share*: it has zero installed base,
is research-use-only, has no diagnostic clearance, and its headline $0.06/Mread economics are at
~Q23 quality, which is not competitive with Illumina Q30+ for clinical variant calling.

> ⚠️ **The "$100 genome" is a marketing unit, not an economic one.** Every sub-$200 claim in
> 2026 — Ultima $80, Element $100, Complete Genomics $100, Roche $150, Illumina $200 — is a
> list-price, consumables-only figure computed on the vendor's most favourable run
> configuration. None includes labour, capital amortisation, failed runs, or interpretation.

### Layer 1 — Diagnosing (clinical precision diagnostics)

**This layer has two leaderboards and they do not agree.** That is the most useful thing to
know about it.

**By revenue (FY2025):**

| Rank | Company | FY2025 revenue | 2026 trajectory |
|---|---|---|---|
| 1 | **Abbott** (via Exact Sciences) | $3.25B, +18% | Acquired ~$21B equity / ~$23B EV; **closed 23 Mar 2026** |
| 2 | **Natera** | $2.31B, +35.9% | Q1 2026 $696.6M, +38.8%; FY26 guide $2.74–2.82B |
| 3 | **Tempus AI** | ~$1.27B | Q2 2026 $382.5M, +22%; **first GAAP-profitable quarter** ($5.6M) |
| 4 | **Guardant Health** | $982M, +33% | Q2 2026 $335M, +44.3% — fastest growth at scale |
| 5 | **Caris Life Sciences** | $812M, +97% | IPO 17 Jun 2025; Q1 2026 near breakeven |
| 6 | **Veracyte** | ~$540M | **Best unit economics in the sector** — Q2 2026 GAAP net margin 17.0% |
| 7 | **GRAIL** | $147.2M, +17% | Cash $823.1M; stated runway into 2030 |

**By clinical adoption, the order changes.** Natera is the volume leader by a wide margin:
~3.53M tests in FY2025 and **>1.01M in Q1 2026 alone**, with Signatera the reference-standard
tumour-informed MRD assay and the broadest MolDX/Medicare footprint of any MRD product.
Guardant leads blood-first velocity (~104,000 oncology tests in Q2 2026, +63%) and holds the
only FDA-approved primary CRC screening blood test. Tempus leads data monetisation: >$1.1B
remaining contract value, 126% net revenue retention, relationships with 19 of the top 20 pharma.

**Profitability is the newest fault line, and it separates the field sharply.** Veracyte, Caris
and Tempus have crossed or approached breakeven. Natera and Guardant remain structurally
loss-making despite excellent growth — Guardant burned $69.5M of free cash flow in Q2 2026 and
carries $1.50B of convertible notes against $1.05B of cash. Growth and viability are no longer
the same question in this layer.

### Layer 2 — Interpreting (AI models for biology and medicine)

**Leader: Google DeepMind / Isomorphic Labs on capability; nobody yet on clinical proof.**

- **Isomorphic Labs** reached the field's most-watched milestone: the FDA cleared **ISM8969**
  for human trials on **28 Jan 2026**, among the first AI-designed drugs to do so. The company
  raised **$2.1B** and expects first trials by end-2026 — a slip from its earlier end-2025 target.
- **Epic's Comet** foundation model, trained on **>100 billion patient medical events** from
  Cosmos, opened to participating research organisations in **February 2026**. Built with Yale
  and Microsoft. This is the largest clinical-data foundation model in deployment.
- **FDA-authorised AI-enabled devices reached ~1,450 by mid-2026**, overwhelmingly radiology
  and cardiology, overwhelmingly cleared via 510(k). Note FDA's list is a curated term-based
  sample, not an exhaustive inventory.

The honest read: capability is advancing fast, clinical validation is not keeping pace, and the
one AI-native modality with genuine randomised outcome evidence is imaging (see §3).

### Layer 3 — Treating (precision therapeutics)

**Leader: the pharma industry collectively — this is the layer where precision medicine is
unambiguously winning.**

- **Personalised medicines were ~36% of FDA novel approvals in 2025** (16 of ~45) and ~38% in
  2024 (18) — **the sixth consecutive year above one-third**, versus under 10% a decade ago
  (Personalized Medicine Coalition, May 2026).
- **Gene editing reached routine-ish care but not scale.** Casgevy: **64 patient infusions in
  2025** (30 in Q4), ~90% of eligible US patients now covered by reimbursement, FDA label
  expanded to ages 2+ in **July 2026**. The CMS Cell and Gene Therapy Access Model now includes
  **33 states plus DC and Puerto Rico**, covering ~84% of Medicaid beneficiaries with sickle
  cell disease. Sixty-four infusions is a real number and a small one — that tension is the story.

### Layer 4 — The data substrate

**Leader: Epic, decisively, and it is extending.** Epic owns the workflow that every other layer
must route through, and Cosmos/Comet converts that position into a research and prediction
asset no competitor can replicate. For any company selling into US health systems, Epic is
simultaneously the distribution channel and the most likely eventual competitor.

### Layer 5 — Getting paid (where ARDIA operates)

**Leader in general RCM: Waystar. Leader in lab/molecular RCM: XiFin — there is an incumbent,
and the opening is narrower and more specific than "nobody serves this market."**

This layer resolves into four structurally distinct markets that are routinely conflated:
provider-side transaction software, outsourced revenue operations, payer-side adjudication, and
lab/molecular RCM as a largely disconnected vertical.

| Company | Position | Key figures |
|---|---|---|
| **Waystar** (NasdaqGS: WAY) | Overall AI-RCM leader — the only one with audited financials proving AI monetisation | Q1 2026 revenue $314M (+22% YoY, +11% organic); adj. EBITDA $135M at **43% margin**; **subscription revenue +38% to $172M = 55% of total** while volume-based grew only 7%; NRR 111%; FY26 guide $1.27–1.29B. Acquired **Iodine Software for $1.25B EV** (Jul 2025) |
| **XiFin** | **Lab and molecular-diagnostics RCM incumbent** — claims **>half of all molecular-diagnostics lab claims** | Black Book #1 client-rated lab RCM **seven consecutive years** (announced 8 Jan 2026); 19% revenue growth in 2024; Goldman Sachs-led growth capital Sept 2025; **Empower AI ecosystem announced 9 Mar 2026** incl. an **AI Appeals Agent** previewed April 2026 |
| **R1 RCM** (TowerBrook/CD&R) | Outsourced revenue ops at enterprise scale | **Taken private for $8.9B ($14.30/share), Nov 2024**; exclusive **Palantir** partnership + R37 AI lab (Mar 2025); 180M+ annual payer transactions, 1.2B annual workflow actions |
| **Epic** | **The most underrated medium-term threat** | Ships **Penny** — native RCM assistant that *drafts denial appeals and suggests billing codes* — plus predictive denial analytics and automated prior auth in the 2026 feature set |
| **Infinx** | **Most likely consolidator of the lab vertical** | >$200M revenue run rate, KKR/Norwest-backed; acquired i3 Verticals' healthcare RCM for **$96M** and **MedReceivables Advisor (pathology billing)** |
| **Optum/Change** | Largest raw transaction footprint, structurally impaired | Feb 2024 ransomware: $1B–$1.15B direct costs, $350–450M revenue loss; unavoidable payer-ownership conflict |
| Telcor, Quadax | Only other lab-native vendors | Neither discloses revenue, claim volume or customer counts |

**What this means for the "white space" claim.** XiFin's incumbency is real but its published
scale figures are stale and self-contradictory — the "$40B gross annual laboratory claims"
milestone dates to **July 2019** while current marketing says "more than $30 billion," i.e. the
number went *down*. Black Book is a client-satisfaction survey XiFin itself press-releases, not
an independent share measure. **The defensible wedge is not "no one serves molecular labs" — it
is that the incumbent is a billing platform retrofitting AI (Empower announced March 2026),
while the AI-native entrants are all built for hospital and physician-group economics rather
than MolDX/Z-code/gapfill/ADLT machinery.**

> ⚠️ **The contrarian data point that cuts both ways.** KFF found only **0.2% of denied ACA
> marketplace claims were appealed internally** — and that in-network denial rates **fell from
> 22.5% to 19.1% between 2023 and 2024**, the first decline in four years. Vendors present the
> unappealed 99.8% as untapped recovery value. The harder read: if denials have gone unappealed
> for decades despite direct financial incentive, the binding constraint may be economics per
> claim rather than capacity — which is precisely the assumption a success-fee model must
> validate in pilots. Note also that Experian's *provider-reported* survey shows denials rising
> while KFF's *payer-reported* data shows them falling. Know which direction your source runs.

**Why this layer is harder than it looks:**

| Mechanism | Current state (2026) |
|---|---|
| **MolDX / DEX Z-codes** | Required by Palmetto, Noridian, CGS, WPS. UnitedHealthcare now requires a Z-code on every molecular pathology code — phased from DOS 1 Apr 2024, claims on/after 1 Jan 2025 |
| **Gapfill pricing variance** | CPT 0552U in the 2026 cycle: MolDX proposed $1,160, Novitas ~$1,324, NGS MAC ~$325 — a **~4× spread on one test** |
| **ADLT status** | Rare and non-durable. Shield was only the **18th ADLT** (Mar 2025, $1,495). Natera's Signatera ADLT rate **fell $3,920 → $3,590 in Jan 2026** |
| **PLA code proliferation** | Reached **0698U by 1 Jul 2026** — ~700 proprietary codes in eight years; the July 2026 release alone added 39 |
| **Appeal economics** | XiFin: molecular medical-necessity appeals succeed only **12.8%** of the time; additional-information appeals 23% |

### Layer 6 — Policy and the national picture

- **FDA lost its bid to regulate LDTs, permanently.** Judge Sean D. Jordan (E.D. Tex.) vacated
  the LDT Final Rule in its entirety on **31 March 2025** (*ACLA v. FDA*, consolidated with
  *AMP v. FDA*). HHS **did not appeal**, and FDA formally **rescinded the rule in September
  2025**. LDTs remain regulated under CLIA. This materially lowered the compliance barrier for
  lab-developed molecular tests and is a tailwind for independent labs.
- **PAMA is at its most consequential moment since 2018** — see §6.
- **The Nancy Gardner Sewell MCED Act was signed 3 February 2026**, creating a Medicare coverage
  pathway from 2028 for FDA-approved multi-cancer early detection tests.
- **The US is losing ground on population genomics.** All of Us received **$153M in FY2026, a
  ~72% decline from FY2023**, as 21st Century Cures funding expired. It has paused adult
  biosample collection and delayed pediatric cohort expansion, at ~860,000 participants. This is
  a self-inflicted competitive loss against UK Biobank, Our Future Health and Chinese programmes.

---

## 3. Why it is genuinely a game changer — the evidence, honestly tiered

This is the section to use with investors, because it is the one that survives scrutiny.

### Tier 1 — Proven. Randomised or near-randomised evidence of patient benefit.

| Domain | Evidence | Result |
|---|---|---|
| **Pharmacogenomics** | PREPARE trial, *The Lancet*, 3 Feb 2023, n=6,944, 7 countries | **30% reduction in adverse drug reactions** with a 12-gene panel. OR 0.70 (95% CI 0.54–0.91), P=0.0075 |
| **AI-assisted imaging** | MASAI trial, *The Lancet* final results, >100,000 Swedish women | **+29% cancer detection**, **−44% radiologist reading workload**, sensitivity 80.5% vs 73.8% at identical 98.5% specificity, interval cancers −12%, no increase in false positives |
| **Rare disease dx** | NSIGHT1 RCT, rapid whole-genome sequencing in critically ill infants | **31% vs 3%** genetic diagnosis within 28 days. Diagnostic yields of 32–50% across series, with documented management changes |
| **MRD-guided therapy** | IMvigor011, *NEJM* / ESMO 2025, muscle-invasive bladder cancer | ctDNA-guided adjuvant atezolizumab improved **both disease-free and overall survival** — the first survival benefit for an MRD-guided strategy in any solid tumour |

These four are why the field deserves the word "transformative." They are also narrow,
specific, and each took a decade to prove.

### Tier 2 — Real but partial. Works for a defined subset; the subset is smaller than marketed.

**Targeted oncology.** The fraction of clinically actionable tumours rose from **8.9% to 31.6%
between 2017 and 2022** (Memorial Sloan Kettering). But actionability is not benefit: across
series, roughly **38–45% of patients who receive a genomically matched therapy derive clinical
benefit**, and in one cohort that was **3% of the whole screened population**. NSCLC patients on
biomarker-matched targeted therapy showed a **37% lower risk of progression or death** versus
chemotherapy — a genuinely large effect, in a genuinely narrow group.

**Treatment de-escalation — the underrated win.** DYNAMIC-III showed ctDNA-guided management in
colon cancer was non-inferior at five years (**RFS 88.3% vs 87.2%; OS 93.8% vs 93.3%**). The
value here is not better outcomes — it is *equivalent outcomes with less chemotherapy*. That is
a real economic and quality-of-life gain that rarely appears in market forecasts.

### Tier 3 — Not proven. Do not build a thesis on these.

**Population-wide multi-cancer early detection.** GRAIL's **NHS-Galleri trial (n=142,250, three
annual screening rounds) MISSED its primary endpoint** — it did not significantly reduce
combined Stage III–IV diagnoses. Full results were presented at ASCO on 30 May 2026.

The widely-quoted favourable figures — **14% overall reduction in Stage IV** (−9%, −22%, −26%
across rounds one to three), **+16% Stage I/II detection**, **4× detection rate versus standard
screening** — are all *secondary or per-round analyses of a trial that missed its primary
endpoint*. They may well prove out. They are not yet proof.

**Treatment escalation on MRD positivity.** ALTAIR, the first completed randomised trial of
treat-on-molecular-recurrence in any solid tumour, **did not meet its primary endpoint**: median
DFS 9.30 vs 5.55 months, HR 0.79 (95% CI 0.60–1.05), **P=0.107**. Knowing a patient is MRD-positive
is established; knowing what to *do* about it, outside bladder cancer, is not.

**The pattern worth internalising:** precision medicine has repeatedly proven it can *stratify*
patients. It has proven far less often that acting on the stratification changes outcomes. The
gap between those two is where most of the field's disappointment lives.

---

## 4. The counter-case

State these before an investor does.

1. **Reading DNA got ~5× cheaper and Illumina's revenue went flat for two years.** Elasticity
   below one. Cheaper inputs do not automatically create larger markets.
2. **Market-size forecasts in this sector are unusable.** Five firms give 2026 NGS market sizes
   spanning **$11.79B to ~$21B** — a 78% spread for nominally the same market in the same year.
   Proteomics is worse. Quote any single figure only with the firm and definition attached.
3. **The consumer genomics business model failed outright.** 23andMe filed for bankruptcy
   23 Mar 2025; the genetic data of **13M+ customers** sold for **$305M** to TTAM/Anne Wojcicki,
   closing 14 Jul 2025. Scale of genomic data is not, by itself, a business.
4. **US population-genomics leadership is eroding by choice** — All of Us down ~72% from FY2023.
5. **Gene therapy commercial reality lags the science badly.** 64 Casgevy infusions in 2025 for
   a functionally curative therapy with ~90% reimbursement coverage. Delivery infrastructure,
   not science or payment, is the binding constraint.
6. **The screening thesis took a real hit in 2026.** NHS-Galleri missed; the ACS's updated CRC
   guideline (27 May 2026) added blood-based testing only as a **non-preferred** option for
   patients who decline or fail preferred tests. Guardant's Shield realises roughly **$800 ASP
   against ~$410 cost per test** before commercial and bad-debt loading — negative unit
   economics at the margin, against a $1,495 Medicare rate.
7. **Consolidation is closing the independent-player window.** Abbott/Exact ($23B EV, Mar 2026)
   means the largest screening franchise now sits inside a company with a primary-care
   distribution machine no pure-play can match.

---

## 5. Where the capital is actually going

- **Digital health funding recovered in H1 2026: $7.4B across 244 deals** — the strongest first
  half since 2022, ~$1B above H1 2025 (Rock Health).
- **Capital is concentrating hard.** Mega-deals ($100M+) took **45% of all capital in just 8% of
  transactions**.
- **"AI-enabled" has stopped being a category.** Rock Health no longer tracks it as a
  distinguishing label because it has become universal. *An AI story is no longer a
  differentiator in a fundraise — the wedge has to be the domain, the data, or the workflow.*
  This is directly relevant to how ARDIA positions.

---

## 6. What this means for ARDIA

### The timing is better than the business plan states

The white paper describes PAMA cuts as scheduled for 1 Jan 2027 after "seven consecutive
delays." That is right, and the current state is sharper still:

- **§6226 of the FY2026 appropriations package, enacted 3 February 2026**, deferred cuts of up
  to 15% on ~800 codes through **31 December 2026**.
- It moved the reporting window to **1 May – 31 July 2026** — which **closed the day before this
  report**.
- Critically, it replaced the stale 2019 data collection period with **1 January – 30 June 2025**.

**Therefore: CY2027 rates will be the first since 2018 built on contemporary data**, with cuts
capped at 15%/year across 2027–2029. Labs will learn their 2027 economics this autumn. The
commercial window for "recover every claimable dollar" opens *now*, not in January.

**Update the plan on one point:** SALSA is dead — not reintroduced in the 119th Congress,
superseded on 10 September 2025 by the **RESULTS Act (H.R. 5269 / S. 2761)**. That bill has
**97 House cosponsors but no markup** in Energy & Commerce, Ways & Means, or Senate Finance.
Base rates favour an eighth delay; do not model relief as the expected case, and do not cite
SALSA as pending.

### The competitive gap is real, but narrower than "entirely ignored"

The plan's claim that independent labs have been "entirely ignored by the AI RCM wave" **will not
survive diligence and should be rewritten.** XiFin is a genuine incumbent that claims **more than
half of all molecular-diagnostics lab claims**, has been Black Book's #1 client-rated lab RCM
vendor for seven consecutive years, took Goldman Sachs-led growth capital in September 2025, and
**launched its Empower AI ecosystem — including an AI Appeals Agent — in March/April 2026**. An
investor who spends ten minutes on this will find it.

**The defensible version is narrower and genuinely stronger.** State it as three claims that are
each individually checkable:

1. **The incumbent is retrofitting, not AI-native.** XiFin's AI appeals capability was announced
   in March 2026 and previewed in April 2026 — it is roughly contemporaneous with ARDIA, not a
   decade ahead. Its published scale figures are also stale and self-contradictory (the "$40B
   annual lab claims" milestone is from **July 2019**; current marketing says "more than $30B").
2. **The AI-native entrants are built for the wrong economics.** Waystar, R1, Ensemble and
   Infinx are architected around hospital and physician-group revenue cycles. None is built
   around MolDX technical assessments, DEX Z-codes, ~4× gapfill spreads between MACs, ADLT rate
   decay, or ~700 PLA codes churning at 39 new codes per quarterly release.
3. **That machinery is the actual moat.** It is domain knowledge that compounds and does not
   transfer from hospital RCM.

**Two competitive threats to name before an investor does:**

- **Epic ships Penny**, a native RCM assistant that *already drafts denial appeals and suggests
  billing codes*, with predictive denial analytics and automated prior auth in the 2026 feature
  set. Epic's distribution cannot be matched by any point solution. ARDIA's defence is that
  independent labs are largely *not* on Epic — make that explicit rather than leaving it implied.
- **Infinx is consolidating the lab vertical right now** — >$200M run rate, KKR/Norwest-backed,
  having bought i3 Verticals' healthcare RCM ($96M) and MedReceivables Advisor (pathology
  billing). It is the most likely acquirer of this space, which is simultaneously the main
  competitive risk and a credible exit path.

### What to add to the pitch

1. **Lead with the payment-is-the-bottleneck thesis (§1.2).** Medicare genetic-test spend is
   **43% of Part B lab spend on 5% of volume, +20% YoY** (OIG, Jan 2026). That single statistic
   frames ARDIA as infrastructure for where the money already is, not a bet on future growth.
2. **Use the LDT vacatur as a tailwind.** FDA's rule is vacated *and rescinded* with no appeal —
   independent labs face a materially lighter regulatory path than 2024 projections assumed,
   which supports volume growth in exactly ARDIA's customer base.
3. **Retire "AI-native" as the differentiator.** Rock Health stopped tracking AI as a category
   because it is now universal. The differentiator is molecular reimbursement domain depth.
4. **Quantify appeal economics honestly.** XiFin's data shows molecular medical-necessity
   appeals succeed only **12.8%** of the time. The plan's "50–83% appeal win rate" is a very
   different denominator and will not survive diligence if the two are conflated — see §7.

---

## 7. Claims audit — statistics currently published by ARDIA

Run against primary sources. **Two need correcting before an investor checks them.**

| # | Published claim | Verdict | Action |
|---|---|---|---|
| 1 | "Denial **rates** 2.76× higher vs hospital labs" — cited on site as *JAMA Network Open **2024*** | 🔴 **NUMBER CONFIRMED, PHRASING WRONG** | Kang SY, Odouard I, Gresenz CR, *JAMA Netw Open*, **18 Apr 2025**. The paper reports an **odds ratio: OR 2.76 (95% CI 2.58–2.95), P<.001**; n=29,919 claims / 24,443 beneficiaries. Non-hospital sites OR 2.55 (2.12–3.07). **An odds ratio is not a rate ratio.** For an outcome as common as claim denial (~23%) the two diverge substantially, so "denial rates 2.76× higher" **overstates the effect**. Say "2.76× higher *odds* of denial." Also fix "2024" → **2025** |
| 2 | "Denials rose 16.8% pre-NCD → 27.4% post-2020 amendment" (business plan) | ✅ **CONFIRMED** | Same study. Note the intermediate figure is 20.3% post-*initiation*; 27.4% is post-*amendment*. Keep them distinct |
| 3 | "23–31% average denial rate, independent molecular labs — XiFin 2024" (site) | ⚠️ **MISLEADING AS STATED** | XiFin's published figures are **~27% claim-level** and **35.3% CPT-code level** for molecular; overall diagnostics denials *fell* 9.9% → 8.0% in 2024. The "23–31%" band maps to no XiFin figure. **Replace with the exact XiFin pair, or with JAMA's 23.3%** |
| 4 | "$3.8B lab revenue cut by PAMA since 2018 — CMS PAMA Final Rule · MedPAC 2024" (site) | ⚠️ **WRONG ATTRIBUTION** | The figure traces entirely to **ACLA advocacy analysis**. No CBO score, no MedPAC estimate, no OIG audit corroborates it. It is defensible *if attributed to ACLA*. **The current citation to CMS/MedPAC is incorrect and should be changed.** MedPAC's actual finding: private rates were below Medicare's 2017 rates for 77% of tests |
| 5 | "65% of denials never appealed" | ⚠️ **INCONSISTENT SOURCING** | Site cites *MGMA 2023*; business plan cites *HFMA + LigoLab 2024*. Pick one verifiable source and use it everywhere |
| 6 | "$70B+ AI in RCM market by 2030, 24% CAGR — Grand View 2024" | 🔵 **UNVERIFIED** | Not confirmed in this sweep. Given the 78% spread across firms for NGS market size, treat all such forecasts as low-confidence and always name the firm and definition |
| 7 | "Appeal win rate 50–83%" (exec summary) vs "50–80.7%" (body) | ⚠️ **INTERNAL INCONSISTENCY** | Two figures for one statistic in one document. Also reconcile against XiFin's 12.8% molecular medical-necessity success rate — these measure different things and must not be presented interchangeably |
| 8 | "PAMA 2027, up to 15%/yr for 3 years, moratorium through 31 Dec 2026" | ✅ **CONFIRMED & SHARPENED** | §6226, FY2026 appropriations, enacted 3 Feb 2026. Add: reporting window closed **31 Jul 2026**; data period **1 Jan – 30 Jun 2025** |
| 9 | "SALSA and RESULTS Act remain unpassed" | ⚠️ **STALE** | SALSA was **not reintroduced** in the 119th Congress and is superseded. Only the RESULTS Act (97 cosponsors, no markup) is live |
| 10 | Independent labs "entirely ignored by the AI RCM wave" (white paper exec summary) | 🔴 **WILL NOT SURVIVE DILIGENCE** | XiFin claims >half of all molecular lab claims and launched an AI Appeals Agent in Mar/Apr 2026. Rewrite per §6 |

### Cross-page contradictions the site currently publishes

These were found by auditing ARDIA's own pages against each other. Each is the kind of thing a
technically literate investor catches in one sitting.

| Defect | Where | Fix |
|---|---|---|
| **Same source, two incompatible numbers.** "23–31%" molecular denial rate cited to *XiFin 2024* on `market-validation.html:1167` and `investors.html:1430`; **"35%" / "35.3%"** cited to *XiFin 2024* on `ardia-profile.html:331,353`. 35.3% falls outside the 23–31% band | 4 pages | Reconstruct which specific XiFin publication each came from; publish one |
| **Same figure, two different statistics.** 2.76 called a "denial **rate**" on `market-validation.html:1185` but "denial **odds**" on `ardia-profile.html:336,362` | 2 pages | Standardise on **odds** — that is what the paper reports |
| **Same figure, two different windows.** "$3.8B cut by PAMA **since 2018**" (`index.html:1210`, `market-validation.html`) vs "$3.8B … **From 2018–2020 alone**" (`ardia-profile.html:377`) | 3 pages | Pick one. Note cumulative claims are additionally weakened because later cuts were repeatedly *deferred*, not applied |
| **Appeal win rate stated three ways** — "83%", "50–83%", "89%" | across site + white paper | One figure, one source. And keep it distinct from XiFin's **12.8%** molecular medical-necessity success rate |
| **TAM inconsistency** — `email-audit.html` cites a "$12B market" against "$70B+" everywhere else | 1 page | `email-audit.html` is already `.vercelignore`d as internal, but it is still in the repo |

**One thing that checked out:** the $70B/24% CAGR triple is internally coherent — $20.6B (2024)
compounded at 24% for six years is $74.9B, consistent with "$70B+ by 2030." (Exactly $70B would
imply 22.6%.) The residual risk is staleness: a 2024-base forecast is two cycles old in August
2026, and these reports are reissued annually with revised bases. Re-pull before an investor does.

---

## 8. Sources & confidence

**High confidence** — company reported financials (Illumina, Tempus, Natera, Guardant, Caris,
Veracyte, GRAIL, Abbott/Exact, PacBio, Oxford Nanopore, 10x), FDA and CMS regulatory actions,
statutory text (§6226), HHS OIG data, peer-reviewed trials (PREPARE, MASAI, NSIGHT1, IMvigor011,
ALTAIR, DYNAMIC-III, Kang *et al.*), PMC approval counts, Rock Health funding data.

**Medium confidence** — market share estimates, XiFin denial figures (vendor-published, large
sample, no independent audit), MolDX cycle times (administrator-stated, unaudited), the ACLA
$3.8–4.0B PAMA figure, vendor cost-per-genome claims.

**Low confidence — do not quote without caveat** — all market-size forecasts and CAGRs. Five
firms give 2026 NGS market sizes from $11.79B to ~$21B.

**Vendor-reported, treat as marketing** — Waystar's "$15.5B denials prevented," "450 million
annual denied claims" and "$350B administrative waste" all trace to its own January 2025
AltitudeAI press release and are now recirculated as though independently established. XiFin's
Black Book ranking is a client-satisfaction survey XiFin itself promotes, not a share measure.
Epic's "40% undercoding reduction" is a vendor claim.

**Methodological note — read before quoting anything.** Direct document retrieval was blocked by
this environment's egress policy: every `WebFetch` returned HTTP 403, and direct `CONNECT`
attempts were denied for `jamanetwork.com`, `pmc.ncbi.nlm.nih.gov`, `cms.gov`, `medpac.gov`,
`xifin.com`, `mgma.com`, `grandviewresearch.com`, `kff.org` and `healthit.gov`. Figures were
therefore assembled from search-engine summaries of those primary sources, cross-checked across
independent results wherever possible. **Re-verify any figure against the primary document
before it goes into an investor deck or a public page.**

Two exceptions are safe to act on now because they were each confirmed across multiple
independent secondary sources: the §7 item 1 correction (odds ratio, April 2025) and the §7
item 4 correction (ACLA attribution). The five cross-page contradictions in §7 required no
external source at all — they are ARDIA's own pages disagreeing with each other, and can be
fixed immediately.

**Not verified.** The five site statistics were assigned to an independent external-verification
pass that could not complete — its web-search budget was exhausted (200/200) before it began and
its required source hosts were blocked. Items 3, 5 and 6 in §7 therefore remain genuinely
*unverified*, not *verified-and-found-wanting*. Completing that pass needs either a raised search
budget or an egress allowlist for the hosts named above.

---

*Prepared 1 August 2026 · ARDIA PRECISION HEALTH internal market intelligence · not for external distribution*

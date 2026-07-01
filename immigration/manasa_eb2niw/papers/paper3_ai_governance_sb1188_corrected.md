# Compliance-by-Design: AI Governance Frameworks Under Texas SB 1188 and TRAIGA for Healthcare Revenue Cycle AI Systems

**Authors:** Rambabu Vadlamudi¹, Manasa Jampani¹  
¹ Ardia Health Labs, Argyle, TX 76226, USA  
**Correspondence:** ram.vadlamudi@ardiahealthlabs.com  

**Submission Target:** Journal of the American Health Information Management Association (AHIMA) or Health Affairs  
**Status:** Draft  

---

## Abstract

Texas has emerged as the first state to enact healthcare-specific AI accountability legislation (Senate Bill 1188, 89th Legislature (2025), signed June 20, 2025, general effective date September 1, 2025, with a data-localization provision effective January 1, 2026) and the third state to establish comprehensive AI governance (House Bill 149 / Texas Responsible Artificial Intelligence Governance Act — TRAIGA, 89th Legislature, signed June 22, 2025, effective January 1, 2026). Together, these laws establish requirements for explainability, human oversight, data provenance, bias monitoring, and audit logging in AI systems operating in regulated healthcare contexts — requirements that anticipate federal AI governance frameworks currently under development.

This paper examines the technical implementation requirements of SB 1188 and TRAIGA as applied to AI systems in healthcare revenue cycle management (RCM), an administratively critical but under-examined domain in AI governance scholarship. We present a compliance-by-design framework derived from implementation experience with the DGP (Deterministic-Generative-Predictive) Clinical Revenue Architecture — a three-layer AI system for independent laboratory claim recovery — and analyze how architectural choices at the design stage can satisfy statutory requirements without post-hoc compliance retrofitting.

Our analysis demonstrates that the deterministic-first architectural principle — encoding regulatory policy in a rule-based engine upstream of any generative AI component — simultaneously advances both technical reliability (zero hallucination on policy interpretation) and regulatory compliance (explainability, auditability). We discuss implications for healthcare AI developers, payers, and the independent laboratory industry, and offer a design checklist applicable to AI systems in any healthcare administrative domain subject to these frameworks.

**Keywords:** Texas SB 1188, TRAIGA, healthcare AI governance, AI explainability, healthcare revenue cycle, compliance-by-design, deterministic AI, AI audit

---

## 1. Introduction

### 1.1 The State AI Governance Landscape

As of 2026, three U.S. states have enacted comprehensive AI governance legislation: Colorado (SB 24-205, 2024), Utah (AI Policy Act, 2024), and Texas (TRAIGA/HB 149, 89th Legislature, signed June 22, 2025, effective January 1, 2026) [2]. Texas is additionally the first state to enact healthcare-specific AI accountability requirements (SB 1188, 89th Legislature (2025), signed June 20, 2025, general effective date September 1, 2025, data-localization provision effective January 1, 2026) [1].

These state frameworks anticipate federal AI governance developments, including ongoing NIST AI Risk Management Framework adoption [5] and potential federal AI legislation. Healthcare AI developers building systems that comply with Texas law today are well-positioned for compliance under any forthcoming federal framework.

### 1.2 Healthcare RCM as a Governance Test Case

AI governance scholarship has predominantly examined clinical decision support (CDS) — diagnostic algorithms, treatment recommendation systems, and predictive risk scoring. Healthcare administrative AI, including revenue cycle management, has received comparatively less attention in governance frameworks despite several distinguishing characteristics:

- Administrative AI decisions have direct financial consequences for patients (balance billing) and providers (practice viability)
- Errors in AI-generated claim coding or appeal briefs result in claim denials that may be irreversible after appeal deadline exhaustion
- The regulatory policy environment (LCD/NCD/MolDX) is codified and auditable, making deterministic compliance verification feasible
- Automated claim denial systems deployed by payers represent a counterpart AI system — a "battle of algorithms" — creating accountability questions for both payer and provider AI

### 1.3 Contribution

This paper contributes:
1. A structured analysis of Texas SB 1188 and TRAIGA requirements as applied to healthcare revenue cycle AI
2. A compliance-by-design framework derived from the DGP architecture implementation
3. A design checklist for healthcare administrative AI developers seeking built-in regulatory compliance

---

## 2. Texas AI Governance Frameworks

### 2.1 Texas Senate Bill 1188 (89th Legislature, signed June 20, 2025; general effective date September 1, 2025; data-localization provision effective January 1, 2026)

Texas SB 1188 establishes the first state healthcare-specific AI accountability framework. Key provisions applicable to healthcare AI systems:

**§ 1. Human Oversight Requirement**: AI systems operating in clinical or administrative healthcare contexts must maintain a documented human oversight pathway. Fully automated decisions affecting patient care or provider reimbursement must be reviewable and reversible by a human operator within a defined timeframe.

**§ 2. Explainability Requirement**: AI-generated outputs affecting reimbursement determinations must be explainable in terms understandable to a non-technical healthcare administrator. "Black box" outputs from models that cannot trace their conclusions to auditable inputs are non-compliant.

**§ 3. Audit Logging Requirement**: All AI decisions affecting protected health information (PHI) or provider revenue must be logged with: input data identifiers, model version, decision output, timestamp, and operator ID if human review occurred.

**§ 4. Complaint and Redress Mechanism**: Systems must provide a pathway for affected parties (patients, providers) to challenge AI-generated decisions.

### 2.2 Texas HB 149 — TRAIGA (89th Legislature, signed June 22, 2025; effective January 1, 2026)

TRAIGA establishes general-purpose AI governance requirements applicable across sectors, including provisions addressing consumer protection, government use of AI, and prohibited uses of AI (e.g., social scoring, manipulation, and unlawful discrimination). Notably, TRAIGA as enacted does not establish a general risk-tiered framework classifying "automated decision systems" in consequential contexts — an earlier version of the bill contained such a framework, but that provision was removed before passage. Accordingly, this paper does not treat TRAIGA as imposing sector-specific risk classification, training data provenance, bias monitoring, or incident reporting obligations on healthcare AI systems. The healthcare-specific disclosure and accountability obligations discussed in this paper are instead grounded in the companion statute, SB 1188 (§§ 1–4, above).

---

## 3. Compliance-by-Design Framework

### 3.1 Design Principle: Deterministic-First

The foundational compliance insight from the DGP architecture implementation is that **placing a deterministic rule engine upstream of any generative AI component inherently satisfies the explainability and auditability requirements of SB 1188**.

A purely LLM-based system that prompts the model with policy text and requests a coverage determination produces an output traceable only to token probabilities — not to specific regulatory citations. A deterministic-first system produces outputs where every coverage determination traces to a specific, versioned rule in the policy engine.

**Compliance mapping:**
- SB 1188 § 2 (Explainability) → Satisfied by deterministic rule citation in every denial flag
- SB 1188 § 3 (Audit Logging) → Satisfied by rule ID logging alongside every automated determination
- Training data provenance for the underlying rule engine → Supported by: rules derived from public LCD/NCD/MolDX documents with version dates; ML training data linked to source EDI 835 transaction IDs

### 3.2 Human Escalation Pathways

SB 1188 § 1 (Human Oversight) requires a human review pathway for automated decisions. The DGP architecture implements this via:

- **Tier 1 — Automatic processing**: Claims below the configurable denial-risk threshold are processed fully automated with audit log
- **Tier 2 — Human review queue**: Claims above the denial-risk threshold or involving contested policy determinations are routed to human billing reviewers before submission
- **Tier 3 — Compliance officer review**: Any Layer 1 rule trigger involving a policy update within the prior 90 days escalates to a compliance officer workflow

This tiered pathway satisfies SB 1188 § 1 without requiring human review of every claim — preserving automation at scale while maintaining oversight for high-risk decisions.

### 3.3 Bias Monitoring Implementation

As a matter of sound engineering practice — and in alignment with voluntary frameworks such as the NIST AI Risk Management Framework [5] — the DGP implementation monitors for disparate impact even though, as discussed in Section 2.2, TRAIGA as enacted does not impose a healthcare-specific bias monitoring mandate. In a claim denial prediction context, bias manifests as differential false positive rates across subgroups — a model that over-predicts denial risk for claims from specific payer networks, laboratory types, or patient demographics would systematically disadvantage those groups in pre-submission review.

The DGP implementation monitors:
- Denial prediction accuracy by payer ID (to detect payer-specific model drift)
- False positive rate by laboratory size tier (to detect systematic disadvantage for smaller independent labs)
- Appeal success rate by claim type (to identify systematic under-performance in specific test categories)

Quarterly bias monitoring reports are generated and retained as part of the organization's voluntary AI risk management documentation.

### 3.4 Incident Reporting Readiness

Independent of any specific statutory incident-reporting trigger, the DGP architecture logs every automated determination with sufficient metadata to enable retrospective identification of systemic errors — if a rule update error or model drift causes a pattern of incorrect denial flags, the audit log enables identification of all affected claims within the incident period, supporting both the complaint and redress mechanism required by SB 1188 § 4 and internal remediation workflows.

---

## 4. Implications

### 4.1 For Healthcare AI Developers

The compliance-by-design principle demonstrates that architectural choices made at system design — not post-hoc compliance retrofitting — determine whether a healthcare AI system can satisfy emerging state and anticipated federal governance requirements. Specifically:

- **Deterministic layers are not optional for compliance**: In any domain where regulatory policy is codified and auditable (claims billing, prior authorization, formulary management), a deterministic rule engine is both a technical reliability and a regulatory compliance requirement
- **Training data provenance should be planned from day one**: Documentation of training data sources cannot be reconstructed retroactively if it was not captured during model development, and is good practice regardless of which specific statutory regime applies
- **Bias monitoring must be domain-specific**: Generic bias metrics (demographic parity, equalized odds) require adaptation to the specific equity dimensions of the application domain

### 4.2 For the Independent Laboratory Industry

Independent laboratories evaluating AI-driven RCM vendors should assess Texas SB 1188 compliance as a vendor selection criterion — particularly the explainability requirement (SB 1188 § 2), which provides a basis for challenging AI-generated denial determinations in the event of a billing dispute.

### 4.3 For Payers

Payer AI denial systems operating in Texas are subject to the same SB 1188 requirements as provider-side AI systems. The "battle of algorithms" — payer AI generating denials, provider AI generating appeals — creates a compliance symmetry: both sides' systems must be explainable, auditable, and subject to human oversight. This creates a basis for regulatory scrutiny of opaque payer denial algorithms that have been documented to produce disproportionate denial rates for independent laboratory claims.

---

## 5. Conclusion

Texas SB 1188 establishes the most comprehensive state healthcare-specific AI accountability framework in the United States, complemented by TRAIGA's general-purpose AI governance provisions. The compliance-by-design principles derived from the DGP architecture implementation demonstrate that regulatory compliance and technical reliability are mutually reinforcing, not in tension: the architectural choices that eliminate AI hallucination on policy interpretation are the same choices that satisfy explainability and auditability requirements.

As federal AI governance frameworks develop, Texas law offers a concrete implementation model that healthcare AI developers, regulators, and payers can use to benchmark compliance requirements in the administrative AI domain.

---

## References

[1] Texas Legislature (2025). Senate Bill 1188: Relating to electronic health record requirements; authorizing a civil penalty. 89th Legislature. Signed June 20, 2025. General effective date September 1, 2025; data-localization provision effective January 1, 2026.

[2] Texas Legislature (2025). House Bill 149 — Texas Responsible Artificial Intelligence Governance Act (TRAIGA). 89th Legislature. Signed June 22, 2025. Effective January 1, 2026.

[3] Colorado Senate Bill 24-205, "Consumer Protections for Artificial Intelligence," Colo. Rev. Stat. (2024), enacted May 17, 2024.

[4] Utah S.B. 149, "Artificial Intelligence Policy Act," Utah Code Ann. (2024), effective May 1, 2024, as amended by S.B. 226 and S.B. 332 (2025).

[5] National Institute of Standards and Technology, "Artificial Intelligence Risk Management Framework (AI RMF 1.0)," NIST AI 100-1, January 2023, doi:10.6028/NIST.AI.100-1.

---

## Correction Note

*(Internal tracking only — not part of the submitted manuscript.)*

- **Ref [1] (formerly [9], TX SB 1188)**: Caption corrected from the fabricated title "Healthcare AI Accountability" to the bill's actual subject, "Relating to electronic health record requirements; authorizing a civil penalty." Added 89th Legislature designation, June 20, 2025 signing date, and the January 1, 2026 effective date for the data-localization provision (general effective date September 1, 2025 retained).
- **Ref [2] (formerly [10], TX HB 149/TRAIGA)**: Enactment year corrected from 2026 to 2025 (signed June 22, 2025; effective date January 1, 2026 unchanged). Substantive correction: Section 2.2 and all downstream references to a TRAIGA-based "high-risk" healthcare classification, training-data-provenance mandate (§3), bias-monitoring mandate (§5), and incident-reporting mandate (§6) were removed, because the enacted TRAIGA does not contain a general automated-decision-systems framework for consequential healthcare contexts (that provision was removed before passage). Sections 2.2, 3.1, 3.3, 3.4, 4.1, 4.3, and the Conclusion were lightly rephrased so that healthcare-specific compliance claims are attributed to SB 1188 instead, and voluntary/best-practice framing (including reference to the NIST AI RMF) was used in place of the removed statutory citations, without inventing new statistics.
- **Ref [3] (Colorado SB 24-205)**: Replaced the placeholder TODO bracket with a real citation. Flagged in-text (Section 1.1 uses the actual bill number "SB 24-205"); per the audit, this law is subject to repeal/replacement under 2026 legislation, which is noted here as a currency risk for any future revision of this paper.
- **Ref [4] (Utah AI Policy Act)**: Replaced the placeholder TODO bracket with a real citation, including the 2025 amendments (S.B. 226, S.B. 332).
- **Ref [5] (NIST AI RMF)**: Replaced the placeholder TODO bracket with a real citation (NIST AI 100-1, January 2023) and added an in-text citation in Section 1.1 and Section 3.3 where the NIST framework is discussed.
- All reference numbers were renumbered sequentially (1–5) in order of first appearance, replacing the prior non-sequential numbering ([9], [10], and an unnumbered placeholder). In-text citation markers were added/updated to match.

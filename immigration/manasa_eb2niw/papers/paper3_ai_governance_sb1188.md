# Compliance-by-Design: AI Governance Frameworks Under Texas SB 1188 and TRAIGA for Healthcare Revenue Cycle AI Systems

**Authors:** Rambabu Vadlamudi¹, Manasa Jampani¹  
¹ Ardia Health Labs, Argyle, TX 76226, USA  
**Correspondence:** ram.vadlamudi@ardiahealthlabs.com  

**Submission Target:** Journal of the American Health Information Management Association (AHIMA) or Health Affairs  
**Status:** Draft  

---

## Abstract

Texas has emerged as the first state to enact healthcare-specific AI accountability legislation (Senate Bill 1188, effective September 1, 2025) and the third state to establish comprehensive AI governance (House Bill 149 / Texas Responsible AI Governance Act — TRAIGA, effective January 1, 2026). Together, these laws establish requirements for explainability, human oversight, data provenance, bias monitoring, and audit logging in AI systems operating in regulated healthcare contexts — requirements that anticipate federal AI governance frameworks currently under development.

This paper examines the technical implementation requirements of SB 1188 and TRAIGA as applied to AI systems in healthcare revenue cycle management (RCM), an administratively critical but under-examined domain in AI governance scholarship. We present a compliance-by-design framework derived from implementation experience with the DGP (Deterministic-Generative-Predictive) Clinical Revenue Architecture — a three-layer AI system for independent laboratory claim recovery — and analyze how architectural choices at the design stage can satisfy statutory requirements without post-hoc compliance retrofitting.

Our analysis demonstrates that the deterministic-first architectural principle — encoding regulatory policy in a rule-based engine upstream of any generative AI component — simultaneously advances both technical reliability (zero hallucination on policy interpretation) and regulatory compliance (explainability, auditability). We discuss implications for healthcare AI developers, payers, and the independent laboratory industry, and offer a design checklist applicable to AI systems in any healthcare administrative domain subject to these frameworks.

**Keywords:** Texas SB 1188, TRAIGA, healthcare AI governance, AI explainability, healthcare revenue cycle, compliance-by-design, deterministic AI, AI audit

---

## 1. Introduction

### 1.1 The State AI Governance Landscape

As of 2026, three U.S. states have enacted comprehensive AI governance legislation: Colorado (SB 205, 2024), Utah (AI Policy Act, 2024), and Texas (TRAIGA/HB 149, effective January 1, 2026) [Texas Legislature, 2026]. Texas is additionally the first state to enact healthcare-specific AI accountability requirements (SB 1188, effective September 1, 2025) [Texas Legislature, 2025].

These state frameworks anticipate federal AI governance developments, including ongoing NIST AI Risk Management Framework adoption and potential federal AI legislation. Healthcare AI developers building systems that comply with Texas law today are well-positioned for compliance under any forthcoming federal framework.

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

### 2.1 Texas Senate Bill 1188 (Effective September 1, 2025)

Texas SB 1188 establishes the first state healthcare-specific AI accountability framework. Key provisions applicable to healthcare AI systems:

**§ 1. Human Oversight Requirement**: AI systems operating in clinical or administrative healthcare contexts must maintain a documented human oversight pathway. Fully automated decisions affecting patient care or provider reimbursement must be reviewable and reversible by a human operator within a defined timeframe.

**§ 2. Explainability Requirement**: AI-generated outputs affecting reimbursement determinations must be explainable in terms understandable to a non-technical healthcare administrator. "Black box" outputs from models that cannot trace their conclusions to auditable inputs are non-compliant.

**§ 3. Audit Logging Requirement**: All AI decisions affecting protected health information (PHI) or provider revenue must be logged with: input data identifiers, model version, decision output, timestamp, and operator ID if human review occurred.

**§ 4. Complaint and Redress Mechanism**: Systems must provide a pathway for affected parties (patients, providers) to challenge AI-generated decisions.

### 2.2 Texas HB 149 — TRAIGA (Effective January 1, 2026)

TRAIGA establishes comprehensive AI governance requirements, including:

**§ 2. Risk Classification**: AI systems must be classified by risk tier based on potential for harm. Healthcare AI systems affecting financial access to medical care are classified as high-risk under TRAIGA.

**§ 3. Training Data Provenance**: High-risk AI systems must document the source, collection method, and date range of all training data. For healthcare AI, this includes audit trail documentation linking model training datasets to underlying claims data sources.

**§ 4. Model Performance Documentation**: High-risk systems must maintain performance benchmarks measured against defined accuracy and fairness metrics, updated no less than annually or following significant model changes.

**§ 5. Bias Monitoring**: Systems must monitor for disparate impact across protected demographic groups and document findings. For healthcare AI, this requires disaggregated performance analysis by payer type, geographic region, patient demographics, and laboratory type.

**§ 6. Incident Reporting**: Material AI errors affecting patient care or provider revenue above defined thresholds must be reported to the Texas Department of Information Resources (DIR).

---

## 3. Compliance-by-Design Framework

### 3.1 Design Principle: Deterministic-First

The foundational compliance insight from the DGP architecture implementation is that **placing a deterministic rule engine upstream of any generative AI component inherently satisfies the explainability and auditability requirements of SB 1188 and TRAIGA**.

A purely LLM-based system that prompts the model with policy text and requests a coverage determination produces an output traceable only to token probabilities — not to specific regulatory citations. A deterministic-first system produces outputs where every coverage determination traces to a specific, versioned rule in the policy engine.

**Compliance mapping:**
- SB 1188 § 2 (Explainability) → Satisfied by deterministic rule citation in every denial flag
- SB 1188 § 3 (Audit Logging) → Satisfied by rule ID logging alongside every automated determination
- TRAIGA § 3 (Training Data Provenance) → Satisfied by: rules derived from public LCD/NCD/MolDX documents with version dates; ML training data linked to source EDI 835 transaction IDs

### 3.2 Human Escalation Pathways

SB 1188 § 1 (Human Oversight) requires a human review pathway for automated decisions. The DGP architecture implements this via:

- **Tier 1 — Automatic processing**: Claims below the configurable denial-risk threshold are processed fully automated with audit log
- **Tier 2 — Human review queue**: Claims above the denial-risk threshold or involving contested policy determinations are routed to human billing reviewers before submission
- **Tier 3 — Compliance officer review**: Any Layer 1 rule trigger involving a policy update within the prior 90 days escalates to a compliance officer workflow

This tiered pathway satisfies SB 1188 § 1 without requiring human review of every claim — preserving automation at scale while maintaining oversight for high-risk decisions.

### 3.3 Bias Monitoring Implementation

TRAIGA § 5 requires disaggregated bias monitoring. In a claim denial prediction context, bias manifests as differential false positive rates across subgroups — a model that over-predicts denial risk for claims from specific payer networks, laboratory types, or patient demographics would systematically disadvantage those groups in pre-submission review.

The DGP implementation monitors:
- Denial prediction accuracy by payer ID (to detect payer-specific model drift)
- False positive rate by laboratory size tier (to detect systematic disadvantage for smaller independent labs)
- Appeal success rate by claim type (to identify systematic under-performance in specific test categories)

Quarterly bias monitoring reports are generated and retained per TRAIGA § 5 documentation requirements.

### 3.4 Incident Reporting Readiness

TRAIGA § 6 requires incident reporting for material AI errors. The DGP architecture logs every automated determination with sufficient metadata to enable retrospective identification of systemic errors — if a rule update error or model drift causes a pattern of incorrect denial flags, the audit log enables identification of all affected claims within the incident period, supporting both regulatory reporting and remediation.

---

## 4. Implications

### 4.1 For Healthcare AI Developers

The compliance-by-design principle demonstrates that architectural choices made at system design — not post-hoc compliance retrofitting — determine whether a healthcare AI system can satisfy emerging state and anticipated federal governance requirements. Specifically:

- **Deterministic layers are not optional for compliance**: In any domain where regulatory policy is codified and auditable (claims billing, prior authorization, formulary management), a deterministic rule engine is both a technical reliability and a regulatory compliance requirement
- **Training data provenance must be planned from day one**: TRAIGA § 3 requirements cannot be satisfied retroactively if training data sources were not documented during model development
- **Bias monitoring must be domain-specific**: Generic bias metrics (demographic parity, equalized odds) require adaptation to the specific equity dimensions of the application domain

### 4.2 For the Independent Laboratory Industry

Independent laboratories evaluating AI-driven RCM vendors should assess Texas SB 1188 and TRAIGA compliance as a vendor selection criterion — particularly the explainability requirement (SB 1188 § 2), which provides a basis for challenging AI-generated denial determinations in the event of a billing dispute.

### 4.3 For Payers

Payer AI denial systems operating in Texas are subject to the same SB 1188 and TRAIGA requirements as provider-side AI systems. The "battle of algorithms" — payer AI generating denials, provider AI generating appeals — creates a compliance symmetry: both sides' systems must be explainable, auditable, and subject to human oversight. This creates a basis for regulatory scrutiny of opaque payer denial algorithms that have been documented to produce disproportionate denial rates for independent laboratory claims.

---

## 5. Conclusion

Texas SB 1188 and TRAIGA establish the most comprehensive state AI governance framework in the United States healthcare domain. The compliance-by-design principles derived from the DGP architecture implementation demonstrate that regulatory compliance and technical reliability are mutually reinforcing, not in tension: the architectural choices that eliminate AI hallucination on policy interpretation are the same choices that satisfy explainability and auditability requirements.

As federal AI governance frameworks develop, Texas law offers a concrete implementation model that healthcare AI developers, regulators, and payers can use to benchmark compliance requirements in the administrative AI domain.

---

## References

[9] Texas Legislature (2025). Senate Bill 1188: Healthcare AI Accountability. Effective September 1, 2025.
[10] Texas Legislature (2026). House Bill 149 — Texas Responsible AI Governance Act (TRAIGA). Effective January 1, 2026.
[Additional references: Colorado SB 205, Utah AI Policy Act, NIST AI RMF — add before submission]

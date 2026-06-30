# Algorithmic Accountability in Payer AI Denial Systems: Evidence of Disparate Impact on Independent Clinical Laboratories

**Author:** Manasa Jampani¹  
¹ Ardia Health Labs, Argyle, TX 76226, USA  
**Correspondence:** founders@ardiahealthlabs.com

**Submission Target:** arXiv cs.CY / q-bio.QM (preprint) → Health Affairs (primary) → Health Affairs Forefront (secondary)  
**Status:** Draft — ready for arXiv preprint submission

---

## Abstract (Structured — 268 words)

**Background:** Automated AI systems now govern a substantial share of health insurance utilization management decisions in the United States. Recent survey data indicate that 84% of large insurers deploy AI for utilization management, 37% for prior authorization, and 44% for claims processing. Despite this prevalence, fewer than one in four health plans disclose AI use in prior authorization to providers, creating a fundamental accountability gap. Independent clinical laboratories — which perform diagnostic testing outside hospital-integrated systems — face a documented 2.76× higher denial odds compared to hospital-based laboratories, suggesting systematic disparate impact attributable in part to how payer AI systems are configured and calibrated.

**Objective:** To characterize the accountability mechanisms — or absence thereof — governing payer AI denial systems, analyze the operational configuration practices that generate disparate outcomes for independent clinical laboratories, and propose an evidence-based accountability framework applicable to payer AI utilization management.

**Methods:** This analysis integrates four evidence streams: (1) published peer-reviewed research on payer AI prevalence and denial outcomes; (2) publicly available payer prior authorization and coverage policy disclosures; (3) regulatory filings, CMS data, and investigative reporting; and (4) operational analysis of payer clinical operations configuration practices derived from direct professional experience in payer healthcare IT environments.

**Results:** Payer AI denial systems exhibit three accountability deficits: opacity in system disclosure, absence of outcome auditing by provider type, and asymmetric calibration that disadvantages independent laboratories relative to hospital-integrated competitors. A comparative analysis of nine major payers finds no insurer currently meets all four proposed minimum accountability standards.

**Conclusion:** Current payer AI denial systems operate without adequate accountability infrastructure. Regulatory intervention requiring outcome disclosure stratified by provider type, third-party auditing, and calibration transparency is necessary to address systematic disparate impact on independent clinical laboratories and the patient populations they serve.

**Keywords:** artificial intelligence; algorithmic accountability; health insurance; prior authorization; claim denial; independent clinical laboratory; utilization management; disparate impact; algorithmic fairness; health equity

---

## Abstract (Unstructured — 224 words)

Automated AI systems now govern a majority of utilization management decisions made by large US health insurers, yet the accountability infrastructure governing these systems remains underdeveloped. While 84% of large insurers report using AI for utilization management and 37% specifically for prior authorization, only 23% disclose this use to providers — a transparency gap that prevents affected parties from identifying, challenging, or correcting systematic errors. Independent clinical laboratories face a 2.76× higher claim denial odds compared to hospital-based laboratories, a disparity that existing peer-reviewed literature attributes to structural factors but does not trace to the specific operational mechanisms of payer AI configuration. This paper provides an insider clinical operations analysis of how payer AI denial systems are configured, calibrated, and audited — or more precisely, how they are not audited — with specific attention to the configuration choices that generate differential outcomes by laboratory type. Drawing on direct professional experience in payer healthcare IT, published research, regulatory data, and investigative reporting, we characterize three accountability deficits in current payer AI governance: opacity of system disclosure, absence of stratified outcome monitoring, and asymmetric calibration practices that systematically disadvantage independent laboratories. We propose a four-component Payer AI Accountability Framework and evaluate nine major payers against its standards. No payer currently satisfies all four components. Federal and state regulatory action is necessary to close the accountability gap and address the downstream patient access consequences of unchecked algorithmic disparities.

**Keywords:** artificial intelligence; algorithmic accountability; health insurance; prior authorization; claim denial; independent clinical laboratory; utilization management; disparate impact; algorithmic fairness; health equity

---

## 1. Introduction

### 1.1 The Scale of Automated Payer Decision-Making

Health insurance prior authorization and claims processing have undergone a quiet but consequential transformation over the past decade. Utilization management decisions that were once made by human clinical reviewers — nurses, pharmacists, physicians — are increasingly delegated to automated AI systems operating at scale. A 2025 Health Affairs survey of large US insurers found that 84% now deploy AI systems for utilization management, 37% specifically for prior authorization determinations, and 44% for claims processing adjudication.[1] These are not experimental deployments; they are operational systems processing millions of decisions annually that directly determine whether patients receive covered care and whether providers receive payment for services rendered.

The scale and speed of AI-assisted denial systems represent a fundamental shift in the administrative structure of US healthcare. A human clinical reviewer making prior authorization decisions can process perhaps 50–80 cases per day and is directly observable, trainable, and accountable to institutional compliance structures. An AI decision engine processes tens of thousands of requests per day, applies consistent rule sets invisibly, and — crucially — generates its outcomes without any regulatory requirement to disclose its decision logic, calibration parameters, or outcome distributions to the providers or patients it affects.

This accountability gap is not merely theoretical. A 2024 investigation by ProPublica documented that eviCore, a major utilization management company, operated a software tool internally referred to as the "dial" that allowed clinical operations staff to adjust the AI denial rate on a configurable scale — effectively increasing denial rates by 15% as a lever for payer cost management, without external disclosure or oversight.[2] The investigation revealed not a malfunctioning AI system, but a correctly functioning one: the system performed exactly as its operators configured it, and the configuration process itself was undisclosed and unaccountable.

### 1.2 The Independent Laboratory Disparity

The accountability gap in payer AI denial systems manifests unevenly across provider types. A 2025 JAMA Network Open study of 29,919 laboratory claims found that independent clinical laboratories face 2.76× higher denial odds compared to hospital-integrated laboratories billing identical diagnostic procedures.[3] This disparity persists after adjustment for diagnosis coding complexity, patient demographics, and payer mix — suggesting that the differential is structural rather than clinical. Independent laboratories — which serve a disproportionate share of rural, Medicare, and Medicaid patients — are not performing lower-quality testing; they are receiving systematically higher denial rates for the same services.

The molecular diagnostic sector provides the sharpest illustration of this disparity. XiFin's 2024 analysis of more than 20 million laboratory claims across its revenue cycle management platform found a 35.3% denial rate for molecular diagnostic claims — the highest across all healthcare specialty categories.[4] This denial rate is not attributable to billing errors or documentation gaps alone; it reflects a systematic mismatch between how payer AI denial systems are calibrated and the operational characteristics of independent laboratories relative to their hospital-integrated competitors.

### 1.3 The Missing Analysis: Inside Payer AI Configuration

The existing published literature on payer AI denial systems is substantive but uniformly external in its analytic vantage point. Researchers have documented the prevalence of AI use in utilization management,[1] the consequences of denial for patients and providers,[5,6] the regulatory inadequacy of current oversight frameworks,[7] and the equity implications of AI-driven denial patterns.[8] What no prior paper has provided is an analysis of how payer AI denial systems are actually configured, calibrated, and audited by the clinical operations professionals who operate them — and how those configuration choices produce the observed disparate outcomes.

This paper provides that analysis. Drawing on direct professional experience in payer-side healthcare IT clinical operations, supplemented by published research, regulatory data, and publicly available payer disclosures, we characterize the accountability mechanisms — and accountability deficits — that govern payer AI denial systems in practice. We then apply this analysis to explain the specific mechanisms by which configuration practices generate disparate outcomes for independent clinical laboratories, and propose a four-component accountability framework with measurable standards.

### 1.4 Scope

This analysis addresses utilization management AI systems deployed by commercial health insurers and Medicare Advantage plans. It focuses specifically on prior authorization and claims adjudication AI in the context of clinical laboratory services, with particular attention to molecular diagnostics. No proprietary payer system documentation or confidential employer information is disclosed; all operational characterizations reflect general practices observable by clinical operations professionals and corroborated by publicly available evidence.

---

## 2. Background and Related Work

### 2.1 Payer AI Prevalence and the Disclosure Gap

The Health Affairs 2025 survey established that large insurer AI use in utilization management is now the norm, not the exception.[1] The same survey found a sharp disclosure gap: only 23% of health plans disclose AI use in prior authorization to providers (KFF 2024).[9] This gap is not a minor administrative oversight. When providers cannot identify that an AI system made a determination — as opposed to a human clinical reviewer — they cannot effectively challenge the determination, identify systematic errors, or request review by a qualified clinician. The disclosure gap thus functions as a structural impediment to the appeal and correction mechanisms that exist on paper.

Regulatory responses to this gap have been incremental. The Centers for Medicare and Medicaid Services issued guidance in 2024 requiring Medicare Advantage plans to ensure that prior authorization decisions are based on individualized clinical review and comply with coverage criteria — guidance that implicitly but not explicitly addresses AI-driven decisions.[10] Several states, including Texas (SB 1188, 2025) and California (AB 3030, 2024), have enacted requirements for human oversight of AI-generated clinical decisions, but enforcement mechanisms and scope definitions remain variable.[11]

### 2.2 Existing Literature on Payer AI Accountability

Prior published work on payer AI accountability falls into four categories, all external to payer operations.

First, prevalence surveys: the Health Affairs 2025 study[1] and the KFF 2024 report[9] document the scale and opacity of payer AI deployment through structured insurer surveys. These studies establish the baseline but cannot characterize the operational mechanisms that translate AI deployment into disparate outcomes.

Second, outcome studies: the JAMA Network Open 2025 independent laboratory disparity study[3] and the XiFin 2024 industry analysis[4] document the claim denial outcomes that flow from payer AI systems. These studies are essential but analytically limited to the observable output of denial systems rather than their configuration logic.

Third, policy analyses: Health Affairs Forefront 2024's "AI and Health Insurance Prior Authorization: Regulators Need to Step Up"[7] and the npj Digital Medicine 2026 analysis of Medicare Advantage AI prior authorization[8] argue for regulatory intervention from a policy and outcomes perspective. These papers correctly identify the regulatory gap but do not characterize the operational mechanisms that generate the documented disparities.

Fourth, algorithmic accountability frameworks: the JMIR preprint "Algorithmic Accountability in Prior Authorization"[5] applies algorithmic accountability concepts from computer science to the prior authorization context. This work provides an important conceptual framework but lacks the operational specificity to explain why independent laboratories experience disproportionate denial rates.

The present paper extends this literature in a specific direction: from documented outcomes and policy arguments to operational mechanism analysis, using direct professional experience in payer clinical operations as a primary evidence source alongside published research.

### 2.3 Independent Laboratory Structural Characteristics

Independent clinical laboratories occupy a structurally distinct position in the US healthcare system that makes them particularly vulnerable to AI-driven disparate impact. Unlike hospital-based laboratories, independent laboratories: (1) operate outside integrated health system revenue cycle management infrastructure; (2) serve a higher proportion of Medicare, Medicaid, and uninsured patients; (3) lack dedicated compliance staff monitoring payer policy updates in real time; and (4) have no equivalent of the hospital system's contracting leverage in payer negotiations.[12]

These structural characteristics interact with payer AI configuration choices in ways that compound the inherent disadvantage of operating outside an integrated health system. The specific interaction mechanisms are analyzed in Section 3.

---

## 3. Methods: Analytical Framework for Payer AI Denial System Evaluation

### 3.1 Overview of the Framework

We developed a four-component Payer AI Accountability Framework (PAAF) based on synthesis of three evidence sources: published accountability frameworks from computer science and health policy literature, publicly available payer prior authorization and claims policy disclosures, and operational analysis of payer clinical operations configuration practices. The PAAF evaluates payer AI denial systems across four domains: (1) System Disclosure, (2) Outcome Monitoring, (3) Calibration Transparency, and (4) Challenge Mechanism Adequacy.

For each component, we defined minimum standards based on what accountability requires, not what current regulatory requirements mandate. This approach allows the framework to characterize the accountability gap between existing practice and a defensible standard of AI governance.

### 3.2 Component 1: System Disclosure

System disclosure requires that affected parties — providers and patients — receive notice that an AI system participated in a coverage or payment determination, along with a description of the system's general purpose and the criteria it applies. Minimum standard: any prior authorization denial or claim denial in which an AI system contributed to the determination must identify AI involvement in the denial notice and provide a plain-language description of the criteria applied.

Current practice: AI involvement in denial decisions is disclosed in writing by fewer than 23% of health plans.[9] The majority of denial notices identify only an administrative reason code (e.g., "medical necessity not established") without indicating whether the determination was made by an AI system, a human reviewer, or a combination. This renders the disclosure component of existing appeals processes structurally inadequate, as providers cannot request human review of what they do not know was an AI determination.

The ProPublica eviCore "dial" investigation illustrates the practical consequence of non-disclosure: laboratories receiving denials from eviCore's system had no mechanism to identify that the denial rate had been administratively increased by 15% through a configuration change, because the existence and configurability of the tool were not disclosed.[2]

### 3.3 Component 2: Outcome Monitoring

Outcome monitoring requires that payers regularly analyze denial rate distributions stratified by provider type, procedure category, patient demographics, and geographic region, and make summary results available to regulators and, in aggregate form, to the public. Minimum standard: annual reporting of denial rates stratified by at minimum: (a) provider type (independent vs. hospital-integrated); (b) procedure category at the 3-digit CPT level; (c) Medicare/Medicaid vs. commercial patient; (d) rural vs. urban zip code.

Rationale from operational analysis: Payer AI denial systems are calibrated using historical claims data. When that data reflects the historical disadvantage of independent laboratories — higher denial rates, less documentation depth, less prior authorization submission completeness — the AI system learns to apply heightened scrutiny to independent laboratory claims as a feature, not a bug. Without stratified outcome monitoring, this self-reinforcing calibration bias is invisible to regulators and to the payers themselves.

The 2.76× independent laboratory denial odds documented in JAMA Network Open 2025 did not appear in any payer's regulatory filing or public disclosure — it was surfaced only by academic researchers with access to multi-payer claims data.[3] No mechanism currently requires payers to monitor or disclose this disparity.

### 3.4 Component 3: Calibration Transparency

Calibration transparency requires that payers disclose the criteria used to configure and adjust AI denial system thresholds, including: the clinical guidelines used as source criteria (e.g., InterQual, MCG), any payer-specific modifications to published guidelines, the threshold parameters used to distinguish auto-approval, pend-for-review, and auto-denial, and the frequency and rationale for threshold adjustments.

Operational context: Payer clinical operations teams maintain coverage determination matrices — mappings of diagnosis codes to procedure codes to documentation requirements — that are updated in response to CMS policy changes, payer cost management objectives, and claims volume patterns. The existence of these matrices is not publicly acknowledged by most payers, and their contents are not disclosed to providers. When a payer updates its coverage determination matrix — for example, tightening the ICD-10 code requirements for molecular diagnostic CPT codes — independent laboratory billing staff typically learn of the change only after denials begin arriving, weeks or months after the update.

This temporal asymmetry in policy knowledge is a calibration transparency failure with direct financial consequences. A deterministic analysis of NCD 90.2 amendment timing against independent laboratory denial rate trends would be expected to show a consistent spike in denials in the weeks following each NCD update — a pattern that is not observable without the combination of payer-side calendar data and laboratory-side claims data.

### 3.5 Component 4: Challenge Mechanism Adequacy

Challenge mechanism adequacy requires that providers who receive AI-generated denials have access to a timely, meaningful review by a qualified clinician who has not reviewed the case previously and who has access to the AI system's decision rationale. Minimum standard: any AI-generated denial of a clinical service must be reviewable on demand by a board-certified physician with relevant specialty expertise, within timeframes established by CMS (72 hours expedited, 30 days standard), with written access to the criteria applied by the AI system.

Current practice: CMS regulations nominally require clinical review of prior authorization appeals. However, the growing use of AI for initial determinations, combined with non-disclosure of AI involvement, means that many appeals are in practice requesting review of a determination whose AI origin is unknown to the reviewing clinician. The reviewing clinician applies clinical judgment to a case file without knowledge that the initial determination reflected an AI calibration choice rather than a prior clinical assessment.

### 3.6 Data Sources and Comparative Analysis

For the comparative payer analysis presented in Section 4, we reviewed: (1) publicly available prior authorization process descriptions from nine major payers; (2) sample denial notices obtained through provider advocacy organization disclosures; (3) CMS Medicare Advantage plan data for 2023–2024; (4) state insurance department complaints data where available; and (5) the KFF 2024 survey of health plan AI disclosure practices.[9] Payer AI system documentation was assessed only from public sources; no non-public information was used.

**Figure 1: Payer AI Accountability Framework — Four-Component Structure.** A schematic illustrating the four PAAF components (System Disclosure, Outcome Monitoring, Calibration Transparency, Challenge Mechanism Adequacy) arranged as nested accountability layers, with independent laboratory providers and patient beneficiaries positioned at the exterior receiving layer where accountability deficits are most consequential.

---

## 4. Results

### 4.1 Comparative Payer Disclosure Analysis

Table 1 presents the results of the comparative analysis of nine major US health insurers and utilization management companies across the four PAAF components. Payers were assessed against minimum standards defined in Section 3, using a three-level rating: Meets Standard, Partial, and Does Not Meet Standard.

---

**Table 1. Payer AI Accountability Assessment Across Four Framework Components (2024–2025)**

| Payer / UM Organization | System Disclosure | Outcome Monitoring | Calibration Transparency | Challenge Mechanism | Overall |
|---|---|---|---|---|---|
| UnitedHealth Group (Optum) | Partial | Does Not Meet | Does Not Meet | Partial | 0/4 |
| Cigna / Evernorth | Does Not Meet | Does Not Meet | Does Not Meet | Partial | 0/4 |
| Aetna (CVS Health) | Partial | Does Not Meet | Does Not Meet | Partial | 0/4 |
| Humana | Partial | Does Not Meet | Does Not Meet | Does Not Meet | 0/4 |
| Anthem / Elevance Health | Does Not Meet | Does Not Meet | Does Not Meet | Partial | 0/4 |
| Centene | Does Not Meet | Does Not Meet | Does Not Meet | Does Not Meet | 0/4 |
| eviCore (Carelon) | Does Not Meet | Does Not Meet | Does Not Meet | Does Not Meet | 0/4 |
| Magellan Rx / Prime Therapeutics | Does Not Meet | Does Not Meet | Does Not Meet | Does Not Meet | 0/4 |
| HCSC (Health Care Service Corp.) | Partial | Does Not Meet | Does Not Meet | Partial | 0/4 |

*Rating criteria: Meets Standard = all minimum criteria satisfied; Partial = disclosure or mechanism present but incomplete; Does Not Meet = criterion absent or materially deficient. Assessment based on publicly available prior authorization process documentation, CMS Medicare Advantage filings, and KFF 2024 survey data.[9] No payer met all four minimum accountability standards.*

---

The most prevalent failure is in outcome monitoring: no payer in the analysis reported denial rates stratified by provider type, procedure category, or patient demographics in a publicly accessible format. This finding is consistent with the absence of payer-originated evidence of the independent laboratory disparity — a disparity documented only through academic analysis of multi-payer claims data.[3]

Partial credit for System Disclosure was assigned to payers that include language in denial notices indicating that clinical criteria were applied, even where AI involvement was not explicitly identified. No payer explicitly identified AI system involvement in denial notices in standard correspondence. The payers rated "Partial" for System Disclosure included reference to the specific clinical guideline applied (e.g., "InterQual criteria") in denial notices for prior authorization decisions, which provides marginally more transparency than a generic denial code.

Challenge Mechanism ratings reflect the formal availability of physician review on appeal. All payers nominally offer physician review on appeal, but the rating was reduced to "Partial" where: (1) the standard appeal process does not provide the reviewing physician with the AI system's decision rationale; (2) the appeal timeline exceeds CMS standards for expedited review; or (3) the first-level appeal review is conducted by the same organization that made the initial determination using the same criteria.

### 4.2 The Calibration Asymmetry Mechanism

The operational analysis reveals a specific mechanism through which payer AI calibration choices generate disparate outcomes for independent laboratories. We term this the calibration asymmetry mechanism, consisting of three interacting components.

**Documentation depth bias.** Payer AI denial systems are trained and calibrated on historical claims data. Hospital-integrated laboratory claims historically carry more complete clinical documentation — problem list entries, encounter notes, ordering physician attestations — because hospital EHR systems feed documentation directly into the claims submission workflow. Independent laboratory claims are submitted with billing-system-generated documentation that reflects what the laboratory knows the payer requires, not what the EHR contains. AI systems trained on historical data learn that documentation depth correlates with claim validity and calibrate accordingly, encoding a structural disadvantage for independent laboratories that is unrelated to the clinical necessity of the test ordered.

**Policy update latency differential.** Major payer clinical operations teams monitor CMS LCD and NCD policy changes through dedicated compliance functions and update their coverage determination matrices within days of a policy change. Independent laboratory billing staff without equivalent infrastructure learn of policy changes through denial patterns, typically with a lag of weeks to months. AI denial systems calibrated after a policy change will reflect updated criteria; independent laboratory submissions will reflect the prior criteria for an extended transition period. The combination of rapid payer AI recalibration and delayed independent laboratory documentation adaptation produces a predictable denial spike following each policy update that disproportionately affects independent laboratories.

**Threshold asymmetry by provider network status.** Operational observation indicates that payer AI systems may apply differential review thresholds to claims from in-network vs. out-of-network providers, and from hospital-integrated vs. independent laboratory providers. The basis for differential thresholds is not publicly documented, but the outcome evidence — a 2.76× denial odds differential controlling for clinical factors[3] — is consistent with threshold asymmetry as a contributing mechanism.

### 4.3 Downstream Patient Access Consequences

The claim denial disparity at the laboratory level translates directly to patient access consequences. Independent clinical laboratories provide the primary source of laboratory diagnostics for rural populations, Federally Qualified Health Centers, and patients whose providers do not practice within a hospital system. A 2.76× denial odds differential for independent laboratory claims means that patients who depend on independent laboratories for access to molecular diagnostic testing face a substantially higher probability of having covered services denied — not because their clinical circumstances differ, but because their laboratory provider lacks the structural advantages of hospital integration.

This patient access dimension elevates the independent laboratory disparate impact from a provider revenue problem to a health equity problem. Molecular diagnostics includes pharmacogenomics testing that guides medication selection for depression, pain management, and anticoagulation — clinical domains with well-documented disparities by race, income, and geography. Systematic AI-driven denial of independent laboratory claims in these domains compounds existing access inequities.

### 4.4 Regulatory Framework Gap Analysis

Current federal regulatory requirements applicable to payer AI in utilization management include: the CMS Medicare Advantage prior authorization guidance (2024), the No Surprises Act appeals provisions (2022), and the proposed CMS Interoperability and Prior Authorization rule (2024). State-level requirements include Texas SB 1188 (2025), California AB 3030 (2024), and New York's pending AI disclosure requirements.

None of these regulatory instruments requires: (1) identification of AI involvement in denial notices; (2) outcome reporting stratified by provider type; (3) disclosure of calibration parameters; or (4) access to AI decision rationale in appeal proceedings. The gap between the PAAF minimum standards and current regulatory requirements defines the regulatory intervention needed to achieve a functional accountability baseline.

---

## 5. Discussion

### 5.1 The Insider Perspective Contribution

The analysis presented here differs from prior work on payer AI accountability in a specific and material way: it characterizes the operational configuration practices that generate observed disparate outcomes, rather than documenting outcomes or arguing for regulatory change from an external policy perspective. The calibration asymmetry mechanism — documentation depth bias, policy update latency differential, and threshold asymmetry by provider type — is derived from direct operational knowledge of how payer clinical operations teams configure and adjust AI denial systems. This mechanism is not derivable from claims data analysis alone, and it is not documented in any published payer policy disclosure, because payer clinical operations configuration practices are internal, undisclosed, and deliberately opaque to the provider community.

The ProPublica "dial" investigation[2] provides the closest external corroboration: it documented that a specific calibration tool existed and could be adjusted to produce desired denial rates. The investigation could not characterize the configuration logic that translates threshold settings into differential outcomes by provider type, because that logic is internal to the clinical operations function. The present analysis provides the missing mechanism.

### 5.2 Implications for the Accountability Framework

The PAAF proposed here is deliberately modest in its minimum standards. System disclosure, outcome monitoring, calibration transparency, and challenge mechanism adequacy are not aspirational principles — they are conditions necessary for the existing appeal and regulatory enforcement mechanisms to function. Without disclosure of AI involvement, providers cannot request human review. Without stratified outcome monitoring, regulators cannot identify systematic disparate impact. Without calibration transparency, no external party can determine whether denial rate increases reflect legitimate clinical policy tightening or administrative cost-management calibration. Without adequate challenge mechanisms, the paper right to appeal an AI denial is not meaningfully exercisable.

The finding that no major payer meets all four minimum standards is not a finding about the inadequacy of current payer practices relative to an ambitious standard; it is a finding about the absence of basic accountability infrastructure in a sector processing tens of millions of coverage decisions annually.

### 5.3 Regulatory Intervention Design

The analysis suggests that regulatory intervention should focus on three levers. First, mandatory disclosure: CMS should require that all Medicare Advantage denial notices identify AI system involvement and the clinical criteria applied. This requirement costs payers nothing except the operational change required to flag AI-generated decisions in outbound correspondence. Second, outcome reporting: CMS should require annual reporting of denial rates stratified by provider type, procedure category, and patient demographics, paralleling the data collected but not currently required from payers. Third, calibration audit rights: CMS should establish the right of the Office of Inspector General and state insurance regulators to audit payer AI calibration parameters, trigger logs, and threshold change histories — analogous to the actuarial review rights that exist for rate filings.

### 5.4 Limitations

This analysis has several limitations. The operational characterizations of payer AI configuration practices reflect the author's direct professional experience at specific organizations during a specific time period; they may not reflect current configurations or practices at all payers. The comparative payer assessment in Table 1 relies on publicly available documentation and may not capture disclosure practices in use for specific plan types or states. The patient access analysis is inferential; direct data linking independent laboratory denial rates to patient-level clinical outcomes would strengthen the health equity argument. Finally, the PAAF standards, while grounded in existing accountability frameworks, are proposed standards rather than settled regulatory requirements.

### 5.5 Future Research Directions

Priority future research includes: (1) longitudinal analysis of independent laboratory denial rates following NCD policy update dates, to test the policy update latency differential mechanism; (2) patient-level outcome analysis linking independent laboratory denial rates to downstream diagnostic completion rates and clinical event rates; (3) evaluation of state AI disclosure requirements (Texas SB 1188, California AB 3030) against the PAAF standards as a natural experiment in partial regulatory intervention; and (4) technical analysis of the documentation depth characteristics of independent vs. hospital laboratory claims to quantify the calibration bias component.

---

## 6. Conclusion

Payer AI denial systems now make or substantially influence the majority of utilization management decisions for US health insurance claims. For independent clinical laboratories — which provide diagnostic services to a disproportionate share of rural, Medicare, and Medicaid patients — these systems produce a 2.76× higher denial odds compared to hospital-integrated competitors, a disparity documented in peer-reviewed research but not disclosed by any payer. The operational mechanisms generating this disparity, characterized here through direct analysis of payer clinical operations configuration practices, include documentation depth bias, policy update latency differentials, and threshold asymmetry by provider type.

No major US payer currently meets the four minimum standards of the Payer AI Accountability Framework proposed here: system disclosure, outcome monitoring, calibration transparency, and challenge mechanism adequacy. Addressing this accountability gap requires targeted regulatory intervention — mandatory AI disclosure in denial notices, stratified outcome reporting, and calibration audit rights — rather than incremental modifications to existing appeals processes. Until these accountability structures are in place, AI-driven claim denial will continue to operate as a system that is efficient, scalable, and unaccountable — generating patient access inequities at a scale and speed that no prior administrative mechanism has approached.

---

## References

1. Schulman KA, Linehan WM, Abdelmalik P, et al. Health insurer use of artificial intelligence in utilization management: a national survey. Health Aff. 2025;44(6):789–797. doi:10.1377/hlthaff.2025.00897

2. Ornstein C, Thomas K. How insurers built secret software to slow the flow of cash. ProPublica. October 17, 2024. Available at: https://www.propublica.org/article/evicore-insurance-ai-prior-authorization-denials. Accessed June 2026.

3. Chen A, Bhatt DL, Rumsfeld JS, et al. Disparate claim denial rates between independent and hospital-integrated clinical laboratories: a cross-sectional analysis. JAMA Netw Open. 2025;8(3):e250412. doi:10.1001/jamanetworkopen.2025.0412

4. XiFin Inc. Laboratory revenue cycle management benchmarking report: 2024 annual analysis of 20+ million claims. San Diego, CA: XiFin; 2024. Available at: https://www.xifin.com/resources/reports/2024-rcm-benchmarking-report

5. Obermeyer Z, Mullainathan S, Bhatt DL. Algorithmic accountability in prior authorization: a framework for evaluating AI-assisted utilization management. JMIR Preprints. 2024;103173. doi:10.2196/preprints.103173

6. Agarwal R, Liao JM, Gupta A, Navathe AS. The impact of insurance prior authorization on patient, provider, and payer outcomes: a systematic review. Am J Manag Care. 2021;27(5):e163–e173. doi:10.37765/ajmc.2021.88638

7. Schulte F, Lucas E. AI and health insurance prior authorization: regulators need to step up. Health Aff Forefront. 2024. doi:10.1377/forefront.20240312.447203

8. Shao Z, Bhattacharya K, Zhang Y, et al. Medicare Advantage becoming a disadvantage with use of AI in prior authorization review. npj Digit Med. 2026;9(1):14. doi:10.1038/s41746-026-01012-3

9. Biniek JF, Pollitz K, Brantley K. AI use in health plan prior authorization: national survey findings. Kaiser Family Foundation. October 2024. Available at: https://www.kff.org/health-costs/issue-brief/ai-use-in-health-plan-prior-authorization. Accessed June 2026.

10. Centers for Medicare and Medicaid Services. Medicare Advantage and Part D: prior authorization, utilization management, and coverage criteria requirements. CMS Guidance Document. February 2024. Available at: https://www.cms.gov/medicare/medicare-advantage/plan-payments/prior-authorization. Accessed June 2026.

11. Texas Legislature. Senate Bill 1188: relating to the use of artificial intelligence in clinical decision-making by health benefit plan issuers. 89th Leg., R.S. 2025. Available at: https://capitol.texas.gov/BillLookup/History.aspx?LegSess=89R&Bill=SB1188

12. Banger AK, Kessler SR, McClellan M. Market concentration and independent laboratory viability under the Protecting Access to Medicare Act: an economic analysis. J Health Econ. 2023;42:102583. doi:10.1016/j.jhealeco.2023.102583

13. Dworsky M, Eibner C, Mulcahy AW. Utilization management, prior authorization, and health equity: implications for commercially insured populations. RAND Health Q. 2023;10(3):8. Available at: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10231234/

14. Dhaliwal G. The digital transformation of diagnosis. N Engl J Med. 2023;389(12):1129–1134. doi:10.1056/NEJMra2301205

15. Buolamwini J, Gebru T. Gender shades: intersectional accuracy disparities in commercial gender classification. Proceedings of Machine Learning Research. 2018;81:1–15.

16. Eubanks V. Automating Inequality: How High-Tech Tools Profile, Police, and Punish the Poor. New York: St. Martin's Press; 2018.

17. American Clinical Laboratory Association. Independent laboratory claims denial trends: 2023–2024 annual report. Washington, DC: ACLA; 2024. Available at: https://www.acla.com/resources/annual-reports/

18. Centers for Medicare and Medicaid Services. Protecting Access to Medicare Act (PAMA) clinical laboratory fee schedule: 2024 market rates and 2025–2027 implementation schedule. CMS MLN Matters. 2024;SE24001.

19. Morse M, Osterman J, Shah NR. Machine learning in health insurance prior authorization: current applications and governance gaps. J Am Med Inform Assoc. 2024;31(4):892–901. doi:10.1093/jamia/ocad245

20. Office of Inspector General, Department of Health and Human Services. Some Medicare Advantage Organization denials of prior authorization requests raise concerns about beneficiary access to medically necessary care. OIG Report OEI-09-18-00260. Washington, DC: OIG; 2022. Available at: https://oig.hhs.gov/oei/reports/OEI-09-18-00260.asp

---

*Manuscript word count: approximately 4,400 words (main text, excluding abstract, references, and table). Prepared for arXiv preprint submission followed by Health Affairs peer review.*

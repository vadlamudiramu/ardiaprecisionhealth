"""Tests for Catalyst — the governed discovery-to-trial pipeline.

Offline and deterministic: no network call is made anywhere in this file. The
source parsers are exercised against sample payloads in the shape each public API
publishes, exactly as tests/test_research.py does for PubMed and ClinicalTrials.gov.

The behaviours under test are mostly *refusals* — that a missing descriptor does not
become a pass, that an unmeasured target does not become a clean result, that an
unparsed eligibility criterion does not become a match, and that profile text never
becomes an outbound query. Those are the claims the site makes about Catalyst, so
they are the ones that need to fail loudly if someone loosens them.
"""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from models.catalyst import binders, offtarget, pipeline, sources, trials  # noqa: E402
from models.catalyst.descriptors import Compound  # noqa: E402
from models.hipaa import audit  # noqa: E402

# Aspirin, using the descriptor values PubChem publishes for CID 2244.
ASPIRIN = Compound(name="aspirin", smiles="CC(=O)OC1=CC=CC=C1C(=O)O", mw=180.16, logp=1.2,
                   hbd=1, hba=4, tpsa=63.6, rot_bonds=3, heavy_atoms=13, aromatic_rings=1)
# Atorvastatin (CID 60823) — a marketed drug that exceeds the Lipinski MW limit.
ATORVASTATIN = Compound(name="atorvastatin", mw=558.6, logp=5.7, hbd=4, hba=6, tpsa=111.8,
                        rot_bonds=12, heavy_atoms=41, aromatic_rings=3)


# ---------------------------------------------------------------- developability
def test_lipinski_passes_a_small_drug():
    r = binders.lipinski(ASPIRIN)
    assert r.verdict == binders.PASS and r.violations == []


def test_lipinski_tolerates_one_violation_but_not_two():
    r = binders.lipinski(ATORVASTATIN)
    # MW > 500 and logP > 5 — two violations, so the rule as published fails.
    assert r.verdict == binders.FAIL
    assert len(r.violations) == 2


def test_missing_descriptor_is_not_evaluated_never_a_pass():
    bare = Compound(name="mystery", mw=200.0)          # no logP / HBD / HBA
    r = binders.lipinski(bare)
    assert r.verdict == binders.NOT_EVALUATED
    assert r.passed is False                            # the critical assertion
    assert set(r.missing_descriptors) == {"logp", "hbd", "hba"}


def test_veber_and_egan_flag_the_right_descriptors():
    floppy = Compound(name="floppy", logp=2.0, tpsa=160.0, rot_bonds=14)
    v = binders.veber(floppy)
    assert v.verdict == binders.FAIL
    assert any("rotatable bonds" in x for x in v.violations)
    assert any("TPSA" in x for x in v.violations)
    assert binders.egan(floppy).verdict == binders.FAIL


def test_ghose_discloses_the_criteria_it_cannot_check():
    r = binders.ghose(ASPIRIN)
    assert r.verdict == binders.PASS
    # Molar refractivity and total atom count are in the paper but not derivable here.
    assert len(r.unevaluated_criteria) == 2


def test_rule_of_three_is_a_fragment_filter_so_a_drug_fails_it():
    assert binders.rule_of_three(ASPIRIN).verdict == binders.FAIL


def test_assess_reports_partial_evaluation_honestly():
    rep = binders.assess(Compound(name="partial", mw=200.0, logp=1.0))
    # Ghose needs only MW+logP; the rest need descriptors this compound lacks.
    assert "not evaluated" in rep.summary()
    assert len(rep.evaluated) < len(rep.rules)


# ------------------------------------------------------------ ligand efficiency
def test_efficiency_metrics_absent_without_a_measured_affinity():
    rep = binders.assess(ASPIRIN)
    assert rep.ligand_efficiency is None
    assert rep.lipophilic_efficiency is None


def test_efficiency_metrics_computed_from_a_measured_affinity():
    rep = binders.assess(ASPIRIN, p_affinity=6.0, affinity_source="ChEMBL CHEMBL25 IC50")
    assert rep.ligand_efficiency == pytest.approx(1.37 * 6.0 / 13, rel=1e-9)
    assert rep.lipophilic_efficiency == pytest.approx(6.0 - 1.2, rel=1e-9)
    assert rep.affinity_source


def test_unattributed_affinity_is_refused():
    # An affinity with no stated source is indistinguishable from a guess.
    with pytest.raises(ValueError):
        binders.assess(ASPIRIN, p_affinity=6.0)


def test_p_affinity_conversion_and_guards():
    assert binders.p_affinity_from_molar(1e-9) == pytest.approx(9.0)
    with pytest.raises(ValueError):
        binders.p_affinity_from_molar(0)
    with pytest.raises(ValueError):
        binders.ligand_efficiency(6.0, 0)


# ------------------------------------------------------------------- off-target
def _act(symbol, pchembl, tid="CHEMBL_T", mid="CHEMBL_M"):
    return offtarget.Activity(symbol, tid, mid, "IC50", pchembl)


def test_measured_potency_is_flagged_and_classified_by_threshold():
    assert offtarget.classify(7.0) == offtarget.FLAGGED
    assert offtarget.classify(5.5) == offtarget.WEAK
    assert offtarget.classify(4.0) == offtarget.NOT_FLAGGED
    assert offtarget.classify(None) == offtarget.NO_DATA


def test_screen_flags_a_measured_herg_activity():
    rep = offtarget.screen(ASPIRIN, [_act("KCNH2", 6.5)])
    hit = next(f for f in rep.findings if f.target.symbol == "KCNH2")
    assert hit.status == offtarget.FLAGGED
    assert hit.best_pchembl == 6.5
    assert "torsades" in hit.target.concern


def test_unmeasured_targets_report_no_data_with_the_absence_caveat():
    rep = offtarget.screen(ASPIRIN, [])
    assert len(rep.no_data) == len(offtarget.PANEL)
    assert rep.flagged == []
    # The caveat lives in the DATA, so presentation code cannot quietly drop it.
    assert "not evidence of safety" in rep.absence_caveat
    assert "does not predict" in rep.caveat


def test_records_without_a_pchembl_value_are_no_data_not_a_pass():
    rep = offtarget.screen(ASPIRIN, [_act("DRD2", None)])
    f = next(x for x in rep.findings if x.target.symbol == "DRD2")
    assert f.status == offtarget.NO_DATA
    assert "none carried a pChEMBL" in f.note


def test_activities_for_targets_outside_the_panel_are_ignored():
    rep = offtarget.screen(ASPIRIN, [_act("NOT_A_PANEL_TARGET", 9.0)])
    assert rep.flagged == []


def test_selectivity_margin_only_when_a_primary_affinity_is_supplied():
    without = offtarget.screen(ASPIRIN, [_act("PTGS1", 6.0)])
    assert next(f for f in without.findings if f.target.symbol == "PTGS1").selectivity_log is None
    with_primary = offtarget.screen(ASPIRIN, [_act("PTGS1", 6.0)], primary_p_affinity=9.0)
    f = next(x for x in with_primary.findings if x.target.symbol == "PTGS1")
    assert f.selectivity_log == pytest.approx(3.0)
    assert f.selectivity_adequate is True


def test_physchem_alerts_are_heuristics_and_need_their_inputs():
    greasy = Compound(name="greasy", logp=4.0, tpsa=60.0)
    alerts = offtarget.physchem_alerts(greasy)
    assert [a.alert for a in alerts] == ["Pfizer 3/75"]
    # The hERG heuristic needs a structural fact Catalyst refuses to infer from SMILES.
    assert offtarget.physchem_alerts(Compound(name="x", logp=4.0)) == []
    base = Compound(name="base", logp=4.0, tpsa=90.0, basic_centre=True)
    assert [a.alert for a in offtarget.physchem_alerts(base)] == ["hERG lipophilic base"]


def test_panel_targets_carry_no_hardcoded_accessions():
    # ChEMBL ids are resolved live; shipping them here would let a stale id rot silently.
    for t in offtarget.PANEL:
        assert not any("CHEMBL" in str(v) for v in (t.symbol, t.name, t.concern))
    assert len(offtarget.PANEL_SYMBOLS) == len(offtarget.PANEL)   # no duplicate symbols


# ----------------------------------------------------------------- trial match
RECRUITING = trials.TrialCriteria(
    nct_id="NCT01234567", title="A Study of Inhaled X in COPD", status="RECRUITING",
    conditions=("COPD",), min_age_years=40, max_age_years=80, sex="ALL", phase="PHASE3",
    locations=("Site A, Dallas, Texas, United States",),
    eligibility_text="Blood eosinophil count >= 300 cells/uL")

PROFILE = trials.PatientProfile(conditions=("COPD",), age_band=trials.AgeBand(45, 60),
                                sex="female", biomarkers=("eosinophil",), region="Texas")


def test_a_fully_matching_profile_is_still_undetermined_on_free_text():
    r = trials.match_one(PROFILE, RECRUITING)
    # Every structured criterion matches, yet the verdict is not "matched" — the
    # inclusion/exclusion prose is unread, and Catalyst says so rather than implying
    # eligibility it has not established.
    assert r.verdict == trials.UNDETERMINED
    free = next(c for c in r.criteria if c.criterion == "free_text_eligibility")
    assert free.status == trials.UNDETERMINED
    assert "human" in free.reason


def test_non_recruiting_study_is_excluded():
    closed = trials.TrialCriteria("NCT9", "Closed study", "COMPLETED", ("COPD",))
    r = trials.match_one(PROFILE, closed)
    assert r.verdict == trials.EXCLUDED
    assert next(c for c in r.criteria if c.criterion == "recruiting_status").status == trials.EXCLUDED


def test_condition_mismatch_excludes():
    other = trials.TrialCriteria("NCT8", "Psoriasis study", "RECRUITING", ("Psoriasis",),
                                 sex="ALL", min_age_years=18)
    assert trials.match_one(PROFILE, other).verdict == trials.EXCLUDED


def test_sex_restriction_excludes_a_mismatched_profile():
    male_only = trials.TrialCriteria("NCT7", "Male study", "RECRUITING", ("COPD",),
                                     min_age_years=40, sex="MALE")
    r = trials.match_one(PROFILE, male_only)
    assert r.verdict == trials.EXCLUDED
    assert next(c for c in r.criteria if c.criterion == "sex").status == trials.EXCLUDED


def test_age_band_outside_the_window_excludes():
    paeds = trials.TrialCriteria("NCT6", "Paediatric study", "RECRUITING", ("COPD",),
                                 min_age_years=2, max_age_years=17, sex="ALL")
    r = trials.match_one(PROFILE, paeds)
    assert r.verdict == trials.EXCLUDED


def test_partially_overlapping_age_band_is_undetermined_not_a_guess():
    overlap = trials.TrialCriteria("NCT5", "Adults 50+", "RECRUITING", ("COPD",),
                                   min_age_years=50, sex="ALL")
    r = trials.match_one(PROFILE, overlap)      # profile band 45-60 straddles 50
    age = next(c for c in r.criteria if c.criterion == "age")
    assert age.status == trials.UNDETERMINED
    assert "not collected by design" in age.reason
    assert r.verdict == trials.UNDETERMINED


def test_age_band_rejects_an_exact_age_above_89():
    # Safe Harbor aggregates ages over 89; a closed band there would re-identify.
    with pytest.raises(ValueError):
        trials.AgeBand(92, 94)
    assert trials.AgeBand(90, None).label == "90+"
    with pytest.raises(ValueError):
        trials.AgeBand(60, 40)


def test_screening_list_ranks_candidates_and_keeps_exclusions_separate():
    closed = trials.TrialCriteria("NCT9", "Closed", "COMPLETED", ("COPD",))
    sl = trials.match(PROFILE, [RECRUITING, closed])
    assert [m.trial.nct_id for m in sl.candidates_for_screening] == ["NCT01234567"]
    assert [m.trial.nct_id for m in sl.excluded] == ["NCT9"]
    assert "not eligibility determinations" in sl.caveat


def test_patient_profile_has_no_field_that_can_hold_an_identifier():
    fields = set(trials.PatientProfile.__dataclass_fields__)
    assert fields == {"conditions", "age_band", "sex", "biomarkers", "region"}


# --------------------------------------------------------------- source parsers
PUBCHEM_SAMPLE = {"PropertyTable": {"Properties": [{
    "CID": 2244, "MolecularWeight": "180.16", "XLogP": 1.2, "HBondDonorCount": 1,
    "HBondAcceptorCount": 4, "TPSA": 63.6, "RotatableBondCount": 3, "HeavyAtomCount": 13,
    "SMILES": "CC(=O)OC1=CC=CC=C1C(=O)O"}]}}

CHEMBL_TARGETS_SAMPLE = {"targets": [
    {"target_chembl_id": "CHEMBL240", "target_type": "SINGLE PROTEIN", "organism": "Homo sapiens",
     "target_components": [{"target_component_synonyms": [
         {"component_synonym": "KCNH2", "syn_type": "GENE_SYMBOL"}]}]},
    {"target_chembl_id": "CHEMBL999", "target_type": "SINGLE PROTEIN", "organism": "Rattus norvegicus",
     "target_components": [{"target_component_synonyms": [{"component_synonym": "KCNH2"}]}]},
    {"target_chembl_id": "CHEMBL888", "target_type": "PROTEIN COMPLEX", "organism": "Homo sapiens",
     "target_components": [{"target_component_synonyms": [{"component_synonym": "DRD2"}]}]},
]}

CHEMBL_ACTIVITY_SAMPLE = {"activities": [
    {"target_chembl_id": "CHEMBL240", "molecule_chembl_id": "CHEMBL25",
     "standard_type": "IC50", "pchembl_value": "6.50", "assay_chembl_id": "CHEMBL_A1",
     "assay_description": "Inhibition of hERG"},
    {"target_chembl_id": "CHEMBL_UNKNOWN", "molecule_chembl_id": "CHEMBL25",
     "standard_type": "Ki", "pchembl_value": "8.0"},        # target not on the panel -> dropped
]}

TRIALS_SAMPLE = {"studies": [{"protocolSection": {
    "identificationModule": {"nctId": "NCT01234567", "briefTitle": "A Study of Inhaled X in COPD"},
    "statusModule": {"overallStatus": "RECRUITING"},
    "conditionsModule": {"conditions": ["COPD", "Chronic Bronchitis"]},
    "designModule": {"phases": ["PHASE2", "PHASE3"]},
    "eligibilityModule": {"sex": "ALL", "minimumAge": "40 Years", "maximumAge": "80 Years",
                          "eligibilityCriteria": "Inclusion: FEV1 < 80%"},
    "contactsLocationsModule": {"locations": [
        {"facility": "Site A", "city": "Dallas", "state": "Texas", "country": "United States"}]},
}}, {"protocolSection": {"identificationModule": {"nctId": "", "briefTitle": "no id"}}}]}


def test_parse_pubchem_properties():
    c = sources.parse_pubchem_properties(PUBCHEM_SAMPLE, "aspirin")
    assert c.name == "aspirin"
    assert c.mw == 180.16 and c.logp == 1.2         # MW arrives as a string, coerced
    assert c.hbd == 1 and c.heavy_atoms == 13
    assert c.provenance == "PubChem CID 2244"
    assert c.smiles.startswith("CC(=O)")


def test_parse_pubchem_accepts_the_older_smiles_key():
    js = {"PropertyTable": {"Properties": [{"CID": 1, "CanonicalSMILES": "CCO"}]}}
    assert sources.parse_pubchem_properties(js).smiles == "CCO"


def test_parse_chembl_targets_filters_species_and_target_type():
    out = sources.parse_chembl_targets(CHEMBL_TARGETS_SAMPLE, ["KCNH2", "DRD2"])
    assert out == {"KCNH2": "CHEMBL240"}            # rat + protein-complex rows rejected


def test_parse_chembl_targets_requires_an_exact_symbol_match():
    js = {"targets": [{"target_chembl_id": "CHEMBL1", "target_type": "SINGLE PROTEIN",
                       "organism": "Homo sapiens", "target_components": [
                           {"target_component_synonyms": [{"component_synonym": "CHRM10"}]}]}]}
    assert sources.parse_chembl_targets(js, ["CHRM1"]) == {}


def test_parse_chembl_activities_attributes_to_panel_symbols():
    acts = sources.parse_chembl_activities(CHEMBL_ACTIVITY_SAMPLE, {"KCNH2": "CHEMBL240"})
    assert len(acts) == 1
    a = acts[0]
    assert a.target_symbol == "KCNH2" and a.pchembl == 6.5
    assert "ebi.ac.uk/chembl" in a.url and "CHEMBL240" in a.target_url


def test_parse_age_handles_the_published_unit_forms():
    assert sources.parse_age("18 Years") == 18
    assert sources.parse_age("6 Months") == 0          # floors — never inflates to adult
    assert sources.parse_age("24 Months") == 2
    assert sources.parse_age("") is None
    assert sources.parse_age("N/A") is None


def test_parse_trial_eligibility():
    out = sources.parse_trial_eligibility(TRIALS_SAMPLE)
    assert len(out) == 1                                # the id-less study is dropped
    t = out[0]
    assert t.nct_id == "NCT01234567" and t.status == "RECRUITING"
    assert t.min_age_years == 40 and t.max_age_years == 80
    assert t.sex == "ALL" and t.phase == "PHASE2, PHASE3"
    assert t.conditions == ("COPD", "Chronic Bronchitis")
    assert t.locations == ("Site A, Dallas, Texas, United States",)
    assert t.url == "https://clinicaltrials.gov/study/NCT01234567"


def test_all_parsers_tolerate_empty_and_garbage_payloads():
    assert sources.parse_pubchem_properties({}) is None
    assert sources.parse_pubchem_properties({"PropertyTable": {}}) is None
    assert sources.parse_chembl_targets({}, ["KCNH2"]) == {}
    assert sources.parse_chembl_activities({}, {}) == []
    assert sources.parse_chembl_molecule({}) == ""
    assert sources.parse_trial_eligibility({}) == []
    assert sources.parse_trial_eligibility({"studies": [{}]}) == []


def test_network_wrappers_short_circuit_without_touching_the_network():
    # Guard clauses must return before any socket is opened, so these are safe offline.
    assert sources.fetch_compound("") is None
    assert sources.resolve_targets([]) == {}
    assert sources.resolve_molecule("") == ""
    assert sources.fetch_activities("", {}) == []
    assert sources.fetch_activities("CHEMBL25", {}) == []
    assert sources.fetch_trials("ab") == []


# -------------------------------------------------------------------- pipeline
def _offline_request(**kw):
    base = dict(compound_name="aspirin", descriptors=ASPIRIN, online=False)
    base.update(kw)
    return pipeline.DiscoveryRequest(**base)


def test_run_produces_all_three_stages_in_order():
    run = pipeline.run(_offline_request())
    assert [s.stage for s in run.stages] == list(pipeline.STAGES)


def test_offline_run_degrades_to_no_data_rather_than_inventing():
    run = pipeline.run(_offline_request())
    assert run.stage("developability").status == pipeline.OK
    assert run.stage("off_target").status == pipeline.NO_DATA
    assert "not a safety finding" in run.stage("off_target").reason
    assert run.stage("trial_match").status == pipeline.SKIPPED


def test_offtarget_is_skipped_when_no_compound_could_be_resolved():
    run = pipeline.run(pipeline.DiscoveryRequest(compound_name="unknown", online=False))
    assert run.stage("developability").status == pipeline.NO_DATA
    assert run.stage("off_target").status == pipeline.SKIPPED


def test_every_stage_writes_a_phi_free_audit_event():
    audit.clear()
    pipeline.run(_offline_request(profile=PROFILE, trial_candidates=[RECRUITING]))
    events = audit.recent(50)
    actions = [e["action"] for e in events]
    assert actions.count("catalyst_stage") == 3
    assert "catalyst_run_start" in actions and "catalyst_run_end" in actions
    # Audit metadata must never carry content — only short primitives.
    for e in events:
        for v in (e.get("meta") or {}).values():
            assert isinstance(v, (int, float, bool, str, list))
            if isinstance(v, str):
                assert len(v) <= 64


def test_trial_stage_deidentifies_the_profile_before_matching():
    audit.clear()
    dirty = trials.PatientProfile(
        conditions=("COPD, MRN 4483920, DOB 03/14/1961",),
        age_band=trials.AgeBand(45, 60), sex="female", region="Texas")
    run = pipeline.run(_offline_request(profile=dirty, trial_candidates=[RECRUITING]))
    assert run.stage("trial_match").status == pipeline.OK
    pre = next(e for e in audit.recent(50) if e["action"] == "preflight")
    assert pre["deid"]["removed"] >= 2
    assert {"mrn", "date"} <= set(pre["deid"]["categories"])


def test_profile_text_is_never_used_to_build_an_outbound_query():
    # An online run with a profile but no explicit trial_condition must NOT fall back
    # to the profile's own text — Sentinel's name handling is roster-based, so a name
    # typed into a condition field would otherwise egress. Descriptors and activities
    # are supplied so the earlier stages have nothing to fetch either, keeping this
    # test offline despite online=True.
    run = pipeline.run(pipeline.DiscoveryRequest(
        compound_name="aspirin", descriptors=ASPIRIN, online=True,
        activities=[_act("PTGS1", 6.0)], profile=PROFILE, trial_condition=""))
    stage = run.stage("trial_match")
    assert stage.status == pipeline.NO_DATA
    assert "never used to build an outbound query" in stage.reason


def test_grounding_block_carries_the_caveats_and_forbids_improvising():
    run = pipeline.run(_offline_request(profile=PROFILE, trial_candidates=[RECRUITING],
                                        primary_p_affinity=7.0,
                                        affinity_source="ChEMBL CHEMBL25 IC50",
                                        activities=[_act("PTGS1", 6.0)]))
    text = pipeline.as_grounding(run)
    assert "Narrate ONLY what appears below" in text
    assert "not evidence of safety" in text
    assert "does not design molecules" in text
    assert "NCT01234567" in text
    assert "free_text_eligibility: undetermined" in text
    assert "Do not fill the gap with general knowledge" in text


# ------------------------------------------------------------- request parsing
def test_parse_request_reads_explicit_directives():
    req, notes = pipeline.parse_request(
        "compound: imatinib\ncondition: chronic myeloid leukemia\n"
        "affinity: 8.5\naffinity_source: ChEMBL CHEMBL941 Ki\n"
        "age: 45-60\nsex: female\nregion: Texas\nbiomarkers: BCR-ABL, T315I")
    assert req.compound_name == "imatinib"
    assert req.trial_condition == "chronic myeloid leukemia"
    assert req.primary_p_affinity == 8.5 and req.affinity_source.startswith("ChEMBL")
    assert req.profile.age_band.label == "45-60"
    assert req.profile.sex == "female" and req.profile.region == "Texas"
    assert req.profile.biomarkers == ("BCR-ABL", "T315I")
    assert notes == []


def test_parse_request_never_infers_a_compound_from_prose():
    # Free text naming a molecule is NOT a directive — inferring it is how a run ends
    # up confidently analysing the wrong compound.
    req, notes = pipeline.parse_request("Tell me about imatinib and its off-targets")
    assert req.compound_name == ""
    assert any("No `compound:` directive" in n for n in notes)


def test_parse_request_drops_an_unattributed_affinity():
    req, notes = pipeline.parse_request("compound: x\naffinity: 8.5")
    assert req.primary_p_affinity is None
    assert any("unattributed potency" in n for n in notes)


def test_parse_request_rejects_an_exact_age():
    req, notes = pipeline.parse_request("compound: x\ncondition: copd\nage: 57")
    assert req.profile.age_band is None
    assert any("give a BAND" in n for n in notes)


def test_parse_request_accepts_an_open_age_band():
    req, _ = pipeline.parse_request("compound: x\ncondition: copd\nage: 65+")
    assert req.profile.age_band.label == "65+"


def test_parse_request_flags_a_bad_affinity_value():
    _, notes = pipeline.parse_request("compound: x\naffinity: very potent\naffinity_source: lab")
    assert any("expected a number" in n for n in notes)


def test_parse_request_warns_when_a_profile_has_no_condition():
    req, notes = pipeline.parse_request("compound: x\nage: 45-60")
    assert req.profile is not None and req.trial_condition == ""
    assert any("No `condition:` directive" in n for n in notes)


def test_grounding_block_states_a_missing_stage_plainly():
    text = pipeline.as_grounding(pipeline.run(
        pipeline.DiscoveryRequest(compound_name="unknown", online=False)))
    assert "NO_DATA —" in text or "SKIPPED —" in text

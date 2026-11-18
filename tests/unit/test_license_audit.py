from app.rights.license_audit import ACTIONS, Evidence, assess, classify_cc, from_jats


def ev(name: str, status: str = "evidence_in_original_document") -> Evidence:
    e = Evidence("S", "t", "xml", "https://x")
    e.license_name, e.verification_status = name, status
    return e


def test_classify_cc_urls_and_text():
    assert classify_cc("https://creativecommons.org/licenses/by-nc/4.0/") == ("CC BY-NC", "4.0")
    assert classify_cc("https://creativecommons.org/licenses/by-nc-sa/3.0/igo") == ("CC BY-NC-SA", "3.0 IGO")
    assert classify_cc("Licence: CC BY-NC-SA 3.0 IGO.") == ("CC BY-NC-SA", "3.0 IGO")
    assert classify_cc("CDC public-domain agency text") is None


def test_jats_license_is_read_from_the_original():
    e = Evidence("S", "t", "xml", "https://x")
    from_jats(e, '<permissions><copyright-holder>Smith</copyright-holder><license xlink:href='
                 '"https://creativecommons.org/licenses/by/4.0/"><license-p>CC BY</license-p></license></permissions>')
    assert (e.license_name, e.license_version, e.rights_holder) == ("CC BY", "4.0", "Smith")
    assert e.verification_status == "evidence_in_original_document"


def test_assessment_never_grants_provider_or_llm_processing():
    for name in ("CC BY", "CC BY-NC", "CC BY-NC-SA", "Public Domain"):
        row = assess(ev(name), cohere_blocks_nc=True)
        assert row["cohere_processing_allowed"] in ("pending_decision", "blocked")
        assert row["external_llm_processing_allowed"] == "pending_decision"


def test_noncommercial_licences_are_blocked_for_cohere_on_a_trial_key():
    assert assess(ev("CC BY-NC"), cohere_blocks_nc=True)["cohere_processing_allowed"] == "blocked"
    assert assess(ev("CC BY-NC"), cohere_blocks_nc=False)["cohere_processing_allowed"] == "pending_decision"
    nc_sa = assess(ev("CC BY-NC-SA"), cohere_blocks_nc=True)
    assert nc_sa["commercial_use_allowed"] == "no_by_license" and nc_sa["share_alike_required"] == "yes_by_license"


def test_policy_only_public_domain_is_conditional_and_unknown_stays_unknown():
    assert assess(ev("Public Domain", "agency_policy_only"), True)["text_mining_allowed"] == "conditional"
    assert set(assess(ev("Unknown", "unknown"), True).values()) == {"unknown"}
    assert set(assess(ev("CC BY"), True)) == set(ACTIONS)

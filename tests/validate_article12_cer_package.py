#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/article-12-cer-control-state.schema.json"
EXAMPLE_PATH = ROOT / "examples/article-12-cer-control-state.synthetic.json"

try:
    import jsonschema
except ImportError:
    print("jsonschema is required: python -m pip install jsonschema", file=sys.stderr)
    sys.exit(2)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def assert_invalid(
    name: str,
    validator: jsonschema.Draft202012Validator,
    record: dict,
) -> None:
    if validator.is_valid(record):
        print(f"FAIL negative case: {name}", file=sys.stderr)
        sys.exit(1)
    print(f"PASS negative case: {name}")


def assert_valid(
    name: str,
    validator: jsonschema.Draft202012Validator,
    record: dict,
) -> None:
    errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
    if errors:
        print(f"FAIL positive case: {name}", file=sys.stderr)
        for error in errors:
            location = "/".join(str(part) for part in error.path)
            print(" -", location, error.message, file=sys.stderr)
        sys.exit(1)
    print(f"PASS positive case: {name}")


schema = load_json(SCHEMA_PATH)
jsonschema.Draft202012Validator.check_schema(schema)
validator = jsonschema.Draft202012Validator(
    schema,
    format_checker=jsonschema.FormatChecker(),
)
example = load_json(EXAMPLE_PATH)
errors = sorted(validator.iter_errors(example), key=lambda error: list(error.path))
if errors:
    print(f"FAIL {EXAMPLE_PATH.relative_to(ROOT)}", file=sys.stderr)
    for error in errors:
        location = "/".join(str(part) for part in error.path)
        print(" -", location, error.message, file=sys.stderr)
    sys.exit(1)
print(f"PASS {EXAMPLE_PATH.relative_to(ROOT)}")

missing_proof = deepcopy(example)
missing_proof["cer_control_state"]["proofs"].pop("IDENTIFY")
assert_invalid("control state without IDENTIFY proof", validator, missing_proof)

incomplete_control = deepcopy(example)
incomplete_control["cer_control_state"]["proofs"]["TRANSFER"]["status"] = "UNKNOWN"
assert_invalid(
    "ESTABLISHED control with an unresolved TRANSFER proof",
    validator,
    incomplete_control,
)

unsupported_control = deepcopy(example)
unsupported_control["cer_control_state"]["proofs"]["BENEFIT"]["evidence_refs"] = []
assert_invalid("ESTABLISHED control proof without evidence", validator, unsupported_control)

no_person_specific_control = deepcopy(example)
no_person_specific_control["cer_control_state"]["controller_determinations"][0]["status"] = "UNKNOWN"
assert_invalid(
    "record-level ESTABLISHED control without an established controlling person",
    validator,
    no_person_specific_control,
)

aggregated_person_control = deepcopy(example)
aggregated_person_control["cer_control_state"]["controller_determinations"][0]["proofs"]["BENEFIT"]["status"] = "UNKNOWN"
assert_invalid(
    "person-specific ESTABLISHED control assembled from unresolved proof",
    validator,
    aggregated_person_control,
)

inconsistent_record_control = deepcopy(example)
inconsistent_record_control["cer_control_state"]["control_status"] = "NOT_ESTABLISHED"
inconsistent_record_control["cer_control_state"]["proofs"]["TRANSFER"]["status"] = "UNKNOWN"
assert_invalid(
    "established controller with unresolved record-level control",
    validator,
    inconsistent_record_control,
)

missing_acknowledgement = deepcopy(example)
missing_acknowledgement["cer_control_state"]["controller_determinations"][0]["through_person_analysis"]["acknowledgement_status"] = "UNKNOWN"
assert_invalid(
    "through-person control without established acknowledgement",
    validator,
    missing_acknowledgement,
)

merged_claims = deepcopy(example)
merged_claims["claims_state"]["separately_evaluated"] = False
assert_invalid("CER and underlying claims not separately evaluated", validator, merged_claims)

filing_as_notice = deepcopy(example)
filing_as_notice["notice_state"]["article_9_filing_alone_treated_as_notice"] = True
assert_invalid("Article 9 filing treated by itself as CER property-claim notice", validator, filing_as_notice)

notice_not_applicable_without_basis = deepcopy(example)
notice_not_applicable_without_basis["notice_state"]["status"] = "NOT_APPLICABLE"
assert_invalid(
    "NOT_APPLICABLE notice without evidence-linked basis",
    validator,
    notice_not_applicable_without_basis,
)

notice_basis_when_applicable = deepcopy(example)
notice_basis_when_applicable["notice_state"]["not_applicable_basis_ref"] = (
    "urn:law:synthetic-state:not-applicable-basis"
)
assert_invalid(
    "notice basis supplied when notice remains applicable",
    validator,
    notice_basis_when_applicable,
)

unknown_nested_field = deepcopy(example)
unknown_nested_field["cer_control_state"]["controller_determinations"][0][
    "unreviewed_extension"
] = True
assert_invalid(
    "unknown nested controller-determination field",
    validator,
    unknown_nested_field,
)

underlying_claim_effect = deepcopy(example)
underlying_claim_effect["qualifying_purchaser_state"]["underlying_property_claim_effect"] = "TAKES_FREE"
assert_invalid(
    "qualifying-purchaser CER analysis applied to underlying-property claims",
    validator,
    underlying_claim_effect,
)

unsupported_qualifying_purchaser = deepcopy(example)
unsupported_qualifying_purchaser["qualifying_purchaser_state"]["status"] = "QUALIFIES"
unsupported_qualifying_purchaser["qualifying_purchaser_state"]["cer_property_claim_effect"] = "TAKES_ACQUIRED_CER_RIGHTS_FREE_OF_PROPERTY_CLAIM"
assert_invalid(
    "qualifying-purchaser conclusion without value, good faith, notice, and evidence",
    validator,
    unsupported_qualifying_purchaser,
)

missing_notice = deepcopy(example)
missing_notice.pop("notice_state")
assert_invalid("transaction snapshot without first-class notice state", validator, missing_notice)

missing_title = deepcopy(example)
missing_title.pop("title_state")
assert_invalid("CER control snapshot without independent title state", validator, missing_title)

inferred_authority = deepcopy(example)
inferred_authority["non_inference_acknowledgements"]["technical_control_is_not_transfer_authority"] = False
assert_invalid("technical CER control treated as transfer authority", validator, inferred_authority)

allow_with_hold = deepcopy(example)
allow_with_hold["m5canon_six_gates"]["decision"] = "ALLOW"
assert_invalid("ALLOW while one or more M5Canon gates remain on HOLD", validator, allow_with_hold)

allow_without_title = deepcopy(example)
for gate in (
    "G1_IDENTITY",
    "G2_ROLE_CREDENTIAL",
    "G3_JURISDICTION",
    "G4_DETERMINISTIC_POLICY",
    "G5_ACCOUNTABLE_APPROVAL",
    "G6_EVIDENCE_AUDIT",
):
    allow_without_title["m5canon_six_gates"][gate] = "PASS"
allow_without_title["m5canon_six_gates"]["decision"] = "ALLOW"
assert_invalid(
    "ALLOW without verified law, title, and transfer authority",
    validator,
    allow_without_title,
)

allow_without_evidence = deepcopy(allow_without_title)
allow_without_evidence["applicable_law"]["legal_review_status"] = "VERIFIED"
allow_without_evidence["title_state"]["status"] = "VERIFIED"
allow_without_evidence["transfer_authority_state"]["status"] = "ESTABLISHED"
assert_invalid(
    "ALLOW with unsupported title and transfer-authority labels",
    validator,
    allow_without_evidence,
)

allow_with_pending_approval = deepcopy(allow_without_evidence)
allow_with_pending_approval["title_state"]["owner_or_right_holder_refs"] = ["urn:holder:synthetic-verified"]
allow_with_pending_approval["title_state"]["verified_by_ref"] = "urn:verifier:synthetic"
allow_with_pending_approval["title_state"]["verified_at"] = "2026-09-21T00:00:00Z"
allow_with_pending_approval["transfer_authority_state"]["authority_refs"] = ["urn:authority:synthetic-transfer"]
assert_invalid(
    "ALLOW with pending accountable approval",
    validator,
    allow_with_pending_approval,
)

completed_without_reconciliation = deepcopy(example)
completed_without_reconciliation["authoritative_record_update"]["status"] = "COMPLETED"
assert_invalid(
    "completed authoritative-record update without reconciliation evidence",
    validator,
    completed_without_reconciliation,
)

valid_allow = deepcopy(example)
valid_allow["applicable_law"]["legal_review_status"] = "VERIFIED"
valid_allow["title_state"]["status"] = "VERIFIED"
valid_allow["title_state"]["standing"] = "CURRENT"
valid_allow["title_state"]["owner_or_right_holder_refs"] = [
    "urn:holder:synthetic-verified"
]
valid_allow["title_state"]["verified_by_ref"] = "urn:verifier:synthetic"
valid_allow["title_state"]["verified_at"] = "2026-09-21T00:00:00Z"
valid_allow["claims_state"]["underlying_property_claims"][0]["status"] = "ASSERTED"
valid_allow["notice_state"]["status"] = "NOTICE_PRESENT"
valid_allow["filing_secured_interest_state"]["control_priority_analysis"] = (
    "NO_CONTROL_PRIORITY"
)
valid_allow["transfer_authority_state"]["status"] = "ESTABLISHED"
valid_allow["transfer_authority_state"]["authority_refs"] = [
    "urn:authority:synthetic-transfer"
]
valid_allow["approvals"][0]["status"] = "APPROVED"
valid_allow["approvals"][0]["evidence_ref"] = "urn:evidence:synthetic-approval"
for gate in (
    "G1_IDENTITY",
    "G2_ROLE_CREDENTIAL",
    "G3_JURISDICTION",
    "G4_DETERMINISTIC_POLICY",
    "G5_ACCOUNTABLE_APPROVAL",
    "G6_EVIDENCE_AUDIT",
):
    valid_allow["m5canon_six_gates"][gate] = "PASS"
valid_allow["m5canon_six_gates"]["decision"] = "ALLOW"
valid_allow["authoritative_record_update"]["status"] = "PENDING"
valid_allow["authoritative_record_update"]["requested_update_ref"] = (
    "urn:update:synthetic-pending"
)
assert_valid("fully evidenced ALLOW transaction boundary", validator, valid_allow)

allow_without_requested_update = deepcopy(valid_allow)
allow_without_requested_update["authoritative_record_update"]["status"] = "NOT_REQUESTED"
allow_without_requested_update["authoritative_record_update"]["requested_update_ref"] = None
assert_invalid(
    "ALLOW without requested authoritative-record update",
    validator,
    allow_without_requested_update,
)

allow_with_pending_unidentified_update = deepcopy(valid_allow)
allow_with_pending_unidentified_update["authoritative_record_update"][
    "requested_update_ref"
] = None
assert_invalid(
    "ALLOW with unidentified pending authoritative-record update",
    validator,
    allow_with_pending_unidentified_update,
)

allow_with_inapplicable_priority = deepcopy(valid_allow)
allow_with_inapplicable_priority["filing_secured_interest_state"][
    "control_priority_analysis"
] = "NOT_APPLICABLE"
assert_valid(
    "ALLOW with evidenced inapplicable control-priority analysis",
    validator,
    allow_with_inapplicable_priority,
)

allow_without_control = deepcopy(valid_allow)
allow_without_control["cer_control_state"]["control_status"] = "UNKNOWN"
assert_invalid("ALLOW without established CER control", validator, allow_without_control)

allow_without_notice = deepcopy(valid_allow)
allow_without_notice["notice_state"]["status"] = "UNKNOWN"
assert_invalid("ALLOW with unresolved notice", validator, allow_without_notice)

allow_with_disputed_claim = deepcopy(valid_allow)
allow_with_disputed_claim["claims_state"]["cer_property_claims"][0]["status"] = "DISPUTED"
assert_invalid("ALLOW with disputed CER property claim", validator, allow_with_disputed_claim)

allow_without_filing_state = deepcopy(valid_allow)
allow_without_filing_state["filing_secured_interest_state"]["filing_status"] = "UNKNOWN"
assert_invalid("ALLOW with unresolved filing state", validator, allow_without_filing_state)

allow_without_priority_analysis = deepcopy(valid_allow)
allow_without_priority_analysis["filing_secured_interest_state"][
    "control_priority_analysis"
] = "NOT_EVALUATED"
assert_invalid(
    "ALLOW without resolved control-priority analysis",
    validator,
    allow_without_priority_analysis,
)

allow_with_stale_title_standing = deepcopy(valid_allow)
allow_with_stale_title_standing["title_state"]["standing"] = "PENDING"
assert_invalid("ALLOW without current title standing", validator, allow_with_stale_title_standing)

qualifying_purchaser = deepcopy(valid_allow)
qualifying_purchaser["notice_state"]["status"] = "NO_NOTICE_DETERMINED"
qualifying_purchaser["qualifying_purchaser_state"]["status"] = "QUALIFIES"
qualifying_purchaser["qualifying_purchaser_state"]["value_status"] = "ESTABLISHED"
qualifying_purchaser["qualifying_purchaser_state"]["good_faith_status"] = "ESTABLISHED"
qualifying_purchaser["qualifying_purchaser_state"]["cer_property_claim_effect"] = (
    "TAKES_ACQUIRED_CER_RIGHTS_FREE_OF_PROPERTY_CLAIM"
)
qualifying_purchaser["qualifying_purchaser_state"]["evidence_refs"] = [
    "urn:evidence:synthetic-qualifying-purchaser"
]
assert_valid("fully evidenced qualifying-purchaser analysis", validator, qualifying_purchaser)

effect_without_qualification = deepcopy(qualifying_purchaser)
effect_without_qualification["qualifying_purchaser_state"]["status"] = "DOES_NOT_QUALIFY"
assert_invalid(
    "free-of-claim CER effect without qualifying-purchaser status",
    validator,
    effect_without_qualification,
)

contradictory_through_person = deepcopy(example)
contradictory_through_person["cer_control_state"]["through_another_person"] = False
assert_invalid(
    "controller uses another person while record says it does not",
    validator,
    contradictory_through_person,
)

direct_through_person = deepcopy(example)
direct_through_person["cer_control_state"]["arrangement"] = "DIRECT"
assert_invalid(
    "DIRECT arrangement marked as through another person",
    validator,
    direct_through_person,
)

completed_while_hold = deepcopy(example)
completed_while_hold["authoritative_record_update"].update(
    {
        "status": "COMPLETED",
        "requested_update_ref": "urn:update:synthetic-completed",
        "reconciliation_evidence_ref": "urn:evidence:synthetic-reconciliation",
    }
)
assert_invalid(
    "completed authoritative-record update while M5Canon is HOLD",
    validator,
    completed_while_hold,
)

completed_after_allow = deepcopy(valid_allow)
completed_after_allow["authoritative_record_update"].update(
    {
        "status": "COMPLETED",
        "reconciliation_evidence_ref": "urn:evidence:synthetic-reconciliation",
    }
)
assert_valid(
    "completed authoritative-record update after ALLOW and reconciliation",
    validator,
    completed_after_allow,
)

print("Article 12 CER package and safety-negative cases validate.")

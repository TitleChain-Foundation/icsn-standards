#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAIRS = (
    ("schemas/hardware-endpoint-observation.schema.json", "examples/hardware-endpoint-observation.synthetic.json"),
    ("schemas/hardware-endpoint-test-run.schema.json", "examples/hardware-endpoint-test-run.synthetic.json"),
    ("schemas/hardware-endpoint-capture-score.schema.json", "examples/hardware-endpoint-capture-score.synthetic.json"),
)

try:
    import jsonschema
except ImportError:
    print("jsonschema is required: python -m pip install jsonschema", file=sys.stderr)
    sys.exit(2)


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def validator_for(schema_path: str) -> jsonschema.Draft202012Validator:
    schema = load_json(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())


def assert_invalid(name: str, validator: jsonschema.Draft202012Validator, record: dict) -> None:
    if validator.is_valid(record):
        print(f"FAIL negative case: {name}", file=sys.stderr)
        sys.exit(1)
    print(f"PASS negative case: {name}")


validators = {}
examples = {}

for schema_path, example_path in PAIRS:
    validator = validator_for(schema_path)
    example = load_json(example_path)
    errors = sorted(validator.iter_errors(example), key=lambda e: list(e.path))
    if errors:
        print(f"FAIL {example_path}")
        for e in errors:
            print(" -", "/".join(str(p) for p in e.path), e.message)
        sys.exit(1)
    print(f"PASS {example_path}")
    validators[schema_path] = validator
    examples[example_path] = example

observation = deepcopy(examples["examples/hardware-endpoint-observation.synthetic.json"])
observation["privacy"]["authorized_test"] = False
assert_invalid(
    "unauthorized device observation",
    validators["schemas/hardware-endpoint-observation.schema.json"],
    observation,
)

observation = deepcopy(examples["examples/hardware-endpoint-observation.synthetic.json"])
observation["evidence_status"] = ["observed", "independently_reproduced"]
observation["replication"] = {"independent_reproduction_count": 0}
assert_invalid(
    "independent reproduction claim with zero reproductions",
    validators["schemas/hardware-endpoint-observation.schema.json"],
    observation,
)

observation = deepcopy(examples["examples/hardware-endpoint-observation.synthetic.json"])
observation.pop("vendor_response")
assert_invalid(
    "observation without vendor-response disposition",
    validators["schemas/hardware-endpoint-observation.schema.json"],
    observation,
)

observation = deepcopy(examples["examples/hardware-endpoint-observation.synthetic.json"])
observation["vendor_response"] = {}
assert_invalid(
    "vendor response without status",
    validators["schemas/hardware-endpoint-observation.schema.json"],
    observation,
)

test_run = deepcopy(examples["examples/hardware-endpoint-test-run.synthetic.json"])
test_run["authorization"]["network_authorized"] = False
assert_invalid(
    "unauthorized network test run",
    validators["schemas/hardware-endpoint-test-run.schema.json"],
    test_run,
)

test_run = deepcopy(examples["examples/hardware-endpoint-test-run.synthetic.json"])
test_run["observations"] = []
assert_invalid(
    "test run without observations",
    validators["schemas/hardware-endpoint-test-run.schema.json"],
    test_run,
)

capture_score = deepcopy(examples["examples/hardware-endpoint-capture-score.synthetic.json"])
capture_score.pop("aggregation_method")
assert_invalid(
    "aggregate without disclosed method",
    validators["schemas/hardware-endpoint-capture-score.schema.json"],
    capture_score,
)

capture_score = deepcopy(examples["examples/hardware-endpoint-capture-score.synthetic.json"])
capture_score["comparative_ready"] = True
assert_invalid(
    "comparative claim without readiness basis",
    validators["schemas/hardware-endpoint-capture-score.schema.json"],
    capture_score,
)

comparative_basis = {
    "device_models_or_vendors": 3,
    "same_method_version": True,
    "comparable_state_definitions": True,
    "limitations_published": True,
    "vendor_response_opportunity": True,
    "material_observation_independently_reproduced": True,
}
capture_score["comparative_basis"] = comparative_basis
if not validators["schemas/hardware-endpoint-capture-score.schema.json"].is_valid(capture_score):
    print("FAIL positive case: complete comparative readiness basis", file=sys.stderr)
    sys.exit(1)
print("PASS positive case: complete comparative readiness basis")

for criterion in comparative_basis:
    incomplete_score = deepcopy(capture_score)
    if criterion == "device_models_or_vendors":
        incomplete_score["comparative_basis"][criterion] = 2
    else:
        incomplete_score["comparative_basis"][criterion] = False
    assert_invalid(
        f"comparative readiness without {criterion}",
        validators["schemas/hardware-endpoint-capture-score.schema.json"],
        incomplete_score,
    )

print("All package examples and safety-negative cases validate.")

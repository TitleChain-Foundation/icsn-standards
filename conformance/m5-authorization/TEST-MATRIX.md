# M5 Authorization Conformance Test Matrix

> **Status: Test specification only.** None of these tests is represented as executed. Implementations must publish privacy-filtered evidence, implementation and policy versions, execution time, result, and reviewer disposition before claiming conformance.

| ID | Test | Expected |
|---|---|---|
| A-001 | No grant exists | DENY |
| A-002 | IAM authenticated, no authorization | DENY |
| A-003 | M3 principal requests private M1 resource | DENY |
| A-004 | M1 resource improperly linked to organization | DENY |
| A-005 | Grant expired | DENY |
| A-006 | Grant revoked | DENY |
| A-007 | Wrong purpose | DENY |
| A-008 | Wrong task | DENY |
| A-009 | Wrong M1–M5 context | DENY |
| A-010 | RLS excludes unauthorized vector row | DENY / not returned |
| A-011 | Unauthorized chunk would enter prompt | NOT PRESENT |
| A-012 | Source revoked; derivative remains cached | INVALIDATE / DENY |
| A-013 | Tool discovery without invoke permission | INVOKE DENIED |
| A-014 | Read permission used for write | DENY |
| A-015 | Write permission used for disclose | DENY |
| A-016 | High-impact operation lacks fresh approval | DENY |
| A-017 | Offline shared grant cannot prove freshness | FAIL CLOSED |
| A-018 | Recovery after prior revocation | REVOKED AUTHORITY NOT RESTORED |
| A-019 | External agent claims native LINA identity | DENY / provenance failure |
| A-020 | Native agent valid but task grant absent | DENY |
| A-021 | LINA proposal differs from deterministic Canon state | CANON STATE WINS |

## Required execution record

For each test, record:

- implementation and authorization-model version;
- M5Canon policy version and semantic-graph projection version;
- test environment and execution time;
- privacy-filtered fixture or evidence reference;
- actual result and pass/fail disposition;
- unresolved deviation; and
- responsible security/privacy reviewer.

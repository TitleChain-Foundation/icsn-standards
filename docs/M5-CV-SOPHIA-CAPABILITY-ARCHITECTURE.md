# M5-CV / SOPHIA Capability Architecture

> **Status:** Public reference architecture.

M5-CV is a member-controlled capability, contribution, learning, and evidence record. SOPHIA is the shared vocabulary used to describe roles, skills, credential requirements, and learning pathways.

```text
Private Human Root
      ↓
M5IAM / TCID / M5HUM
      ↓
M5POD — private source + evidence
      ↓
M5-CV
      ↓
SOPHIA role / capability mapping
      ├─ contributor view
      ├─ learning view
      ├─ operator eligibility view
      ├─ developer / builder view
      └─ business/team view
```

No projection becomes a new source of identity truth.

## Evidence states

Capability state should be explicit rather than collapsed into one score:

- `self-declared`
- `evidence-backed`
- `credential-backed`
- `peer-attested`
- `sophia-verified`
- `current`
- `lapsed`
- `revoked`

## Authority boundary

A capability or credential can support eligibility for a role but does not itself activate an M5AGT or authorize a regulated action. Operational authority is evaluated separately through M5Canon, current credentials/appointments, jurisdiction, purpose, restrictions, and required approvals.

## Privacy

Shared views expose only consented professional attributes. Legal identity, private credentials, employment records, account information, and sensitive evidence remain in the holder-controlled private plane.

See also [`M5-CV-FAIR-MATCHING.md`](M5-CV-FAIR-MATCHING.md) and the [`SOPHIA Public Role Registry`](../SOPHIA-PUBLIC-ROLE-REGISTRY.md).

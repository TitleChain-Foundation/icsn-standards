---
industry: software-and-cloud-services
use_case: AI coding agent requesting promotion of an approved security patch
submission_type: scenario
claimed_tier: 4
threats:
  - supply-chain-poisoning
  - identity-abuse
  - context-blind-authorization
  - excessive-agency
  - scope-creep-lifecycle
  - audit-tampering
  - cascading-failure
  - evidence-repudiation
---

# AI coding agent requesting production promotion under delegated authority

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

A platform engineer delegates a bounded task to an AI coding agent: remediate
a dependency vulnerability in one service. Unlike a fixed deployment script,
the agent chooses edits and calls tools across source control, CI, an artifact
registry, and the deployment API without a human approving each intermediate
step. It may inspect the repository, edit a branch, and request CI runs. It
does not hold a reusable production credential.

The protected action is a compare-and-swap update of the authoritative
deployment reference for one production service, from its expected current
digest to one approved artifact digest. Runtime rollout happens afterward and
is outside the Tier 4 claim. Before the production target accepts the reference
update, it evaluates authorization evidence bound to:

- the artifact digest, target service, operation, and expected current
  production state;
- the principal's delegation, including its scope and validity window;
- the committed policy version and the required review and CI records; and
- a nonce or equivalent replay guard.

The policy can check that the required records exist and match the request. It
cannot establish that a reviewer exercised good judgment or that the tests
were adequate. Source, build, and registry statements also retain their
disclosed roots of trust; a signature does not make the asserted lineage true.

## Claimed tier: Tier 4

The Tier 4 requirement is narrow: Authorization for the production mutation.
The production target's update protocol verifies the action-bound evidence
before changing the authoritative reference. It commits the state check,
reference update, replay-guard consumption, and durable transition evidence as
one atomic operation. The evidence binds the previous and resulting reference,
the authorization inputs, and the verifier and policy versions. An accepted
request alone is not evidence that this transition committed. Missing, invalid,
stale, replayed, or mismatched evidence leaves the reference unchanged. Failure
to durably commit the transition evidence also leaves it unchanged.

Every mutation of that reference, including an emergency change, uses a
separately scoped delegation but the same verifier and atomic, fail-closed
update protocol. No out-of-band credential or API exists inside the claim
boundary. Enforcement belongs to the relying party, outside the agent
operator's control; disabling an operator-side check cannot authorize a write.

The scenario does not prescribe a proof system or require proof of a
frontier-model inference. The transition evidence, verification procedure, and
versioned policy are available without operator credentials. Independent
verifiers can check the protected reference history against externally
witnessed checkpoints and detect conflicting histories. The evidence and
checkpoints must remain available independently of the operator: publishing
only an operator-signed receipt does not meet this target. Lower-tier source,
build, and credential assertions remain inputs with disclosed trust roots;
checking their bindings does not establish their truth.

## Why not one tier down?

At Tier 3 (Trust-minimized), anyone could check the cryptographic bindings and
recorded policy result under the disclosed trust roots. The evidence could even
be generated at deployment time. The authoritative reference could still
change without first requiring a successful check.

**Reversibility.** For a privileged software change, detection is not the
required control. A substituted artifact can expose data, alter access, or
disrupt service before rollback begins, and rollback cannot undo those effects.
Tier 4 closes that gap
by making successful verification a precondition of the production state
change.

**Completeness.** A Tier 3 record can be authentic and still omit a reference
change made through an uninstrumented path. This scenario requires every
protected mutation to commit its evidence with the state transition, including
emergency changes. Under the disclosed enforcement and history assumptions,
absence of a committed transition record means that protected mutation did
not happen. It says nothing about actions outside this boundary, including
the later runtime rollout. An audit log added after the reference update does
not satisfy this requirement.

## Tier by domain

Authorization drives the overall Tier 4. The other rows state the evidence
strength this scenario actually describes; the numbers are not averaged.

| Domain        | Tier | Why |
|---------------|------|-----|
| Provenance    | 2 | Source, build, CI, and registry records are signed by identified systems and assessed under disclosed trust roots. The Tier 4 Authorization gate binds the already-approved artifact digest; it does not elevate the full lineage claim. |
| Privacy       | not claimed | No privacy claim is made about source, test, or incident data. |
| Portability   | 2 | An open evidence package carries the same action and artifact identifiers across source control, CI, the registry, and deployment. Its records remain rooted in the systems that issue them; an open format alone does not establish their truth. |
| Authorization | 4 | The production target updates the authoritative reference only after independently verifying that the artifact, target, operation, policy, delegation, freshness data, and current state fit the authorized envelope. No path inside the claim boundary can skip that check. |
| Identity      | 2 | Principal, agent, and workload credentials are authenticated, but their binding still depends on credential issuers and key-management processes. Identity is an input to Authorization, not evidence that the actor is trustworthy. |
| Security      | 2 | Attestations and assessments can show that named controller and CI configurations matched approved references, but they still depend on attestors or hardware and software roots. The story makes no broader security claim. |

No conformance stage is claimed. This hypothetical assigns target evidence
strength to a control design; it does not represent a Self-Declared,
Third-Party Assessed, or Continuously Monitored deployment.

## Threats exercised

| Threat | What it looks like here |
|---|---|
| `supply-chain-poisoning` | A compromised build tool or registry substitutes an artifact; the gate checks its binding to the approved digest, not whether an approved artifact is safe. |
| `identity-abuse` | An agent presents another principal's credential or an invalid delegation when requesting the production mutation. |
| `context-blind-authorization` | A valid approval is reused for a different service, operation, policy version, or current production state. |
| `excessive-agency` | Authority to edit and test is treated as authority to promote an arbitrary production artifact. |
| `scope-creep-lifecycle` | A changed artifact or policy is promoted using records approved for an earlier version. |
| `audit-tampering` | An operator tries to omit or rewrite the evidence of a protected reference change. |
| `cascading-failure` | A verifier, evidence store, or freshness service becomes unavailable and the update path defaults to allow. |
| `evidence-repudiation` | The operator denies a committed reference change or presents an authorization request as proof of completion. |

## What Proof-of-Control does not verify here

The Tier 4 claim supports one conclusion: the production target applied the
committed authorization predicate to the action-bound evidence and refused the
state transition unless it passed, with a durable record for each committed
transition. It does not establish that the policy was adequate or that the
authority granted to the agent was appropriately narrow.

The evidence does not show that the patch is correct or secure, that a human
review was careful, that CI covered every relevant failure, or that authenticated
lineage statements were truthful beyond their disclosed roots. It does not
prevent credential theft or human social engineering, establish that the risk
classification was correct, or make an approved upstream artifact trustworthy.
A bad patch that satisfies the committed policy can still pass the gate.
Code review, testing, incident response, and human accountability remain necessary.

The pre-action authorization record is also separate from the deployment
outcome. After actuation, the controller may emit a completion record describing
the resulting state it observed. That record does not prove that every runtime
instance is healthy or that the rollout achieved its intended effect. The
claim does not prevent cascading failures across the wider system or establish
what a recorded action means for accountability. Hardware or verifier
compromise can invalidate the evidence assumptions below.

## Residual trust assumptions to disclose

- **Credential and approval roots.** Identify the principal, agent, workload,
  reviewer, CI, and registry issuers and their key-management processes. Their
  signatures bind assertions to issuers; they do not prove that the assertions
  are truthful. Disclose delegation expiry, the maximum tolerated clock skew,
  and how the gate obtains a current revocation state. Unavailable or stale
  required revocation information halts promotion.
- **Verifier and enforcement boundary.** Publish the authorization predicate,
  verifier version and digest, cryptographic assumptions, and the mechanism
  enforcing the atomic state-and-evidence commit. Enumerate every reference
  write path and administrator privilege. If one administrator can bypass the
  verifier or rewrite the authoritative history undetectably, this Tier 4
  target has not been met. A halt test must include an attempted direct write
  and an emergency change, not just an invalid agent request.
- **Attestation inputs.** If controller or CI assessments rely on hardware
  attestation, disclose the silicon vendor, provisioning and collateral
  services, firmware and attestation-chain versions, reference-value publisher,
  freshness window, and revocation policy. Disclose how an attested key is
  bound to the controller performing this exact mutation. Two reports naming
  the same machine are not by themselves a binding to the action. A
  vendor-rooted report alone is not Tier 4 authorization evidence.
- **History and monitors.** Identify checkpoint witnesses, transparency-log
  operators, independent monitors, their collusion assumptions, and the
  checkpoint freshness policy. Durable evidence must remain retrievable when
  the operator withdraws cooperation. A missing required checkpoint, evidence
  store failure, or lapse of the required monitor set halts new promotions;
  a locally buffered receipt does not justify continuing. Recovery preserves
  prior evidence and replay state and goes through the same verifier.
- **Availability and scope.** Disclose the tolerated promotion outage and an
  exercised recovery procedure. Halting promotions leaves the existing runtime
  deployment in place; it does not establish runtime health. Completeness is
  conditional on the disclosed write-path inventory and enforcement
  assumptions, and covers only the authoritative reference transitions.

## Notes / open questions

- Evidence crosses four administrative surfaces: source control, CI, artifact
  registry, and deployment. Does independently verifiable continuity belong
  under Portability, or should continuity across boundaries become an evidence
  property of its own?
- Should the standard require separate, linked records for pre-action
  authorization and post-action completion, so an authorization record cannot
  be mistaken for evidence of the deployment outcome?
- The [tier chapter](../../0.1/en/0x10-C08-Verifiability-Tiers.md)
  both requires residual-trust disclosure and retains
  language capping single-party trust at Tier 2. This target needs a
  mechanism-specific trust analysis; it does not settle that working-group
  question. A control asserted but absent from a reference-write path has no
  Tier 4 claim, however strong the evidence from the other paths is.
- Submitted to AAI-Society/openverification as [pull request #3](https://github.com/AAI-Society/openverification/pull/3) by GitHub @AbdelStark, and ported here when the use-case corpus moved into this repository, with the tier-chapter link made relative.

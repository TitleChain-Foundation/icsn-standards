---
industry: consumer-lending
use_case: One line on what the AI system does
submission_type: scenario
claimed_tier: 4
threats:
  - context-blind-authorization
  - excessive-agency
---

<!--
This file is the thing you copy. Replace every value above and every italic
prompt below, then delete this comment.

FOR A DOCUMENTED INCIDENT rather than a hypothetical scenario, change the
frontmatter to:

  submission_type: incident
  observed_tier: 1
  required_tier: 4
  sources:
    - <title> — <url>

and replace the two headings "Claimed tier" and the disclaimer as shown in the
README. Everything else is the same.

The README explains the tiers, how a tier is set, and how to fill each section.
-->

# The title of your use case

> *Illustrative, hypothetical scenario for calibration. Not necessarily
> indicative of any specific organization's current state.*

## Scenario

*Who the user is, what the AI system does, and what is at stake if verification
is weak. Keep it concrete: one user, one decision, real consequences.*

## Claimed tier: Tier N

*Why this use case belongs at this tier. What does reaching this tier require,
and why does this use case specifically need it?*

## Why not one tier down?

*Name the exact failure mode at Tier N-1 that this use case cannot tolerate.
That gap is what the next tier up closes. Two tests help, and the README
explains both: whether the harm can be undone once you detect it, and whether
you need the record to be guaranteed complete.*

## Tier by domain

*The overall tier above is set by the domains carrying the most risk here. The
others can sit lower, and that is expected. Write "not claimed" rather than
leaving a domain blank, so a reader takes the claim as silent on it rather than
reassuring.*

| Domain | Tier | Why |
|---|---|---|
| Provenance | | |
| Privacy | | |
| Portability | | |
| Authorization | | |
| Identity | | |
| Security | | |

## Threats exercised

*The threats this deployment is exposed to, using the slugs in THREATS.md.
Tagging a threat says the deployment is exposed to it, rather than that the
deployment defends against it. These slugs must match the `threats:` list in
your frontmatter.*

| Threat | What it looks like here |
|---|---|
| `slug` | |
| `slug` | |

## What Proof-of-Control does not verify here

*Start from the out-of-scope entries in THREATS.md for the threats you tagged,
then add anything specific to this deployment. A submission with nothing here is
over-claiming.*

*Verification is not validation. Proof-of-Control shows what an agent did and
whether each action stayed within its controls. It does not judge whether a
control was adequate, whether a decision was sound, or whether an effect settled
in the outside world.*

## Residual trust assumptions to disclose

*What a reader still has to trust after every claim above holds. Name the roots
of credential issuance, the attestation chain with its version, freshness and
revocation policy, the monitor set for any transparency log and what happens if
monitors lapse, and any point where two attestations are assumed to describe the
same machine.*

## Notes / open questions

*Anything unresolved, or where reasonable people might place this differently.
If this use case turns on a control that was asserted but never wired into the
execution path, note it here: no tier closes that gap.*

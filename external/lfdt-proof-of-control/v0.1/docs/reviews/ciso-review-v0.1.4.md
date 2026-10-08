# CISO Review — Working Draft v0.1.4
<!--aais-record-->

*An operator-perspective security review of the Proof-of-Control requirement chapters,
conducted as if preparing to (a) implement the standard in a regulated enterprise and (b) rely
on a vendor's claim against it. Findings were either applied directly as new requirements
(existing requirement IDs were not renumbered) or referred to the working group via
[Appendix D](../../0.1/en/0x93-Appendix-D_Open-Issues.md). Prepared as a draft review
contribution for working-group disposition.*

## Overall Assessment

The standard's core design is sound and unusually honest: the binary threshold is drawn in the
right place (trust removed, not cryptography present), the mechanism-fit rule (C8.2) closes the
most common conformance-gaming path, the determinism boundary keeps the claim defensible, and
the threat model names what it does *not* cover — which is what makes the rest credible. The
naming discipline (Tier/Stage/Layer/Phase) prevents the axis confusion that plagues comparable
frameworks.

The gaps found are the operational ones that show up when a standard meets production: what
happens when the evidence pipeline itself fails, is attacked, or is scoped into meaninglessness.
Those are exactly the places a sophisticated vendor under commercial pressure — or an attacker —
will go first.

## Findings

| # | Severity | Finding | Disposition |
| :---: | :---: | --- | --- |
| F1 | **High** | **No fail-closed requirement.** Nothing specified what happens when evidence generation fails mid-action. A system that keeps acting while its evidence pipeline is down is fail-open by omission — and "the gateway was degraded that hour" becomes the new "the model did it." | Applied: **C7.6.1**, **C7.6.3** |
| F2 | **High** | **Omission was undetectable.** The tamper-evident property covered alteration, fabrication, and backdating — but not *absence*. A compromised system that silently skips records defeats every other control, and Appendix B itself concedes this ("does NOT prevent… selectively omitting telemetry"). Completeness must be a verifier-checkable property. | Applied: **C7.6.2** |
| F3 | **High** | **Scope gaming.** The statement declared domains but not the system boundary or which action classes are in scope. The SOC 2 lesson: a technically true claim over a carefully drawn boundary misleads every relying party. The binary question "does your AI have Proof-of-Control?" is only procurable if the scope underneath it is declared. | Applied: **C10.1.6** |
| F4 | **High** | **No key lifecycle.** Every mechanism in the standard rests on signing and attestation keys, yet no requirement governed their custody, rotation, or compromise recovery. An unrotated, unrevocable key silently converts mechanism-generated evidence back into operator-trusted evidence — dropping the claim below the binary threshold without anyone noticing. | Applied: **C6.3.1–6.3.3** |
| F5 | Medium | **Whose clock?** "Contemporaneous" and "backdating detectable" presuppose trusted time, but the time source was unspecified. An operator-controlled clock undermines both properties. | Applied: **C7.2.2** |
| F6 | Medium | **Internal contradiction on TEE attestation.** C8.1.3 correctly caps vendor-rooted attestation at Tier 2, while Appendix B presents TEE attestation as a mechanism for Tier 3–4 evidence. Both are defensible, but the composition rule that reconciles them (vendor-rooted attestation + independent anchoring → Tier 3, with the vendor assumption disclosed) was unstated — the exact seam an assessor dispute would open on. | Applied: **C8.1.7** |
| F7 | Medium | **The verification method itself wasn't required to be open.** The standard's founding premise — anyone can check, with the public method, without privileged access — appeared in the definitions but never as a requirement. A conformant-looking system could demand an NDA to obtain the verifier. | Applied: **C8.1.8** |
| F8 | Medium | **The evidence store is a new attack surface.** Comprehensive execution records are a honeypot (business activity, data-access patterns) and a legal liability (immutable records vs. GDPR-style erasure obligations). No requirements governed evidence access control, retention, or the erasure tension. | Applied: **C7.6.4–7.6.5**, **C2.4.1–2.4.2** |
| F9 | Medium | **Human approvals weren't evidenced.** The threat model claims coverage of approval fatigue ("evidences the raw, true intent presented for approval") but no requirement delivered it. Approval and override decisions are authorization events and must be bound to the approver's identity. | Applied: **C4.1.6** |
| F10 | Medium | **No machine-readable claim format.** The insurance thesis depends on actuaries comparing claims across implementations; prose statements don't price. | Applied: **C10.1.7** |
| F11 | Low | **Coverage decay was invisible.** The roadmap defines a proof-coverage metric, but nothing required measuring or disclosing it — so coverage could rot silently between assessments. | Applied: **C10.3.6** |
| F12 | Low | **Tier 4's availability cost was undisclosed.** Self-enforcing execution means the system halts when proofs can't be produced. That is the right default, but it creates an availability dependency a CISO must plan for and a claim should disclose. | Applied: **C8.3.4** |

## Referred to the Working Group (no text change)

Recorded as [Appendix D, issue 11](../../0.1/en/0x93-Appendix-D_Open-Issues.md):

1. **Incident response beyond alerting** — C10.3 requires alerts; whether conformance is
   suspended on a detected control failure is already WG issue 8. The review recommends the
   suspension model over the attestation-continues model.
2. **Third-party dependency inventory** — whether the conformance statement should enumerate the
   external services and subprocessors the agent crosses into (extends C10.1.6 and the C3
   continuity requirements).
3. **Verifier-side denial of service** — economic limits on verification (proof size, cost per
   verification) as a disclosure item, so "anyone can verify" holds in practice, not just in
   principle.
4. **Insider threat at the silicon/HSM layer** — currently handled via trust-assumption
   disclosure, which the review judges adequate; flagging for the cryptography review under WG
   issue 6.

## Method Notes

* New requirements were **appended** to existing sections (or added as new sections); no
  existing requirement was renumbered, so prior references such as `v0.1-C4.1.4` remain stable.
* Level assignments follow the grading scheme in force at the time of each edit. *Post-review
  note:* the standard subsequently moved to a four-level scheme aligned one-to-one with the
  Verifiability Tiers (Level 3 = binary threshold, Level 4 = self-enforcing/continuous), and all
  requirements — including those added by this review — were re-graded and rewritten with
  per-section auditor-evidence guidance.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*

# Public-comment register, October 2026

**Date:** 2026-10-07 · **Scope:** every issue open in this repository at the close of the
public-comment window on Working Draft v0.1 · **Status:** informative, dated record

This register lists each comment received as a GitHub issue, what it asks, and how it was
disposed of on 7 October 2026. It adds no requirements. A comment marked *Working group*
was not resolved: it is logged here with the Appendix D issue or chapter it bears on, the
issue was closed to clear the queue, and the working group takes it up when it resolves
the open items on the [roadmap](../roadmap.md). Anyone may reopen an issue if a
disposition below misreads it.

On the close date: the FAQ says the window closed on 7 October 2026. The Preface,
Frontispiece, README, chapter header and roadmap still say 30 October 2026, and that
discrepancy awaits the Owner's direction. Comments filed after this register was written
are not in it.

*Note added 2026-10-07:* the Owner settled both points the same day. The window closes on
30 October 2026, and the label is Working Draft v0.1 everywhere until ratification; the FAQ
and the front-page labels were changed to match, and #86 was resolved on that basis. The
paragraph above is left as written.

## Resolved by a pull request

| Issue | Raised by | Sections | What it asked | Disposition |
| --- | --- | --- | --- | --- |
| [#35](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/35) | kenhuangus | docs/proposals | Two companion documents cited by `tooling-findings.md` do not exist | Links made plain mentions that say the companions were not published, [#98](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/98) |
| [#37](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/37) | kenhuangus | C5, Appendix B, Appendix D issue 12 | Verifiable Trust Circles attributed inconsistently across four places | C5 and Appendix D now carry the two-part attribution research-basis.md and Appendix B use, [#98](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/98) |
| [#47](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/47) | kenhuangus | paper, Section 1 and 9.3 | Section 1's "no real hardware enclave" caveat contradicts the TDX results | Section 1 now says which numbers still run on the stand-in and points at the TDX section, [#99](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/99) |
| [#48](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/48) | kenhuangus | paper, abstract and 9.5 | The abstract headlines the 42% figure the paper says was wrong | Abstract, related-work line and conclusion now carry the corrected 44.8%; the caveat names its experiment, [#99](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/99) |
| [#49](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/49) | kenhuangus | paper, Table tab:claims | The claims table defines two fields the worked token lacks | Listing caption names the two absent claims and when a token carries them, [#99](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/99) |
| [#79](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/79) | imran-siddique | docs/one-pager.md, C8, C10.2 | One-pager still says Tiers 3 to 4 require trusting no one | Replaced with the disclosed residual trust set and a link to C10.2, [#93](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/93) |
| [#80](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/80) | rakeshgohel01 | C7.7, schema/ | CDDL and JSON schema define different claim sets; `alg` encoded wrongly | Claim keys -70014 to -70016 allocated and `dispatched_snapshot_hash` declared, [#83](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/83); `alg` now the COSE identifier, [#97](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/97). Still open: no test reads the CDDL |

## Awaiting the Owner

| Issue | Raised by | Sections | What it asked | Disposition |
| --- | --- | --- | --- | --- |
| [#86](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/86) | joseruiz1571 | 10.1.5, README, header, roadmap | Five version labels for one text; 10.1.5 cannot be cited | Left open. The label (v0.1 everywhere, or v1.0-draft) is the Owner's call; the change is mechanical once made |

## Working group

Each row names the open item the comment attaches to. Where several comments bear on one
item they are grouped so the working group reads them together.

### Appendix D issue 1, and the C4.2 working-group box: identity, authority and accountability

| Issue | Raised by | What it asked |
| --- | --- | --- |
| [#94](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/94) | csingcloud | An optional, opaque reference from the execution record to the versioned upstream authority a grant was made under, its accountable grantor and its recorded status, plus one sentence stating that an evidenced grant does not establish the standing of that authority |
| [#69](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/69) | basilpuglisi | Principal identity (C5.1.1) does not by itself assign accountability; add an accountable-person field or say so |
| [#67](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/67) | basilpuglisi | C8 open item 2: whether human authority belongs in the Tier 4 root-of-trust cell or on a separate axis the evidence references |
| [#75](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/75) | basilpuglisi | Record who accepted each policy bundle version, when and under what authority, bound into the same log as the actions that cite it |
| [#73](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/73) | basilpuglisi | Evidence-status declarations per record and a classification of the human act in C4.1.6 (CARCS, offered as reference) |
| [#56](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/56) | evidifyai-svg | C4.1.6's approval record is a self-report with no interception boundary, so its auditor evidence cannot be closed out; either bind the approval to a commitment outside the presenting system (Level 3) or state the limit and cap it at Tier 2 (Level 2). The comment thread reads the two remedies as two Levels of one requirement |

### Appendix D issues 3 and 5, and C7.6: continuity, completeness and omission

| Issue | Raised by | What it asked |
| --- | --- | --- |
| [#92](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/92) | evidifyai-svg | If a fifth property is added, define it as bounded completeness relative to a declared capture envelope, with per-scope accounting, declared gaps and a stated limit; keep it distinct from transport continuity (C3.2) and sequence continuity (7.6.2) |
| [#87](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/87) | Levaj2000 | Continuity across a representation boundary must preserve proof properties, not only linkage; a producer-declared signed end-of-stream marker for 7.6.2; an OCSF crosswalk offered under mappings/ |
| [#89](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/89) | MattyIceMatrix | Three Level 2 additions to C7.6: start and end records per source, in-band drop records for counted loss, and refusals recorded as refusals; a VLC-1 crosswalk and checker offered |
| [#65](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/65) | rakeshgohel01 | A declared source that stops emitting is caught only by 10.3.2 at Level 4; is that intended, and does it belong in C7.6 or C10 |
| [#57](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/57) | terryncew | Implementation report on receiver-held continuity across a provider switch and effect closure after revocation. Landed as the use case `provider-replacement-live-mandate.md` ([#96](https://github.com/LFDT-ProofOfControl/ov-poc-standard/pull/96)); the reconciliation question it raises stays with this group |
| [#78](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/78) | imran-siddique | C7.1 makes an enforcement point a precondition and Appendix C has no row for it: add gateway-compromise and gateway-bypass rows, disclose who operates the gateway in C10.2, and restate the boundary. The thread proposes a grading for the bypass row |
| [#60](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/60) | ajayc47 | Default orchestration frameworks produce a faithful log of a manipulated action; add a caveat that logging alone does not meet the authority-definition and evidence requirements |

### Appendix D issues 6, 7, 8 and 11: the threshold, the disclosure format, monitoring and verifier economics

| Issue | Raised by | What it asked |
| --- | --- | --- |
| [#82](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/82) | rakeshgohel01 | When issue 7 fixes the category set, keep 10.2.1's named subject and reconcile its subject list with 7.4.1 and 10.2.2; OSFI E-23 needs the named party |
| [#64](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/64) | aglamadrid19 | Field note: name evidence-signing-key custody in the issue 7 disclosure; let generation and anchoring claim Tiers separately (issue 6); separate economic recourse from monitoring and say what an open challenge does to a claim (issue 8); add verifier-side cost to the disclosure (issue 11); an ERC-8004 crosswalk offered (issue 9). The thread adds two worked Tier 2 placements and asks whether 8.1.3's literal reading is intended |
| [#76](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/76) | bkuan001 | Permitted public wording for a Tier 1 or Tier 2 placement under 8.1.4; support for the split claim in #64; a reformulated Tier 2/3 test; a Tier 1 evidence floor |
| [#72](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/72) | basilpuglisi | Appendix D issue 13: a seven-day anchoring maximum for high-risk records, the history-rewrite risk it bounds, and an operator-side halt monitor that does not meet C8.3.5 (offered as reference) |

### C4.1, C7.1, C7.5 and the schema: vocabularies and the verifier result

| Issue | Raised by | What it asked |
| --- | --- | --- |
| [#81](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/81) | rakeshgohel01 | The eight interception points and the four verdicts are required claims with no chapter defining them; define both in C7.1 and C4.1, or record them as schema-only |
| [#66](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/66) | rakeshgohel01 | How a token represents an evaluation that could not complete, and whether the token needs a result claim distinct from the decision |
| [#77](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/77) | elekto-energy | Require the published verifier's result to state its scope as execution facts and mark content correctness as not assessed; an Appendix C row for relying-party over-inference. Keep "could not evaluate" (#66) distinct from "outside scope" |

### Appendix C and Appendix D issue 12: threat rows and citations

| Issue | Raised by | What it asked |
| --- | --- | --- |
| [#36](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/36) | kenhuangus | The "Insecure inter-agent communication" out-of-scope cell reads as copy/paste drift; Appendix C is normative, so the replacement text is a working-group call |
| [#71](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/71) | basilpuglisi | Approval fatigue is Partial and has no worked use case; pattern-level signals over approval records could narrow the gap (offered as reference) |
| [#70](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/70) | basilpuglisi | A source-custody record for each research-driven requirement and crosswalk citation before ratification |
| [#68](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/68) | basilpuglisi | Align the informative "open verification must replace human verification" framing with the normative text, which keeps validation and accountability with humans |

### Offers of contributions

These ask whether a contribution is wanted. The answer in each case is yes, by the route
CONTRIBUTING.md names, and the issue is closed so the contribution can arrive as a pull
request.

| Issue | Raised by | Offer | Route |
| --- | --- | --- | --- |
| [#88](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/88) | optimization2026 | An informative worked example linking a declared skill control (AISOP/AISP) to action evidence, with a mapping table and negative tests | A note under docs/proposals/, following P01 as the pattern; informative, no new claim fields |
| [#74](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/74) | basilpuglisi | A short informative crosswalk from H.R. 10362's provisions to the draft's requirements | A crosswalk under mappings/, Appendix D issue 9 |
| [#90](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/90) | reflectme-source | A provider-neutral source-rights observation as pre-action evidence | Outside the core, which verifies adherence to declared controls and does not name control types; a use case or a mechanism-inventory entry (Appendix B) is the place to show it |
| [#63](https://github.com/LFDT-ProofOfControl/ov-poc-standard/issues/63) | terryncew | An independent appraisal of a reference token, and a request for a fresh token | The published vectors under schema/vectors/ are the reference tokens; the appraisal is welcome as a use case or an implementation note, as #57 was |

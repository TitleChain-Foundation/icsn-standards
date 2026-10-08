# Contributing to the Proof-of-Control Standard

Thank you for your interest in Proof-of-Control. The standard is developed in the open, by
working-group consensus, and stewarded by the
**[Advanced AI Society](https://advancedaisociety.org/)**.

> **The front door for contributing is [advancedaisociety.org](https://advancedaisociety.org/) —
> sign up there to join a working group or become a member.**

## Ways to Contribute

1. **Comment on the draft.** Anyone can comment during the public-comment period (open until
   October 30, 2026). The working group reviews every comment and publishes a disposition:
   accepted, rejected with rationale, or deferred.
2. **Weigh in on open decisions.** Open working-group decisions are marked
   `[WG-INPUT NEEDED]` throughout the standard — search for that tag to find every one. Those
   are the questions the working group most needs input on.
3. **Join a working group.** There are six domain working groups (Provenance, Privacy,
   Portability, Authorization, Identity, Security), plus an insurance working group where
   carriers, reinsurers, and actuaries define what the standard must carry to be priceable.
   [Sign up at advancedaisociety.org](https://advancedaisociety.org/).
4. **Contribute a crosswalk.** Extend the [framework mappings](mappings/README.md) to other
   standards and frameworks. Several crosswalks are marked as needing a volunteer.
5. **Contribute a use case.** Sector working groups produce the worked use cases
   ([use cases](docs/use-cases/README.md)) that validate the standard against real
   deployments. Copy [`docs/use-cases/_TEMPLATE.md`](docs/use-cases/_TEMPLATE.md), tag
   the threats it exercises from [`THREATS.md`](docs/use-cases/THREATS.md), and open a
   pull request; the folder README walks through it.

## Change Process

* The mechanics — fork, branch, regenerate, test, open the pull request — are stepped out in the
  [README](README.md#propose-a-change-with-a-fork-and-a-pull-request). Anyone may open one; no
  membership required.
* The **normative core** (the requirement chapters C1–C10 in [`0.1/en/`](0.1/en/)) is the versioned specification
  under change control. Formal change proposals (issues and pull requests) are made against it.
* **Informative material** (the companion documents in [`docs/`](docs/)) rides alongside as
  clearly-marked context.
* Decisions are made by working-group consensus, with independent review and final sign-off by
  the Distinguished Review Board — see [Governance](docs/governance.md).
* Requirements language follows RFC 2119/8174
  ([Appendix A: Glossary](0.1/en/0x90-Appendix-A_Glossary.md)).

## Editorial Conventions

* `[WG-INPUT NEEDED]` marks an open working-group issue; `[DRAFT]` marks a section still
  being written; `[INSERT]` marks a pending merge from a companion document.
* **Naming discipline:** *Tier* grades the evidence (1–4); *Level* grades the requirements
  (1–4, aligned to the Tiers); *Stage* grades the audit of the claim (named, never numbered);
  *Layer* locates the evidence in the stack (MAESTRO 1–7); *Phase* tracks an adopter's rollout
  (1–3). An unqualified number always means a Tier.
* **Auditability rule:** every requirement must name a verifiable artifact or testable behavior,
  and each section's *Auditor evidence* note must tell an assessor what to collect and what to
  test. A requirement an auditor cannot close out against an artifact is not ready to merge.
* **Regenerate the checklist and diagrams:** after changing any requirement table, run
  `python3 tools/generate_checklist.py` and `python3 tools/generate_crosswalks.py`
  (and `python3 tools/generate_diagrams.py` if a diagram
  changed) and commit the regenerated Appendix E, `checklist/` exports, and
  `images/diagrams/` SVGs alongside your change. After adding or editing a use case, run
  `python3 tools/validate_use_cases.py`, then `python3 tools/generate_use_case_coverage.py`,
  and commit `docs/use-cases/COVERAGE.md`.
* "Prove" is reserved for genuine cryptographic proofs and the coined name Proof-of-Control;
  what an agent did is *shown* or *evidenced*, never "proven."

## Recognition

Contributors shape the standard, and their names stand behind the version that ships.
Contributors and member organizations are listed, with their consent, in the
[Acknowledgments](0.1/en/0x01-Frontispiece.md).

## License

By contributing, you agree that your contributions are licensed under
the [Apache License 2.0](LICENSE.md), consistent with the specification.

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*

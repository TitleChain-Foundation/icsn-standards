# Public Review Process

## What is open for review

The [filed SEC comment and its checksums](README.md) are an immutable public record. The separate [Appendix B artifact directory](../../../docs/PUBLIC-REFERENCE-ARTIFACTS.md) contains evolving reference architectures, control models, schemas, and RFCs.

Unless an artifact expressly states otherwise, material labeled **Public Review Draft**, **Public Review**, or **Draft RFC**:

- invites evidence, objections, implementation analysis, accessibility feedback, and proposed revisions;
- is not an adopted standard or mandated design;
- is not represented as deployed, credentialed, certified, or authorized for production use; and
- does not indicate SEC or other governmental endorsement.

## GitHub Discussion

Use [Foundation Discussion 19](https://github.com/orgs/TitleChain-Foundation/discussions/19) for the accessible overview, introductions, general questions, and comments that span more than one recommendation. The [featured public-review visuals](../../../assets/public-review/README.md) provide illustrated entry points into wallet authority, the economic stack, and the private M5POD boundary.

## GitHub Issues

Use the [SEC S7-2026-30 public-review board](https://github.com/orgs/TitleChain-Foundation/projects/2/views/2) to follow all seven recommendations through Todo, In Progress, and Done, with each card showing its review focus, Foundation response stage, labels, milestone, and SEC deadline. The [SEC milestone](https://github.com/TitleChain-Foundation/icsn-standards/milestone/2) provides the deadline-progress summary, while the [filtered SEC review queue](https://github.com/TitleChain-Foundation/icsn-standards/issues?q=is%3Aissue%20state%3Aopen%20label%3Aregulatory-review%20label%3Asec) provides the same issues with their review-type labels. There is one issue for each recommendation:

1. [Voluntary open standards](https://github.com/TitleChain-Foundation/icsn-standards/issues/56)
2. [Credential-bound participant identifiers](https://github.com/TitleChain-Foundation/icsn-standards/issues/57)
3. [Technology-neutral Forms TA-1 and TA-2 disclosures](https://github.com/TitleChain-Foundation/icsn-standards/issues/58)
4. [Machine-readable legends and transfer rights](https://github.com/TitleChain-Foundation/icsn-standards/issues/59)
5. [Pre-activation controls for automated agents](https://github.com/TitleChain-Foundation/icsn-standards/issues/60)
6. [Separation of origination and transfer authority](https://github.com/TitleChain-Foundation/icsn-standards/issues/61)
7. [Reference state model for the underlying right](https://github.com/TitleChain-Foundation/icsn-standards/issues/62)

Use comments for evidence, objections, implementation analysis, legal review, accessibility feedback, and proposed revisions. Open a pull request when proposing a concrete repository change, and link it to the relevant review issue.

Do not request or post private financial information, identity documents, privileged communications, investor information, or nonpublic agency correspondence.

## How the Foundation will respond

Subject to maintainer capacity, the Foundation's public response lifecycle is:

1. **Acknowledge and route.** A maintainer identifies the relevant artifact or recommendation and applies or confirms appropriate labels.
2. **Evaluate in public.** Maintainers and participants examine cited evidence, objections, implementation consequences, interoperability, privacy, security, accessibility, and legal-review needs.
3. **Record the proposed disposition.** The thread or linked pull request states whether the input is proposed for acceptance, accepted with revision, deferred pending evidence, referred for specialized review, or not adopted, with a reason.
4. **Review changes.** Material changes proceed through a pull request and the applicable RFC or governance process. Automated checks do not substitute for substantive review.
5. **Close with traceability.** When a thread is resolved, a maintainer links the resulting commit, pull request, follow-up issue, or written disposition. Accepted changes update the evolving artifact, not the immutable filed SEC document.

There is no guaranteed response time or guarantee that a proposal will be adopted. Silence, an open thread, repository publication, or automated validation does not constitute approval. Only authorized standards stewards may advance an artifact's maturity under [GOVERNANCE.md](../../../GOVERNANCE.md).

## Official SEC channel

The official SEC comment form is https://www.sec.gov/comments/s7-2026-30/transfer-agent-rules.

GitHub participation is not an official SEC submission. Anyone who wants a comment considered by the SEC must submit it through the SEC’s official process before November 3, 2026.

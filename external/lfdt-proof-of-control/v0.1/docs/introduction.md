# Section 1 — Introduction (informative)

***This section answers:*** *Who is this for and how do they use it? What is this a standard for?
And how is it designed? — Proof-of-Control is written for security practitioners and auditors
first, then business and governance owners, in any organization. It is the standard for Open
Verification, achieved through Proof-of-Control, built on seven design principles: industry-led,
insurance-ready, speed, interoperable, technology-neutral, vendor-neutral, and open.*

## The Concept

In **open verification**, the root of trust is a mechanism anyone can verify, not a party
anyone must believe. Open verification carries the ethos of open source software into the
agentic era, extending it from inspecting source code to verifying the actions agents take in
the agentic stack. It is a category of approaches that is purpose-built for the agentic age,
where deployment of non-deterministic agents requires mechanisms that remove the need to trust
a single gatekeeper.

The category is defined by the openness of the method and the evidence, not by who is asking.
Proof-of-Control is one approach to it, built for AI agents.

Openness began in software as open source and extended into open hardware, open data, and open
standards. Open source opened the code: it published the source and gave everyone the right to
inspect, use, modify, and share the software, with no license fee and no vendor lock.

Open verification carries the same open-source principles into new territory: the verification of
what AI and other autonomous systems actually did. The standard and the method of verification
are openly published, so anyone can read and implement them instead of depending on a proprietary
black box. And the evidence is openly verifiable: any party who needs to verify what a
system did can do so with the public method, without privileged access and without trusting the
operator. What open verification removes is the need to trust a single gatekeeper.

What defines open verification is where its root of trust sits. Every verification rests on a
root of trust, the thing you ultimately rely on to believe it, and that root is what makes a
verification open or not. For decades the root has been a party: an operator's own key, a
certificate authority, a chip vendor's attestation service, whoever controls a ledger.
Verification whose root of trust is a party is closed, however strong the cryptography, because
you are still trusting that party. Verification is open when its root of trust is not a party but
something anyone can verify: mathematics, or a decentralized, distributed protocol with no single
party to trust, and at its strongest, execution that is self-enforcing and cannot run unless its
integrity holds. The test is not whether cryptography is used, but where the root of trust lives.

What makes this practical now is a convergence of trust-minimized methods that move the root of
trust off of any single party. Zero-knowledge proofs, public transparency logs, verifiable
computation, and independent attestation are examples of the mechanisms, not a required list. And
because zero-knowledge techniques can confirm a fact without revealing the information behind it,
openness of the verification and privacy of what is verified are no longer opposed.

Open verification is interoperable on two levels, existing infrastructure and standards/specs. It
is interoperable with existing infrastructure: these methods are built to sit on top of the
closed and centralized systems already in place, so open verification is added to what an
organization runs, not swapped in for it. And it is also interoperable with existing standards:
the field is crowded with AI frameworks and standards, and open verification is designed to
produce the evidence that makes their requirements verifiable, rather than to compete with or
replace them. Doing this work in an interoperable way, at both the infrastructure level and the
standards level, is what lets it be adopted at all, which is why the standards work around it
matters as much as the technology.

This is also why open verification is not an ideological position, and not all-or-nothing. It
does not ask an entire system to be open, and it can be built on top of a closed one. It makes a
narrow claim about a specific interaction at a specific moment, that this action can be
openly verified, without requiring that the whole system be open to the world. A closed,
proprietary system can still produce openly verifiable evidence of the one thing that matters in
a given interaction and reveal nothing else.

Open verification is one part of a larger movement to make AI accountable: the field of AI
assurance. Fathom is advancing that field through independent verification and the Independent <!--aais-allow-->
Verification Organization (IVO) model, and through PACT AI, the first industry association for AI
assurance, which convenes the ecosystem across deployers, assurance providers, and insurers.
Together they are building the institutions and the market that assurance depends on. Open
verification's job is to give those institutions something they can verify: openly
verifiable, tamper-evident evidence of what a system did, so an assurance provider or an IVO can
verify rather than take a claim on trust.

Proof-of-Control is one way to reach open verification.

It is the approach this standard defines, for AI agents, and it is a demonstration of open
verification rather than the whole of it. Proof-of-Control qualifies because it meets the
defining condition: its evidence is openly verifiable, with the root of trust moved off
the operator and any single party, so what an agent did can be checked without trusting the
operator's word. Other approaches can reach open verification for other subjects, the way the DEV
Standard does for environmental claims; each counts as open verification if, and only if, it
meets the same root-of-trust test. Proof-of-Control produces a continuously verifiable record of
what an AI agent did, the data it touched and the actions it took, and grades that evidence on
the Verifiability Tiers, which are ordered by exactly that question of where the root of trust
sits.

Two clarifications on common misconceptions. Open verification is about the openness of the
verification system, the standard, the process, and the tools that check what a system did, not
about whether the model being checked is open-source: a closed model can be openly verified, and
an open-source model can ship with no verification at all. And closed conformance or
self-certification is not open verification, even when it borrows the language: if the party
being checked also runs the check, the result is an assertion in disguise
([Section 7](../0.1/en/0x10-C10-Conformance-and-Disclosure.md)).

**Proof-of-Control** is open verification that the controls governing an agent system are
implemented and held, graded on the four Verifiability Tiers by how independently that can be
verified. For each control it claims, across the six domains (Provenance, Privacy, Portability,
Authorization, Identity, Security), a conformant implementation MUST produce evidence, generated
by the enforcing mechanism at execution time, that the control held; place that evidence on the
Verifiability Tiers; and disclose its residual trust assumptions. A system has Proof-of-Control
when, and only when, its evidence reaches Tier 3 or Tier 4.

Proof-of-Control is the evidence layer AI governance depends on: the part that lets decisions <!--aais-allow-->
about what agents may do, and whether they did it, be checked and enforced rather than merely
asserted.

As agents take on more of the work that runs our institutions, from insurance and finance to law
and government, they enter systems built and governed by people, and those systems run on
accountability: every actor must be able to show what it did. Proof-of-Control lets an agent meet
that bar, so the institutions we already rely on can take agents in, manage them, and hold them
to account rather than take their behavior on faith.

*The concept here is the introduction; the precise, normative definitions of these terms are
consolidated in [Section 3, Terms and definitions](../0.1/en/0x90-Appendix-A_Glossary.md).*

## What It Answers, and What It Does Not

Proof-of-Control answers whose agent this is, what it was allowed to do, whether it stayed within those controls, and whether you can attribute and contain it when it does not. The verification-not-validation line this rests on is normative, not introductory: [C7.5, the determinism boundary](../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md), defines what the evidence may and may not represent as verified.

Proof-of-Control does not prevent every harm. It evidences and gates control-boundary adherence, so an unauthorized action is rejected and every action is attributable. It composes with evaluation and oversight; it does not replace them.

## What This Is: the Standard

This document defines the foundations of the Proof-of-Control standard, what verifiable evidence
of an agent's behavior must be, under the umbrella of open verification. After the foundation is
defined, then come the operational frameworks, the implementation guides, the training, and the
certifications that turn the standard into everyday practice. FinOps is a useful example: its
framework gave engineering, finance, and business one shared language for cloud value. The
standard comes first because everything else rests on it. This document is that first piece.

## Who It's For

The framework is for the people who make, defend, and answer for AI governance decisions, in any
organization, enterprise, government, or nonprofit. The first adopters are security practitioners
and leaders, the CISOs, security engineers, and auditors who answer for what an agent did and who
need evidence, not the vendor's claim about it; it is written so they want it and can require it.
It is written just as deliberately for the non-technical side, and for a wider set of readers by
name: product and business owners, who decide whether an agent ships and answer for what it does
without building it themselves; AI safety and responsible-AI leads, who are responsible for
oversight and need to check what an agent actually did rather than take it on trust; and policy
and regulatory readers, who shape the rules for agents and need to understand what evidence and
verification make possible. Non-technical readers are a first-class audience here, not an
afterthought: a governance decision only the technical team can read is not a governance
decision.

Like FinOps, an operational framework that lets engineering, finance, and business make
cloud-value decisions together, the Verifiability Tiers is built to be the common language
technical and non-technical people use to make AI governance decisions together, especially for
agentic systems. (FinOps Foundation, finops.org.)

* **For a CISO:** Zero Trust is native to your budget and your architecture. Proof-of-Control is
  the evidence substrate that lets you show an auditor, insurer, or regulator that your agents
  did only what they were authorized to do.
* **For an insurer or regulator:** Setting the controls is not the same as verifying they held.
  Proof-of-Control is the evidence you can price and adjudicate against.

## Who Made This

This standard is developed in the open with its working groups, advisors, and member
organizations, who are named in the [Acknowledgments](../0.1/en/0x01-Frontispiece.md).

**[Advanced AI Society](https://advancedaisociety.org/) convenes the field and stewards the
Proof-of-Control standard as a public good.** It brings
together the founding members and working groups that draft the standard, and it administers the
standards process. Co-chairs Ken Huang and Tricia Wang lead the effort with the Society's members
and the industry founding contributors. To become a member,
**[sign up at advancedaisociety.org](https://advancedaisociety.org/)**.

The standard is built to be independent of any single company, including Advanced AI Society.
During development it is incubated within the Society. On completion, ownership transfers to the
Verifiable AI Foundation, where it is held as a public good:
neutral, freely available, and protected from commercial capture. The specification is freely
available under an Apache 2.0 license, so anyone can use, implement, translate, and build on it;
the certification mark ("Proof-of-Control Certified") is protected as a trademark so that only
systems assessed as conformant may claim it.

Independence is built into how it is governed:

* The **leadership team** drafts the standard.
* A **Distinguished Review Board** provides senior technical review, so it holds up with
  cryptographers and standards bodies.
* **Founding members** shape it through feedback and working-group participation, with sector
  working groups producing the use cases that validate it against real deployments.
* **Standards-body, vertical-industry, and implementation partners** extend its reach and feed
  real experience back into future versions.

The people behind this bring a track record of moving fields across sectors, from civil society
to enterprise to technology, which is the range a cross-industry, public-interest standard
requires. (Contributors and founding members are listed in the acknowledgments, with their
consent.)

## What Comes Later: Two Certifications

Two certifications will follow the standard.

1. **Professional certification**, earned by the technical and non-technical people who learn to
   apply the framework, the way a FinOps practitioner earns certification.
2. **Third-party system certification**, the conformance mark an organization earns for an AI
   system when an accredited assessor verifies it against the standard, the way an organization
   earns SOC 2. Auditors sit at the center of the second: they need the standard now, because
   they will perform that independent certification.

Neither exists yet; this document defines the standard they will rest on.

## Design Principles: How the Standard Is Built

*How to read these.* We wrote these principles to keep the effort true to its intent: an open
standard that gives people the foundation to trust agents, and gives vendors and buyers a common
way to assess that trust.

A standard no one adopts is a standard that does not exist. So we keep a principle here only if
it passes two tests: ignoring it would leave us with an unused standard, and it resolves a real
trade-off. Characteristics everyone already agrees on are requirements of the standard, not
principles; those live in the specification.

Standards building runs on hard calls, usually a choice among several good options that pull
against each other. These principles are how we pressure-test those calls: when the options
conflict, we ask which one better serves the principles here. They are not stack-ranked.

* **Industry-led:** built by the enterprises that deploy agents and the builders who make
  verification, not a standard for its own sake. It exists because the field needs it and is
  shaped by the people who will use it, which is also what keeps it adoptable: an industry-led
  standard is grounded in what organizations can actually put into practice. The strongest
  verification is usually the most expensive, so the standard gives adopters a graded path to
  choose the tier that matches their risk and their budget rather than prescribing one tier for
  everyone. This is why the Verifiability Tiers scale has four tiers, and why Proof-of-Control at
  Tiers 3 and 4 are kept distinct: the gain in trustworthiness at the top comes with a real jump
  in cost, and adopters should make that call deliberately. (The scale itself lives in the
  specification, [Section 6](../0.1/en/0x10-C08-Verifiability-Tiers.md).)
* **Insurance-ready:** built so insurers can underwrite on its evidence. Insurance is the forcing
  function for adoption, so the standard is designed to be insurable from day one, not
  retrofitted for it.
* **Speed:** the AI industry is moving faster than any standards process is built for. Agents are
  already being deployed at scale, ahead of governance, so a standard that waits for a perfect
  version arrives after the decisions it was meant to inform. We ship a working draft and iterate
  in the open, because the risk here is arriving late, not arriving imperfect.
* **Interoperable:** it points to and complements existing specs and standards (MAESTRO, OWASP,
  NIST AI RMF, ISO/IEC 42001) rather than duplicating them. No repeat work; it produces the
  evidence that makes their requirements verifiable.
* **Technology-neutral:** defines what the evidence must be, not which mechanism produces it. The
  standard never mandates a specific technology, so a new approach can meet it and none is locked
  in.
* **Vendor-neutral:** favors no company. No member's product is the reference implementation, and
  governance gives no vendor an edge. For a member-based body this is also member-neutrality, no
  favorites among the companies at the table, which is what lets competitors adopt the same
  standard and buyers trust it.
* **Open:** the standard and the process that assesses conformance are open and
  inspectable, and verification does not belong to the verified. A closed standard, or a vendor
  certifying itself, would return us to claims-based assurance even while using the word
  "verified."

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) —
**[join at advancedaisociety.org](https://advancedaisociety.org/)**.*

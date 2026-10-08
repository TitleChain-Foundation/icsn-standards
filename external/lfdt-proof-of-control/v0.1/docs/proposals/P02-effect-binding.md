# Proposal: normative changes for message-to-effect binding (P02)

**Status:** proposal only. No file under `/Users/jimschwoebel/Desktop/ov-poc-standard/` has been
modified.

**Source research:** `research/Message to Effect Binding Research.md` — §Formalization of the
Effect Model and the Binding Gap, §Sufficient Endpoint Conditions for Execution Fidelity,
§Empirical Survey and Taxonomy of Production APIs, §Adversarial Vulnerability Surface and Parsing
Differentials, §Remediation Architecture and Standard Profiles, §Restatement of Theorem 1 and
Proof Sketch, §Actionable Recommendations and Implementation Framework.

**Corroborating implementation:** `transit` — `src/guard.rs` (`decide`, the enforcing proxy),
`src/classify.rs` (`judge_c1`–`judge_c4`, the endpoint classifier), `src/corpus.rs`
(`Condition`, `Evidence`). Cited throughout as evidence of what is *specifiable*: every condition
proposed below is already enforced or classified by shipped code, with the bypasses it closes
measured end to end.

**Targets:** `0.1/en/0x10-C04-Authorization.md`,
`0.1/en/0x10-C07-Evidence-Generation-and-Properties.md`, `schema/canonicalization.md`.

---

## 0. The finding, in one paragraph

The standard's central theorem is stated as: *an adversary cannot make a relying party execute an
action other than the one the policy evaluated*. What the proof actually establishes is that the
relying party will not execute a **request representation** other than the one the policy
evaluated. Those are the same proposition only if the endpoint's state transformation is a
function of the request representation alone. Commercial APIs are not built that way: they apply
server-side parameter defaults, resolve aliases to canonical resources, execute non-idempotently
under network retry, and read unsigned background state between check and use. Under any of those,
two byte-identical canonical requests can produce two different effects, and the digest comparison
that Theorem 1 turns on compares something that does not determine the outcome
(§Formalization of the Effect Model and the Binding Gap). The research closes the gap with four
sufficient endpoint conditions, and measures how many production endpoints meet them: **4 of 24
(16.7%) qualify; 6 (25.0%) qualify only if the client volunteers optional parameters; 14 (58.3%)
cannot qualify at all** (§Empirical Survey).

The proposal therefore has three jobs:

1. **Stop the overclaim.** Requirements that assert executed-effect evidence where only
   message-level evidence exists must be narrowed or bounded (§1, §2 below).
2. **Restate the theorem accurately.** A weaker, true theorem with its hypotheses named (§6).
3. **Say what an implementer does about it.** The four conditions are properties of the *endpoint*,
   not of the agent system. A requirement written against them is unimplementable unless it also
   specifies the remediation path for the 83.3% of endpoints that do not qualify (§3, C4.3).

---

## Editorial precondition: a naming collision that must be resolved first

The research names its conditions **C1–C4** (parameter completeness, representation injectivity,
strict idempotency, contextual state pinning). The standard already uses **C1–C10** for its domain
chapters, where **C4 is Authorization** and **C7 is Evidence Generation**. Importing the research's
labels verbatim would make "C4" ambiguous inside the very chapter this proposal amends.

**Proposal:** the standard adopts the prefix **EB1–EB4** ("effect-binding condition") for the four
endpoint conditions, with a glossary entry in
[Appendix A](../../0.1/en/0x90-Appendix-A_Glossary.md) mapping each to the research's C1–C4 so citations remain
traceable. All proposed text below uses EB1–EB4.

- EB1 — **Parameter completeness and default invariance**
- EB2 — **Representation injectivity**
- EB3 — **Strict idempotency with nonce-decoupled retries**
- EB4 — **Contextual state pinning**

**Confidence:** editor's fix. No substantive question; only the label is in play.

---

## 1. C4 Authorization — Control Objective

### Where
`0x10-C04-Authorization.md`, **§Control Objective**, second half of the first paragraph.

### Current text (verbatim)

> Produce verifiable evidence that the system acted within the permissions it was granted. This domain covers delegation-chain verification, scope and policy enforcement, signed authorization tokens checked against granted permissions, and the traceability of whether each agent action stayed within its authorized boundary — proving not just that the tool was authorized, but that its *evaluated payload parameters* matched the exact structural schema at execution time.

### Proposed text

> Produce verifiable evidence that the system acted within the permissions it was granted. This domain covers delegation-chain verification, scope and policy enforcement, signed authorization tokens checked against granted permissions, and the traceability of whether each agent action stayed within its authorized boundary — proving not just that the tool was authorized, but that its *evaluated payload parameters* matched the exact structural schema at execution time.
>
> **The boundary of that claim.** Matching the evaluated parameters to the executed request binds the *request representation*. It binds the *effect* only where the endpoint's state transformation is determined by that representation alone. Endpoints that fill omitted parameters from server-side state, resolve several spellings of a resource to one target, execute non-idempotently under retry, or read unsigned background state between authorization and execution can produce different effects from byte-identical authorized requests. [C4.3](#c43-effect-binding-at-the-endpoint) states the conditions under which representation binding extends to effect binding, and what a deployment does when the endpoint it must call does not meet them.

### Why

§Formalization of the Effect Model and the Binding Gap: "Message Authorization can be satisfied
trivially while Effect Binding fails entirely." The objective's phrase "acted within the
permissions it was granted" is an effect claim; the mechanism named in the same sentence
(structural schema match on payload parameters) is a message claim. §Parameter Defaulting and
Alias Attacks gives the worked counterexample — a policy engine approves
`POST /v1/transfer?to=acct-9` because no `fee_tier` is present, the endpoint expands `fee_tier`
from a user profile that evaluates to `priority`, and the approved low-risk transformation is not
the one that executed.

### Confidence

**Settled by measurement.** The counterexample is reproduced against a live endpoint in `transit`'s
hostile-server corpus and is the case `guard.rs`'s `require_parameters` exists to close; the
comment at `guard.rs:580–587` records the measurement (`"fee_tier":false` reaching the upstream and
being silently defaulted to `"priority"`). The wording of the added paragraph is an editor's fix.

---

## 2. C4.1.4 — the parameter digest binds the wrong thing

### Where
`0x10-C04-Authorization.md`, **C4.1 Authority and Scope Enforcement**, requirement **4.1.4**.

### Current text (verbatim)

> | **4.1.4** | **Verify that** tool-call parameters are validated against the registered tool schema at execution time, that out-of-schema calls are rejected, and that the validated parameter digest is stored in the execution record. | 2 |

### Proposed text

> | **4.1.4** | **Verify that** tool-call parameters are validated against the registered tool schema at execution time, that out-of-schema calls are rejected, and that the **digest stored in the execution record is computed over the normalized parameter set** — every optional parameter resolved to an explicit value under a published normalization function before evaluation, so that no parameter the endpoint would supply from its own state is absent from the digested form. A parameter counts as supplied only when it is present **and of the declared type**; a present-but-unusable value (`null`, or a value of the wrong JSON type) is treated as absent. | 2 |

### Auditor evidence — proposed addition to the C4.1 evidence line

Replace the existing `4.1.4` clause:

> 4.1.4 — tool schema registry, a rejected malformed call, parameter digests in records.

with:

> 4.1.4 — tool schema registry, a rejected malformed call, parameter digests in records; take one registered tool, identify an optional parameter the endpoint documents a default for, submit a call omitting it, and confirm the call is refused or the digest covers the normalized value rather than the omission. Submit the same parameter as `null` and as the wrong JSON type and confirm both are refused the same way as an omission.

### Why

§Condition 1 (Parameter Completeness and Default Invariance): "the endpoint must commit to a public
normalization schema ... ensuring that policy evaluation and message digest binding operate
strictly on" the normalized form. §Actionable Recommendations, item 1: "Capabilities MUST NOT sign
un-expanded wire payloads containing optional fields."

Schema validation as currently written accepts a request that omits an optional parameter, and the
digest then commits to the omission — which is precisely the value the endpoint is free to fill
from unsigned state. The type clause is not pedantry: `classify.rs`'s `judge_c1` counts a property
as unbound when it is `!required || has default`, and `guard.rs`'s `ParamType::matches` exists
because a presence-only check was itself the bypass. The comment at `guard.rs:112–121` records
why: the upstream reads `fee_tier` with `.and_then(Json::as_string)`, which returns `None` — the
same as absent — for `false`, `0`, `[]`, `{}` and `null` alike, and then falls into the defaulting
branch. Enumerating only `null` as the rejected shape caught one member of the class; the class is
"any value the reader on the other end cannot use", which is *wrong type*, not *specifically null*.

### Confidence

**Settled by measurement.** Both halves — the omission bypass and the wrong-type bypass — were
measured end to end against the shipped hostile endpoint, and both are closed in shipped code.

---

## 3. New subsection C4.3 — Effect Binding at the Endpoint

### Where
`0x10-C04-Authorization.md`, inserted as a new subsection after **C4.2 Delegation** and before
**References**.

### Current text
None. This is new material.

### Proposed text

> ---
>
> ## C4.3 Effect Binding at the Endpoint
>
> An authorization decision binds a request representation. It binds the resulting effect only where the endpoint's state transformation is determined by that representation. This is a property of the endpoint, not of the agent system — so a deployment either calls an endpoint that has it, supplies it at an enforcement point in front of one that does not, or states that its evidence is message-level.
>
> The four conditions, together sufficient for representation binding to extend to effect binding:
>
> * **EB1 — Parameter completeness.** No parameter reaching the state transformation is supplied by the endpoint from its own state. Every optional parameter is either forbidden or resolved to an explicit value under a published normalization function before the digest is computed.
> * **EB2 — Representation injectivity.** Two wire requests that canonicalize to the same bytes name the same target and the same transformation. No resource alias (`/users/me` for `/users/{id}`, a channel name for a channel ID), no open parameter set, and no parser differential between the point that evaluates and the point that executes.
> * **EB3 — Strict idempotency with nonce-decoupled retries.** Repeating an executed request produces no additional effect, and the business idempotency key is a distinct field from the authorization freshness nonce, so a network retry is not indistinguishable from a replay.
> * **EB4 — Contextual state pinning.** Every state dependency of the transformation is named in the request as a precondition (ETag, version vector, parent commit, CAS version), and execution fails atomically if the state moved between evaluation and execution.
>
> | # | Description | Level |
> | :--------: | ------------------------------------------------------------------------------------------------------------------- | :---: |
> | **4.3.1** | **Verify that** every in-scope tool endpoint carries a recorded classification against EB1–EB4, that the classification names each condition as satisfied, client-dependent, unknown, or failed, and that the recorded verdict is the weakest of the four — never an average and never a summary that omits a failing condition. | 2 |
> | **4.3.2** | **Verify that** each classification records **how it was established**, distinguishing a reading of the endpoint's specification from a measurement against the endpoint itself, and that a specification-derived reading is registered as *at most* client-dependent for EB1 and EB4 — a document cannot establish what an implementation does with a parameter it was not sent, or whether an effect depends on state the request does not name. | 2 |
> | **4.3.3** | **Verify that** where an in-scope endpoint does not satisfy all four conditions, the deployment either (a) interposes an enforcement point that supplies the missing conditions before the request reaches the endpoint — refusing, not repairing, any request it cannot bring into conformance — or (b) records the endpoint in the claim as message-bound, subject to [C7.1.5](../../0.1/en/0x10-C07-Evidence-Generation-and-Properties.md#c71-generation-at-the-action-boundary). An endpoint that is neither remediated nor declared is a conformance failure. | 3 |
> | **4.3.4** | **Verify that** every request reaching an in-scope endpoint is ingested by a **single strict parser** that rejects duplicate object keys, lone surrogates, unbounded numeric literals and non-canonical encodings — and that the bytes the policy evaluated and the bytes the endpoint receives are produced by that one parse, so no second parser downstream can read the same input differently. | 2 |
> | **4.3.5** | **Verify that** the request target is resolved once, and that ambiguity in it is **refused rather than repaired**: dot segments, multiply-encoded escapes, encoded path separators, and targets carrying a fragment are rejected, and route policy is matched against the same resolved target that is forwarded. | 2 |
> | **4.3.6** | **Verify that** authorization replay protection and business idempotency are carried in **distinct fields**, so that an infrastructure retry of an already-executed request is answered from the recorded outcome rather than refused as a replay or executed a second time. | 3 |
>
> **Auditor evidence:** 4.3.1 — the endpoint register; recompute the verdict for three sampled endpoints from their condition rows and confirm the weakest governs. 4.3.2 — for one endpoint classified as qualifying, ask for the measurement, not the document; a specification-only basis for EB1 or EB4 is not a qualifying classification. 4.3.3 — for each non-qualifying endpoint, either the enforcement point's configuration and a refusal test (omit a required-by-policy optional parameter and confirm the request never reaches the endpoint), or the claim line declaring it message-bound. 4.3.4 — submit a payload with a duplicate object key, a lone surrogate, and an integer beyond 2^53, and confirm each is refused at ingress; then confirm the digest covers the parse, not the wire bytes. 4.3.5 — submit `/{allowed}/../{restricted}`, a doubly-encoded and a re-cased spelling of a restricted path, and confirm each is refused rather than resolved onto a relaxed rule. 4.3.6 — interrupt the response to an executed request and reissue it verbatim; confirm the second call returns the first call's outcome and produces no second effect.

### Why

- **4.3.1 / 4.3.2** — §Empirical Survey establishes the taxonomy (Qualified / Conditional /
  Non-Qualifying) and the distribution across 24 production endpoints. The evidence-grade
  distinction in 4.3.2 is not the paper's; it comes from the implementation, and is the tightest
  practical limit on the whole scheme: `classify.rs`'s `judge_c4` returns `Unknown` rather than
  `Failed` when no precondition mechanism is described, with the comment *"a specification cannot
  say whether the effect depends on server state. Only a probe can, which is the methodological
  crux of the whole empirical half of this paper."* `corpus.rs`'s `Evidence` enum carries the same
  distinction as a first-class type (`SpecDerived`, `HostileServer`, `LiveProbed`, `DeskStudy`)
  with the caveat printed next to every result. A standard that let a vendor claim qualification
  from an OpenAPI document would be certifying a hypothesis.
- **4.3.3** — §Remediation Architecture and Standard Profiles, the Boundable API Conformance
  Profile, plus §Re-Ordering Complete Mediation Options, which identifies the co-located
  enforcement point as the strongest posture. The "refusing, not repairing" clause is the shipped
  design: `guard.rs`'s `normalize_target` refuses traversal rather than resolving it, because
  "resolving it would mean the guard deciding on one path and a URL parser downstream deriving
  another".
- **4.3.4** — §Parser Differentials and RFC 8785 (JCS) Violations, and the decoder table showing
  Go, Elixir, Jackson and Node.js resolving duplicate keys, surrogates, negative zero and numeric
  range four different ways. §Actionable Recommendations item 2: "Lenient language-default decoders
  MUST NOT be utilized within authorization pipelines." Implemented: `guard.rs` runs `parse_strict`
  before anything else looks at the request and forwards the canonical body, never the wire body —
  and `parse_config` refuses `strict_ingestion = false` outright, on the ground that "a config that
  could switch it off is a config that can reintroduce the bug it exists to prevent."
- **4.3.5** — §Condition 2 (URI path aliases collapsing distinct canonical strings onto one
  internal target). This requirement is written from measured failures rather than from the paper:
  `guard.rs:308–326` records that matching route rules against still-encoded text let
  `/v1/tra%6Esfer`, `/v1/%74ransfer`, `/v1/transfe%72` and `/v1/TRANSFER` all reach
  `/v1/transfer` upstream while matching no route rule — with `require_parameters` and every
  per-route check switched off for them. `guard.rs:328–338` records the fragment variant:
  `/v1/transfer#z` matched no rule at the guard while the upstream received `/v1/transfer`, "the
  parameter-defaulting bypass, through the enforcement point, with the guard's own digest header
  attached to it."
- **4.3.6** — §Condition 3 and §Nonce Replay versus Network Retry Ambiguity, which walks the
  five-step trace where a TCP reset after commit turns a legitimate retry into a 401/409 while the
  state transformation has already happened — and the mirror case where a proxy that re-signs
  against a fresh nonce duplicates the effect.

### Confidence

- 4.3.1, 4.3.2, 4.3.4, 4.3.5 — **settled by measurement.** Each is implemented and each closed a
  measured bypass.
- 4.3.3 — **judgement call for the working group.** The *mechanism* is settled; the **Level** is
  not. Level 3 makes remediation-or-declaration mandatory at the Proof-of-Control threshold, which,
  given that 58.3% of surveyed endpoints are non-qualifying, is the single most commercially
  consequential line in this proposal. `[WG-INPUT NEEDED]`
- 4.3.6 — **judgement call.** The failure mode is demonstrated; whether the standard should
  require a *cached-outcome* response (as against merely requiring the two fields to be distinct)
  is a stronger obligation than the research strictly establishes. `[WG-INPUT NEEDED]`

---

## 4. C7.1.4 — the three mediation options are not equivalent

### Where
`0x10-C07-Evidence-Generation-and-Properties.md`, **C7.1 Generation at the Action Boundary**,
requirement **7.1.4**.

### Current text (verbatim)

> | **7.1.4** | **Verify that** the effect channel is mediated within the same trust boundary as policy evaluation, by at least one of: (a) the credentials and transport for the effect are held inside the attesting environment, which emits the request itself; (b) the mechanism releases a single-use capability cryptographically bound to the evaluated snapshot digest and target resource, which the relying party checks before executing; or (c) egress is confined to an attested enforcement point that admits only requests carrying matching evidence. The conformance claim states which. | 3 |

### Proposed text

> | **7.1.4** | **Verify that** the effect channel is mediated within the same trust boundary as policy evaluation, by at least one of the following — **which are not equivalent, and are listed in descending order of what they establish**. The conformance claim states which, and states the endpoint's EB1–EB4 classification ([C4.3.1](../../0.1/en/0x10-C04-Authorization.md#c43-effect-binding-at-the-endpoint)) alongside it. | 3 |
> | | **(a) Attested enforcement point at the execution boundary.** Egress is confined to an enforcement point co-located with the target — a sidecar, in-process interceptor, or equivalent — which admits only requests carrying matching evidence, and which performs its check on the fully parsed and normalized request immediately before the endpoint acts on it. This is the only option that mediates the effect rather than the message, because it is the only one positioned after parameter expansion and alias resolution. | |
> | | **(b) Enclave-held credentials and transport.** The credentials and transport for the effect are held inside the attesting environment, which emits the request itself. This establishes effect binding **only where the target endpoint is classified as satisfying EB1–EB4**; against an unclassified or non-qualifying endpoint it establishes that the attested environment emitted a particular request, not that a particular effect followed. | |
> | | **(c) Capability bound to the evaluated snapshot.** The mechanism releases a single-use capability cryptographically bound to the evaluated snapshot digest and target resource, which the relying party checks before executing. The relying party's check is over the request representation; where its own parameter expansion, alias resolution or state dependencies are outside the signed material, this option **does not establish effect binding** and the claim states so. | |

### Why

§Re-Ordering Complete Mediation Options (C7.1.4) is explicit and is written directly against this
requirement: "Security standards historically treat mediation deployment topology options as
equivalent alternatives. Corrective analysis proves these options provide non-equivalent security
guarantees." It ranks the attested co-located enforcement point first ("This represents the
strongest security posture"), direct endpoint enforcement second and only "strictly under the
condition that the endpoint formally conforms to the Boundable API Profile", and concludes of the
third that it "cannot guarantee effect binding and must be demoted in standards specifications."

Note that the research's option letters and the standard's do not correspond: the research's
"Option (c)" is the standard's current option (c) (attested enforcement point), its "Option (a)" is
the standard's (a), and its "Option (b)" is the standard's (b). The proposed text reletters into
descending strength so that a reader who takes the first listed option takes the strongest one.
**This reletttering is a hazard for anyone holding an existing conformance claim** — a claim that
says "option (b)" today means something different under the proposed text. See Confidence.

The auditor evidence line for 7.1.4 must be updated to match; the current substitution test
("submit snapshot A to the mechanism while attempting to dispatch action B, and confirm B is
refused (option a/c) or rejected by the relying party (option b)") refers to the old letters.

Proposed replacement for that clause:

> 7.1.4 — the mediation option declared in the claim, plus a substitution test: submit snapshot A to the mechanism while attempting to dispatch action B, and confirm B is refused (options a, b) or rejected by the relying party (option c). Then, separately, an **effect** substitution test: dispatch two requests that canonicalize identically but that the endpoint could execute differently — one omitting an optional parameter the endpoint defaults, one naming no state precondition — and confirm the mediation point refuses them, or that the claim declares the endpoint message-bound.

### Confidence

**Judgement call for the working group.** `[WG-INPUT NEEDED]`

The *substance* — that the three options are not equivalent, and that (b) and (c) as currently
written are conditional on endpoint properties — is settled by the research and corroborated by
implementation. What is not settled is (i) whether to reletter at all, given that the letters are
already referenced from `0x94-Appendix-E_Audit-Checklist.md` and from live conformance claims, and
(ii) whether the demoted option should remain a valid route to a Level 3 requirement at all, or be
struck. [Appendix D issue 13](../../0.1/en/0x93-Appendix-D_Open-Issues.md) already lists the adjacent question
open: "whether capability-bound dispatch (which requires relying-party cooperation) should be
mandatory rather than one option among three at Tier 4." The research answers the reverse of that
question — capability-bound dispatch is the *weakest* of the three, not the one to mandate — and
the WG should reconcile the two before either is ratified.

A lower-cost alternative the WG may prefer: **keep the current letters and ordering**, and add only
the conditional clauses and the cross-reference to C4.3.1. That captures the whole security
substance and none of the migration cost.

---

## 5. C7.1.5 — the tier cap is drawn at the wrong place

### Where
`0x10-C07-Evidence-Generation-and-Properties.md`, requirement **7.1.5**.

### Current text (verbatim)

> | **7.1.5** | **Verify that** the claim does not assert that evidence describes executed actions unless 7.1.4 is met — a system evidencing evaluation but not mediating the effect channel may claim Tier 1–2 only. | 1 |

### Proposed text

> | **7.1.5** | **Verify that** the claim does not assert that evidence describes executed actions unless 7.1.4 is met **and the endpoint is classified as satisfying EB1–EB4 on measured evidence** ([C4.3.1](../../0.1/en/0x10-C04-Authorization.md#c43-effect-binding-at-the-endpoint), [C4.3.2](../../0.1/en/0x10-C04-Authorization.md#c43-effect-binding-at-the-endpoint)). A system evidencing evaluation but not mediating the effect channel may claim Tier 1–2 only. A system that mediates the effect channel but calls an endpoint that is not so classified may claim Tier 1–2 for that endpoint, and **states in the claim that its evidence for that endpoint binds the request representation and not the effect**. | 1 |
> | **7.1.6** | **Verify that** where a claim covers a mixture of qualifying and non-qualifying endpoints, the Tier is recorded **per endpoint** and the claim carries no aggregate Tier that a non-qualifying endpoint's evidence does not support. | 1 |

### Auditor evidence — proposed addition

Append to the C7.1 evidence line:

> 7.1.5 — check the claim's wording against the mediation option actually implemented **and against the endpoint register from C4.3.1; an endpoint qualifying on specification-derived evidence alone does not support an executed-action claim**. 7.1.6 — take the claim's per-endpoint Tier table and confirm every in-scope endpoint appears in it.

### Why

§Conformance Tier Restrictions (C7.1.5) states the rule directly: "Tier 1 & Tier 2 Claims
(Message-Level Authorization): Granted to endpoints that verify message signatures over canonical
wire bytes but do not satisfy Conditions C1–C4. These tiers guarantee that the request byte
sequence was approved, but explicitly DISCLAIM execution fidelity over real-world side effects."
And: "Tier 3 & Tier 4 Claims ... Restricted exclusively to endpoints that either prove full
conformance to the Boundable API Profile under verified formal inspection, or utilize Option (c)
Attested Enforcement Points co-located within the execution boundary."

The current 7.1.5 draws the cap at *mediation*, which is necessary but not sufficient: a system can
mediate its effect channel perfectly and still call `POST /gmail/v1/users/me/messages/send`, which
the survey classifies Non-Qualifying on both alias resolution and idempotency. Its evidence
truthfully describes a request that was emitted; it does not describe an effect. The word "endpoint"
in 7.1.6 is essential because a real deployment calls many, and the survey's distribution makes a
mixed estate the normal case, not the exception.

### Confidence

**Judgement call for the working group.** `[WG-INPUT NEEDED]`

The technical content is settled by the research and by the survey. What the WG must decide is the
commercial consequence: under this text, a deployment whose tools are Slack, Jira, Google Calendar
and Salesforce — all Non-Qualifying in the survey — cannot claim Proof-of-Control for those
actions, however good its enclave is. That is the honest result, and it is also the result most
likely to be argued with. The WG should decide it explicitly rather than let it arrive as a
side effect of an editorial change.

---

## 6. The restated theorem

### Where
`schema/canonicalization.md`, **§Why this document exists**, first paragraph. (Also the paper's own
Theorem 1, which is outside this repository; the change should be made in both, and the canonical
statement should live in one place with the other citing it.)

### Current text (verbatim)

> Theorem 1 in the paper says an adversary cannot make a relying party execute an
> action other than the one the policy evaluated. The proof turns on one step: the
> relying party recomputes a digest over the request it has been asked to perform,
> and compares it to the digest the attesting environment committed to. Equal
> digests, execute; different digests, refuse.

### Proposed text

> **Theorem 1 (conditional execution fidelity).** Let a policy P be evaluated over a normalized
> decision context and issue a capability committing to a digest of the normalized request
> representation. Let E be an endpoint whose state transformation is τ. If
>
> 1. the relying party verifies the capability's signature and recomputes the digest over the
>    request it has been asked to perform, refusing on any mismatch; **and**
> 2. E satisfies EB1 (parameter completeness), EB2 (representation injectivity), EB3 (strict
>    idempotency with nonce-decoupled retries) and EB4 (contextual state pinning),
>
> then no adversary can cause E to execute a state transformation other than the one P approved.
>
> **What this claims.** Under hypotheses (1) and (2), the digest comparison is decisive: signature
> unforgeability and hash collision resistance force the executed representation to be the
> evaluated one; EB2 forces that representation to name one transformation; EB1 forces the
> representation to determine the full parameter space, with nothing supplied from unsigned state;
> EB4 forces execution to abort rather than proceed against state that moved; EB3 forces retries to
> collapse to a single application. The executed transition then equals the approved one.
>
> **What this does not claim.** Hypothesis (2) is a property of the endpoint. Nothing in the
> protocol establishes it, and nothing the agent system does can supply it remotely. Without (2),
> the theorem degrades to a strictly weaker statement — *an adversary cannot make a relying party
> execute a request representation other than the one the policy evaluated* — which is what the
> digest comparison alone buys. Binding a message is not binding an effect. Against an endpoint
> that defaults omitted parameters, aliases resource names, executes non-idempotently, or reads
> unsigned background state, both requests in an attack can carry the same valid capability, the
> same canonical bytes and the same digest, and produce different effects. Every signature verifies;
> nothing looks broken; the property is gone.
>
> The proof establishes hypothesis (2) as **sufficient**. Its *necessity* — that dropping any one
> of EB1–EB4 always admits an attack — is argued per condition by counterexample rather than proved
> in general, so the theorem should be read as an "if", not an "if and only if", until that is
> settled.
>
> Everything below concerns hypothesis (1), and specifically the fact that it holds only if *the
> same action produces the same bytes in every implementation*. If your serializer emits keys in
> insertion order and mine emits them sorted, we produce different digests for identical actions.
> Every signature still verifies. Nothing looks broken. But the comparison fails, so either
> legitimate work is refused for reasons nobody can diagnose, or — far worse — an implementer
> "fixes" it by relaxing the comparison, and Theorem 1 quietly stops being true.

### Why

§Restatement of Theorem 1 and Proof Sketch gives exactly this statement and the seven-step sketch
the "what this claims" paragraph compresses. The final line of that section — "If any condition
C1–C4 is omitted, an adversary can construct [a request] such that [the digest check] holds while
[the effects differ], invalidating execution fidelity" — is the necessity argument, and it is a
counterexample per condition rather than a general proof, which is why the proposed text says so.

The honesty caveat is the deliverable. The research's own restatement is phrased "if and only if";
the proof sketch discharges only the "if". Publishing the "iff" would repeat, at one remove, the
same class of error this whole proposal exists to correct.

### Confidence

**Settled by proof** for the statement itself and for the sufficiency/necessity distinction. The
prose framing is an editor's fix. The decision to publish the weaker theorem in place of the
stronger claim is a `[WG-INPUT NEEDED]` item only in the sense that someone must accept that the
headline gets weaker; the mathematics is not in dispute.

---

## 7. C7.7 — the commentary states the property the comparison cannot deliver

### Where
`0x10-C07-Evidence-Generation-and-Properties.md`, **C7.7 The Interoperable Property**, the block
quote beginning "Why this is a security property and not a documentation one."

### Current text (verbatim, first sentence)

> **Why this is a security property and not a documentation one.** The binding between an evaluated action and an executed one ([C7.1.4](#c71-generation-at-the-action-boundary)) works by recomputing a digest and comparing it. Two implementations that serialize the same action differently produce different digests for identical actions.

### Proposed text

> **Why this is a security property and not a documentation one.** The binding between an evaluated action and the request that is executed ([C7.1.4](#c71-generation-at-the-action-boundary)) works by recomputing a digest and comparing it. Two implementations that serialize the same action differently produce different digests for identical actions.
>
> Note the direction of the guarantee. Different digests reliably mean different requests, so the comparison refuses reliably. Equal digests mean the same request — not necessarily the same effect, which depends on properties of the endpoint stated in [C4.3](../../0.1/en/0x10-C04-Authorization.md#c43-effect-binding-at-the-endpoint). Canonicalization is what makes the refusal sound; it is not what makes the execution faithful.

### Why

§Formalization of the Effect Model: canonical byte equality over a message representation does not
guarantee deterministic state transformation. The existing commentary is correct about why
canonicalization matters and is the strongest passage in the chapter; the proposed addition only
prevents a reader from concluding that a correct canonical form is *sufficient* for the binding
C7.1.4 names.

### Confidence

**Settled by measurement.** Editor's fix in wording.

---

## 8. C7.7.5 — the duplicate-key rule covers evidence, not actions

### Where
`0x10-C07-Evidence-Generation-and-Properties.md`, requirement **7.7.5**.

### Current text (verbatim)

> | **7.7.5** | **Verify that** a parser rejects duplicate object keys rather than resolving them last-wins, so that one evidence artifact cannot mean different things to different readers. | 2 |

### Proposed text

> | **7.7.5** | **Verify that** a parser rejects duplicate object keys rather than resolving them last-wins, so that one evidence artifact cannot mean different things to different readers — **and that the same strictness applies to the action payload on the path from evaluation to execution ([C4.3.4](../../0.1/en/0x10-C04-Authorization.md#c43-effect-binding-at-the-endpoint))**, since an action that means different things to the evaluator and to the endpoint defeats the binding regardless of how strictly the evidence about it was parsed. | 2 |

### Why

§Duplicate Object Key Attack: "the authorization engine uses an Elixir or custom parser evaluating
the first key as an authorized recipient, while the downstream endpoint uses a Node.js or Go parser
evaluating the last key as an adversarial account ... The authorization signature verifies over the
canonicalized bytes, but the backend transfers funds to the attacker." The current 7.7.5 governs
the evidence artifact. The attack is on the action payload. As written, an implementation can pass
7.7.5 in full while remaining fully exposed — and the decoder table in §Parser Differentials shows
that the four most common production JSON stacks disagree on this exact case in four different
ways.

Whether the substance lands as a clause on 7.7.5 or as C4.3.4 is an editorial choice; it must land
somewhere, and 7.7.5 is where a reader will look for it.

### Confidence

**Settled by measurement.** Implemented: `transit` ships a strict decoder (`src/json.rs`
`parse_strict`) and a differential harness (`src/differential.rs`, `src/decoder.rs`) built for
this comparison exactly.

---

## 9. `schema/canonicalization.md` — the snapshot's number rules

### Where
`schema/canonicalization.md`, **§The two canonical forms**, second paragraph, and
**§A divergence we did not hide**.

### Current text (verbatim)

> **The snapshot** contains application data — the parameters of whatever the
> agent is trying to do — and the profile cannot restrict its shape. Snapshots are
> canonicalized with **RFC 8785 (JSON Canonicalization Scheme)** in full,
> including its number rules, which specify ECMAScript `Number::toString`
> behaviour.

and

> Neither can affect the claim set: its keys are ASCII and it contains no floats.
> Both can affect a snapshot carrying application data with exotic keys or
> floating-point parameters.

### Proposed text

> **The snapshot** contains application data — the parameters of whatever the
> agent is trying to do — and the profile cannot restrict its shape. Snapshots are
> canonicalized with **RFC 8785 (JSON Canonicalization Scheme)** in full,
> including its number rules, which specify ECMAScript `Number::toString`
> behaviour.
>
> A conforming implementation MUST additionally **reject** — not normalize, not accept — the
> inputs on which common decoders disagree, before the snapshot digest is computed: duplicate
> object keys, lone surrogate code points, lexical negative zero, numeric literals that underflow
> to zero, and integers outside the exactly-representable range of an IEEE 754 double. These are
> not canonicalization edge cases. They are the points at which the evaluating parser and the
> executing parser can be made to read one input two ways, which is exactly the binding the digest
> exists to provide.

and

> Neither can affect the claim set: its keys are ASCII and it contains no floats.
> Both can affect a snapshot carrying application data with exotic keys or
> floating-point parameters. **A snapshot carrying a floating-point parameter is therefore the
> weakest point in the whole scheme** — the claim set excludes floats precisely because number
> formatting is the hardest part of any canonicalization scheme, and the snapshot readmits the
> problem without the exclusion. `[WG-INPUT NEEDED]` — whether the profile should forbid
> floating-point in snapshots as it does in the claim set, requiring application parameters to be
> carried as strings or scaled integers, and what that costs implementers.

### Why

§Numeric Serialization and Exponent Precision: "An authorization engine utilizing
arbitrary-precision integer arithmetic parses large integers exactly, whereas a downstream endpoint
converting the JSON input to a double-precision float rounds the value, causing numerical state
drift." The decoder table shows Go floats underflowing to zero, Node.js normalizing `-0`, Jackson
truncating bignums and Elixir rejecting outright — four behaviours, one input. The existing
document already discloses that the reference implementation's float repr "is not ECMAScript
`Number::toString` in every case", which means the divergence is present in the shipped code today
and is currently disclosed rather than closed.

### Confidence

- The rejection list — **settled by measurement**. It is the same list `transit`'s `parse_strict`
  enforces, and each entry appears in the research's decoder differential table with at least two
  disagreeing implementations.
- Forbidding floats in snapshots — **judgement call for the working group.** `[WG-INPUT NEEDED]`
  It is the clean fix and it has a real compatibility cost, since application payloads containing
  monetary or measurement values are common.

---

## 10. Summary table

| # | Where | Kind | Confidence |
| :-- | :-- | :-- | :-- |
| 0 | Appendix A glossary | Adopt EB1–EB4 to avoid the C1–C10 domain collision | Editor's fix |
| 1 | C4 Control Objective | Bound the effect claim | Settled |
| 2 | C4.1.4 | Digest over the normalized parameter set; type-checked presence | Settled by measurement |
| 3 | New C4.3 (4.3.1–4.3.6) | Endpoint classification, evidence grade, remediation, strict ingestion, target resolution, nonce/idempotency split | Settled, except 4.3.3 Level and 4.3.6 scope `[WG-INPUT NEEDED]` |
| 4 | C7.1.4 | The three mediation options are not equivalent | `[WG-INPUT NEEDED]` |
| 5 | C7.1.5 + new 7.1.6 | Tier cap keyed to endpoint qualification, recorded per endpoint | `[WG-INPUT NEEDED]` |
| 6 | canonicalization.md §Why this document exists | Restated Theorem 1 | Settled by proof |
| 7 | C7.7 commentary | Equal digests mean same request, not same effect | Settled |
| 8 | C7.7.5 | Extend strict parsing from the evidence artifact to the action payload | Settled by measurement |
| 9 | canonicalization.md §two canonical forms | Snapshot rejection list; float question | Rejection list settled; float ban `[WG-INPUT NEEDED]` |

## 11. Requirements this proposal judges to overclaim today

| Requirement | The overclaim |
| :-- | :-- |
| **C4 Control Objective** | "acted within the permissions it was granted" is an effect claim; the mechanism named alongside it (structural schema match) is a message claim. |
| **C4.1.4** | A digest over the validated-but-unexpanded parameter set commits to the *omission* of exactly the parameters the endpoint will fill from unsigned state. Passing 4.1.4 is compatible with the paper's headline attack succeeding. |
| **C7.1.4** | Presents three mediation options as interchangeable ("by at least one of"). Two of the three are conditional on endpoint properties the standard does not currently require anyone to establish. |
| **C7.1.5** | Caps the tier on *mediation*, which is necessary but not sufficient. A perfectly mediated system calling a Non-Qualifying endpoint currently passes 7.1.5 and may claim executed-action evidence it does not have. |
| **C7.7 commentary** | "The binding between an evaluated action and an executed one works by recomputing a digest and comparing it" — the digest comparison delivers the refusal, not the fidelity. |
| **C7.7.5** | Scoped to the evidence artifact only, leaving the action payload — where the duplicate-key attack actually lands — ungoverned. |
| **canonicalization.md ¶1** | States Theorem 1 as effect binding when its proof establishes representation binding plus unstated endpoint hypotheses. |

## 12. Deliberately not proposed

The research supports none of the following, and they are recorded here so a later reader does not
assume they were overlooked:

- **No requirement that endpoints adopt the Boundable API Profile.** The research recommends it to
  API maintainers; this standard binds the agent-system operator, who cannot make a third-party
  endpoint conform. C4.3.3 requires the operator to remediate or declare, which is what an operator
  can actually do.
- **No numeric threshold for how many endpoints must qualify.** The 16.7 / 25.0 / 58.3 split is a
  survey of 24 endpoints in six sectors, not a population estimate, and cannot support a quota.
- **No requirement of differential fuzzing.** §Actionable Recommendations item 4 recommends it, but
  the research gives no pass criterion, and a requirement to run a test with no defined outcome is
  not auditable. It belongs in guidance until someone specifies what counts as passing.
- **No change to C4.1.7 / C4.1.8.** Path-aware authorization and trust-transfer are a different
  finding (SCR-Bench) and remain as they are.

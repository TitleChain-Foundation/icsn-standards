# Independent Paper Review — Round 3 (Cross-Model, Three Lenses)
<!--aais-record-->

**Date:** August 2026 · **Method:** three independent passes by a different vendor's model (OpenAI Codex), each given a distinct reviewer lens and the full paper text, instructed to review to the standard of IEEE S&P / USENIX Security / CCS.

**Verdict: 2 (weak reject) from all three, all at high confidence.** Rounds 1 and 2 were human-simulated reviews by the same model that wrote the paper; this is the first pass by a model that did not.

| Lens | Rating | Blocking | Major | Minor |
| --- | --- | ---: | ---: | ---: |
| Security | 2-weak-reject | 3 | 5 | 1 |
| Empirical | 2-weak-reject | 1 | 4 | 2 |
| Standards | 2-weak-reject | 2 | 5 | 1 |

## Blocking findings

### B1. The Tier 3/4 claim conflicts with the stated trust assumptions. §4.2 says, “At Tier 3, there is nobody left to trust,” and §7.4 says Tier 3 is obtaine

*Lens:* Security · *Where:* §4.2; §7.1–§7.4; §10.1; Figure 1.

**The objection.** The Tier 3/4 claim conflicts with the stated trust assumptions. §4.2 says, “At Tier 3, there is nobody left to trust,” and §7.4 says Tier 3 is obtained by “adding independent anchoring, so nobody has to take the vendor’s word about which code ran.” Yet §7.1 assumes (C1) that the chip vendor does not “vouch for a lie,” P1 explicitly requires (C1), and §10.1 concedes “Everything above Tier 2 rests on (A1), (B1), (C1).”

**Why it matters.** Remote attestation normally establishes a statement through an endorsement/certificate and verifier reference-value supply chain. Publishing a root does not independently establish an enclave measurement or remove trust in vendor roots, revocation, provisioning, or the party that publishes golden measurements and policy registry entries. Thus the advertised binary threshold is not defined coherently and is materially misleading.

**Suggested fix.** Define tiers in terms of explicit trust assumptions and distinguish public verifiability from trustlessness. Either retain hardware/vendor/reference-value trust in Tier 3 or provide a precise independent-verification construction and proof. Update all prose, Figure 1, and conformance claims accordingly.

### B2. Theorem 1 does not prove the stated execution-fidelity property under its actual system model. It assumes a “compliant relying party R” that checks a 

*Lens:* Security · *Where:* §7.3, Definition 1, Definition 2, Theorem 1 and proof sketch; §5.5–§5.6.

**The objection.** Theorem 1 does not prove the stated execution-fidelity property under its actual system model. It assumes a “compliant relying party R” that checks a request against H(σsnap), but Definition 1 requires σsnap to “describe[] exactly e”; no syntax/semantics relation between a snapshot and effect is defined. The proof silently treats hash equality as semantic equality. It also does not bind the agent, policy identity/version, ticket issuance time/expiry, operation idempotency semantics, response, or all effect-relevant request context.

**Why it matters.** Canonical byte equality can bind only an agreed request representation, not an external API’s semantics. Real endpoints have defaults, server-side state, redirects, retries, content negotiation, aliases, concurrent requests, and effects induced by a request body or credentials. A ticket can therefore authenticate a different semantic effect while all listed checks pass. The formal result is at best an authenticity result for a narrowly specified request message.

**Suggested fix.** Specify an effect model and a deterministic request-to-effect relation, including endpoint parsing and relevant server state, or weaken the theorem to message-level authorization. Bind a unique operation identifier, audience, expiry, policy/agent/session identity, and response/effect receipt; prove the revised game with explicit replay and concurrency assumptions.

### B3. Theorem 1’s reduction is incomplete and its assumptions are inconsistent with §5.3. The construction uses c=SignkE(H(σsnap)||r||nonce), but Theorem 1 

*Lens:* Security · *Where:* §5.3; §7.3 Theorem 1/proof; §7.4.

**The objection.** Theorem 1’s reduction is incomplete and its assumptions are inconsistent with §5.3. The construction uses c=SignkE(H(σsnap)||r||nonce), but Theorem 1 requires that a valid ticket be accompanied by an allow token; that linkage is not cryptographically included in c. It also invokes collision resistance where a second-preimage/preimage-style binding property is needed for a fixed signed digest. Finally, §5.3 says options 1 and 3 “shrink the problem rather than removing it,” while later Tier-4 prose presents the ticket construction as if it covered the architecture generally.

**Why it matters.** A proof cannot transfer from the narrow ticket design to deployments using proxy/egress mediation, and an unbound allow token leaves room for substitution across otherwise matching ticket fields. Incorrect hash assumptions invalidate the stated reduction as written.

**Suggested fix.** Make ticket and decision token one signed, domain-separated object or cryptographically cross-bind them. State the exact hash assumption required. Give separate properties/theorems for each of the three mediation options, with residual trusted components made part of the theorem statement and tier assignment.

### B4. The measured implementation does not exercise the security boundary or deployment path needed for the paper's central claims, yet Sections 9.1-9.3 use

*Lens:* Empirical · *Where:* Section 9 opening paragraph; Section 9.1/Table 5; Section 9.2/Table 6; Section 10.1(1).

**The objection.** The measured implementation does not exercise the security boundary or deployment path needed for the paper's central claims, yet Sections 9.1-9.3 use it to support efficacy and overhead conclusions.

**Why it matters.** The paper states: "the enclave is an in-process object whose key is never handed out." Under the threat model in Section 7.1, the attacker owns the OS, container, orchestration, and network. An in-process object cannot model resistance to that attacker; nor does it measure attestation, enclave entry/exit, protected credential access, gateway IPC, remote ticket verification, or public-root publication. Thus "All nine are refused or caught when it is there" establishes only behavior of a cooperative harness, not the claimed end-to-end property against the stated adversary. Likewise 201 µs is not a lower bound on a deployed system in a useful end-to-end sense: it omits several mandatory deployment components, not just an enclave transition.

**Suggested fix.** This is required for acceptance. Evaluate an end-to-end prototype on at least one actual TEE platform (e.g., TDX or SEV-SNP) with a separately deployed relying-party/gateway process and an adversarial host. Report action latency and throughput including attestation/key provisioning as applicable, enclave crossings, IPC/networking, ticket verification, durable evidence storage, and anchoring. Re-run A1, A7, A8, and A9 with host-level adversarial control, clearly separating attacks that are genuinely tested from assumptions delegated to hardware.

### B5. The Tier-3/Tier-4 definition contradicts the stated trust model. Section 4.2 says, “At Tier 3, there is nobody left to trust; anyone can check the evi

*Lens:* Standards · *Where:* Sections 4.2, 7.1, 7.4, and 10.1.

**The objection.** The Tier-3/Tier-4 definition contradicts the stated trust model. Section 4.2 says, “At Tier 3, there is nobody left to trust; anyone can check the evidence with published tools,” while Section 7.1 assumes “(C1) get the chip vendor to vouch for a lie” cannot happen, Section 10.1 says “Everything above Tier 2 rests on (A1), (B1), (C1),” and Section 7.4 claims that “You get to Tier 3 by adding independent anchoring, so nobody has to take the vendor’s word about which code ran.”

**Why it matters.** Anchoring a TEE-produced statement can make its history publicly auditable; it does not independently establish the hardware measurement, key provenance, or correctness of the chip-vendor attestation root. Thus it cannot remove C1. A standard whose primary procurement threshold is based on this distinction is unsound or, at minimum, materially underspecified.

**Suggested fix.** Redefine tiers in terms of explicit trust assumptions. For example, distinguish public verifiability of evidence from trust independence of its roots, and require every conformance claim to enumerate hardware vendor, endorsement-key, verifier, transparency-log, witness, and relying-party assumptions. Do not label vendor-rooted TEE evidence “trust no one.”

### B6. The paper claims an “open standard with six domains of verification covering 125 testable requirements” (Abstract), but the requirements, their identi

*Lens:* Standards · *Where:* Abstract; Sections 1, 4, 5.6, 8, and 10.2.

**The objection.** The paper claims an “open standard with six domains of verification covering 125 testable requirements” (Abstract), but the requirements, their identifiers except fragments such as C7.3.5, normative language, applicability conditions, and pass/fail procedures are not presented. Referring to an unspecified repository is inadequate for a self-contained security evaluation.

**Why it matters.** Neither the coverage results nor conformance, security, and adoption claims can be assessed without the actual normative corpus. “Testable” is particularly unsubstantiated: many requirements may require judgment, unavailable source material, or a trusted test harness. Implementers cannot determine the minimal conforming profile or mutually interoperable behavior.

**Suggested fix.** Include the complete normative requirements as an artifact with immutable version/commit hash; provide a requirements-to-test mapping, applicability/profile rules, error handling, conformance claim syntax, and a machine-runnable conformance suite. In the paper, tabulate each domain’s requirement classes and representative normative requirements.

## Status

Two defects were found while working through the review and are **fixed**, with regression coverage as attacks A10 and A11:

* **A10 — the binding check failed open.** `RelyingParty` performed check (iv) of Theorem 1 by calling a snapshot probe, and returned *match* when no probe was configured. A probe requires a callback into the enclave, so essentially no independent endpoint could supply one. An endpoint with `enforce=True` that verified signature, measurement, resource and nonce would still execute a substituted action. The capability now carries a digest of the action itself, which a relying party can recompute unaided, and the check refuses when it can do neither.
* **A11 — capability and evidence record were not cross-bound.** They were two independently signed objects that happened to agree on a snapshot digest, so a valid ticket could be presented beside a record it was never issued with. The capability now commits to the step index and the digest of its evidence record.

The blocking findings above are **not** addressed. Three need decisions rather than code:

1. **The Tier 3 definition contradicts the trust assumptions** (raised independently by two lenses). The paper says Tier 3 means "nobody left to trust" while also assuming the chip vendor does not vouch for a lie. Anchoring makes a history publicly auditable; it does not establish a hardware measurement or remove the endorsement root. Tiers should be defined by *which* trust assumptions remain, distinguishing public verifiability from trust independence. **This is a normative change to the standard, not a wording fix.**
2. **Theorem 1 binds a message, not an effect.** Definition 1 says the snapshot "describes exactly" the effect, but no snapshot-to-effect relation is defined, and canonical byte equality cannot bind an endpoint's semantics — defaults, redirects, retries, aliases, server-side state. The honest repair is to weaken the theorem to message-level authorization and say plainly that endpoint semantics are out of scope.
3. **No real TEE.** Both the Security and Empirical lenses call this required for acceptance, not a limitation to note. Under an adversary that owns the OS, an in-process object cannot model resistance to anything.

## Reproducing

```bash
pdftotext -layout paper/main.pdf paper.txt
# then one pass per lens, with the prompt and schema in this directory
```

---

*Proof-of-Control is stewarded by the [Advanced AI Society](https://advancedaisociety.org/) — **[join at advancedaisociety.org](https://advancedaisociety.org/)**.*

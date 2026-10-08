<!--aais-record-->

# Style notes for `paper/main.tex`

**What this is.** `aais_check.py` reports advisory flags on this manuscript that are **deliberate and should stay**. Each is recorded here with its reason so nobody re-litigates a decision that was already made carefully, and so nobody "fixes" a use the paper depends on.

**How to use it.** Run the linter. Every blocking flag is a defect and must be fixed. Every advisory flag should either appear in a category below, or be new and want a decision. **If you add a retained use, add it here.**

**Why a record rather than suppression comments.** An `<!--aais-allow-->` marker suppresses every rule on its line, not the one you meant, so a marker placed for one word silently hides anything else on that line. Batch 1 hid two unrelated advisory flags that way with only seven markers. Owner decision, 2026-08-31.

**Last reviewed:** 2026-08-31, against the batch 2 substitutions. **79 advisory flags, 0 blocking.**

---

## `check` · 38 retained

**A named control, not the verb.** The paper defines controls called checks and its theorems cite them by number. Renaming these means rewriting Theorem 1 and Proposition 1.

> `check~(i)`, `check~(ii)`, `check~(iv)` in the proof sketch · *the far-end check* · *the truncation check* · *one specific check* · *A check is a signature verification and a comparison* · *No check anywhere is violated* · *a factual spot-check* · *ticket checking* · *its own checks* · *the checking is still done by people*

Lines 295, 296, 716, 988, 992, 996, 1001, 1010, 1078, 1084, 1142, 1149, 1177, 1308, 1367, 1370, 1377, 1378, 1847, 1927, 2056.

**A mechanism or role performing the action.** *Verify* is either tautological or wrong.

> *a **Verifier** checks it against published reference values* — the RATS role. *A Verifier verifies it* is a tautology
> *the enclave … checks the bundle signature* · *That environment checks it* · *checks before doing anything*
> *the signature **checks out*** — an idiom. *Verifies out* is not English

Lines 463, 473, 500, 522, 539, 1071, 1819.

**The word means *investigate*, not *verify*.**

> *you should **check** whether somebody already filled the gap*
> *We also **checked** whether the size of the bounded summary mattered*

Lines 1098, 1524.

**Plain English, where the house term changes the register.** Section 2 argues about human-scale oversight and deliberately uses the ordinary word.

> *…**check**? Today, in nearly every deployment, you cannot.* · *At Tier~4, **checking** is not optional*

Lines 113, 115, 177, 181, 183, 428.

**The truncation passage, lines 1927 to 1947.** *the truncation check* is a noun three words from *we checked the length*. Splitting the vocabulary across that passage breaks the confession it is making.

---

## `proof` and `proofnoun` · 31 retained

**LaTeX theorem environments, 7.** `\begin{proof}`, `\end{proof}`, `\begin{proof}[Proof sketch]`, `\label{sec:proofs}`. Structural markup, not prose. Lines 945, 986, 999, 1007, 1011, 1035, 1040.

**Genuine cryptographic proof mechanisms.** Merkle inclusion and consistency proofs, zero-knowledge statements, attestation quotes.

> *a 544-byte **proof*** · *logarithmic **proofs*** · *a **proof** of $\lceil \log_2 n \rceil$* · *a consistency **proof*** · *Those **proofs** run 224 to 480 bytes* · *a non-repudiable **proof** of equivocation* · *the relation **proven**, the setup assumption* · *the nonce … **proves** freshness* · *A quote on its own **proves** that some measured…*

Lines 136, 201, 220, 224, 347, 398, 419, 425, 638, 657, 667, 773, 1031, 1548, 1727, 1869, 1879, 1930, 1933, 1953, 2063.

**The paper's own theorems.** The manuscript contains proved theorems, so the verb is accurate.

> *We **prove** that this arrangement does not do what…* · *We **proved** the parts that are provable*

Lines 122, 2062.

**These fire because the exemption is evaluated one line at a time** and LaTeX hard-wraps prose at 78 characters, so the exempting word lands on the line above. See the open decision below.

---

## `independent` · 5 retained

Per the Owner ruling of 2026-08-31 recorded in the Verbal Brand Guide, rule 6, the ban covers **independent** as an adjective for evidence or verification in outward copy. These are the retained senses.

| Line | Use | Sense |
| --- | --- | --- |
| 730 | *An **independent** engineer implemented a verifier* | third-party independence |
| 740 | ***independent** reconstruction from a specification* | third-party independence |
| 1171 | *an **independent** generator of objections* | structural |
| 1415 | *cost **independent** of how long the agent has been going* | mathematical |
| 1993 | *without being trust-**independent*** | the passage contrasting the two words, where naming it is the point |

---

## `layer` · 1 retained

Line 1280, *At the API layer*, a cell in the comparison table naming a real stratum. Per the Owner ruling of 2026-08-31, *the evidence layer* is retained only in `README.md` and `docs/introduction.md`; this is neither that phrase nor that job.

---

## Open, and not decided here

**The linter's exemptions are evaluated per line.** LaTeX hard-wraps prose, so an exempting keyword frequently sits on a different line from the word it should exempt. Evaluating the exemption over the paragraph instead takes this file from 35 such flags to 16, and the repository from 176 to 80, with no change to any text. That is a change to a shared tool and needs an Owner decision.

**`check` has no noun form in the rule.** 24 of the 38 retained uses above are the grammatical noun. A rule that could tell a named control from a verb would not flag them at all.

**The eleven figures use neon as status chrome**, against `design_system/DECISIONS.md`. Generator change, awaiting an Owner brief.

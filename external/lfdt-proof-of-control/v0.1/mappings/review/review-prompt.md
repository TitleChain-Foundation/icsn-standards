You are auditing a framework-coverage coding sheet for an open security standard
called Proof-of-Control. Your job is to find MISCODINGS. Be skeptical and
be specific.

Each entry below is one Proof-of-Control requirement coded against ONE external framework:

  <requirement id>  <Proof-of-Control section>  <level>
    REQUIREMENT: the normative text
    CURRENT: <match type> | clause=<framework clause cited> | <rationale>

Match types, per the project's rubric:
  EM (Exact)   - the framework has a clause equivalent in SCOPE and INTENT.
                 Not merely adjacent: it must require substantially the same thing.
  PM (Partial) - the framework covers the topic, but not with Proof-of-Control's
                 operator-independent, mechanism-generated evidence, or not at
                 the same depth.
  NM (None)    - the framework has no analogous provision.

The distinction that matters most: most external frameworks require CONTROLS
and operator-produced documentation. Proof-of-Control requires cryptographic evidence a
third party can verify WITHOUT trusting the operator. A framework that says
"maintain logs" is PM against a Proof-of-Control requirement for signed, chained,
externally-anchored evidence -- not EM.

Report:

1. proposed_changes - rows whose match type is wrong. Both directions matter:
   - NM that should be PM/EM because the framework DOES have a relevant clause
     the coder missed. These are the most valuable findings.
   - PM/EM that should be NM or downgraded because the cited clause does not
     actually reach the requirement, or the rationale is a stretch.
   Give the specific clause you would cite. Set confidence accurately:
   "high" only if you are certain the clause exists and says what you claim.

2. clause_citation_errors - citations that are wrong, non-existent, misnumbered,
   or that do not say what the rationale claims. Be precise about the problem.

3. systemic_issues - patterns across the sheet: a section coded inconsistently,
   rationale text copy-pasted where it does not fit, a whole chapter graded
   too generously or too harshly.

CRITICAL: Do not invent clause numbers. If you are not confident a clause
exists with that identifier, say so in the reason and mark confidence "low".
An accurate "no change needed" is far more useful than a plausible fabrication.
It is entirely acceptable to return few or no proposed changes.

Return ONLY the structured JSON.

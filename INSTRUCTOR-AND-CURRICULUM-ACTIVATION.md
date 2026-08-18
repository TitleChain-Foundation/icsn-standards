# Instructor and Curriculum Activation

> **Status: Public Review Draft for the people's review.**

## Objective

The Foundation's first curriculum task is to organize people who can teach, mentor, review and build learning pathways for the Sophia registry. The process begins with human capability and evidence rather than an automated résumé score.

## Instructor pathway

1. **Follow the work.** Star the repository, watch releases and join public discussion.
2. **Begin IAM activation.** Teachers and attendees must first enter the separate IAM activation process. Repository activity or class registration does not itself activate IAM.
3. **Join the BOM waitlist.** After beginning IAM activation, the person may join the waitlist for a BOM member account. A waitlist position is not an activated financial account.
4. **Create an M5isYOU profile.** Select only the information the person wants to share.
5. **Choose role relationships.** Mark roles as practiced, learning, demonstrated, credentialed, able to teach, able to mentor or able to review.
6. **Add evidence selectively.** Reference a course, credential, work sample, publication, community result or peer attestation.
7. **Propose or attend a class.** State audience, outcomes, prerequisites, delivery mode, accessibility needs and assessment method.
8. **Receive human review.** Domain stewards review fit, conflicts, safety and learning quality.
9. **Pilot and improve.** Run a small cohort, collect participant feedback and version the curriculum.

## Account sequence

For the initial activation phase, the sequence is:

1. `IAM` — identity and access activation is the first required step;
2. `BOM waitlist` — the member may request a future BOM account after beginning IAM activation;
3. `BOM activation` — only an activated account may receive supported payments through that account; and
4. optional later pathways — the member may join an eligible BOU or connect an existing business to, or register a new business for, a BOB pathway under separate terms and review.

Teaching, attending, following the repository or completing an M5isYOU profile does not guarantee IAM approval, BOM activation, a BOU relationship, business registration, a BOB account, payment, employment, grant funding or Foundation membership.

## M5isYOU teaching extension

An instructor may add the following holder-controlled section to an M5isYOU profile:

```yaml
teaching:
  roles:
    - role: urn:m5:role:example:v1
      relationship: can-teach
      evidence_disclosure: holder-selected
  formats: [cohort, workshop, mentor-led, self-paced-review]
  audiences: []
  languages: []
  accessibility_practices: []
  proposed_classes: []
  availability_disclosed: false
```

This section is a declaration, not an issued credential. A verifier must distinguish self-declared, peer-attested, course-issued and Sophia-issued evidence.

## Curriculum module minimum

Every proposed module should include:

- stable identifier and version;
- title and plain-language description;
- role and capability relationships;
- intended learners;
- prerequisites, including a `none` option;
- learning outcomes;
- teaching and mentoring requirements;
- delivery and accessibility modes;
- assessment or demonstration method;
- credential or badge, if any;
- safety, privacy and conflict disclosures;
- license and reusable materials; and
- public review and change history.

## Instructor safeguards

- No hidden instructor score or permanent ranking.
- No automatic rejection based on an incomplete profile.
- No inference of protected or sensitive attributes.
- Accommodations are handled separately and are not ranking inputs.
- Teaching interest does not guarantee selection, payment or Foundation status.
- Compensated work requires a separate signed agreement.
- Compensation through M5 requires the appropriate activated account and a supported payment route. A BOM waitlist entry cannot receive payments.

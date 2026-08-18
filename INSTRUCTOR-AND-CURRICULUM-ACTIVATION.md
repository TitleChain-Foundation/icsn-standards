# Instructor and Curriculum Activation

> **Status: Public Review Draft for the people's review.**

## Objective

The Foundation's first curriculum task is to organize people who can teach, mentor, review and build learning pathways for the Sophia registry. The process begins with human capability and evidence rather than an automated résumé score.

## Instructor pathway

1. **Follow the work.** Star the repository, watch releases and join public discussion.
2. **Create an M5isYOU profile.** Select only the information the person wants to share.
3. **Choose role relationships.** Mark roles as practiced, learning, demonstrated, credentialed, able to teach, able to mentor or able to review.
4. **Add evidence selectively.** Reference a course, credential, work sample, publication, community result or peer attestation.
5. **Propose a class.** State audience, outcomes, prerequisites, delivery mode, accessibility needs and assessment method.
6. **Receive human review.** Domain stewards review fit, conflicts, safety and learning quality.
7. **Pilot and improve.** Run a small cohort, collect participant feedback and version the curriculum.

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

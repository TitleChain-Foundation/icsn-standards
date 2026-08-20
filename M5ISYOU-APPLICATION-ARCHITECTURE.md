# M5isYOU application architecture

Status: Public review draft

The public standards repository defines interoperable schemas, examples and holder-control requirements. Completed profiles, private credentials, evidence, contact details and applicant records do not belong in GitHub.

## Pilot separation

1. `icsn-standards` publishes specifications and sanitized examples.
2. A separate private application repository provides the M5isYOU and M5-CV builder.
3. Netlify deploys the application from that private repository.
4. Supabase provides temporary pilot authentication and holder-scoped storage protected by Row Level Security.
5. IAM remains the identity-origin and provenance pathway; Supabase authentication is not IAM.
6. Matrix is the default Foundation communication channel; it is not the authoritative identity or membership registry.

## Holder-control requirements

- A profile begins as a private draft.
- The holder previews the exact disclosure snapshot.
- No version becomes shareable without affirmative holder approval.
- Each approved version has a non-sequential random public identifier.
- The holder can correct, export, revoke or request deletion.
- Credentials retain issuer, subject, status and verification provenance.
- A credential validates only its stated claim and grants no ownership of the person.
- Project matching uses only holder-approved fields and never makes an automatic final hiring decision.
- Human-language claims support spoken, signed, written and multimodal languages without inferring disability or protected status.
- Programming, blockchain and AI taxonomies are versioned discovery aids, not proof of proficiency; verified credentials and approved work samples remain separate claims.

## Prohibited public data

Do not publish identity documents, private keys, wallet recovery material, account numbers, private contact details, medical information, protected-trait data or confidential evidence in issues, Discussions or pull requests.

## Pilot sequence

Create profile → save private draft → select capabilities and credentials → preview disclosure → approve version → optionally request IAM → join the BOM waitlist → optionally express BOU or BOB interest → opt into a project or curriculum pathway → consent to a Matrix invitation.

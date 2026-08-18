# Release checklist

Use this checklist for every public ICSN release. A release packages public-review material; it does not by itself establish legal effect, implementation status, endorsement or standards maturity.

## Content

- [ ] Confirm the release scope and standards status of every included document.
- [ ] Update `CHANGELOG.md` and the RFC index.
- [ ] Confirm every asset has an explicit entry in the license matrix.
- [ ] Confirm public-review drafts are labeled consistently.
- [ ] Remove private paths, personal data, credentials, wallets, secrets, internal account rules and unsupported claims.

## Review

- [ ] Complete technical, security, privacy, accessibility and governance review appropriate to the scope.
- [ ] Record material dissent, unresolved questions and implementation limitations.
- [ ] Confirm contributor attribution and any required notices.
- [ ] Obtain the approvals required by `GOVERNANCE.md`.

## Validation

- [ ] Run `python3 scripts/validate_repository.py`.
- [ ] Confirm JSON and YAML schemas parse.
- [ ] Confirm internal Markdown links resolve.
- [ ] Confirm the release renders correctly on GitHub.

## Publication

- [ ] Create an annotated tag and GitHub release using semantic versioning.
- [ ] State whether the release is a Public Review Draft, Candidate or Stable package.
- [ ] Link the relevant Discussion and issues.
- [ ] Publish a plain-language summary and contribution request.
- [ ] Verify the release appears from a logged-out browser.


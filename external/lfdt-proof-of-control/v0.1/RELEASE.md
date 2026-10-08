# Release and Versioning Policy

Proof-of-Control uses a two-part version number, `v<MAJOR>.<MINOR>` (for example, `v0.1`,
`v1.0`). Major versions cover chapter and section changes; minor versions cover additions,
removals, and material edits to requirements within the existing structure; patch fixes ship
in-branch without a separate version.

Each stable release is published as a numbered folder in this repository. Once a version is
released, its folder is locked; all future work happens in a new folder. This mirrors the
approach used by [OWASP ASVS](https://github.com/OWASP/ASVS) and
[OWASP AISVS](https://github.com/OWASP/AISVS).

```text
/
├── 0.1/        <- Working Draft v0.1.x (public comment, in progress)
```

## Current Status

The current version is **v1.0**, open for public comment until
October 30, 2026.

| Milestone | Target |
| --- | --- |
| Working Draft opens for public comment | August 1, 2026 |
| Public comment window closes | October 30, 2026 |
| Revised draft, all `[WG-INPUT NEEDED]` items resolved | November 15, 2026 |
| Working-group ratification and final review | December 2026 – January 2027 |
| **Stable Version 1.0 published** | **February 1, 2027** |

After 1.0, changes are proposed and ratified through the working-group process and released as
numbered versions, so a conformance claim always references a specific version. The published
repository is the single source of truth for the current text. The full schedule and the
adopter-side rollout guide are in [docs/roadmap.md](docs/roadmap.md); the change-control process
is in [docs/governance.md](docs/governance.md).

A **reference implementation** and a **conformance-test suite** are committed on the roadmap, so
conformance can be demonstrated with running code, not only asserted on paper.

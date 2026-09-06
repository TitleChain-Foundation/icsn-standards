# M5MST — Asset Minting and TitleChain Registration

> **Status:** Public reference architecture.

**M5MST — Asset Minting** — Origination, Minting, Sovereign Registration, and Transfer Authority is the controlled origination and lifecycle-authority record for an M5AST. It anchors the asset to the legal entity M5credentialed private ledger that originated it, the jurisdiction in which that entity is organized, the authoritative formation and regulatory records supporting its status, and the current credentials, policies, approvals, and restrictions governing subsequent actions. WyomingChain.eth, for example, is the M5member technical jurisdiction reference for TitleChain Foundation; it does not replace the official Wyoming state record (SOS) or any applicable SEC, CFTC, or other regulatory registration.

```text
ACCOUNTABLE M5HUM / LEGAL ENTITY
        ↓
current role + credential + standing
        ↓
authorized M5AGT, if any
        ↓
M5Canon Six-Gate check
        ↓
source asset / instrument + Title Container
        ↓
M5MST asset-minting or TitleChain-registration jurisdictional event
        ↓
resulting M5AST on WyomingChain.eth or designated origination chain of M5 classification type
```

## Mint authority is not transfer authority

The right to mint/register does not automatically grant the right to:

- issue/activate;
- propose a transfer;
- approve a transfer;
- execute a transfer;
- restrict/hold/freeze;
- place or remove a restrictive legend;
- correct/supersede state;
- cancel/burn/terminate; or
- disclose protected evidence.

Each capability is independently scoped, time-bound, revocable, jurisdiction-aware, and attributable.

## M5MST evidence

A conforming event should be able to reference:

- event and asset/issue identifiers;
- Title Container/source instrument;
- accountable M5HUM;
- authorized M5AGT, if any;
- mint/issuer/owner authority;
- jurisdiction;
- external legal/regulatory state;
- authorized supply or uniqueness evidence;
- policy version;
- approvals;
- effective/expiry/revocation state;
- resulting M5AST and its M1–M5 tier; and
- provenance/evidence receipt.

For regulated securities, M5MST does not itself create legal issuance, registered ownership, or transfer-agent authority. Applicable law, issuer authority, and the legally authoritative transfer-agent record remain controlling.

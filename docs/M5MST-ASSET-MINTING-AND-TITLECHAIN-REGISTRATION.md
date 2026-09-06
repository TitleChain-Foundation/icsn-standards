# M5MST — Asset Minting and TitleChain Registration

> **Status:** Public reference architecture.

**M5MST — Asset Minting** is an asset-minting event or TitleChain registration on WyomingChain.eth. It records **who had authority to mint or register an M5AST**, under which source right, issuer/owner authority, jurisdiction, policy, and approvals.

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
M5MST asset-minting or TitleChain-registration event
        ↓
resulting M5AST on WyomingChain.eth
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
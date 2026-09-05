# Certificate of Title — Multi-Party, Multi-Jurisdiction Examples

> **Status:** Public reference examples. Named companies/venues are used only to illustrate interoperability roles and do not imply a partnership, endorsement, or that the named organization uses TitleChain/M5.

The Certificate of Title/Right Record should make the **current human/entity authority, M5 account context, jurisdiction, regulated role, and append-only state changes** reconstructable.

## TCID and state

The certificate may reference the TCID/M5HUM root, but a public certificate should normally expose a **pairwise or privacy-preserving TCID reference**, not the private canonical identity record.

Keep these states separate:

```text
identity_state      active | suspended | recovered | retired
authority_state     active | limited | suspended | expired | revoked
credential_state    current | lapsed | suspended | revoked
relationship_state  employed | appointed | delegated | terminated | superseded
```

The human identity can persist while a role, credential, or transfer capability disappears.

## Account context and asset state are separate axes

```text
ISSUER COMPANY
M3-BOB account context
Delaware corporation
delawarechain.eth technical jurisdiction reference

UNDERLYING COMPANY EQUITY
M3 titled/unique source-right record

FINANCIAL REPRESENTATION
M4 financial-wrapper state

TRANSFER AGENT
M4-BOI institutional account context
SEC-registered transfer-agent role

BROKER / ATS
M4-BOI institutional account context
separately verified broker-dealer / ATS authority
```

The field name tells the reviewer which M3/M4 axis is being used.

## Example A — Delaware private issuer → Fairmint TA → eligible securities distribution/secondary path

A private Delaware corporation can be represented as an **M3-BOB** company/account context with `delawarechain.eth` as the TitleChain/JNR technical jurisdiction reference and a separate official Delaware Secretary of State evidence reference for formation/good standing.

If the company appoints **Fairmint TA** as transfer agent, the example represents Fairmint as an **M4-BOI institutional actor** with its SEC transfer-agent registration separately referenced. Fairmint publicly states that its transfer-agent subsidiary is SEC-registered, operates an authoritative shareholder register onchain, and is not a broker-dealer, exchange, or ATS.

A later private offering or secondary path adds separate records for the applicable registration/exemption, eligible-holder rules, broker-dealer/placement-agent role if required, ATS/venue eligibility if used, the transfer agent's authoritative ownership update, and settlement evidence.

The transfer agent remains distinct from the broker or trading venue.

## Example B — Human-rooted BOU / DAO-like pool

A member collective can use **M2-BOU** as its shared account/governance context, but it is never treated as a free-floating autonomous principal.

```text
M5HUM requests / authorizes registration
        ↓
M2-BOU collective context
        ↓
if a legal vehicle is formed:
M3-BOB legal-entity context
        ↓
if a regulated institutional function is required:
M4-BOI regulated operator
```

An M5AGT can automate administration only within delegated authority. The authority root remains the M5HUM/legal entity plus governing documents, credentials, jurisdiction, and M5Canon policy.

## Example C — ElectronX as a CFTC venue branch

ElectronX illustrates that the same human/entity/role/jurisdiction/evidence model can extend beyond the SEC securities stack.

**Electron Exchange DCM, LLC is a CFTC-designated contract market.** That is not the same as an SEC securities ATS. Accordingly, a private-company equity certificate should not route to ElectronX merely because it is an electronic market. Instead, a commodity/energy-derivative Title Container can resolve to the CFTC DCM branch.

## Append-only state transitions

Typical events can include:

```text
ENTITY_FORMED
GOOD_STANDING_VERIFIED
M5HUM_AUTHORITY_GRANTED
M5MST_SOVEREIGN_REGISTRATION
M5AST_CREATED
TRANSFER_AGENT_APPOINTED
CAPTABLE_MIGRATED
PRIVATE_OFFERING_ENABLED
RESTRICTION_PLACED
TRANSFER_PROPOSED
TRANSFER_APPROVED
TRANSFER_RECORDED
SETTLEMENT_CONFIRMED
ROLE_REVOKED
GOOD_STANDING_CHANGED
CORRECTION_SUPERSEDED
```

Every state change should identify the acting principal/entity, delegated agent if any, authority decision, jurisdiction, authoritative record affected, and supporting evidence.

## Six-Gate enforcement

For every consequential state change:

1. accountable M5HUM/lawful principal resolved;
2. current role/credential resolved;
3. jurisdiction resolved;
4. M5Canon policy/restrictions evaluated;
5. required accountable approval present; and
6. evidence receipt anchored.

The certificate is therefore a **stateful, jurisdiction-aware evidence record**, not merely a static PDF or token metadata file.

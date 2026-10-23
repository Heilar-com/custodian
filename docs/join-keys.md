# Join keys for bridging rooms

> Status: design claim (Markús, Grok.com briefing, 2026-10-23). Refines the "join key for longitudinal view" in `docs/civic-contract-sketch.md`. Not built; legal classification unresolved.

## Design
- There is no permanent link between a person's contributions in different rooms.
- When the system wants to propose a **bridge** (a pairing of people or contributions across rooms), it creates a fresh credential scoped to exactly that pairing.
- The person consents to each proposal separately.
- The link is dissolved after the session.

## Unresolved
- To propose a pairing at all, something must recognise the same person, or their contributions, in two rooms. Which party holds that ability, and for how long? If any party can link rooms, the data is pseudonymous, not anonymous (EDPB pseudonymisation guidance, cited in the 2026-10-23 legal brief).
- Can an alternative work where the person, not the system, holds their own per-room tokens and chooses to present two of them?
- Does a per-proposal, consented, expiring key move the data out of the "stable pseudonym" (Variant B) case? Not yet assessed.

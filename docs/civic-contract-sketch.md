# Civic Contract Sketch

This sketches a civic extension of the VitNet-style contract spine for public discourse layers.

## Core Principles
- Raw capture with explicit consent (ephemeral options, encrypted at edge).
- Aggregated anonymized signal only leaves the room.
- Electronic ID or ZK proofs as join key for longitudinal view without full identity exposure.
- Opt-in public layers for civic courage.
- Percentage-based resource/attention allocation, not binary votes.
- Self-care floors for nodes.
- Independent nodes that cooperate but maintain separation (error correction via network).

## New Ops (inspired by VitNet)
- `civic.begin`: Start a public or table session with consent scopes.
- `civic.capture`: Log raw input (voice, text, art fingerprint) with sequence and provenance.
- `civic.aggregate`: Produce discourse map embeddings, preserving dark regions.
- `civic.vote_weight`: Non-sellable presence/knowledge keys, weight by skin-in-game.
- `civic.erasure`: Export and right-to-be-forgotten for participants.
- `civic.audit`: Cryptographic proof of neutrality and non-deletion.

## Principal Kinds
- `citizen`: Longitudinal across contexts via join key.
- `table`: Scoped session with present persons.
- `node`: Independent custodian unit with floor resources.
- `network`: Cooperative but non-controlling federation.

Privacy model evolves from per-org/per-talk to per-citizen with controlled longitudinal correlation.

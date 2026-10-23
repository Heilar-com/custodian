# Civic Contract Sketch

This sketches a civic extension of the VitNet-style contract spine for public discourse layers.

## Core Principles
- Raw capture with explicit consent (ephemeral options, encrypted at edge).
- Aggregated anonymized signal only leaves the room.
- Revocable per-proposal join keys: a fresh time-boxed credential for each pairing, consent for each proposal, dissolved after the session.
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
- `citizen`: Linked across rooms only by a revocable per-proposal key, dissolved after the session.
- `table`: Scoped session with present persons.
- `node`: Independent custodian unit with floor resources.
- `network`: Cooperative but non-controlling federation.

Pairings use a fresh time-boxed credential, with consent for each proposal, dissolved after the session. Open question: recognising someone across rooms is pseudonymous while the link is live.

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
- `civic.erasure`: Export, and right-to-be-forgotten by destroying the raw content and its opening keys/salts (crypto-shredding). Raw speech lives in a deletable store and stays erasable by the participant. Only a content-free erasure record (and the now-unopenable commitment) stays in the log.
- `civic.audit`: Tamper-evident, independently witnessed log of salted commitments to every captured input and every erasure event. It provides inclusion and consistency proofs: no logged entry is removed or rewritten. It does not prove that capture was complete or that the outcome was neutral; neutrality is subject to independent process audit.

### Non-deletion scope (decided 2026-10-23)
- "Never deleted" means: no logged entry is removed or rewritten. This covers the aggregate discourse map and content-free records (commitments, sequence counts, erasure events).
- Raw speech is not covered by non-deletion. It is erasable, and each erasure is itself logged.
- Commitments to content must be salted (random per-entry salt, at least 128 bits) or keyed (HMAC); unsalted hashes of short utterances can be guessed.
- Open (legal, unverified): EDPB Guidelines 02/2025 treat salted or keyed hashes as personal data; whether a commitment stops being personal data once content and salt are destroyed is unsettled (see EDPS v SRB, C-413/23 P).
- Pilot order: public Alþingi transcripts first, then one adult table. No raw recording of minors.

Sources: RFC 6962 / RFC 9162 (Certificate Transparency), C2SP tlog-checkpoint and tlog-witness, EDPB Guidelines 02/2025, GDPR Art 9 and Art 17.

## Principal Kinds
- `citizen`: Linked across rooms only by a revocable per-proposal key, dissolved after the session.
- `table`: Scoped session with present persons.
- `node`: Independent custodian unit with floor resources.
- `network`: Cooperative but non-controlling federation.

Pairings use a fresh time-boxed credential, with consent for each proposal, dissolved after the session. Open question: recognising someone across rooms is pseudonymous while the link is live.

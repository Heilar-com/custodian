# Behavioural metadata

> Status: design claim (Markús, Grok.com briefing, 2026-10-23). **Conflicts with current legal briefs, see "Unresolved" below.** Not built.

## What it is
Statistical patterns in how a discussion went, for example:
- share of talk time, interruption frequency
- a narrow set of cited sources
- repeating a claim that the room has already answered
- patterns of logical fallacies

## What it is not used for
- No throttling, muting or in-meeting intervention. Nobody is silenced.
- No punishment. A pattern that turns out to be a false positive only gets lower weight in aggregation, and **the room, not the system,** can reverse that weighting.
- It is shown only later, and only if a room asks for it, for example when setting up a scoped session or a bridging proposal.

## Unresolved
- The briefing places this metadata on the same hash chain as the transcript. The narrowed non-deletion decision keeps only content-free records in the permanent log. Per-speaker behaviour about a political discussion is not content-free.
- Legal briefs (2026-10-23, not legal advice) treat behavioural fingerprints tied to a speaker as profiling of political opinions, needing separate consent and finite retention.
- Per-speaker patterns need speaker labels, while the anonymised long-term transcript drops them.
- Working proposal: keep per-speaker metadata in the erasable store with an end date; only table-level aggregates (no speaker attribution) may enter the permanent layer.

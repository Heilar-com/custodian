# Agents: ground rules for building from this repo

For any person or AI agent that reads this repo to build from it. These rules apply to all docs, issues and PRs.

## (a) Read order
1. [README](README.md)
2. Primitives. There are two files: [primitives.md](primitives.md) at the root and [docs/primitives.md](docs/primitives.md). Read both; they say the same thing in slightly different words.
3. [Manifesto](docs/manifesto.md)
4. [Civic contract sketch](docs/civic-contract-sketch.md)
5. [Research notes](docs/research-notes.md)
6. [Prior-art index](docs/research/prior-art-index.md)
7. [Graph schema](docs/graph-schema.md)
8. [Slide deck outline](docs/slide-deck-outline.md), last. It uses metaphor on purpose.

Where an older doc disagrees with these rules, these rules and the latest dated decision win. Open an issue for the mismatch instead of silently following the older doc.

## (b) Neutral language
- Entry-level docs (README, overviews, this file, schemas) never use infection, cancer or immune-system metaphors.
- Use clinical terms: coherent / incoherent, integrity gaps, undisclosed ties, suppressed nulls, paper-mill patterns.
- Metaphor is allowed only in the slide deck and deeper docs, after the plain frame is established.

## (c) The system never settles a disagreement
- Flags and scores are claims that can be challenged, never verdicts.
- A challenge is its own node, linked to what it challenges. Both stay visible.
- Record detector provenance and model version on every flag.

## (d) No permanent per-speaker data
- Behavioural metadata and speaker scores are erasable and carry an end date.
- Speaker scores are computed on demand from challengeable flags. They are not stored as a standing number.
- The permanent layer holds only table-level or network-level aggregates, with a minimum table size, and nothing that can point at one person.

## (e) Two identities, never joined
- A wallet is for node or governance identity.
- Blind tokens are for table participation.
- No record, key, log or index may join the two.

## (f) Discourse first
Topics emerge from people talking. Research is the mirror that shows what those topics rest on. Do not start from a research agenda and fit people to it.

## (g) How to change things
- Open an issue or PR. Do not edit `main` directly. Markús merges.
- Log every design decision as a `decision` node in the graph ([docs/graph-schema.md](docs/graph-schema.md)), with its tensions as `contradicts` edges or `conflict` nodes.
- Separate confirmed findings from claims. Cite nothing you have not checked.

## Experimental Posture

There are no sacred cows. Every node, edge, primitive and design decision in this repo is a hypothesis until the data says otherwise.

The project proposes the structure and shape of the discourse layer, and tries everything experimentally: run it, observe what comes out, keep what survives. Nothing is assumed to work out of the box.

Decisions stay revisable nodes, and evidence that contradicts them is recorded as `contradicts` edges ([docs/graph-schema.md](docs/graph-schema.md)).

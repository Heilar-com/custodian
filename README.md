# custodian

A civic information layer. People talk, and what they talk about goes into a graph: topics, extracts, and how those connect. The raw words inform that graph. They do not have to stay. Holding on to anyone's exact sentence is not the point.

Precise wording belongs to research and to other public sources. Those sit still, and you can trace them. Public discourse is the part that gets to move. It is updated as people keep talking.

**People are the mind. The platform is the memory.** It reflects what was given back, crystallized enough to be cited, never frozen enough to be owned. Divergence is the data — a lattice preserves where a hive mind would converge.

**Status**: Thinking artifact. Manifesto, contract spine, and a small ontology. No production code yet. Whether any raw talk is retained at all is still open. The direction is the one above.

## Core idea

People talking first. Topics come from that talk. Research is the mirror: it shows where a topic rests on coherent or incoherent ground, where the method and the funding are visible, and where there are integrity gaps (undisclosed ties, suppressed nulls, paper-mill patterns, selective reporting).

The tool surfaces what is there and connects it in more than one way. It does not decide. Disagreement stays visible. One side does not get to erase the other.

Three primitives:
- **Verifiability** — an audit trail built as a certificate-and-checker split. Each graph's inference engine is untrusted by design. What crosses a boundary is a certificate: the asserted claims, the rule that derived each conclusion, and a hash binding it to the source set. An independent checker — sharing no code with the engine — verifies or refuses. A forged conclusion is refused by name and rule. This is inspired by the separation in [Open Ontologies](https://github.com/fabio-rovai/open-ontologies) between an untrusted reasoner and a Lean-verified checker.
- **Disagreement preserved** — when two nodes derive different claims about the same entity, both are shown with provenance. The divergence is not averaged away. It is the most interesting output the lattice can surface.
- **Incentive transparency** — funding, ties, and repeated patterns are visible metadata. A flag can be challenged.

Public, free, and open source. Funded by giving. No fee to take part. Everyone may talk.

## The federated graph: gathering in a void

There is no hub. Information does not funnel up into a center that collects. It coalesces — crystallizes into static, citable data that carries conversation forward as reflection.

Each node is its own graph: a scoped ontology whose domain is one sphere of participants (a class of people by age, work, or whatever grouping actually forms), with its own rule table, its own membrane, its own aggregation floor, and its own verdict vocabulary. A sphere is not a UI room bolted onto a shared database. It is a structural unit — same engine, different rules, different membranes.

What crosses a node boundary is a **slice**: approved extracts, derived claims, flag objects, and axiom-candidates, each carrying provenance; membrane metadata naming the rules, the aggregation size, the publication time, and the handoff-parameter version that governed it; and a salted commitment so a subscriber can later verify nothing was added or dropped. What never crosses: raw transcripts, speaker identities, blind tokens, individual-level participation, and anything below the aggregation floor.

A display composes slices from many nodes by aligning on shared entity identifiers and rendering the union with per-slice provenance visible. Its only allowed operations are fetch, align, render, and disclose. No scoring, no curation, no recommendation engine. If someone wants a scored view, that scoring must be a published, versioned function any node can run identically — and then it is just another slice.

The thresholds that govern handoff are versioned, published parameters. Every change is logged. The danger is not that a threshold exists. It is someone quietly raising it to suppress a topic that crossed it.

The static layer — research, news, politics, norms — does not need federation the way discourse does. OpenAlex is already global. What federates is the derived graph: the claims, flags, and axiom-candidates each node extracts from those public sources. Two nodes running the same mirror should produce compatible graphs, and where they diverge, that divergence is itself a claim with provenance.

## How the pieces currently fit

A sketch, not a build.

- **Open mode**: people talk, and the map is topics and extracts, including the quiet places.
- **Scoped mode**: a sphere picks a topic, and an agent brings in provenance from the graph, the nearest support and the nearest contradiction, funding included.
- **Bridging**: the system can suggest a pairing across spheres, with a join key that is consent-based and revocable.
- **Behavioral patterns**: talk ratios, repeated claims, narrow citations, fallacy density. Metadata only. No interrupting the sphere. A flag can be challenged.
- **Seed path**: public speakers first, where the words are already on the record (parliamentary transcripts, and podcasts as another named class). Then people talking without their names on the words.
- **Voice**: used to check consent and whether the capture is usable. Never to label intent or character.

## Docs

- [Manifesto](docs/manifesto.md)
- [Primitives](primitives.md)
- [Civic Contract Sketch](docs/civic-contract-sketch.md)
- [Research Notes](docs/research-notes.md)
- [Meeting modes](docs/meeting-modes.md)
- [Join keys](docs/join-keys.md)
- [Behavioural metadata](docs/behavioural-metadata.md)
- [Challengeable flags](docs/challengeable-flags.md)
- [Participant classes and seed path](docs/participant-classes.md)
- [Handoff: from discourse map to agenda](docs/handoff.md) (proposal)
- [Adversary model](docs/adversary.md) (proposal)
- [Graph schema](docs/graph-schema.md), [seed data](graph/graph.yaml) and the [checker](graph/README.md)
- Visions (hypotheses, not decisions): [Solo node and AI-as-questioner](docs/visions/solo-node-and-reverse-rag.md), [Idea farm](docs/visions/idea-farm.md), [Diary, commons and coin](docs/visions/diary-commons-and-coin.md) (superseded)
- [Slide Deck Outline](docs/slide-deck-outline.md) (organism metaphor and cascade for deeper exploration)
- [Framework](docs/framework.md) (a small ontology, beside this civic sketch)
- [Video outline: the membrane](docs/video-outline.md) (exploration notes, not the project pitch)

## Licensing

Documentation, research notes, manifestos, and other written content are under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by-4.0/) (CC BY 4.0). Attribution is required.

Source files, scripts, and configuration files are under the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html) (AGPL-3.0).

Which paths and file types each license covers is set out in [LICENSE](LICENSE). The verbatim texts are [LICENSES/CC-BY-4.0.txt](LICENSES/CC-BY-4.0.txt) and [LICENSES/AGPL-3.0.txt](LICENSES/AGPL-3.0.txt).

Start small. One node. One table. Let the talk move.

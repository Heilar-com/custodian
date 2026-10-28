# custodian

A civic information layer. People talk, and what they talk about goes into a graph: topics, extracts, and how those connect. The raw words inform that graph. They do not have to stay. Holding on to anyone's exact sentence is not the point.

Precise wording belongs to research and to other public sources. Those sit still, and you can trace them. Public discourse is the part that gets to move. It is updated as people keep talking.

**Status**: Thinking artifact. Manifesto, contract spine, and a small ontology. No production code yet. Whether any raw talk is retained at all is still open. The direction is the one above.

## Core idea

People talking first. Topics come from that talk. Research is the mirror: it shows where a topic rests on coherent or incoherent ground, where the method and the funding are visible, and where there are integrity gaps (undisclosed ties, suppressed nulls, paper-mill patterns, selective reporting).

The tool surfaces what is there and connects it in more than one way. It does not decide. Disagreement stays visible. One side does not get to erase the other.

Three primitives:
- **Verifiability** (an audit trail, not the truth)
- **Disagreement preserved**
- **Incentive transparency**

Public, free, and open source. Funded by giving. No fee to take part. Everyone may talk. People can also talk in their own spheres, by age, work, or whatever groups actually form. A sphere is a room, not a gate.

## How the pieces currently fit

A sketch, not a build.

- **Open mode**: people talk, and the map is topics and extracts, including the quiet places.
- **Scoped mode**: a room picks a topic, and an agent brings in provenance from the graph, the nearest support and the nearest contradiction, funding included.
- **Bridging**: the system can suggest a pairing across rooms, with a join key that is consent-based and revocable.
- **Behavioral patterns**: talk ratios, repeated claims, narrow citations, fallacy density. Metadata only. No interrupting the room. A flag can be challenged.
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

Documentation, research notes, manifestos, and other written content are under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/) (CC BY 4.0). Attribution is required.

Source files, scripts, and configuration files are under the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html) (AGPL-3.0).

Which paths and file types each license covers is set out in [LICENSE](LICENSE). The verbatim texts are [LICENSES/CC-BY-4.0.txt](LICENSES/CC-BY-4.0.txt) and [LICENSES/AGPL-3.0.txt](LICENSES/AGPL-3.0.txt).

Start small. One node. One table. Let the talk move.

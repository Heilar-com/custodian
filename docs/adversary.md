# Adversary model

> Status: proposal (Claude Fable 5.1 with Markús, 2026-10-24). Not a decision, and no `decision` node is recorded for it. Expands `dsn:adversary-model` in [graph/graph.yaml](../graph/graph.yaml). Every line below under "what the design buys" is a claim about an unbuilt system. Nothing has been attacked yet. The pattern is the adversarial track in Cornell's Laude moonshot proposal (prior-art index entry 2), which stress-tests the system against its declared roles: each attack here is meant to become a test the pilot runs before any citizen table is recorded, not an argument that the design holds.

For each attack: what the existing design buys, and what it does not. Sources are the prior-art index, the [civic contract sketch](civic-contract-sketch.md), the [graph schema](graph-schema.md) and the rules in [agents.md](../agents.md).

## 1. Flooding tables and endorsements
Sybil tables that never met, paid participants, or a coordinated campaign to push one topic across the handoff threshold ([handoff.md](handoff.md)).

- **Buys.** Blind tokens tied to an eligibility proof (ZKorum's zero-knowledge passport route, self-description, entry 3) make each token cost a real eligible person. Voice used for proof of consent and capture quality raises the cost of a fabricated table. Thresholds are tunable parameters, as in Join's point 21 (entry 11). Nothing is deleted, so a flood stays visible as a pattern after it ends. Incentive transparency applies to proposers.
- **Does not.** A token proves a person, not an unpaid one. Join verifies identity by phone and email and organised interest groups still pass more often (entry 11). Telling a paid campaign from a motivated public is not possible from the record alone. Detecting coordination needs correlation across tables, which is exactly what rules (d) and (e) restrict. Attesting that a table physically met makes the node a trusted party. `primitives.md` says flood protection is required; no mechanism is specified anywhere.

## 2. Poisoning the research graph
Paper-mill output, self-citation chains, reviews and models with no primary data, press releases cited as primary, so that a weak claim appears well supported. This is the Woozle effect (entry 12): Greenberg's citation bias, amplification and invention; Rekdal's moves of citing a secondary as primary, padding with secondaries and dropping hedges.

- **Buys.** The independence rule in the graph schema: supports linked by `same-as`, `derives-from` or a cites-only basis, or sharing provenance, count once, and axiom-candidate status needs two independent supports from different tiers. Greenberg's three distortions map onto those exclusions. A `contradicts` edge never hides a `supports` edge, and a disputed claim is marked disputed.
- **Does not.** The rule governs axiom-candidate status only. It says nothing about what scoped mode retrieves as the nearest source ([meeting-modes.md](meeting-modes.md), open question). It works only on edges that exist: an undeclared `derives-from` is invisible until someone records it. Check 4, different provenance, is defeated by a mill that fabricates distinct author groups and journals. There is no marker for a paper with no primary data, so amplification papers count as sources (entry 12, open question). Any retrieval that weights by citation inherits the measured bias toward significant results, 1.6 to 2.1 times (entry 12). An empty funding field in OpenAlex reads as no tie.

## 3. Capturing a node or its funder
A node operator, its funder, or whoever trains and funds the matching model shapes retrieval, routes handoff questions, or decides what gets captured.

- **Buys.** Independent nodes that cooperate but stay separate (civic contract). An independently witnessed audit log, so a captured node cannot remove or rewrite a logged entry. Incentive transparency applied to the system itself (`dsn:self-applied-incentive-transparency`): node funders and model providers are disclosed as ties like any other.
- **Does not.** The sketch says itself that `civic.audit` proves inclusion and consistency, not that capture was complete or the outcome neutral. Omission leaves no entry to witness. Disclosure shows a tie; it does not remove it (`cnf:matching-ai-as-undisclosed-tie`). A witness can go dormant: ZKorum's never verified or stored proofs and has been dormant since 2025-03, and its proof channel never covered moderation (entry 3). Node separation buys nothing if the nodes share a funder; concentration of funding is itself a tie to show.

## 4. Gaming or disputing detectors at scale
A flood of flags against one speaker, which is a smear with provenance. A flood of disputes to bury a real one. Probing a detector's version for phrasing it misses.

- **Buys.** Flags carry detector, model version and date ([challengeable-flags.md](challengeable-flags.md)). A dispute is a claim. No verdict exists to flip. Version drift is auditable. Speaker-level readings are computed on demand and erasable (`dsn:on-demand-speaker-scores`).
- **Does not.** "Both stay visible" gives no way to read a thousand disputes; volume becomes the signal. Who may file a flag or a dispute, and at what cost, is unspecified. Filed through blind tokens, a dispute flood is indistinguishable from a room that disagrees. Flags attach to claims and stay, while the per-speaker pattern they add up to must be erasable under rule (d). The Laude pattern applies here first: red-team the detectors before deployment and publish their failure rates as claims.

## 5. Re-identification from small tables
Combine a table's aggregate (topic, region, date, dark regions, scoping choice) with outside knowledge to name a speaker.

- **Buys.** Rule (d): only table-level or network-level aggregates with a minimum table size enter the permanent layer. Per-speaker metadata is erasable with an end date. Commitments are salted. Voice is never used to label a person.
- **Does not.** No number and no method is set. Iceland's forums sat eight and nine to a table (entries 10 and 13); in a country of this size, topic plus municipality plus date can identify a table, and from a table of eight often a speaker. What a table avoided (dark regions) identifies too. A solo node ([visions/solo-node-and-reverse-rag.md](visions/solo-node-and-reverse-rag.md)) is a table of one. A floor high enough to protect at municipal scale shrinks the map at that scale. Whether a salted commitment stops being personal data once content and salt are destroyed is unsettled (`cnf:commitments-as-personal-data`).

## 6. Forcing a join between wallet and table identities
Correlate timestamps on wallet governance actions with timestamps on table commitments in the public audit log, or use network metadata seen by a node, to link a governance identity to a table participant.

- **Buys.** Rule (e): no record, key, log or index joins the two. Per-proposal join keys dissolve after the session ([join-keys.md](join-keys.md)).
- **Does not.** Rule (e) governs records, not side channels. The audit log is public and timestamped by design; governance actions are timestamped; one node operator may see both. The join-keys document already concedes that something must recognise the same person across rooms while a key is live. Mitigations to test, all untested: batching commitments into fixed intervals, delaying publication, separating the operators of governance and of tables. Each trades against audit freshness or against node count.

## 7. Erasure abuse versus erasure as a right
A speaker erases raw speech to escape a record of what they said. Or an operator erases under the guise of a participant's request.

- **Buys.** Erasure is crypto-shredding of raw content. A content-free erasure event stays in the log with the now-unopenable commitment, so the fact and time of erasure are provable (`cnf:erasure-vs-audit-trail`). The aggregate map is not erasable. The request itself carries provenance.
- **Does not.** Whether claims and flags derived from an erased utterance go with it is unspecified. The seed path records a card per claim from public transcripts ([participant-classes.md](participant-classes.md)); whether a named public speaker holds an erasure right over that card is unaddressed. An erasure record shows that something was removed, not what. A pattern of erasures around one topic is visible, and is itself a per-speaker trace. The design does not try to tell abuse from right. That is consistent with rule (c) and leaves the gap in view.

## 8. Record loss
A node shuts down, a funder withdraws, a domain lapses, a witness goes quiet.

- **Buys.** `civic.audit` follows Certificate Transparency: inclusion and consistency proofs, independent witnesses, several nodes. At least the commitments are meant to survive the node.
- **Does not.** Þjóðfundur 2009's own site now serves unrelated content and its results pages return 404; even the published summary did not last a decade (entry 13). ZKorum's witness never stored proofs (entry 3). A commitment proves what was published and when, not the content, if the content store dies with the node. Witnesses need operators and funding, which is another tie. Who keeps a copy with no stake in the content is open (entry 13 names vefsafn.is as unchecked).

## What the pattern asks for
Each attack above becomes a test. Results are recorded as claims, with `contradicts` edges to the design items they weaken, before any decision rests on those items.

## Unresolved
- Minimum table size has a name in rule (d) and no number, no method and no owner.
- Every coordination detector in attacks 1 and 4 needs cross-table or cross-room correlation. Candidate `conflict` node with rules (d) and (e).
- Who may file flags and disputes, and at what cost: a blind token can be flooded; a wallet joins governance identity to table content. Candidate `conflict` node with rule (e).
- Erasure of raw speech against the claims, flags and claim cards derived from it. Candidate `conflict` node with the non-deletion scope in the civic contract sketch.
- The independence rule has no marker for a source with no primary data.
- No document proposes a mitigation for timing correlation. Candidate `conflict` node between audit freshness in `civic.audit` and rule (e).
- No document proposes a completeness check against capture by omission. The sketch says the audit log does not prove completeness; nothing else does either.
- None of the eight attacks has been run against anything.

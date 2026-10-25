# Handoff: from discourse map to agenda

> Status: proposal (Claude Fable 5.1 with Markús, 2026-10-24). Not a decision, and no `decision` node is recorded for it. Not built or tested. Expands `dsn:handoff-agenda-power` and addresses `cnf:handoff-gap` in [graph/graph.yaml](../graph/graph.yaml). Draws only on prior-art index entries 10, 11 and 13 ([docs/research/prior-art-index.md](research/prior-art-index.md)); nothing here cites anything the index has not checked.

## The principle under test

A discourse map has no force unless some institution is bound to answer it. The working principle, to be tested rather than asserted: **agenda power, not decision power.** The map decides what must be answered in public and by when. It never decides what the answer is. Nothing in this document gives a table, a count of tables or the map itself a vote.

Why this shape and not a plebiscite. Iceland ran the whole pipeline once (entry 10): a random-sample forum, elected drafters, open comment, and an advisory referendum that approved the draft as a basis with 66.9% yes on 48.9% turnout. The bill was tabled in November 2012 and never passed; Alþingi enacted a temporary amendment procedure instead. Two failures sit in that case. No institution was bound to act on the result. And the capture step had already been damaged before the Council sat, when the Supreme Court annulled the 2010 election. Þjóðfundur 2009 (entry 13) failed one step earlier: about a hundred recommendations were published the same day and had no addressee. They were not scheduled for presentation to Parliament. A map that asks for a decision inherits both problems: it needs a legitimacy the capture step cannot carry, and it still needs someone bound to act.

Taiwan's Join platform (entry 11) is the one working case found so far. A proposal with 5,000 endorsements within 60 days becomes a case. The responsible agency must publish a reasoned response within two months, extendable once by up to two months. The agency is bound to answer, not to adopt. That is the shape proposed here. Join's evidence also sets expectations: 1.5% to 6% of endorsed proposals reach the threshold, most ministries missed the deadline in the 2015 to 2018 cases studied, and proposals backed by organised interest groups pass more often.

## Parts of the duty

**Addressee.** Every triggered question names one body obliged to answer: a ministry, an Alþingi committee or a municipality. The routing from topic to addressee is a claim made by a node, with provenance, and can be disputed like any flag ([challengeable-flags.md](challengeable-flags.md)). Join limits itself to matters within the Executive Yuan and its agencies (point 5). A Custodian map does not scope its topics in advance, so some triggered questions will have no competent addressee. Those are recorded as such, not dropped.

Hypothesis: the duty cannot be imposed by the platform. Join's duty is an executive directive the government gave itself. In Iceland the addressee would have to adopt the duty in advance, by statute, standing order or a public commitment by a party or council. Whether any Icelandic body would do so is an open research question (entry 10, open questions).

**Trigger.** Two signals, both network-level aggregates: the number of distinct tables in which a topic appeared, and persistence of the topic across rooms and over time. The threshold on each is a tunable parameter, published and versioned, as Join's point 21 lets the National Development Council adjust its threshold. Each change of threshold is itself logged. The first values are guesses to be revised against pilot data; there is no evidence yet for any particular number.

**Response.** Following Join's point 8: the answer states one of adopted, partly adopted, under study or rejected, gives reasons, and is published on the platform next to the question it answers. The answer then enters the research mirror like any other source. Its reasons are claims. Research it cites goes through the same integrity checks as anyone else's ([participant-classes.md](participant-classes.md)).

**Missed deadline.** Join shows deadlines are missed often. The platform cannot compel. What it can do: record the miss as a dated, content-free event beside the still-open question, keep the question open and visible, and count misses per addressee as a network-level aggregate. Whether a visible miss changes an addressee's behaviour is the central thing a pilot would measure. It is unknown.

**Organised endorsement.** Join's data shows organised groups pass the threshold more easily. Prevention is not proposed; detection and display are. Incentive transparency applies to proposers: where a campaign to raise a topic has an organiser or a funder, that tie is shown next to the triggered question, in the same way a funding tie is shown next to a study. Coordination patterns across tables (identical phrasing, clustered timing) are flags: challengeable, with detector and model version recorded. The attacks this invites are in [adversary.md](adversary.md).

**Trace versus content.** Three layers, following the non-deletion scope in the [civic contract sketch](civic-contract-sketch.md):
- Permanent, content-free: that a threshold was crossed, when, for which addressee, the deadline, whether it was met, and that a response exists and when it was published.
- Permanent content, in the aggregate map layer: the text of the question and the text of the response with its reasons.
- Erasable, with an end date: any per-table or per-speaker signal used to detect coordination.

## Unresolved

- Join requires the agency to contact the proposer (point 8). Tables use blind tokens and have no proposer to contact. Who, if anyone, speaks for a triggered question on the citizens' side? Candidate `conflict` node with rule (e) in [agents.md](../agents.md).
- Incentive transparency applied to proposers needs a proposer with a disclosable tie. An anonymous table cannot disclose one. Detecting an organised campaign from table patterns is per-table behavioural metadata, erasable with an end date ([behavioural-metadata.md](behavioural-metadata.md)), while the displayed tie would need to sit permanently beside the question. Candidate `conflict` node with rule (d).
- The civic contract sketch has `civic.vote_weight` (presence and knowledge keys, weight by skin in the game) and percentage-based allocation. Any weighting of whose topics count is a step toward decision power. Candidate `conflict` node between the sketch and this document.
- Routing a topic to an addressee is a judgment. If a node makes it, the node holds agenda power the tables did not give it. If the addressee makes it, it can route questions to itself or away from itself.
- Whether a triggered question is a content-free trace or content is the same open question as the scoping signal in [meeting-modes.md](meeting-modes.md).
- At Join's rates, 94% to 98.5% of endorsed topics never trigger a duty. Is a visible, mostly unanswered map worth running at that rate, or must the threshold be low enough that missed deadlines dominate?
- Join pauses proposals and endorsements for 60 days before a national election (point 9). A map that goes quiet before an election removes exactly the signal an election is about. No position taken.
- Nothing above has been put to a ministry, a committee or a municipality.

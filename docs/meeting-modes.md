# Meeting modes

> Status: design claim (Markús, Grok.com briefing, 2026-10-23). Not built or tested.

A Custodian table runs in two modes, always in this order.

## 1. Open mode
- Only the people in the room speak. No agent interrupts or adds information.
- The talk is captured with consent and turned into the discourse map, including dark regions (topics the conversation avoided).

## 2. Scoped mode
- Later, the room may choose **one** topic to look at more closely.
- An agent may then show provenance from the research graph in real time: the nearest supporting and the nearest contradicting research, plus funding information.
- **Symmetry rule:** the agent shows sources on every side, including sources with integrity gaps, or it shows nothing. It never shows only one side.
- Choosing to scope a topic is itself recorded as a signal in the map (which topics rooms chose to examine).

## Open questions
- Who chooses the "nearest" sources, and how is that retrieval logged and audited?
- Is the scoping signal content or a non-content trace? This decides whether it can sit in the permanent layer (see `docs/civic-contract-sketch.md`, `civic.audit`).

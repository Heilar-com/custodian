# Challengeable flags

> Status: design claim (Markús, Grok.com briefing, 2026-10-23). Extends the "disagreement preserved" primitive (`primitives.md`). Not built.

A flag from an automated detector (for example "possible logical fallacy") is not a verdict. It is a **claim**, stored like any other claim, with provenance:
- which detector produced it, its version and model, and when
- the passage it refers to

Anyone reviewing later can file a **dispute**. The dispute is its own claim, linked to the flag. Both remain visible. The system does not decide between them.

Recording detector name and version makes the flagging itself auditable: a reviewer can see if a change of model changed the flags.

## Open question
Slides 6 and 8 in `docs/slide-deck-outline.md` describe truthfulness scores, trust metrics and "high-fallacy speakers". A per-speaker score resolves disagreement on the reader's behalf. Should flags stay at the level of individual claims, with no speaker-level score?

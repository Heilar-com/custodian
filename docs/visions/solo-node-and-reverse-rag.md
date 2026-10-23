# Solo Node and AI-as-Questioner (Vision / Hypothesis)

**Status:** Vision. Under the Experimental Posture (agents.md), this is a hypothesis until data says otherwise. It is not a decision and nothing here is built.

## Summary
This doc proposes two more input channels next to group tables:

1. **Solo node.** One person records a monologue, or a conversation with an AI, through an app. Identity is proven with Icelandic electronic ID (rafræn skilríki) and bound to a Sui wallet address. The recording is transcribed. Raw data is stored on Walrus and is owned by the citizen through cryptography. The citizen may choose to connect it to the discourse layer using the same eID and wallet. The system processes only what is handed over (labels, concepts, light writing), and nothing is taken without an explicit handoff.
2. **AI-as-questioner ("reverse RAG").** The AI produces the questions and people supply the answers, possibly for payment. Low-quality or noisy answers are kept as variability data and filtered by the integrity layer.

The key difference from bridging: in a solo node the **citizen** links identities, voluntarily and reversibly. The system does not.

## Channel comparison
| Channel | Who links identity | Social filter | Signal it gives | Main risk |
|---|---|---|---|---|
| Group table | Nobody (blind tokens, anonymous) | High: real-time social editing | Social performance and disagreement | Self-censorship, small-table re-identification |
| Solo node | The citizen (eID + wallet, opt-in, reversible) | Low: no audience | Unfiltered prior: what people think rather than perform | Linkage leaking into table identity; erasure of stored raw data |
| AI-questioner | Not decided | Medium: shaped by the question | Directed exploration of what the system does not know | Incentive distortion from payment; question bias |

## 1. Solo node
Group talk is edited socially in real time. People self-censor and perform. Alone, that filter drops, so solo input may be the highest-signal channel for what people actually think. This is data multiplayer nodes cannot produce.

Flow (hypothesis):
1. Prove citizenship with rafræn skilríki, then bind it to a Sui wallet.
2. Record a monologue or AI conversation in the app, then transcribe it.
3. Store the raw data on Walrus under the citizen's control.
4. Optionally hand over a selected portion to the discourse layer. The system derives labels and concepts from it and does nothing else.

Citizen-stitched vs system-stitched: bridging (docs/join-keys.md) needs some party to recognise one person across rooms. Here the person holding the keys presents the link and can withdraw it.

## 2. AI-as-questioner (reverse RAG)
Today humans prompt models to build and curate. Flip it: in a post-labour world, the AI's goal becomes "get to know humanity". The AI is the source of questions and the human is the source of input, possibly paid for answering.

This connects to Markús's earlier "feedback loop" idea: the AI fertilises the human mind and watches what grows. It is prompt-testing turned around and used as a way of knowing. Even gibberish is a seed. It carries variability, and the integrity layer sorts signal from noise.

## Together
Group, solo and questioner channels form a spectrum. Solo gives the unfiltered prior. Group gives social performance and disagreement. The questioner probes the gaps in the map. Comparing channels may show where people's private and public positions differ.

## Open tensions (with existing repo decisions)

These are flagged, not resolved. Nothing here overrides a recorded decision.

- **Solo node privacy risk (sharpest edge case).** In a group node a wrong label is spread across roughly fifteen people and dilutes; in a solo node, one wrong flag lands on one citizen whose identity is bound to a Sui wallet. This must be resolved before anything merges.

1. **Two identities, never joined (agents.md rule e).** The wallet is for governance identity, and blind tokens are for table participation. A solo node binds eID to the wallet. That link is started by the citizen, but it must never flow into table tokens: no shared identifiers, no timing correlation, and no handoff that shows a person both spoke solo and sat at a given table. How a citizen could bring solo material and table material together without breaking rule (e) is still open.
2. **Walrus storage vs erasure.** The non-deletion decision (2026-10-23) keeps raw speech in a deletable store, erasable by crypto-shredding (docs/civic-contract-sketch.md, `civic.erasure`). Walrus blobs are public, and earlier integrity research found Seal unsuitable for erasure. So each entry would need encryption before upload, with keys the citizen can destroy. Whether "owned by the citizen" holds when keys are lost or the citizen withdraws is not assessed.
3. **GDPR Art 9 and consent withdrawal.** Solo monologues may reveal political opinions (special category). Withdrawing consent has to reach any data already handed to the discourse layer, including derived labels. Profiling (Art 4(4)) applies if solo labels are tied to a wallet. A DPIA applies (Auglýsing 828/2019). The controller for solo data is not decided.
4. **No per-person permanent data.** Derived labels from a wallet-linked solo session are per-person data. They cannot enter the permanent layer, which holds only aggregates with a minimum size.
5. **Payment for answers.** Payment may shift answers toward what pays, invite volume over substance, and affect whether consent is freely given. Paying requires an identity or payment rail, which creates a new linkage risk. Not assessed.
6. **Questioner bias.** Whoever sets the AI's questions shapes the map, which echoes the scoped-mode retrieval audit question.

## Not yet verified
The feasibility of eID-to-wallet binding, Walrus erasure in practice, and the legal basis for paid answers. All need research briefs before any decision.

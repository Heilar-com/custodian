# Prior-art index

Annotated index of projects and studies related to Custodian. Checked 2026-10-23 (Atlantic/Reykjavik).

How to read each entry:
- **Confirmed**: checked against the primary source linked in the entry.
- **Self-description**: what a project says about itself. Not independently checked.
- **Not verified**: we could not find a primary source for it.

Status markers: **Verified** / **Partly verified** / **Not verified**.

---

## 1. Audrey Tang and Caroline Green: Civic AI and the 6-Pack of Care
**Status:** Verified (framework and authorship); the vTaiwan lineage is a statement the authors make.

- **What they built or studied.** Confirmed: "Civic AI — 6-Pack of Care" is a research project by Audrey Tang and Caroline Green at the Oxford Institute for Ethics in AI (Accelerator Fellowship Programme). The six packs are Attentiveness, Responsibility, Competence, Responsiveness, Solidarity and Symbiosis. civic.ai describes the goal as AI "that the people it affects can check, correct and switch off". Packs 1–4 follow the four phases of care set out by Fisher and Tronto (1990). Self-description: the site says a book is due from Wiley in February 2027 and that the framework was presented at Rhodes House, Oxford, on 25 March 2026.
- **Lineage.** Self-description: the Oxford article says the framework builds "on real-world precedents such as the vTaiwan platform" and on the ⿻ Plurality vision.
- **Strongest overlap with Custodian.** Pack 4 (Responsiveness): affected people can contest outcomes and force a repair. Custodian's challengeable flags and its "the system is not the editor" rule ask for the same thing.
- **Open questions.** Can the per-pack "public measure" serve as an audit check for Custodian's integrity layer? Pack 6 (one job, one place, time-limited) compared with Custodian's permanent record. Has the framework been tested against any deployed system?
- **Sources.** https://civic.ai/ · https://afp.oxford-aiethics.ox.ac.uk/civic-ai · https://afp.oxford-aiethics.ox.ac.uk/article/civic-ai-and-6-pack-care-reimagining-ai-alignment-relational-health · https://civic.ai/podcast/

## 2. Cornell team, Laude Institute Moonshot: "Rebuilding Trust in Civic Discourse: An Auditable AI-Mediated Infrastructure"
**Status:** Verified (grant and amounts, via the Laude page and Cornell Chronicle in the landscape brief).

- **What they built or studied.** Confirmed: the Cornell team (PI Jon Kleinberg, with Bazarova, Danescu-Niculescu-Mizil, R. Kleinberg, Naaman and Rand) received a **$250,000 seed** from the Laude Institute and is competing for **$10M**. It is one of 8 seeds. The project is a *proposal*. It has three layers: AI assistants for individuals, AI moderators for groups, and an independent AI auditing layer that produces "a transparent record of each agent's interventions". It also has an adversarial track for stress-testing. No code was found.
- **Strongest overlap with Custodian.** An audit trail as trust infrastructure. The difference: Cornell audits AI agents against their declared roles, while Custodian keeps a record of human speech and of the research it cites.
- **Open questions.** What exactly does the cryptographic verification cover? Would the adversarial track test Custodian's detectors? Also look at the second Laude civic team: Harvard/MIT "Deliberation at National Scale" (Procaccia et al., Frankly platform).
- **Sources.** https://www.laude.org/moonshots/one/rebuilding-trust-civic-discourse · https://news.cornell.edu/stories/2026/04/moonshot-project-aims-restore-trust-digital-public-sphere · https://www.laude.org/updates/moonshots-one

## 3. ZKorum / Agora Citizen Network
**Status:** Partly verified (licence, repo, funders and audit code confirmed; ZK identity and AT Protocol DDS are self-description).

- **What they built.** Confirmed: an open-source monorepo, `zkorum/agora`, licensed AGPL-3.0, maintained by ZKorum (Paris) and very active (HEAD `98edd28`, 2026-10-21). Funding comes from EU Horizon Europe through NGI TrustChain and NGI Sargasso. Self-description: zero-knowledge proofs of eligibility (for example ZK passport proofs), Polis-style opinion clustering and bridging ranking, and a planned move to the Decentralized Deliberation Standard (DDS) on AT Protocol with "tamper-evident verification".
- **Code findings (landscape brief, 2026-10-23).** From 2025-01 to 2026-02 the API published a proof of 8 write actions to a Nostr channel. **Moderation endpoints were never covered.** The watchdog witness never verified or stored proofs and has been dormant since 2025-03. The broadcast was removed in commit `d968353` (2026-02-22) because "the project is moving to DDS". Moderation today is ordinary mutable Postgres rows, and deletion is soft-delete followed by hard delete. Conclusion: there is no working verifiable-moderation feature to layer on.
- **Strongest overlap with Custodian.** Proving eligibility without revealing identity, combined with preserved disagreement.
- **Open questions.** Will DDS cover moderation actions and deletions, and when? Has anyone audited the ZK passport route, and does it work in Iceland? The `zkorum/dds` and `zkorum/racine` repos have not been inspected.
- **Sources.** https://github.com/zkorum/agora · https://github.com/zkorum/agora/commit/d968353d5f1f34ae50f57a7392d078e251a3dc17 · https://github.com/zkorum/watchdog · https://trustchain.ngi.eu/zkorum/ · https://www.agoracitizen.network/

## 4. Pol.is / Computational Democracy Project
**Status:** Verified (licence, method, vTaiwan Uber case); funder not verified.

- **What they built.** Confirmed: open-source software (AGPL-3.0, `compdemocracy/polis`). Participants agree, disagree or pass on short statements and cannot reply to each other directly. The software clusters opinion groups and shows consensus statements next to divisive ones.
- **vTaiwan Uber case (August 2015).** Confirmed: it was the first vTaiwan process to use Pol.is. There were 4 weeks of survey, 31,115 votes, 925 survey voters and 145 statements. A live-streamed two-hour meeting followed on 2015-08-27 with 1,875 online participants. Afterwards Uber committed to sharing its insurance policy and to having drivers registered (Audrey Tang's account on the pol.is blog; the CrowdLaw case study). Self-description (Co-Intelligence Institute): statements with more than 80% consensus set the agenda.
- **Strongest overlap with Custodian.** The preserved-disagreement primitive in its working form.
- **Open questions.** Funder. Can Custodian take in Pol.is exports as an input to its discourse map? What AGPL obligations would apply?
- **Sources.** https://pol.is/ · https://github.com/compdemocracy/polis · https://compdemocracy.org/case-studies/2014-vtaiwan/ · https://blog.pol.is/uber-responds-to-vtaiwans-coherent-blended-volition-3e9b75102b9b · https://congress.crowd.law/files/vtaiwan-case-study.pdf

## 5. Bak-Coleman, West, O'Connor, Bergstrom (2026): "Industry Influence in High-Profile Social Media Research"
**Status:** Verified.

- **What they studied.** Confirmed (arXiv:2601.11507): 295 social media articles in Science, Nature, PNAS and their transfer journals. 49% [43–55%] have disclosable ties to Meta, X, Google or Microsoft (funding, collaboration or employment), and fewer than half of those disclose them. 42% of papers that declared "no competing interests" still had ties. Industry-tied work receives roughly twice the attention. Ties are concentrated in few people (Gini 0.919). About 35% of papers with an academic editor were handled by an editor with ties. The estimated share of papers with industry involvement across production and review is 79.9%. The authors call their figures a conservative lower bound.
- **Strongest overlap with Custodian.** It is a working example of incentive transparency: OpenAlex funding data joined to papers. That is the method Custodian's research mirror proposes.
- **Open questions.** The dataset is not released for de-identification reasons, so can the method be reproduced on open data alone? How well does it carry over to Icelandic or Nordic venues?
- **Sources.** https://arxiv.org/abs/2601.11507

## 6. Briggs, Mellon, Arel-Bundock (2026): "It must be very hard to publish null results"
**Status:** Verified.

- **What they studied.** Confirmed: 101,475 articles from 156 political science journals, 2010–2024, extracted with large language models and validated. Main text: "94% of abstracts explicitly report a non-null result". Only 2% report only a null result. A calibrated model estimates that significant results are "one to two orders of magnitude" (10–100×) more likely to enter the published record. Pre-registration and randomised experiments are associated with more nulls being accepted. The abstract itself says "over 90%". Preprint on SocArXiv/OSF (v2, 2026-05-08) and I4R Discussion Paper 281.
- **Strongest overlap with Custodian.** Suppressed nulls are a kind of integrity gap the mirror is meant to show: what the published record leaves out.
- **Open questions.** The data will be released "upon article acceptance", so can it feed Custodian's mirror? Is there an equivalent for the fields Alþingi cites?
- **Sources.** https://osf.io/preprints/socarxiv/zr5vf_v2 · https://doi.org/10.31235/osf.io/zr5vf_v2 · https://www.econstor.eu/bitstream/10419/336819/1/I4R-DP281.pdf

## 7. David Shapiro: post-labour economics
**Status:** Partly verified (the framework exists and is his; the link to Custodian is our own notes).

- **What he built or studied.** Self-description: an economic framework for a world where automation makes human labour non-essential. It proposes broad ownership (for example sovereign wealth funds and baby bonds), transparent governance and income that does not depend on jobs. Not verified: the "post-labour vs communism" comparison in research-notes.md. No primary source was found for that framing.
- **Strongest overlap with Custodian.** Incentive structures: who gains when a finding holds. This is conceptual background, not prior art for tooling.
- **Open questions.** Is there a specific Shapiro text that research-notes.md relies on? Is there a link to incentive transparency beyond analogy?
- **Sources.** https://daveshap.substack.com/p/a-post-labor-economics-manifesto · https://medium.com/@dave-shap/what-is-post-labor-economics-a-gentle-introduction-81aa265abbe0

## 8. President Halla Tómasdóttir / Samtalið, 2026-10-10 (seed trigger)
**Status:** Partly verified. **The 80% figure is not verified.**

- **What happened.** Confirmed: on Saturday 2026-10-10, 14:00–17:00, a national dialogue ("Tölum saman") was held at the initiative of President Halla Tómasdóttir, who is its patron. It was run by Samtal, félag til almannaheilla, with young people leading the tables and people of all ages taking part. It took place at 23 sites, according to Vísir. The question was "Hvernig samfélag viljum við skapa saman?" Each table wrote one summary sentence per topic, and the sentence "does not have to mean everyone at the table agreed". Results were presented at Harpa on 2026-10-11, 40 years after the Höfði summit. The most-discussed topics were AI, social media, education and society. Confirmed (Vísir): AI was used to summarise the results across sites, and participants asked for more such dialogues.
- **Not verified:** "80% of participants wanted it again". No primary source found. Vísir reports a stated wish to repeat the event, with no percentage. Also not verified: "thousands of people" (manifesto), the board and data policy, and whether there will be a 2027 edition.
- **Strongest overlap with Custodian.** The appetite for dialogue was there, but the record was a human or AI summary rather than the raw signal. That is the capture gap Custodian names.
- **Open questions.** Source of the 80% figure (an organiser survey?). Samtal's data and recording policy. Is the association open to a pilot?
- **Sources.** https://www.visir.is/g/20262946865d/upp-byggi-legra-sam-tal-en-i-at-huga-semdum · https://www.ruv.is/frettir/innlent/2026-10-11-i-beinni-nidurstodur-samtalsins-kynntar-489529 · https://www.ruv.is/frettir/innlent/2026-09-25-forseti-bydur-framhaldsskolanemum-til-samtals-488101 · https://www.fss.is/is/skolinn-starfid/annad/frettir/samtalid-i-fs-10-oktober · https://www.mk.is/is/frettir/tolum-saman-um-framtidina

---
Not legal advice. Coverage gaps are listed per entry.

# Hallmarks and the scrub: the machine-artifact layer

*Synthesized from the field catalog maintained by Wikipedia's WikiProject AI Cleanup ("Signs of AI writing"), the excess-vocabulary corpus study of Kobak, González-Márquez, Horvát, and Lause (Science Advances, 2025), Liang et al. on detector bias, and the public discourse that made certain tells famous. Links in the Sources section; the distillation, the tier system, the salience-and-precision framing, and the examples are mine.*

*The other files ask whether the prose is good. This one asks whether it carries the residue of machine generation. The two questions converge at depth: the deepest tell is Gardner's frigidity, the reader sensing that nobody cared, and no scrub fixes that. But the residue has a surface catalog of its own, and the surface catalog is what this file holds. Reach for it late, in two modes described below. The numbers live in the register profiles; this file defines what to count.*

*Unlike the craft files, this file is perishable. It describes the habits of specific model generations, and those habits drift.*

**Version: calibrated July 2026.** Describes the 2023 to 2026 model generations (GPT-3.5 through 5.x, Claude 2 through 4.x, Gemini, DeepSeek, and peers). Live for use now, to be questioned at the next revision or by January 2027, whichever comes first.

*The examples below are for calibration, not for lifting.*

---

## How to use this file

Two modes, split by tier. The budgets both modes enforce live in `register-profiles.md`; the string patterns and marked terms the gate scans for live in `machinelexicon.csv`.

**The gate (stage 7).** Tiers 0 and 1 run as a deterministic final pass, after Gardner. Scan, count against the active profile's budgets, report violations with proposed fixes. The gate runs last precisely because it is the only pass dumb enough to be safe there: it counts and matches, it does not interpret, so it cannot undo the judgment work of the stages before it. Anything smarter would need a re-read. Two consequences follow. First, the gate proposes and the writer decides, like every other stage; it never rewrites silently. Second, any accepted fix beyond a trivial substitution gets a quick continuity spot-check, because even a small edit can break a seam Gardner already passed.

**The annotation vocabulary (Tiers 2 and 3).** These artifacts need judgment, so they ride the existing late reads (stages 5 and 6) rather than adding a pass. Mark spans with the hallmark ID and a short note, the way the cut list works; the two vocabularies are now one, and the scaffold holds the mapping. Tier 3 marks carry an extra duty: they route to the pushback discipline, because a Tier 3 deficit is a request for material only the writer has.

Tier 4 is not scrubbed directly. It improves as a side effect of the others, and the entry explains why chasing it directly is a mistake.

---

## Salience and precision

Every artifact below carries two ratings, and the gap between them is the load-bearing idea.

**Salience** is how often the artifact is cited as a tell: its notoriety. **Precision** is how reliably it indicates machine authorship: the false-positive risk when a human wrote the text. The two anti-correlate at the top of the catalog. The em dash is the most litigated tell of the era and one of the least reliable, because skilled human writers have used it heavily forever. "Certainly, here is a possible introduction for your topic" has near-perfect precision, and almost nobody meets it in the wild. The famous tells are famous partly because humans also do them, which is exactly what makes the accusations contentious.

The enforcement consequence: hard bans where precision is absolute, frequency budgets where the artifact is a legitimate device that machines simply overuse. And a diagnostic consequence: no single artifact proves anything. Co-occurrence is the signal. An em dash proves nothing; an em dash inside a negation-antithesis inside a bold-led bullet, closing on a trailing participle, is a signature. Readers who use these models heavily identify machine-generated articles about ninety percent of the time; the catalog below is, roughly, the feature set they have internalized.

---

## Tier 0: leaked interaction artifacts

Fragments of the chat session pasted into the finished text. Rare, instantly conclusive, and budgeted to zero in every profile. The gate treats any hit as a stop-and-report. These are string patterns, not judgments; the lexicon data file carries them.

**H0.1 Preamble and postamble leakage.** The conversational frame survives into the artifact: "Certainly! Here's a revised version...", "I hope this helps!", "Would you like me to expand on any section?" The canonical case is a peer-reviewed paper whose introduction opened "Certainly, here is a possible introduction for your topic", published and later retracted.

**H0.2 First-person machine disclaimers.** "As an AI language model, I cannot..." Documented in published case reports, product listings, and the body text of books.

**H0.3 Knowledge-cutoff hedges.** "As of my last knowledge update...", or a paragraph hedging about available information in exactly the register of a model asked to write about something it could not verify.

**H0.4 Placeholder text.** "[Insert company name]", "[Your Name]". The model delivered a template; nobody filled it in.

**H0.5 Formatting spillover.** Literal `**asterisks**`, stray `#` marks, or interface residue in a context that does not render them. The chat window's markup leaked into a destination with different rules.

---

## Tier 1: the famous tells

The patterns with names. High salience, mixed precision, and every one of them a legitimate device at human base rates. The tell is density, not existence, which is why these take budgets rather than bans, and why the budgets live in the profiles where a register can tune them.

**H1.1 Em dash overuse.** Several times human base rate, placed where a human would choose commas, parentheses, or colons, and usually spaced on both sides, against the closed-up style most habitual human users follow. *Example:* "The launch wasn't flawless — few are — but the team shipped on time — and that's what matters." Owner: none prior; punctuation frequency is new territory for the library. Precision warning: severe. Human writers who love the dash predate the association by decades, and some now self-censor to dodge the accusation. The spacing sub-signal calibrates to the writer's hand like every number in this catalog: a hand that spaces its dashes inverts the prior. And the doubled em dash is a print-era mark, not a documented habit of the cataloged generations; the gate counts dash marks rather than characters and reports run lengths, because a double is one mark and one counter-signal. Drift note: as of late 2025, at least one vendor suppresses the dash on request, so the tell is version-bound in both directions.

**H1.2 The marked lexicon.** A small vocabulary that spiked so hard after 2022 that it functions as a dialect: delve, tapestry, realm, testament, underscore, showcase, intricate, pivotal, seamless, and their cohort. The corpus evidence is unusually strong. Kobak et al. measured excess vocabulary across more than fifteen million biomedical abstracts and estimated that at least 13.5 percent of 2024 abstracts show signs of machine processing; their published example from a real abstract begins "By meticulously delving into the intricate web connecting", which is nearly a bingo card in nine words. Owner: Orwell's rules 1, 2, and 5 hold the mechanism, and the calibration overlay's avoid-list holds the writer's own bans; this file adds the frequency lens and the data. The curated list lives in `machinelexicon.csv`, matched by lemma, all inflections. Precision warning: dialect-shaped. The words are ordinary in Nigerian and other post-colonial Englishes, and real writers have watered down their prose to stop triggering detectors. Budgets should be calibrated to the writer's own English, not to one dialect's base rates. Drift note: the cohort has already shifted between the 2023 and 2025 corpora; honor the version header.

**H1.3 Negation-antithesis.** "It's not just X. It's Y." Also "not only X but also Y", "no X, no Y, just Z", and the two-sentence form where the first sentence asserts a pedigree and the second pivots on "however" into complexity. Machines stack these back to back, which no human editor tolerates. *Example:* "This isn't just a product update. It's a fundamental rethinking of how teams collaborate." Owner: the Forsyth surprise family holds antithesis as a figure, including the false-antithesis test; this file adds the density cap. Practitioner consensus marks this as one of the few patterns worth suppressing directly, because its density in raw output is extreme and its removal costs little.

**H1.4 Rule-of-three saturation.** Triads in every load-bearing slot: "faster, cheaper, and more reliable." *Example, saturated:* "The platform is fast, flexible, and built to scale. Teams can plan, execute, and measure in one place. The result is clarity, alignment, and speed." Owner: the Forsyth repetition family already sets the ceilings ("three is the number and four is a list") and names the fatigue; this file adds the count. Consecutive-sentence triads are an automatic flag.

**H1.5 Bold-led bullet scaffolding.** A list where each item opens with a bolded label and continues with a sentence that restates the label without adding anything. Three artifacts in one package: over-formatting, redundancy, and template rhythm. *Example:*

- **Efficiency:** The workflow is designed to reduce manual effort.
- **Scalability:** The system scales easily across use cases.

Owner: none; the formatting layer is new to the library, which was prose-only before this file. The repair is structural, not lexical: collapse label-restatement pairs into single assertions, and return lists to prose wherever the content is not genuinely enumerable. Note the distinction from the craft files' own labeled-paragraph pattern, where the label opens a paragraph that earns it; the artifact is the restatement, not the bold.

**H1.6 Sycophancy and engagement scaffolding.** "Great question!" at the top, "Let me know if you'd like me to expand!" at the bottom, and the engagement-bait closer in between. In a chat window these are interface conventions; surviving into a document they are Tier 0-adjacent, and the verbatim strings live in the lexicon data. The process cousin, praising a mediocre draft instead of evaluating it, is handled by the scaffold's pushback discipline: the same failure at the collaboration layer instead of the text layer. The row's scope covers the pipeline's own replies as well as the artifacts it gates: a report that ends on "let me know if you'd like me to expand" or "say the word and I'll run the next stage" is the artifact the row bans, produced by the agent enforcing the ban. End on the finding. Offers of further work are a closer, not a service, and the writer knows the pipeline is there.

---

## Tier 2: rhetorical and structural patterns

Individually weak, collectively strong; this is where co-occurrence does the diagnostic work. These form the promoted annotation vocabulary. Some rows are countable and appear in the budget tables; the rest are marked and judged.

**H2.1 Throat-clearing openers.** The zoomed-out scene-setter before any information arrives. *Example:* "In today's rapidly evolving digital landscape, businesses face unprecedented challenges." Fifteen words, zero content, three lexicon hits. Owner: the cut list named this first; Williams's concision pass is the repair.

**H2.2 Summary closers.** "In conclusion," "Overall," "Ultimately," followed by a restatement of what the reader just read, sometimes per section. Owner: Truby's new-equilibrium-as-moral flinch and McDonald's over-explanation test.

**H2.3 The transition metronome.** "Moreover," "Furthermore," "Additionally" at sentence heads with mechanical regularity, standing in for actual logical connection; the paragraph-initial case is the worst of it, not the whole of it. Owner: Williams's cohesion pass, which supplies the real connective tissue these fake.

**H2.4 Significance inflation.** The subject forever elevated into a broader story: "stands as a testament to," "plays a vital role in," "cementing its legacy." The phrasing repertoire is narrow, which makes this one of the higher-precision patterns in the tier. Owner: McDonald, who already orders the stated lesson cut when the piece has earned it and the piece rebuilt when it has not.

**H2.5 Trailing participial analysis.** A sentence states a fact, then appends an -ing clause that narrates the fact's significance: "..., highlighting the region's growing role in renewable energy." The sentence grades its own homework. High precision; humans rarely produce these in volume. Owner: Williams's end-stress pass, plus McDonald's respect for the audience.

**H2.6 False ranges.** "From X to Y" where X and Y sit on no actual scale: "from ancient temples to cutting-edge skyscrapers." Breadth gestured at, nothing specified.

**H2.7 Audience hailing.** "Whether you're a seasoned investor or just starting out..." The reader sorted into a two-bucket taxonomy and promised universal relevance. Inherited from the training corpus's content farms.

**H2.8 Weasel attribution.** Claims assigned to vague authorities: "Experts argue," "Studies show" with no study. The vague authority usually shows up to sponsor an opinion the model inserted. Owner: the library's sourcing guardrail; the repair is verify or cut.

**H2.9 Symmetric hedging.** Every consideration pre-balanced, every verdict dissolved into "it depends on your specific needs." *Example:* "Both approaches have merit, and the right choice ultimately depends on your specific needs and priorities." Owner: the cut list's hedging category and McDonald's demand for an armature with an edge. Precision warning: inverted, and this row is the catalog's one case where the folk belief runs backward. The structural claim, that considerations arrive pre-balanced and the verdict dissolves, is untested; no corpus study the library has found measures it. The lexical claim, that machines hedge more, is contradicted. Herbold et al. compared human-written and ChatGPT-generated argumentative essays at scale and found machine text carries fewer discourse and epistemic markers, with humans using more modals and hedges instead; the result replicates in later corpora, including a 2026 study spanning Gemini, GPT, and Claude that reports substantially fewer hedging markers in machine text. Counting hedge words therefore does not separate machine from human, and the hand that hedges is likelier the human one. This row is a craft rule wherever it is enforced rather than a detection signal, which is why only the job-search register declares it: a hedge in a cover letter is a withdrawal whoever wrote it. Do not cite H2.9 as evidence of machine authorship.

**H2.10 Uniform cadence.** Sentence lengths clustered in a narrow band, paragraphs of three to four sentences forever, no fragments, no long rolling risks. This is the visible face of what detectors measure statistically (see Tier 4), and it is why light lexical scrubbing fails: swap the words and the rhythm still testifies. It is budgeted as a uniformity ceiling, a cap on consecutive same-shaped sentences, which keeps the fix inside the budget schema. The repair direction matters and is easy to get backwards; see the over-scrubbing section.

---

## Tier 3: content-level tells

The tier that cannot be scrubbed, only authored. No lexical filter fixes an absence; only knowledge does. Marks from this tier route to the pushback discipline, because each one is a request for something the pipeline cannot supply: material, verification, or a verdict.

**H3.1 Fluent vagueness.** High polish, low information density: a statistical regression to the genre mean, specific facts smoothed into statements that could apply to many topics. Owner: Gardner's vividness (a vague dream does not hold) and the storytelling file's transportation diagnostic.

**H3.2 Missing lived specificity.** No prices, no dates, no proper nouns, no named failure, no incident that could only have happened to one person. A floor on specificity markers (proper nouns, numerals, dates per thousand words) gives this partial mechanical teeth, and the profiles carry that floor, but the floor is a proxy. The real repair is material only the writer has, which is pushback trigger one. Owner: Goldberg, whose whole file is the discipline of getting that material onto the page.

**H3.3 Fabricated or ornamental citations.** Invalid identifiers, real authors on nonexistent papers, citations that exist but do not support the claim. Near-perfect precision when checked; checking is the cost. The rule is verify or cut, and it admits no register exceptions.

**H3.4 Semantic redundancy.** The same assertion re-clothed across consecutive sentences, each restatement syntactically fresh and informationally identical. Owner: Williams's concision pass; H1.5 is its structural twin.

**H3.5 Register-mismatched puffery.** Travel-brochure adjectives in contexts that did not order them: "breathtaking," "must-visit," "nestled in the heart of." Models drift toward promotional tone even when prompted for neutrality. Owner: the calibration overlay's reserved vocabulary and Orwell's rule 5.

**H3.6 Non-committal conclusions.** The close lands on balance, careful consideration, and collaboration among stakeholders: structurally present, rhetorically absent. Nothing was risked, so nothing concludes. The pipeline cannot commit on the writer's behalf, so this mark asks for a ruling rather than proposing prose; that is pushback trigger four. Owner: McDonald's armature and Truby's new equilibrium.

---

## Tier 4: the statistical substrate

What automated detectors measure. Included so the pipeline understands the machinery and, more importantly, its limits. Nothing in this tier is targeted directly.

**H4.1 Low perplexity.** Machine text is systematically more probable, token by token, than human text: fewer surprising choices. **H4.2 Low burstiness.** The variance of that predictability, and of sentence structure, across a document; humans oscillate, machines regress to a mean. Both improve as side effects of the real work: the H2.10 ceiling caps uniformity from below, and the generation stage supplies variance from above. Chasing the metrics directly produces the counter-tell described in the next section.

**H4.3 Typographic fingerprints.** Model-family specific and fragile: some families emit curly quotation marks and apostrophes, sometimes inconsistently mixed with straight ones; others emit straight quotes; machine em dashes tend to arrive spaced. All of it collides with legitimate sources of the same characters, from word-processor smart quotes to professional typesetting, so precision alone is low. The gate simply normalizes typography to the register's convention and moves on. One boundary: normalization is silent when the gate serves the writer's own draft, and disclosed when it measures someone else's text, because a measurement must record its transcription.

**H4.4 Watermarks.** Statistical signals embedded at generation time. High precision where deployed, rarely deployed, vendor-specific, and removable by paraphrase. Not a factor in this pipeline in either direction.

**The reliability caveat, which is load-bearing.** Detectors built on these signals fail in both directions, and the failures have victims: one study found seven popular detectors flagged sixty-one percent of genuinely human TOEFL essays on average, ninety-seven percent were flagged by at least one, while the same detectors were near-perfect on essays by native-speaking eighth graders. The mechanism is that limited lexical and syntactic range mimics low perplexity. Two consequences for this library. "Passes a detector" is the wrong objective, technically and ethically; the target is the primed human reader, and beneath that, good writing. And the dialect lesson transfers: budgets and floors are calibrated to the writer's own English, never to the assumption that one dialect's base rates are universal.

---

## Over-scrubbing: the counter-tell

A document with zero dashes, zero triads, zero transitions, and uniformly flat affect reads as defensive, and defensiveness is legible. Practitioner advice converges here: suppress the few highest-value patterns and edit the rest by judgment, because stacking restrictions produces prose that is stiff and generic, which is its own artifact.

The uniformity problem (H2.10, H4.2) is where over-correction is most tempting and most damaging. Injected chaos does not read as human; it reads as the next tell. The performative fragment and the manufactured staccato are already auditioning for the role the em dash vacated. The organic fix has two halves, both already in the library. From above: the generation stage produces natural variance, and the cut stages are forbidden to sand it off, which is what the interesting-but-failed principle defends. From below: the uniformity ceiling flags sameness without prescribing its replacement. Preserve variance; cap uniformity; never spray chaos on afterward.

---

## Things to flinch at

- **This file scrubs; it does not accuse.** Its precision ratings are miserable for detection, by design of the world: humans dash, dialects delve. Using the catalog to accuse a writer imports every false-positive documented above.

- **The moving target.** Every entry describes model generations, not laws of nature. A budget calibrated against 2024 output misfires against 2026 output in both directions. Honor the version header; re-run the calibration protocol when it expires.

- **Zeroing everything.** A profile of all-zeros fails the objective it serves. The goal is human base rates, not absence.

- **The lexicon as a blacklist of thought.** When "pivotal" is the precise word, the meta-rule applies: budgets break deliberately and for cause, stated rather than silent. A word ban that forces a worse word has failed twice.

- **Satire is a register, not a loophole.** The satirical profile inverts budgets to produce period-accurate slop on purpose. That register weaponizes the catalog inside a frame labeled as satire; it never launders machine text as human elsewhere.

---

## How this fits with the other files

This file and Goldberg form a pincer. The generation file fights the machine's defaults from the front, with positive instruction toward the raw and the specific; this file sweeps the residue at the back. Neither contaminates the other, and the cardinal rule holds: nothing from this file runs during generation, ever. Rules-during-generation produce dead prose, and dead prose is the disease this file exists to treat.

In the late window it is the third lens beside two others. Orwell asks whether each word is right. Gardner asks whether anything wakes the reader. This file asks whether anything smells of the machine. The three overlap, and a sentence can fail all three, but the questions are different and reading once for each catches more than reading once for all.

The scaffold owns the process: the stage sequence, the unified annotation vocabulary, the pushback discipline, the calibration protocol. The register profiles own the numbers. This file owns the artifacts and their names.

---

## What this file does not cover

Detection for accusation, which the catalog is unfit for and the flinch list forbids. Detector-evasion tricks, which target the wrong objective. The budget numbers, which are register decisions and live in the profiles. The craft repairs, which belong to the owner files named in each entry. And the research trail in full: the entries compress a longer evidence base, and the sources below are the canonical treatments.

---

## Sources

- Wikipedia: Signs of AI writing (WikiProject AI Cleanup): https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Kobak, González-Márquez, Horvát, and Lause, "Delving into LLM-assisted writing in biomedical publications through excess vocabulary," Science Advances 11(27), 2025: https://www.science.org/doi/10.1126/sciadv.adt3813 (data, including ~900 annotated excess words: https://github.com/berenslab/llm-excess-vocab)
- Liang, Yuksekgonul, Mao, Wu, and Zou, "GPT detectors are biased against non-native English writers," Patterns, 2023: https://arxiv.org/pdf/2304.02819
- Herbold, Hautli-Janisz, Heuer, Kikteva, and Trautsch, "A large-scale comparison of human-written versus ChatGPT-generated essays," Scientific Reports 13, 2023: https://doi.org/10.1038/s41598-023-45644-9 (the finding H2.9 rests on: machine text carries fewer discourse and epistemic markers than human text, not more)
- "Does the Thesis Still Make Sense? A Comparative Analysis of Scientific Essays Generated by Humans and Generative Artificial Intelligence," 2026: https://doi.org/10.3390/educsci16060920 (replication across Gemini, GPT, and Claude: substantially fewer hedging markers in machine text)
- TechCrunch, "OpenAI says it's fixed ChatGPT's em dash problem," November 2025: https://techcrunch.com/2025/11/14/openai-says-its-fixed-chatgpts-em-dash-problem/
- The Scholarly Kitchen on chatbot phrases in the published literature, March 2024: https://scholarlykitchen.sspnet.org/2024/03/20/the-latest-crisis-is-the-research-literature-overrun-with-chatgpt-and-llm-generated-articles/
- GPTZero, "What is perplexity & burstiness for AI detection?": https://gptzero.me/news/perplexity-and-burstiness-what-is-it/
- Vanguard (Nigeria) on the "delve" episode, April 2024: https://www.vanguardngr.com/2024/04/nigerians-tackle-american-author-for-claiming-delve-is-only-used-by-chatgpt/

---

## A note to the AI assistant using this file

When you run the gate, return the report, not a silently cleaned draft: each finding as hallmark ID, location, count against the active profile's budget, and a proposed fix offered as a candidate. Name the profile you enforced. And scale the report to its findings: a clean sheet earns a short report, because commentary is spent where flags are. When you annotate in the late reads, mark spans with the ID and a short note and leave the prose alone.

If you also edited, end with the library's standard note: the two or three moves that did the most work, plainly, in a sentence or two. One combined note per edit, never one per file. And never present a scrubbed draft as finished; the writer decides, here more than anywhere, because this file's whole authority is borrowed from theirs.

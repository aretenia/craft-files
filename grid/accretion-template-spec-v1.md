# The accretion template: specification v1.0

*Working document for the implementation agents, not repo canon. Provenance: drafted by the craft-files library orchestrator, July 23, 2026, at the Proprietor's direction, following the ruling that replaced `--trackchanges` with an accretion conversation. No human pass. Canon touchpoints: `scaffold-and-calibration.md` defines the sensor, `pipeline-flags.md` holds the flag semantics, `grid-spec-v1.md` section 4 consumes this file's output.*

---

## 1. What this is, and why it exists

The template is the ratified record of one human pass: what the machine did, what the writer did in response, and what the writer says each of those responses meant. It is the only thing the generator reads.

It exists because direction is a claim about intent and a diff cannot carry one. A struck em dash might be refusing the machine's habit, restoring a quotation, or fixing a typo, and those are three different signals pointing three different ways. A generator that decides between them is deciding. The one rule says it proposes.

So the judgment happens in conversation, where the writer is, and the template records the result. Downstream of this file everything is mechanical.

## 2. The seam requirement, which is the whole point

A template built from the finished prose has rebuilt bare occurrence with extra steps.

The conversation must know what the machine did, not only what the document now says. The canonical example, from `grid-spec-v1.md` section 4: the machine closing a spaced em dash and the writer re-spacing it is one `human_strike` against the machine's habit, not two occurrences of a dash. Reading that correctly needs both sides of the seam.

Concretely, the agent conducting the conversation needs the machine pass output and the writer's marked-up version, and it asks in seam terms. "You re-spaced the dash I closed in paragraph four; was that refusing the close, or restoring a quotation?" Not "you have a spaced dash here."

How the writer marks the pass up is their business: tracked changes, comments, a rewritten file, or spoken corrections. The conversation reads whatever is there.

## 3. Schema

```json
{
  "template_version": "1.0",
  "desk_id": "craft-files",
  "ratified_on": "2026-07-23",
  "author": "Proprietor",
  "artifact": "Rupture_V4.md",
  "artifact_label": "machine pass output",
  "model": "the generation-side model and version for the pass being reviewed",
  "changes": [
    {
      "seq": 1,
      "machine_move": "closed the spaced em dash, paragraph 4",
      "human_move": "restored the spacing",
      "rule_id": "H1.1",
      "direction": "human_strike",
      "evidence": "rupture-v4.evidence.md#h11-2",
      "note": ""
    },
    {
      "seq": 2,
      "machine_move": null,
      "human_move": "cut a sincerity preamble of their own from the opening",
      "rule_id": null,
      "cluster_key": "first-person-softening",
      "direction": "human_add",
      "evidence": null,
      "note": "no named rule; third pass running"
    }
  ]
}
```

## 4. Field rules

**There is no `run` field, deliberately.** The generator owns `run_counter`, assigns the run on consumption, and records it in its own consumption ledger; the ratified template is never mutated afterward. A template should not carry a number it cannot know, and an advisory field that can disagree with reality is worse in a provenance record than an absent one. A template carrying `run` anyway was written against an earlier draft of this file, and a generator may ignore it with a warning rather than refusing.

`ratified_on` is provenance for the reader, never an input to anything computed. The desk's time model is work done, not time elapsed.

`author` is a configured desk value. It is never read from document metadata, because metadata records the machine a file was opened on rather than the hand that did the writing, and this library has one document whose tracked changes name a person who made none of them. It is held to a publication standard, since every grid export embeds its source verbatim.

`rule_id` is null when the change matches nothing the library has named. That is not a failure; it is how the undefined region fills, and a cluster that recurs there is how a rule gets discovered.

`direction` is one of `human_add`, `human_strike`, `stand`, and it is always the writer's ruling rather than the agent's reading. The agent proposes; the template records what was ratified.

`machine_move` is null when the writer acted on their own prose rather than against something the machine did. A `human_strike` therefore requires a non-null one, since a strike is a response to a move; residue may carry either, and which it carries is the difference between a habit the writer refuses and a habit the writer has.

`model` names the generation-side model and version for the pass under review. It may be null, and null is the honest value when the pass was not recorded and nobody remembers, since inventing it would put a fact in a provenance record that nobody established. But null is not free. `grid-spec-v1.md` section 7 makes survival across a model-version change the classifier that sorts a recurring pattern into craft canon or into the hallmarks catalog with a version block, and it answers that question from this field as it rides the reel. A tuple with a null model cannot answer it, so a cluster built entirely from null-model passes can accumulate evidence and still never promote. Record it where you can.

`cluster_key` groups entries that carry a null `rule_id`. It is a label local to this template, ratified in the conversation like everything else, and it exists because deciding that five scattered edits are instances of one unnamed pattern is judgment, and the generator does not do judgment. Entries sharing a key are one cluster. An entry with a null `rule_id` and no key is a cluster of one. The key is never a `U-` serial: the generator mints those, and merging a new cluster with one from an earlier pass is a separate ratified step rather than something the conversation reaches back to do. The field is absent or null wherever `rule_id` is set.

## 5. Invariants

**A `human_strike` requires a non-null `machine_move`.** You cannot strike a move nobody made. A template violating this was built from the prose rather than from the seam, which is the failure section 2 exists to prevent, and the generator should refuse it rather than repair it.

**Every entry is ratified.** A change the writer did not rule on does not appear. There is no pending state; unratified material stays in the conversation.

**One entry per change, and `seq` is stable within a template.**

**A `cluster_key` appears only on entries with a null `rule_id`.** A key beside a named rule means the conversation could not decide which of the two it was, and an entry the conversation could not classify is not ratified.

**`stand` is logged at low weight**, per `grid-spec-v1.md` section 4. It is weak confirmation, not agreement.

## 6. What the generator does with it

Nothing requiring judgment. The three-way sort in `grid-spec-v1.md` section 4 resolves off `rule_id` alone: a countable row updates mechanically, an annotation-category row updates with the conversation's note carried through, and a null lands in the undefined region as a cluster member. One provenance tuple per entry, no exceptions.

## 7. Open, and not blocking

Settled, and recorded here so nobody reopens it: the template is JSON, schema-validated, with a deterministic read-only render for the ratification step, and corrections route back through the accretion conversation rather than by hand-editing either artifact. The file is the format and the human view is a derived projection, which is the pattern `grid-spec-v1.md` section 2 already sets for the grid. The deciding fact was that the template is agent-authored rather than writer-authored, so machine-parsing its prose would invite a silent mis-parse, which is the worst failure available in a provenance record.

Whether `note` should be structured for the annotation-category case, since "the judgment noted" is doing real work there and free prose may not survive aggregation into the population layer.

Whether a template can span more than one artifact. One pass over one document is the simple case and the samples all assume it.

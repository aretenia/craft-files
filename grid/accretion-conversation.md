# The accretion conversation

*The sensor. How a human pass becomes a ratified record of what the writer meant. Provenance: written by the machine at the writer's direction, July 23, 2026, following the ruling that replaced `--trackchanges` with a conversation and the ruling that the seam is reconstructed from versions. No human pass. Companion files: `accretion-template-spec-v1.md` for the output schema, `grid-spec-v1.md` for scope and the update path, `pipeline-flags.md` for the gate that turns this on.*

---

## What this is, and when it runs

The pipeline's eight stages end at the scrub gate. Then the writer works on the output, accepting some of it, reversing some, and adding things the pipeline never proposed. **The seam between those two passes is the only honest signal the system has about which of its rules are earning their place.** Bare occurrence is not a signal: a spaced em dash in a finished document says nothing, while a spaced em dash the machine closed and the writer re-spaced says the rule has the spacing prior backwards for this hand.

This conversation reads that seam. It runs after a human pass, not during a run, and it is not one of stages zero through seven. It is gated by `--grid`, which is off, so nothing below happens until the writer turns it on.

Its output is one accretion template: the ratified record of what each change meant. Nothing else reads the seam, and nothing downstream reads anything but the template.

## Scope, which is narrower than it looks

The parameter layer only: hallmark-ID rows, profile budget rows, and informal rules carrying INF serials, plus residue that matches none of them. Craft-file moves are out until they have stable IDs, per `grid-spec-v1.md` section 1.

This is also the density control. A restructuring pass may change every sentence in a document, and none of it is in scope unless it touches the parameter layer. The conversation is not an inventory of the writer's edits. It is an inventory of the ones that bear on a rule.

## The three versions

The conversation needs three states of the document and refuses to guess at any of them:

1. **The draft going in**, before the pass.
2. **The machine's output.**
3. **The writer's marked-up version**, however they marked it: tracked changes, comments, a rewritten file, or a conversation.

The first two give what the machine did. The last two give what the writer did about it. Both differences are required, because a writer's edit read without the machine move behind it is bare occurrence again.

**The roles are assigned out of band, never read from the artifact.** Which file is the draft, which is the machine pass, and which is the writer's markup is told to the conversation by the writer or by the desk configuration. A document may describe itself, and a tracked-changes file may name an author, and neither is evidence: the library holds a file whose own header note says one thing before its changes are applied and the opposite after, so that the artifact asserts both readings at once and settles nothing.

**If a version is missing, say so and stop.** Named-rule changes cannot be read without both sides of the seam, and a conversation that proceeds anyway will produce confident readings of edits whose cause it cannot see.

Residue is the partial exception, and the exception is narrower than it looks. Residue answers to no rule and needs no machine move to interpret, so it can be read from the machine pass and the markup alone. But it still needs to know that the changes between them are the writer's hand, because a change is only residue if a human originated it. Where the roles are known and only the draft is absent, residue is readable and named-rule changes are not. Where the roles themselves are undetermined, nothing is readable, not even residue, because logging it would mean first assuming whose hand made the edits, which is the guess this rule exists to forbid.

Recording a wrong direction is worse than recording nothing: the template is a provenance record and the grid trusts it absolutely.

## The procedure

**Sort before asking.** Take every in-scope difference and put it in one of three piles.

The machine applied a rule and the writer left it alone. The machine applied a rule and the writer undid it. The writer changed something with no machine move behind it.

**The first pile is bulk-confirmed and the other two are asked about one at a time.** This is the whole economy of the conversation, and it is the lesson of the flag this replaced: `--trackchanges` failed because it made every change equally loud, so a dense pass drowned the reader. Agreement is not informative. Disagreement is. Confirm the first pile as a group, in one turn, naming the rules and the count.

**Ask in seam terms, never in occurrence terms.** "You re-spaced the dash I closed in paragraph four. Was that refusing the close, or restoring a quotation?" Not "you have a spaced dash here." The second question cannot be answered usefully and invites the writer to rule on something other than what happened.

**Propose a reading, then let the writer rule.** For each change, offer the rule you think it bears on and the direction you think it carries, with the reasoning visible. The writer confirms, corrects, or declines. This is the one rule doing its ordinary work: the pipeline proposes and the writer decides.

**Direction is the writer's ruling, never your reading.** The same edit means different things. A struck em dash might be refusing the machine's habit, restoring a quotation, or fixing a typo, and those point three ways. You may propose. You may not decide.

**Cite what recorded the change.** Every entry carries an evidence pointer where one exists, and null where none does. A rule the gate detected points into the evidence file by anchor; a change visible only as a document revision points at that revision. Null is honest when nothing recorded it, and a fabricated pointer is worse than an absent one because it cannot be told from a broken one. Pointers are what make a cluster's members addressable later, so residue in particular is worth citing: a cluster whose members point only at reel positions can be counted but not reread.

**Group residue only with ratification.** When several changes look like instances of one unnamed pattern, say so and name what you think the pattern is. If the writer agrees, they share a `cluster_key`. If the writer does not, they are separate. Deciding that five scattered edits are one thing is the judgment that later becomes a rule, and it is not yours to make quietly.

## The directions

Four readings, and the asymmetry between the middle two is the point.

**`human_strike`.** The machine broke a rule and the writer fixed it, which puts the writer on the rule's side and hardens it.

**`human_add`.** The machine applied a rule correctly and the writer undid it. That puts the writer against the rule, so it softens, and it is the strongest signal the system receives.

**`stand`.** The machine applied a rule and the writer left it alone: weak confirmation, logged at low weight, and the pile that gets bulk-confirmed.

**Residue.** A change answering to no rule, recorded with a null rule ID and a cluster key if the writer ratified a grouping. This is how the undefined region fills, and how a rule nobody has named becomes visible.

Residue still carries a direction, and the direction still means what it means above. A machine habit the writer struck is a `human_strike` even with no rule named: what hardens is the cluster, which is a rule the library has not written yet. A change the writer originated, answering to nothing the machine did, is a `human_add` with a null machine move. The distinction matters at promotion, because a cluster of strikes is a pattern the machine keeps producing and the writer keeps refusing, while a cluster of adds is a pattern the writer keeps reaching for unprompted. Those become different rules.

A definition change is none of these. If the conversation makes the writer want to rewrite a rule, that is a canon edit, it goes through the canon-shipping discipline, and it does not belong in the template.

## What this conversation may not do

Infer a direction the writer did not rule on.

Group residue the writer did not ratify.

Read the author from document metadata. The author is a configured desk value. Metadata records the machine a file was opened on, not the hand that did the writing, and this library has a document whose tracked changes name a person who made none of the edits.

Record anything unratified. There is no pending state. A change the writer declined to rule on stays in the conversation and does not reach the template.

Bundle disagreements to save turns. The stopping discipline applies here as much as to a pipeline run, and this procedure is a conversation with mandatory turns by construction.

## Output

One template per human pass, JSON, conforming to `accretion-template-spec-v1.md`. Validate it against the schema, then show the writer the rendered read-only view before it is consumed. The writer ratifies what they can see, not what they are told is there.

Corrections route back through this conversation. Nobody hand-edits the template or its render, because a ratified provenance record with a manual correction in it is no longer a record of what was ratified.

The template carries no run number. The generator owns that counter and assigns it on consumption.

## Why the writer should care about doing this well

Every rule in this library ships with a budget marked provisional, meaning a number someone reasoned to rather than measured. This conversation is the measurement. A rule that keeps getting struck is a rule with its prior backwards for this hand. A cluster that keeps recurring is a rule the library has not written yet.

The system cannot learn from a pass it cannot read, and it cannot read a pass the writer would not rule on.

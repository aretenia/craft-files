# Decisions log

- 2026-09-07 · Pairing 5, Crimson Pro + Public Sans, chosen provisionally
  from six; the others lost on discretionary ligatures. Final call waits
  on colour and weight experiments.
- 2026-09-07 · x-height matching adopted (0.81× for this pair); liga on,
  dlig off; unattributed words set in the human face, uncoloured.
- 2026-09-07 · Palette: human 250°, machine 40°, green at the midpoint;
  three colour modes built; runs merged; verdict pending.
- Open · the ten drafts have not all arrived; attribution is V1 vs V10
  only, 71 percent unattributed. Lines layer untested on a real move.
- 2026-09-07 · Colour mode: glyph. Colour only where there was back and
  forth; pure human and pure machine words stay ink. Leaning encoded in
  hue (toward 250° human, 40° machine, green when balanced), intensity
  in saturation. Weights for the tinted state: sans 470, serif 420.
- 2026-09-07 · First real chain (V1 human, V2 machine, V3 human, V10
  mixed): 30% human, 50% machine (all approved in V3), 21% unattributed.
  Back and forth defined at the sentence level; threshold 12% vs 25%
  compared on the opening, verdict pending. Machine-leaning mixed
  sentences land in olive (hue 60° to 100°); consider bending the hue
  path toward orange. No moves detected: reworded moves are invisible to
  exact-run detection.
- 2026-09-07 · Threshold for a mixed sentence: 12% (the Proprietor's call).
  First full ten-draft run: 70% machine, 30% human, 99 of 175 sentences
  mixed; V8's human edits invisible in the flattened copy (real docx
  requested).
- 2026-09-07 · Under colour the serif/sans difference softens. Eight
  pairings rendered on the real provenance with colour on: the lever is
  the sans. Recursive with its Monospace axis at 0.6 (a proportional
  semi-typewriter) and Space Grotesk both make the machine unmistakable;
  Alegreya offers a modern Th ligature on the serif side. Candidates 3
  (Crimson Pro + Recursive 0.6) and 7 (Alegreya + Recursive 0.6) put
  forward. Renderer now takes per-face axis overrides (--axes-sans).
- 2026-09-07 · Pair 7 chosen: Alegreya (human, 400) with Recursive
  (machine). Tuned on the full run: Monospace 0.5, weight 370, sans at
  0.95 of the x-height match (0.907x overall), because at 0.6 and 420 the
  wide semi-mono letters outweighed the serif and the machine words read
  as larger. In CSS: the sans span at 0.907em with
  font-variation-settings "MONO" 0.5, "CASL" 0, "wght" 370.
- 2026-09-07 · "That is my grievance." showed as machine: the sentence
  was reworded in V7, a pipeline pass labelled machine in which the
  writer ruled the edits. Attestations added to the manifest so the
  writer's memory can override the pass label; the 70/30 split is an
  upper bound on machine authorship for the same reason.
- 2026-09-07 · Attestations set aside (the writer does not want to keep
  a list). Generalised instead: ruled machine passes (V4, V5, V7, V9 by
  their headers) and rewrites across passes count as back and forth.
  110 of 175 sentences now mixed; the page shows more colour because ten
  alternating passes touched most sentences. Threshold remains 12%.
- 2026-09-07 · Fonts and colour locked as V1. Red explored on the ten
  drafts: no sentence-level moves exist in the final (the rewrite
  restructured by rewording; the one block move, the writer's V1 feature
  notes parked at the end by V2, was later cut), so comets have nothing
  to draw here. Meaningful red events found: restorations (V3 bringing
  back "mediocre, but human, author" with its em dashes over the
  machine), cuts by the other hand (V6's 112-word cut of the reminders
  block), heat (the grid sentence rewritten in nine passes), loss (V2
  discarding 1,717 of V1's 3,405 words, heaviest in the axiom
  paragraph). Five red layers built; verdict pending.
- 2026-09-07 · Red, first full run: restored (D) with heat in the gutter
  (A) on the whole essay. Heat floor is a knob (--heat-floor); at the
  default the grievance region reads as a continuous pale rule because
  most of its sentences were rewritten two or three times, with the
  library section darkest. Verdict pending.
- 2026-09-07 · HTML render built (render_html.py, make_webfonts.py):
  self-contained, fonts instanced and subset to ~60 KB, four layers with
  checkboxes, gutter by inline script. Spec for the craft library V3.4
  written; Rupture provenance package assembled; brief to Postmaster.
- 2026-09-07 · Correction: the red thread did ship. The live end plate
  (rupture-03-rupture-thread-red) carries it; the earlier line saying R6
  was not built describes the state before the Proprietor's late call.
  The inheritance design (the red carried from essays 02 and 03 as one
  thread) shipped as made.
- 2026-09-07 · Deployment 2 live at slopshops.ai/essay-04-rupture/layers/,
  linked beneath the closing plate's caption. Spec revision 2: ruled
  carries its evidence class (Slopsmith's finding); header-sourced
  rulings in the Rupture record marked as such; picture and ledger
  unchanged; acceptance halts fixed.
- 2026-09-07 · Spec revision 3 after Slopsmith's full return. Rulings
  made by Artlord: keep the measured alt sentence on the threaded plate;
  plates stay lossless WebP. Slopsmith's fixture finding exposed a real
  bug in the tracked-changes reader (double parse); fixed and proven.

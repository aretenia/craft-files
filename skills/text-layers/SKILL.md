---
name: text-layers
description: Render a draft-provenance map as visual layers over the text itself, with a serif face for words a human wrote, a sans for words a machine wrote (x-height matched so they share a line), colour by authorship that turns green where the two hands mixed, and faint trails where runs of text were moved. Use this whenever the user wants to see human versus machine authorship on the page, try font pairings for that purpose, run colour or weight experiments on mixed-authorship text, visualise collaboration across drafts, or mock up how an essay would look with authorship made visible. Use it for any request that mentions the triad (fonts, colours, lines), the human font or the machine font, or version-theory visuals, even if the user does not say "render". Requires a provenance.json from the draft-provenance skill.
---

# Text layers

The essay is the picture. Three layers sit on the words, one at a time,
each cheap to remove: **fonts**, then **colours**, then **lines**. Every
render is a PNG sheet for judging at the site's column width (672 px).
Nothing here ships as runtime code; the shipping form is a later step.

## Decisions so far (Essay Art, September 2026)

- **Human face: Alegreya. Machine face: Recursive at Monospace 0.5.**
  Chosen 2026-09-07 under colour, after Crimson Pro + Public Sans (the
  first pick) proved too close once tinted. The sans is a proportional
  face pushed halfway to a typewriter grid, weight 370, and it is the
  lever: a machine sans stays a machine at any colour. Alegreya brings a
  modern Th ligature and a quiet st.
- **X-height match is not optional, and sometimes not enough.** The sans
  is sized so its x-height equals the serif's, then trimmed by a factor
  when its mass (width, stroke) still outweighs the serif; for this pair
  that is 0.95 on top of the match, **0.907× overall**. In CSS: the sans
  span at `font-size: 0.907em` with `font-variation-settings: "MONO" 0.5,
  "CASL" 0, "wght" 370`. Without it the machine words shout.
- **Ligatures: `liga` on, `dlig` off.** Discretionary ligatures turn
  "system" into "syſtem" and read as a tell of their own.
- **When in doubt, human.** Unattributed words are set in the serif and
  left uncoloured; the colour layer only speaks where provenance knows.
- **Colour speaks only where there was back and forth.** Words purely
  authored by either hand stay ink; the fonts already say who wrote
  them. A word both hands were in (`mix` above 0.15) takes a colour that
  leans toward whichever hand did more: human hue **250°** (blue pulled
  toward purple), machine hue **40°** (yellow pulled toward orange),
  interpolated linearly so a balanced exchange lands on **green (145°)**;
  faint interaction is faint colour. Mode `glyph` (coloured letters at
  readable darkness) is the chosen mode; `highlight` and `underline`
  remain available. Adjacent words of the same colour on a line share
  one run. `--color-all` restores colour on pure authorship for
  comparison only. See `references/palette.md`.
- **Red is for what the fonts and colours cannot say: history that left
  no words behind.** Five red layers exist, each drawn from the
  provenance file, each rare by construction: `restored` (a red rule
  under words a later pass brought back from an earlier draft; the
  human taking back their own wording), `heat` (a red rule in the gutter
  beside lines whose sentence was rewritten in many passes), `loss` (a
  gutter rule scaled by how many of the other hand's words were cut
  from the paragraph), `scars` (a red hairline where one hand cut at
  least `--min-scar` of the other's words, after the last word when the
  cut was at the end), `heatwash` (heat as a wash behind the lines; the
  loud one). `lines` (trails for moved runs) stays experimental and has
  nothing to draw until a chain reorders sentences. Use one red layer at
  a time, two at most; red loses its meaning when it is everywhere.

## Commands

```bash
# fonts only, the real attribution, the essay's opening
python3 scripts/render_layers.py provenance.json -o fonts.png --layers fonts --find "Tàpies was a giant" --window 110

# colour experiments (three modes) and a weight variant
python3 scripts/render_layers.py provenance.json -o glyph.png     --layers fonts,colors --color-mode glyph
python3 scripts/render_layers.py provenance.json -o highlight.png --layers fonts,colors --color-mode highlight
python3 scripts/render_layers.py provenance.json -o underline.png --layers fonts,colors --color-mode underline
python3 scripts/render_layers.py provenance.json -o heavy.png     --layers fonts,colors --weight-sans 470 --weight-serif 420

# red layers, one at a time
python3 scripts/render_layers.py provenance.json -o restored.png --layers fonts,colors,restored
python3 scripts/render_layers.py provenance.json -o heat.png     --layers fonts,colors,heat
python3 scripts/render_layers.py provenance.json -o loss.png     --layers fonts,colors,loss --paras 0:3
python3 scripts/render_layers.py provenance.json -o scars.png    --layers fonts,colors,scars --min-scar 8

# try other pairings against the same passage, with any layers on
python3 scripts/font_pairings.py provenance.json pairs.json -o pairings.png --layers fonts,colors --find "Every logical system"

# variable-axis knobs per face (Recursive's Monospace axis makes a semi-typewriter sans)
python3 scripts/render_layers.py provenance.json -o mono.png --sans Recursive-Variable.ttf --axes-sans '{"Monospace": 0.6, "Casual": 0}'
```

`--demo` treats unattributed words as machine and synthesises some
mixing so a palette can be judged before the intermediate drafts exist;
the legend says DEMO whenever it is on. Never present a demo render as
attribution.

Selection: `--find "phrase" --window N`, `--range a:b` (tokens), or
`--paras a:b`. Size and measure: `--size 20 --width 672 --scale 2`.

## The HTML render (the shipping form)

```bash
# static, subset web fonts for the piece (once per piece; ~60 KB for the pair)
python3 scripts/make_webfonts.py provenance.json webfonts \
    --human assets/fonts/Alegreya-Variable.ttf --machine assets/fonts/Recursive-Variable.ttf

# one self-contained page: fonts embedded, four layers with checkboxes, gutter drawn after layout
python3 scripts/render_html.py provenance.json -o layers.html \
    --human-font webfonts/human.woff2 --machine-font webfonts/machine.woff2 \
    --title "Rupture" --subtitle "Essay 04, with its ten drafts showing through" \
    --essay-url https://slopshops.ai/essay-04-rupture/ --credit "D. Brinkman, with Claude (Anthropic), 2026"
```

The page has no external references beyond the link back to the piece,
reads offline on a phone, and turns into the plain essay when all four
boxes are unchecked. `assets/webfonts/` holds the Rupture instances
(Alegreya 400; Recursive Monospace 0.5, weight 370) if the piece's
characters are covered; regenerate for a piece that uses others.

## How to use it in a session

1. Get `provenance.json` from `draft-provenance`. Read its summary
   first; if most words are unattributed, say so before rendering.
2. Render one layer at a time. Show the user one sheet per question
   (which pairing, which colour mode, which weight), not everything.
3. Judge at 1× as well as 2×: the site's readers see 672 px.
4. Record decisions in `references/decisions.md` in this skill so the
   next session starts where this one ended.
5. When a render is going to be read rather than judged, build the HTML;
   the PNG sheets are for decisions, the HTML is for readers.

## Assets

`assets/fonts/`: Crimson Pro and Public Sans, variable, OFL (licences
alongside), saved as `CrimsonPro-Variable.ttf` and
`PublicSans-Variable.ttf`. Other candidates come from the google/fonts
repository on GitHub; fetch with `curl -g` (the repository's filenames
carry brackets) and rename them to plain names before bundling: the
skill importer rejects paths with brackets or commas.

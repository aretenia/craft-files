# Palette

Two poles and a path between them, and a rule above both: colour only
where both hands were in a word. Pure authorship stays ink; the fonts
carry it. Below `mix` 0.15 a word is ink; from there the saturation
rises with `mix`, so light back-and-forth is a tint and heavy
back-and-forth is a colour.

| role | hue | why |
|---|---|---|
| human | 250° | blue, pulled toward purple so it is not "link blue" |
| machine | 40° | yellow, pulled toward orange so it survives on a light page |
| mixed | 145° | the midpoint of a linear hue interpolation: green, which is what blue and yellow make |

The interpolation runs the short way round the hue circle (250 → 145 →
40), so any word's colour is `hue = 40 + 210 * t` where `t = 1` is pure
human, `t = 0` pure machine, and a word's `mix` score pulls `t` toward
0.5. Red (0°) is never on the path, which keeps it free for the lines
layer.

Lightness and saturation by mode (HSL):

| mode | letters | band or rule |
|---|---|---|
| glyph | s 0.55, l 0.34 to 0.36 | none |
| highlight | ink | s 0.55, l 0.87 |
| underline | ink | s 0.55, l 0.55, 1.2 px at 1× |

`--strength` scales saturation for all modes; 0 is ink.

Readability notes from the first experiment (2026-09-07): glyph colour
reads but a sentence with many hand-changes turns into Christmas lights;
highlight is the most legible (the letters stay ink) and the most
literal (marker mixing) but the loudest; underline is the quietest and
reads as hyperlinks unless the rule is thin and low in lightness. Runs
must be merged (one band per same-colour run) in every mode.

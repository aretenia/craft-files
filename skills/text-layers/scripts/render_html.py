#!/usr/bin/env python3
"""
render_html.py  --  one self-contained HTML page of a provenance map: the essay
with the text layers on it. No external dependencies: the two faces are
embedded as base64 woff2, the gutter is drawn by a few lines of inline JS,
and the page reads on a phone offline.

    python3 render_html.py provenance.json -o layers.html \
        --human-font alegreya-400.woff2 --machine-font recursive-mono05-370.woff2 \
        --title "Rupture" --essay-url https://slopshops.ai/essay-04-rupture/ \
        --credit "D. Brinkman, with Claude (Anthropic), 2026"

Layers rendered: fonts, colours, restored (red rule beneath), heat (red rule in
the gutter). Each has a checkbox on the page; the defaults are all on. The
rules match text-layers/references/palette.md and decisions.md.

Fonts: pass static instances (see the skill's assets/webfonts). If the machine
face is a variable Recursive, add --machine-variation "'MONO' 0.5, 'CASL' 0, 'wght' 370".
"""
import argparse
import base64
import html
import json
from pathlib import Path

MIX_FLOOR = 0.15


def colour(lean, mix):
    st = min(1.0, (mix - MIX_FLOOR) / (0.6 - MIX_FLOOR) + 0.35)
    hue = 40 + 210 * lean
    return "hsl(%d %d%% %d%%)" % (round(hue), round(62 * st), round(33 + 5 * (1 - st)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("provenance")
    ap.add_argument("-o", "--out", default="layers.html")
    ap.add_argument("--human-font", required=True)
    ap.add_argument("--machine-font", required=True)
    ap.add_argument("--machine-scale", type=float, default=0.907, help="sans size relative to the serif (x-height match, then trim)")
    ap.add_argument("--machine-variation", default="", help="font-variation-settings for a variable machine face")
    ap.add_argument("--title", default="Untitled")
    ap.add_argument("--subtitle", default="the drafts made visible")
    ap.add_argument("--essay-url", default="")
    ap.add_argument("--credit", default="")
    ap.add_argument("--heat-floor", type=int, default=1)
    args = ap.parse_args()

    prov = json.loads(Path(args.provenance).read_text(encoding="utf-8"))
    toks = prov["tokens"]; summ = prov["summary"]
    hf = base64.b64encode(Path(args.human_font).read_bytes()).decode()
    mf = base64.b64encode(Path(args.machine_font).read_bytes()).decode()

    # ---- the essay as paragraphs of sentences of words
    heat_max = max((t.get("heat", 0) for t in toks), default=1) or 1
    paras = []
    cur_para, cur_sent, last_p, last_s = [], [], None, None
    for t in toks:
        if last_p is not None and t["para"] != last_p:
            if cur_sent: cur_para.append(cur_sent)
            paras.append(cur_para); cur_para, cur_sent = [], []; last_s = None
        elif last_s is not None and t["sentence"] != last_s:
            cur_para.append(cur_sent); cur_sent = []
        cur_sent.append(t); last_p, last_s = t["para"], t["sentence"]
    if cur_sent: cur_para.append(cur_sent)
    if cur_para: paras.append(cur_para)

    body = []
    for p in paras:
        out = ["<p>"]
        for s in p:
            first = s[0]
            mix, lean, heat = first.get("mix", 0.0), first.get("lean"), first.get("heat", 0)
            cls = ["s"]
            style = ""
            if lean is not None and mix >= MIX_FLOOR:
                cls.append("x"); style = ' style="--c:%s"' % colour(lean, mix)
                tip = "Both hands: %d%% human. Rewritten in %d passes." % (round(lean * 100), heat + 1)
            else:
                hands = {t["class"] for t in s if t["class"] in ("human", "machine")}
                tip = ("One hand: a person." if hands == {"human"} else "One hand: the machine." if hands == {"machine"} else "Unattributed.")
                if heat: tip += " Rewritten in %d passes." % (heat + 1)
            words = []
            for t in s:
                wc = "m" if t["class"] == "machine" else "h"
                w = html.escape(t["text"])
                if t.get("restored"):
                    w = '<span class="r">%s</span>' % w
                words.append('<span class="%s">%s</span>' % (wc, w))
            out.append('<span class="%s" data-heat="%d"%s title="%s">%s</span>' % (" ".join(cls), heat, style, html.escape(tip), " ".join(words)))
        out.append("</p>")
        body.append(" ".join(out))
    essay = "\n".join(body)

    share = summ.get("share", {})
    n_mixed = summ.get("mixed_sentences", 0); n_sent = summ.get("sentences", 0)
    n_rest = summ.get("restorations", 0); n_drafts = len(summ.get("drafts", []))
    restored_note = "" if n_rest else " There are none in this piece."
    essay_link = ('<a href="%s">Read the essay as published.</a>' % html.escape(args.essay_url)) if args.essay_url else ""
    var_css = ("font-variation-settings:%s;" % args.machine_variation) if args.machine_variation else ""

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(args.title)}: {html.escape(args.subtitle)}</title>
<style>
@font-face {{ font-family: "Human"; src: url(data:font/woff2;base64,{hf}) format("woff2"); font-weight: 400; font-display: swap; }}
@font-face {{ font-family: "Machine"; src: url(data:font/woff2;base64,{mf}) format("woff2"); font-weight: 400; font-display: swap; }}
:root {{ --bg: #f4f2ee; --ink: #262422; --muted: #6f6b66; --rule: #d9d5cd; --red: #b0281e; --gutter: 18px; }}
html {{ background: var(--bg); }}
body {{ margin: 0; color: var(--ink); font-family: "Human", Georgia, serif; font-size: 19px; line-height: 1.62; -webkit-text-size-adjust: 100%; }}
.wrap {{ max-width: 672px; margin: 0 auto; padding: 32px 20px 72px calc(20px + var(--gutter)); position: relative; }}
header h1 {{ font-weight: 400; font-size: 1.55em; line-height: 1.2; margin: 0 0 .15em; }}
header .sub {{ margin: 0 0 1.4em; color: var(--muted); }}
header p.key {{ margin: 0 0 1em; }}
.controls {{ display: flex; flex-wrap: wrap; gap: .4em 1.4em; margin: 0 0 2.2em; padding: .8em 0; border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); font-family: "Machine", ui-monospace, monospace; font-size: .8em; {var_css} }}
.controls label {{ display: inline-flex; align-items: center; gap: .45em; cursor: pointer; }}
.controls input {{ accent-color: var(--red); width: 1em; height: 1em; margin: 0; }}
article p {{ margin: 0 0 1.25em; }}
/* faces */
body.fonts .m {{ font-family: "Machine", ui-monospace, monospace; font-size: {args.machine_scale}em; {var_css} }}
/* colour, only where both hands wrote the sentence */
body.colors .x {{ color: var(--c); }}
/* words taken back from an earlier draft */
body.restored .r {{ text-decoration: underline; text-decoration-color: var(--red); text-decoration-thickness: 1.5px; text-underline-offset: .16em; }}
/* rewrite heat, drawn into the gutter by the script below */
.gutter {{ position: absolute; left: 0; top: 0; width: 0; height: 0; pointer-events: none; }}
.gutter i {{ position: absolute; width: 3px; background: var(--red); border-radius: 1px; }}
body:not(.heat) .gutter {{ display: none; }}
footer {{ margin-top: 3em; padding-top: 1em; border-top: 1px solid var(--rule); color: var(--muted); font-size: .85em; }}
footer p {{ margin: 0 0 .5em; }}
a {{ color: inherit; }}
:focus-visible {{ outline: 2px solid var(--red); outline-offset: 2px; }}
@media (max-width: 480px) {{ body {{ font-size: 17px; }} .wrap {{ padding-top: 22px; }} }}
</style>
</head>
<body class="fonts colors restored heat">
<div class="wrap">
<header>
<h1>{html.escape(args.title)}</h1>
<p class="sub">{html.escape(args.subtitle)}</p>
<p class="key">This is the essay with its {n_drafts} drafts showing through. <span class="h">Words in this face were written by a person.</span> <span class="m">Words in this face were written by a machine.</span> <span class="x" style="--c:{colour(0.5, 0.8)}">A sentence in colour was written by both</span>, and its colour leans toward whichever hand wrote more of it: <span class="x" style="--c:{colour(0.85, 0.5)}">bluer for the person</span>, <span class="x" style="--c:{colour(0.15, 0.5)}">warmer for the machine</span>. <span class="r">A red line under words</span> means a later draft brought them back from an earlier one.{restored_note} A red mark in the left margin means the sentence was rewritten in many drafts; the darker the mark, the more of them.</p>
<div class="controls">
<label><input type="checkbox" data-layer="fonts" checked> two faces</label>
<label><input type="checkbox" data-layer="colors" checked> colour where both wrote</label>
<label><input type="checkbox" data-layer="restored" checked> words taken back</label>
<label><input type="checkbox" data-layer="heat" checked> rewrite marks</label>
</div>
</header>
<div class="gutter" aria-hidden="true"></div>
<article>
{essay}
</article>
<footer>
<p>{html.escape(args.credit)}</p>
<p>{n_drafts} drafts; {round(100 * share.get("human", 0))} percent of the words were typed by a person and {round(100 * share.get("machine", 0))} percent by a machine, every one of those kept by the person in a later pass; {n_mixed} of {n_sent} sentences were written by both. Footnotes are not shown.</p>
<p>{essay_link}</p>
</footer>
</div>
<script>
(function () {{
  var body = document.body, gutter = document.querySelector('.gutter'), wrap = document.querySelector('.wrap');
  var floor = {args.heat_floor}, hmax = {heat_max};
  function draw() {{
    gutter.innerHTML = '';
    var wr = wrap.getBoundingClientRect();
    var sents = document.querySelectorAll('article .s');
    for (var k = 0; k < sents.length; k++) {{
      var h = +sents[k].getAttribute('data-heat');
      if (h <= floor) continue;
      var a = Math.min(1, (h - floor) / Math.max(1, hmax - floor));
      var rects = sents[k].getClientRects();
      for (var j = 0; j < rects.length; j++) {{
        var i = document.createElement('i');
        i.style.top = (rects[j].top - wr.top + 3) + 'px';
        i.style.height = Math.max(4, rects[j].height - 6) + 'px';
        i.style.left = (wr.left - wr.left + 20) + 'px';
        i.style.opacity = (0.18 + 0.82 * a).toFixed(2);
        gutter.appendChild(i);
      }}
    }}
  }}
  var boxes = document.querySelectorAll('.controls input');
  for (var b = 0; b < boxes.length; b++) boxes[b].addEventListener('change', function (e) {{
    body.classList.toggle(e.target.getAttribute('data-layer'), e.target.checked); draw();
  }});
  var t; window.addEventListener('resize', function () {{ clearTimeout(t); t = setTimeout(draw, 120); }});
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw); else draw();
  window.addEventListener('load', draw);
}})();
</script>
</body>
</html>
"""
    Path(args.out).write_text(page, encoding="utf-8")
    print("wrote", args.out, len(page) // 1024, "KB")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
render_layers.py  --  render a provenance map as the human/machine text layers.

    python3 render_layers.py provenance.json -o out.png [options]

Layers (any combination, default fonts):
    --layers fonts            serif for human and unattributed words, sans for machine
    --layers fonts,colors     plus colour by class and interaction
    --layers fonts,colors,lines   plus faint trails for moved runs (experimental)

Colour (see references/palette.md):
    --color-mode glyph        colour the letters (readable dark tints)
    --color-mode highlight    ink letters on a pale tinted band, marker style
    --color-mode underline    ink letters, a thin coloured rule beneath
    --hues 250,40             human hue, machine hue (degrees); the midpoint is green
    --strength 1.0            0..1 multiplier on the colour

Fonts:
    --serif PATH --sans PATH  default: the locked pair, Alegreya and Recursive
    --weight-serif 400 --weight-sans 370
    --sans-factor 0.95        x-height match trimmed to the locked 0.907 overall
    --size 20                 body size in CSS px; rendered at --scale (default 2)
    --width 672               column width in CSS px (slopshops.ai measures 672)

Selection:
    --find "phrase" --window 120     render a window of tokens around a phrase
    --range 0:400                    or an explicit token range
    --paras 0:3                      or a paragraph range

Demo:
    --demo   treat unattributed words as machine and synthesise some mixing,
             for palette and weight experiments only. The legend says so.
"""
import argparse
import sys
import colorsys
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from PIL import features as _pil_features

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "assets" / "fonts"
BG = (243, 241, 236); INK = (38, 36, 34); MUTED = (120, 116, 110)

# OpenType feature control needs Pillow built with libraqm, which the stock
# Windows wheel is not. Without it Pillow raises rather than ignoring the
# request, so asking for features unconditionally meant no review sheet at
# all on that platform. Degrade instead: the ligature settings are lost and
# the sheet still draws. Everything acceptance compares between the PNG and
# the HTML (faces, colour, the two red layers) is unaffected.
RAQM = _pil_features.check("raqm")


def shaped(feats):
    """The requested OpenType features, or None where they cannot be applied."""
    return feats if RAQM else None


# ------------------------------------------------------------------ fonts
def instance(path, size, weight=400, opsz=None, axes_override=None):
    """A text instance of a (variable) font. axes_override maps axis names
    (as the font names them, e.g. "Monospace", "Casual", "Softness") to values."""
    f = ImageFont.truetype(str(path), size)
    try:
        axes = f.get_variation_axes()
    except Exception:
        return f
    over = {k.lower(): v for k, v in (axes_override or {}).items()}
    vals = []
    for ax in axes:
        name = ax["name"] if isinstance(ax["name"], str) else ax["name"].decode()
        v = ax["default"]
        if name.lower() in ("weight", "wght"): v = weight
        elif name.lower() in ("optical size", "opsz"): v = opsz or min(max(size / 2, ax["minimum"]), ax["maximum"])
        elif name.lower() in ("wonky", "wonk"): v = 0
        elif name.lower() in ("softness", "soft"): v = 30
        elif name.lower() in ("width", "wdth"): v = 100
        if name.lower() in over: v = over[name.lower()]
        vals.append(min(max(v, ax["minimum"]), ax["maximum"]))
    try:
        f.set_variation_by_axes(vals)
    except Exception:
        pass
    return f


def xheight(font):
    b = font.getbbox("x"); return b[3] - b[1]


def load_fonts(serif, sans, size, w_serif, w_sans, ax_serif=None, ax_sans=None, sans_factor=1.0):
    """x-height match, then an optional extra factor on the sans for faces
    whose mass (width, stroke) still outweighs the serif at equal x-height."""
    fs = instance(serif, size, w_serif, axes_override=ax_serif)
    f0 = instance(sans, size, w_sans, axes_override=ax_sans)
    scale = xheight(fs) / xheight(f0) * sans_factor
    fm = instance(sans, max(8, int(round(size * scale))), w_sans, axes_override=ax_sans)
    return fs, fm, scale


# ------------------------------------------------------------------ colour
def hue_for(t, hues):
    """t: 1 = human, 0 = machine, 0.5 = fully mixed. Linear in hue so the
    midpoint lands on green between a purple-blue and an orange-yellow."""
    hm, hh = hues
    return hm + (hh - hm) * t


def rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360.0, l, s)
    return (int(r * 255 + 0.5), int(g * 255 + 0.5), int(b * 255 + 0.5))


MIX_FLOOR = 0.15     # below this a word is treated as purely one hand's and stays ink


def token_t(tok, demo, color_all=False):
    """Returns (t, class, strength). t: 1 human, 0 machine, 0.5 balanced.
    Colour speaks only where both hands were in it; pure authorship stays ink
    unless color_all is set."""
    cls = tok["class"]; mix = tok.get("mix", 0.0); lean = tok.get("lean")
    if demo and cls == "unattributed":
        cls = "machine"
    if lean is not None and mix >= MIX_FLOOR:
        # sentence-level back and forth: the whole sentence takes one colour,
        # leaning toward the hand that wrote more of it
        strength = min(1.0, (mix - MIX_FLOOR) / (0.6 - MIX_FLOOR) + 0.35)
        return lean, cls, strength
    if cls == "human": t = 1.0
    elif cls == "machine": t = 0.0
    else: return None, cls, 0.0
    if not color_all and mix < MIX_FLOOR:
        return None, cls, 0.0
    strength = 1.0 if color_all else min(1.0, (mix - MIX_FLOOR) / (0.6 - MIX_FLOOR) + 0.35)
    return t * (1 - mix) + 0.5 * mix, cls, strength


# ------------------------------------------------------------------ layout
def layout(tokens, fs, fm, d, x0, y0, colw, lead, human_faces):
    """Place every token; returns list of (tok, x, y_baseline, w, font)."""
    placed = []
    space = d.textlength(" ", font=fs)
    x, y = x0, y0
    para = tokens[0]["para"] if tokens else 0
    for tok in tokens:
        if tok["para"] != para:
            para = tok["para"]; x = x0; y += int(lead * 1.7)
        f = fs if tok["face"] in human_faces else fm
        feats = ["liga", "-dlig"] if f is fs else ["-liga"]
        w = d.textlength(tok["text"], font=f, features=shaped(feats))
        if x + w > x0 + colw and x > x0:
            x = x0; y += lead
        placed.append((tok, x, y, w, f, feats))
        x += w + space
    return placed, y + lead


def main():
    if not RAQM:
        sys.stderr.write("note: this Pillow has no libraqm, so ligature "
                         "settings are not applied to the review sheet\n")
    ap = argparse.ArgumentParser()
    ap.add_argument("provenance")
    ap.add_argument("-o", "--out", default="layers.png")
    ap.add_argument("--layers", default="fonts")
    ap.add_argument("--color-mode", default="glyph", choices=["glyph", "highlight", "underline"])
    ap.add_argument("--hues", default="250,40")
    ap.add_argument("--strength", type=float, default=1.0)
    ap.add_argument("--serif", default=str(FONTS / "Alegreya-Variable.ttf"))
    ap.add_argument("--sans", default=str(FONTS / "Recursive-Variable.ttf"))
    ap.add_argument("--weight-serif", type=int, default=400)
    ap.add_argument("--weight-sans", type=int, default=370)
    ap.add_argument("--axes-serif", default=None, help='JSON of axis overrides, e.g. {"Softness": 60}')
    ap.add_argument("--axes-sans", default='{"Monospace": 0.5, "Casual": 0}',
                    help='JSON of axis overrides; the default is the locked machine instance')
    # The locked pair is the x-height match trimmed by 0.95, which comes to
    # 0.907 overall and is what render_html.py uses for --machine-scale. With
    # the factor at 1.0 the sheet drew the pair at 0.955 and disagreed with the
    # HTML on relative face size, which acceptance compares. See
    # references/decisions.md.
    ap.add_argument("--sans-factor", type=float, default=0.95, help="extra size factor on the sans after x-height matching")
    ap.add_argument("--min-scar", type=int, default=8, help="the other hand's words a cut must contain to draw a scar")
    ap.add_argument("--heat-floor", type=int, default=1, help="passes a sentence must have been rewritten in before the gutter shows red (1 = two or more)")
    ap.add_argument("--size", type=float, default=20)
    ap.add_argument("--width", type=int, default=672)
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--find", default=None)
    ap.add_argument("--window", type=int, default=120)
    ap.add_argument("--range", default=None)
    ap.add_argument("--paras", default=None)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--color-all", action="store_true", help="colour pure authorship too (default: only where hands mixed)")
    ap.add_argument("--title", default=None)
    ap.add_argument("--no-legend", action="store_true")
    args = ap.parse_args()

    prov = json.loads(Path(args.provenance).read_text(encoding="utf-8"))
    toks = prov["tokens"]
    layers = set(s.strip() for s in args.layers.split(","))
    hues = tuple(float(h) for h in args.hues.split(","))

    # selection
    if args.find:
        words = [t["text"] for t in toks]
        needle = args.find.lower().split()
        start = 0
        for i in range(len(words)):
            if [w.lower().strip(".,;:!?\"'()") for w in words[i:i + len(needle)]] == [w.strip(".,;:!?\"'()") for w in needle]:
                start = i; break
        toks = toks[start:start + args.window]
    elif args.range:
        a, b = (int(v) for v in args.range.split(":")); toks = toks[a:b]
    elif args.paras:
        a, b = (int(v) for v in args.paras.split(":")); toks = [t for t in toks if a <= t["para"] < b]

    # faces and colour
    human_faces = {"human", "unattributed"}
    for t in toks:
        cls = t["class"]
        if args.demo and cls == "unattributed":
            cls = "machine"
        t["face"] = cls
    if args.demo:                       # synthesise back-and-forth in a few regions, not per word
        n = len(toks)
        regions = [(int(n * 0.10), int(n * 0.18), 0.35), (int(n * 0.42), int(n * 0.52), 0.7), (int(n * 0.74), int(n * 0.80), 0.5)]
        for a, b, m in regions:
            for i in range(a, min(b, n)):
                toks[i]["mix"] = m

    S = args.scale
    size = int(args.size * S)
    fs, fm, scale = load_fonts(args.serif, args.sans, size, args.weight_serif, args.weight_sans,
                               json.loads(args.axes_serif) if args.axes_serif else None,
                               json.loads(args.axes_sans) if args.axes_sans else None, args.sans_factor)
    lead = int(size * 1.62)
    colw = args.width * S
    marg = 48 * S
    # Labels are review chrome, not the art. Public Sans was the reference
    # default and is not in the library, so the labels use the machine face
    # the piece already carries. Flagged to Artlord as a visible change to
    # the review sheet, though not to anything acceptance compares.
    label_font = instance(FONTS / "Recursive-Variable.ttf", 13 * S, 400,
                          axes_override={"Monospace": 0.5, "Casual": 0})

    # measure
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    y0 = 40 * S + (0 if args.no_legend else 44 * S)
    placed, y_end = layout(toks, fs, fm, tmp, marg, y0 + size, colw, lead, human_faces)
    H = y_end + 40 * S
    W = colw + 2 * marg
    page = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(page)

    # legend
    if not args.no_legend:
        parts = []
        if "fonts" in layers: parts.append("serif = human (and unattributed), sans = machine, x-height matched at %.2f×" % scale)
        if "colors" in layers: parts.append("colour only where hands mixed (pure authorship stays ink): leans %d° human, %d° machine, green when balanced; mode %s" % (hues[0], hues[1], args.color_mode))
        if "lines" in layers: parts.append("trails: moved runs (experimental)")
        if "heat" in layers: parts.append("red gutter rule: how many passes fought over the sentence")
        if "heatwash" in layers: parts.append("red wash: how many passes fought over the sentence")
        if "scars" in layers: parts.append("red hairlines: words cut here (full red = cut by the human, pale = by the machine; taller = more words)")
        if "restored" in layers: parts.append("red underline: words brought back from an earlier draft")
        if "loss" in layers: parts.append("red gutter rule: how many of the other hand's words were cut from this paragraph")
        if args.demo: parts.append("DEMO: unattributed words shown as machine, mixing synthesised")
        d.text((marg, 22 * S), (args.title + "  ·  " if args.title else "") + "  ·  ".join(parts), font=label_font, fill=MUTED)

    # trails first (under the text)
    if "lines" in layers:
        para_y = {}
        for tok, x, y, w, f, feats in placed:
            para_y.setdefault(tok["para"], (x, y))
        i = 0
        while i < len(placed):
            tok = placed[i][0]
            if tok.get("moved") and tok.get("move_from_para") is not None:
                j = i
                while j < len(placed) and placed[j][0].get("moved"): j += 1
                x1, y1 = placed[i][1], placed[i][2]
                src = para_y.get(tok["move_from_para"], (marg, y0))
                # a faint red arc from where it was to where it is
                pts = []
                for k in range(41):
                    u = k / 40
                    cx = (src[0] + x1) / 2 - 60 * S
                    px = (1 - u) ** 2 * src[0] + 2 * (1 - u) * u * cx + u ** 2 * x1
                    py = (1 - u) ** 2 * src[1] + 2 * (1 - u) * u * ((src[1] + y1) / 2) + u ** 2 * y1
                    pts.append((px, py))
                over = Image.new("RGBA", page.size, (0, 0, 0, 0))
                od = ImageDraw.Draw(over)
                od.line(pts, fill=(176, 40, 30, 60), width=2 * S)
                page.paste(Image.alpha_composite(page.convert("RGBA"), over).convert("RGB"))
                d = ImageDraw.Draw(page)
                i = j
            else:
                i += 1

    RED = (176, 40, 30)

    def blend(base, color, a):
        return tuple(int(b * (1 - a) + c * a) for b, c in zip(base, color))

    # heat: how many passes fought over the sentence, drawn as a red rule in the gutter (or a wash)
    if "heat" in layers or "heatwash" in layers or "loss" in layers:
        metric = "para_loss" if "loss" in layers else "heat"
        floor = 0 if metric == "para_loss" else args.heat_floor
        hmax = max((tok.get(metric, 0) for tok, *_ in placed), default=1) or 1
        line_heat = {}
        for tok, x, y, w, f, feats in placed:
            line_heat[y] = max(line_heat.get(y, 0), tok.get(metric, 0))
        xh = xheight(fs)
        for y, hval in line_heat.items():
            if hval <= floor: continue
            a = min(1.0, (hval - floor) / (hmax - floor + 1e-6)) * args.strength
            if "loss" in layers:
                d.rectangle((marg - 22 * S, y - xh - 4 * S, marg - 22 * S + 3 * S, y + 4 * S), fill=blend(BG, RED, 0.15 + 0.85 * a))
                continue
            if "heat" in layers:
                d.rectangle((marg - 22 * S, y - xh - 4 * S, marg - 22 * S + 3 * S, y + 4 * S), fill=blend(BG, RED, 0.15 + 0.85 * a))
            if "heatwash" in layers:
                d.rectangle((marg - 6 * S, y - xh - 5 * S, marg + colw + 6 * S, y + 5 * S), fill=blend(BG, RED, 0.03 + 0.12 * a))

    # runs: consecutive words on one line with the same colour share one band or rule
    def runs():
        out = []; cur = None
        for tok, x, y, w, f, feats in placed:
            t, cls, st = token_t(tok, args.demo, args.color_all)
            key = None if t is None else (round(hue_for(t, hues) / 6), y)
            if key is not None and cur and cur["key"] == key:
                cur["x1"] = x + w
            else:
                if cur: out.append(cur)
                cur = None if key is None else {"key": key, "x0": x, "x1": x + w, "y": y, "h": hue_for(t, hues), "cls": cls, "st": st}
        if cur: out.append(cur)
        return out

    # bands under words (highlight mode) before the ink
    if "colors" in layers and args.color_mode == "highlight":
        xh = xheight(fs)
        for r in runs():
            band = rgb(r["h"], 0.55 * args.strength * r["st"], 0.87)
            d.rectangle((r["x0"] - 2 * S, r["y"] - xh - 3 * S, r["x1"] + 2 * S, r["y"] + 3 * S), fill=band)

    # the words
    for tok, x, y, w, f, feats in placed:
        fill = INK
        if "colors" in layers and args.color_mode == "glyph":
            t, cls, st = token_t(tok, args.demo, args.color_all)
            if t is not None:
                h = hue_for(t, hues)
                fill = rgb(h, 0.62 * args.strength * st, 0.33 + 0.05 * (1 - st))
        d.text((x, y), tok["text"], font=f, fill=fill, features=shaped(feats), anchor="ls")
    if "colors" in layers and args.color_mode == "underline":
        for r in runs():
            d.line((r["x0"], r["y"] + 5 * S, r["x1"], r["y"] + 5 * S), fill=rgb(r["h"], 0.55 * args.strength * r["st"], 0.55), width=max(1, int(1.2 * S)))

    # scars: a red hairline where one hand cut the other's words (at least --min-scar of them),
    # taller for bigger cuts, before the word that follows the wound (or after the last word)
    if "scars" in layers:
        xh = xheight(fs)
        for tok, x, y, w, f, feats in placed:
            for key, xx in (("cut_before", x - 3 * S), ("cut_after", x + w + 4 * S)):
                n = tok.get(key + "_other", 0)
                if n < args.min_scar: continue
                hgt = min(xh * 1.4, xh * (0.5 + 0.22 * math.log2(n)))
                d.line((xx, y - hgt, xx, y + 2 * S), fill=RED, width=max(1, int(1.5 * S)))
                d.line((xx - 2 * S, y - hgt, xx + 2 * S, y - hgt), fill=RED, width=max(1, S))

    # restored: words a later pass brought back from an earlier draft, a red rule beneath
    if "restored" in layers:
        cur = None
        for tok, x, y, w, f, feats in placed:
            r = tok.get("restored")
            if r and cur and cur["y"] == y and cur["from"] == r:
                cur["x1"] = x + w
            else:
                if cur: d.line((cur["x0"], cur["y"] + 6 * S, cur["x1"], cur["y"] + 6 * S), fill=RED, width=max(1, int(1.6 * S)))
                cur = {"x0": x, "x1": x + w, "y": y, "from": r} if r else None
        if cur: d.line((cur["x0"], cur["y"] + 6 * S, cur["x1"], cur["y"] + 6 * S), fill=RED, width=max(1, int(1.6 * S)))

    page.save(args.out, optimize=True)
    print("wrote", args.out, page.size, "sans scale %.3f" % scale)


if __name__ == "__main__":
    main()

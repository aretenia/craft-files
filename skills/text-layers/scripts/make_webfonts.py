#!/usr/bin/env python3
"""
make_webfonts.py  --  static, subset woff2 instances of the two faces for embedding.

    python3 make_webfonts.py provenance.json out_dir \
        --human ../assets/fonts/Alegreya-Variable.ttf --human-axes '{"wght": 400}' \
        --machine ../assets/fonts/Recursive-Variable.ttf --machine-axes '{"MONO": 0.5, "CASL": 0, "wght": 370, "slnt": 0, "CRSV": 0}'

Instances the variable fonts at the locked axes (so the page needs no
font-variation-settings) and subsets them to the piece's characters plus
basic Latin. Needs fonttools and brotli (pip install fonttools brotli).
"""
import argparse, json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

BASE = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,;:!?\"'()[]{}<>-/@#%&*+=_|~`^"
           "≠≤≥“”‘’…·×°àáâäãåçèéêëìíîïñòóôöõùúûüýÿÀÁÂÄÃÅÇÈÉÊËÌÍÎÏÑÒÓÔÖÕÙÚÛÜÝ¡¿§¶€£¥©®™")


def make(src, out, axes, chars):
    st = instancer.instantiateVariableFont(TTFont(src), axes, inplace=False)
    tmp = Path(out).with_suffix(".static.ttf"); st.save(tmp)
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
    font = subset.load_font(str(tmp), opts)
    sub = subset.Subsetter(opts); sub.populate(unicodes=[ord(c) for c in chars]); sub.subset(font)
    subset.save_font(font, out, opts); tmp.unlink()
    print(out, Path(out).stat().st_size, "bytes")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("provenance"); ap.add_argument("out_dir")
    ap.add_argument("--human", required=True); ap.add_argument("--human-axes", default='{"wght": 400}')
    ap.add_argument("--machine", required=True); ap.add_argument("--machine-axes", default='{"MONO": 0.5, "CASL": 0, "wght": 370, "slnt": 0, "CRSV": 0}')
    a = ap.parse_args()
    toks = json.loads(Path(a.provenance).read_text(encoding="utf-8"))["tokens"]
    chars = BASE | set(" ".join(t["text"] for t in toks))
    out = Path(a.out_dir); out.mkdir(parents=True, exist_ok=True)
    make(a.human, str(out / "human.woff2"), json.loads(a.human_axes), chars)
    make(a.machine, str(out / "machine.woff2"), json.loads(a.machine_axes), chars)


if __name__ == "__main__":
    main()

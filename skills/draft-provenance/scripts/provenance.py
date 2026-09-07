#!/usr/bin/env python3
"""
provenance.py  --  word-level provenance across an ordered chain of drafts.

    python3 provenance.py manifest.json [-o provenance.json] [--min-move 4]

The manifest lists the drafts in order and says who made each pass:

    {
      "title": "Rupture",
      "drafts": [
        {"file": "Rupture_V1.docx",  "label": "V1",  "agent": "human"},
        {"file": "Rupture_V2.docx",  "label": "V2",  "agent": "machine"},
        {"file": "Rupture_V3.docx",  "label": "V3",  "agent": "mixed"},
        ...
      ]
    }

agent is "human", "machine", or "mixed" (a pass where both worked and the
draft file cannot say who typed what). Files may be .docx, .md, or .txt.

For every token of the LAST draft the script records: origin (which draft
introduced it and who made that pass), the hands that touched it since,
whether a human pass kept it after a machine wrote it (approved), whether
it moved, and how much churn happened around it. Tokens whose origin is a
"mixed" pass are "unattributed": the rendering rule for those is the
human font ("when in doubt, human"), and the summary counts them so you
know how much of the text is still a guess.

The model is deliberately simple: consecutive drafts are aligned with a
longest-common-subsequence diff on normalised words. It is not a parser
and it does not know intent. What it produces is evidence for a picture,
not a verdict.
"""
import argparse
import json
import re
import sys
import zipfile
from difflib import SequenceMatcher
from pathlib import Path
from xml.etree import ElementTree as ET

WORD_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


# ------------------------------------------------------------------ reading
def read_docx(path):
    """Accepted text of a .docx, plus per-character flags for text that sits
    inside a tracked insertion (w:ins). Deleted text (w:del) is dropped.
    Returns (text, flags) where flags is a list of 0/1 per character of text,
    or None when the document has no tracked changes."""
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    _mark_inserted(root)                     # same tree the loop below walks
    has_tracking = root.find(".//" + WORD_NS + "ins") is not None
    paras, flags = [], []
    for p in root.iter(WORD_NS + "p"):
        chunks, pflags = [], []
        for el in p.iter():
            if el.tag == WORD_NS + "t":
                # inside a tracked insertion? walk up via a parent map
                chunks.append(el.text or "")
                pflags.append(1 if el in INSERTED else 0)
        text = "".join(chunks)
        if text.strip():
            paras.append(text)
            f = []
            for c, fl in zip(chunks, pflags):
                f.extend([fl] * len(c))
            flags.append(f)
    out = "\n\n".join(paras)
    if not has_tracking:
        return out, None
    joined = []
    for f in flags:
        joined.extend(f); joined.extend([0, 0])
    return out, joined[:len(out)] if len(joined) >= len(out) else joined + [0] * (len(out) - len(joined))


INSERTED = set()


def _mark_inserted(root):
    """Collect every w:t that sits under a w:ins."""
    INSERTED.clear()
    for ins in root.iter(WORD_NS + "ins"):
        for t in ins.iter(WORD_NS + "t"):
            INSERTED.add(t)


def read_any(path):
    """Returns (text, char_flags_or_None)."""
    path = Path(path)
    if path.suffix.lower() == ".docx":
        try:
            return read_docx(path)
        except zipfile.BadZipFile:
            # a .docx that is really text (project copies arrive this way)
            return path.read_text(encoding="utf-8"), None
    return path.read_text(encoding="utf-8"), None


# ------------------------------------------------------------------ tokens
def clean_markdown(text):
    """Flattened project copies carry emphasis markers (*, **, _) glued to
    words; strip them so they do not read as edits. Headings keep their text."""
    text = re.sub(r"\*{1,3}", "", text)
    text = re.sub(r"(?<!\w)_{1,3}|_{1,3}(?!\w)", "", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.M)
    return text


def tokenize(text, flags=None):
    """Words with their punctuation attached, plus paragraph indices, plus
    ins=True when the word sits in a tracked insertion."""
    toks = []
    pos = 0
    for pi, para in enumerate(re.split(r"(\n\s*\n)", text)):
        if re.fullmatch(r"\n\s*\n", para or ""):
            pos += len(para); continue
        for m in re.finditer(r"\S+", para):
            a, b = pos + m.start(), pos + m.end()
            ins = bool(flags) and any(flags[a:b])
            toks.append({"text": m.group(0), "para": pi // 2, "ins": ins})
        pos += len(para)
    return toks


def norm(w):
    w = w.lower()
    w = (w.replace("à", "a").replace("á", "a").replace("í", "i").replace("é", "e")
          .replace("ó", "o").replace("ú", "u").replace("’", "'"))
    return re.sub(r"[^a-z0-9≠=']", "", w)


# ------------------------------------------------------------------ alignment
def align(prev, cur, prev_records, agent, label, step, min_move, min_run=2, ruled=False, ruled_source="unrecorded"):
    """Carry provenance from prev tokens to cur tokens. Returns cur records
    and the events of this pass."""
    a = [norm(t["text"]) for t in prev]
    b = [norm(t["text"]) for t in cur]
    sm = SequenceMatcher(a=a, b=b, autojunk=False)
    ops = sm.get_opcodes()
    records = [None] * len(cur)
    events = []
    align.last_ops = ops

    deleted_runs = []   # (start_in_prev, list of norm words, list of records)
    inserted_runs = []  # (start_in_cur, list of norm words)
    for tag, i1, i2, j1, j2 in ops:
        if tag == "equal" and (i2 - i1) >= min_run:
            for k in range(i2 - i1):
                r = dict(prev_records[i1 + k])
                r["survived"] = r.get("survived", 0) + 1
                if agent == "human" and r["origin_agent"] == "machine":
                    r["approved_by_human"] = True
                records[j1 + k] = r
        else:
            if tag == "equal":
                tag = "replace"          # a run shorter than min_run is treated as rewritten
            if i2 > i1:
                deleted_runs.append((i1, a[i1:i2], prev_records[i1:i2]))
            if j2 > j1:
                inserted_runs.append((j1, b[j1:j2]))
            # churn: everything near a change gets a tick
            cut_of = {}
            for r in prev_records[i1:i2]:
                cut_of[r["origin_agent"]] = cut_of.get(r["origin_agent"], 0) + 1
            events.append({"step": step, "label": label, "agent": agent, "op": tag,
                           "prev": [i1, i2], "cur": [j1, j2], "cut_of": cut_of,
                           "deleted": " ".join(t["text"] for t in prev[i1:i2])[:160],
                           "inserted": " ".join(t["text"] for t in cur[j1:j2])[:160]})

    # moves: a deleted run that reappears, at least min_move words long, inside an inserted run
    moved = {}
    for (ds, dwords, drecs) in deleted_runs:
        if len(dwords) < min_move:
            continue
        for (ins, iwords) in inserted_runs:
            L = len(dwords)
            for off in range(0, len(iwords) - L + 1):
                if iwords[off:off + L] == dwords:
                    for k in range(L):
                        r = dict(drecs[k])
                        r["moved"] = r.get("moved", 0) + 1
                        r["hands"] = r.get("hands", []) + [agent]
                        r["moved_by"] = r.get("moved_by", []) + [agent]
                        r["move_from_para"] = prev[ds + k]["para"]
                        moved[ins + off + k] = r
                    events.append({"step": step, "label": label, "agent": agent, "op": "move",
                                   "words": L, "from_prev": ds, "to_cur": ins + off,
                                   "text": " ".join(dwords)[:160]})
                    break

    tracked = any(t.get("ins") for t in cur)
    for j in range(len(cur)):
        if tracked and cur[j].get("ins") and j not in moved:
            records[j] = None                                    # a tracked insertion is new, whatever the diff thought
        if records[j] is None:
            if j in moved:
                records[j] = moved[j]
            else:
                records[j] = {"origin_label": label, "origin_step": step, "origin_agent": agent,
                              "hands": [agent] + (["human"] if ruled and agent == "machine" else []),
                              "survived": 0, "moved": 0, "ruled": bool(ruled and agent == "machine"),
                              "ruled_source": (ruled_source if (ruled and agent == "machine") else None),
                              "approved_by_human": False, "tracked": tracked}
    # churn: count, for every token, the number of change ops within a window of 12 tokens
    changed = set()
    for e in events:
        if e["op"] in ("replace", "insert", "delete"):
            j1, j2 = e["cur"]
            for j in range(max(0, j1 - 12), min(len(cur), j2 + 12)):
                changed.add(j)
    for j in changed:
        records[j]["churn"] = records[j].get("churn", 0) + 1
    for j in range(len(cur)):
        records[j].setdefault("churn", 0)
        if agent not in records[j]["hands"] and records[j]["churn"] and j in changed:
            records[j]["hands"] = records[j]["hands"] + [agent]
    return records, events


# ------------------------------------------------------------------ main
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass  # not a real console; nothing to reconfigure

    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("-o", "--out", default="provenance.json")
    ap.add_argument("--min-move", type=int, default=4, help="words a run must have to count as a move")
    ap.add_argument("--min-run", type=int, default=2, help="words an unchanged run must have to carry provenance")
    ap.add_argument("--min-minority", type=float, default=0.12, help="share of a sentence the smaller hand needs before the sentence counts as mixed")
    ap.add_argument("--min-cut", type=int, default=4, help="words a removal needs to count as a scar")
    ap.add_argument("--accept-audit", action="store_true",
                    help="proceed past a halting audit question, recording that it was read")
    args = ap.parse_args()

    man = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    base = Path(args.manifest).parent
    drafts = man["drafts"]
    if len(drafts) < 2:
        sys.exit("need at least two drafts")

    tokens = []
    for d in drafts:
        text, flags = read_any(base / d["file"])
        if flags is None:
            text = clean_markdown(text)
        toks = tokenize(text, flags)
        skip = int(d.get("skip_paragraphs", 0))
        if skip:
            toks = [t for t in toks if t["para"] >= skip]
            for t in toks: t["para"] -= skip
        tokens.append(toks)
        d["tracked_changes"] = bool(flags)
    first = drafts[0]
    records = [{"origin_label": first["label"], "origin_step": 0, "origin_agent": first["agent"],
                "hands": [first["agent"]], "survived": 0, "moved": 0, "approved_by_human": False,
                "churn": 0} for _ in tokens[0]]
    # ruled: a boolean with its evidence class. Accepts true/false, or {"value": bool, "source": "event"|"header"|"attestation"}
    for d in drafts:
        rv = d.get("ruled", None)
        if isinstance(rv, dict):
            d["ruled"], d["ruled_source"] = bool(rv.get("value")), rv.get("source", "unrecorded")
        elif rv is None:
            d["ruled"], d["ruled_source"] = False, "unrecorded"
        else:
            d["ruled"], d["ruled_source"] = bool(rv), d.get("ruled_source", "header")
    all_events = []
    ops_by_step = {}
    for step in range(1, len(drafts)):
        d = drafts[step]
        records, events = align(tokens[step - 1], tokens[step], records, d["agent"], d["label"], step, args.min_move, args.min_run, d.get("ruled", False), d.get("ruled_source", "unrecorded"))
        ops_by_step[step] = align.last_ops
        all_events.extend(events)

    # forward maps: index in draft s -> index in draft s+1 (deleted words map to the block's start)
    def forward(step, idx):
        for tag, i1, i2, j1, j2 in ops_by_step[step]:
            if i1 <= idx < i2 or (idx == i2 == len(tokens[step - 1])):
                return j1 + (idx - i1) if tag == "equal" else j1
        return len(tokens[step])

    def to_final(step, idx):
        for st in range(step + 1, len(drafts)):
            idx = forward(st, idx)
        return min(idx, len(tokens[-1]))        # == len means after the last word

    # cuts: where words were removed, placed at the surviving neighbour in the final text
    scars = []
    for e in all_events:
        if e["op"] in ("delete", "replace") and (e["prev"][1] - e["prev"][0]) >= args.min_cut:
            scars.append({"final_index": to_final(e["step"], e["cur"][0]), "words": e["prev"][1] - e["prev"][0],
                          "by": e["agent"], "step": e["step"], "label": e["label"], "of": e["cut_of"],
                          "text": e["deleted"]})

    # restorations: an inserted run that existed in an earlier draft but not the one just before
    norm_drafts = [[norm(t["text"]) for t in tk] for tk in tokens]
    joined = [" " + " ".join(nd) + " " for nd in norm_drafts]
    restorations = []
    for e in all_events:
        if e["op"] not in ("insert", "replace"): continue
        j1, j2 = e["cur"]; step = e["step"]
        run = norm_drafts[step][j1:j2]
        found = None
        for L in range(min(len(run), 40), 3, -1):
            for off in range(0, len(run) - L + 1):
                sub = " " + " ".join(run[off:off + L]) + " "
                if sub not in joined[step - 1]:
                    earlier = [k for k in range(0, step - 1) if sub in joined[k]]
                    if earlier:
                        found = (off, L, earlier[-1]); break
            if found: break
        if found:
            off, L, k = found
            restorations.append({"step": step, "label": e["label"], "by": e["agent"], "words": L,
                                 "last_seen": drafts[k]["label"], "last_seen_agent": drafts[k]["agent"],
                                 "final_index": to_final(step, j1 + off),
                                 "text": " ".join(tokens[step][j1 + off + i]["text"] for i in range(L))})

    final = tokens[-1]
    out_tokens = []
    for t, r in zip(final, records):
        cls = {"human": "human", "machine": "machine"}.get(r["origin_agent"], "unattributed")
        mix = 0.0
        hs = r["hands"]
        if "human" in hs and "machine" in hs:
            mix = min(1.0, 0.4 + 0.15 * (len(hs) - 2) + 0.1 * r["churn"])
        out_tokens.append({"text": t["text"], "para": t["para"], "class": cls, "proximity_mix": round(mix, 2),
                           "origin": r["origin_label"], "origin_agent": r["origin_agent"],
                           "hands": hs, "survived": r["survived"], "moved": r["moved"],
                           "moved_by": r.get("moved_by", []), "move_from_para": r.get("move_from_para"),
                           "approved": r["approved_by_human"], "churn": r["churn"], "mix": 0.0, "lean": None,
                           "origin_step": r["origin_step"], "ruled": r.get("ruled", False), "ruled_source": r.get("ruled_source")})

    # attestations: phrases the user vouches for ("I wrote this", "the machine
    # wrote this"), applied after the diff. The writer's memory outranks the
    # alignment where the chain is known to be corrupt.
    attested = 0
    fnorm = [norm(t["text"]) for t in out_tokens]
    for att in man.get("attestations", []):
        needle = [norm(w) for w in att["text"].split()]
        L = len(needle)
        for i in range(len(fnorm) - L + 1):
            if fnorm[i:i + L] == needle:
                for k in range(i, i + L):
                    out_tokens[k]["class"] = att["agent"]
                    out_tokens[k]["origin"] = "attested"
                    out_tokens[k]["origin_agent"] = att["agent"]
                    out_tokens[k]["attested"] = True
                    out_tokens[k]["approved"] = False
                attested += L
                break
        else:
            print("attestation not found in the final text:", att["text"][:60], file=sys.stderr)

    # back-and-forth at the sentence level: a sentence both hands wrote parts of
    # is mixed; mix = how balanced, lean = how human. Pure sentences stay 0.
    sent, sents = [], []
    for i, t in enumerate(out_tokens):
        if sent and out_tokens[sent[-1]]["para"] != t["para"]:
            sents.append(sent); sent = []
        sent.append(i)
        if re.search(r"[.!?][\"'”’)]*$", t["text"]):
            sents.append(sent); sent = []
    if sent: sents.append(sent)
    for s in sents:
        toks_s = [out_tokens[i] for i in s]
        h = sum(1 for t in toks_s if t["class"] == "human")
        m_plain = sum(1 for t in toks_s if t["class"] == "machine" and not t["ruled"])
        m_ruled = sum(1 for t in toks_s if t["class"] == "machine" and t["ruled"])
        m = m_plain + m_ruled
        steps = sorted(set(t["origin_step"] for t in toks_s if t["class"] in ("human", "machine")))
        # a rewrite across passes: the sentence's words come from more than one pass, and the
        # later pass was either the other hand or a ruled machine pass (the human ruled the change)
        first_agent = None
        for t in toks_s:
            if t["class"] in ("human", "machine") and t["origin_step"] == (steps[0] if steps else -1):
                first_agent = t["class"]; break
        rewritten = False
        if len(steps) >= 2:
            for t in toks_s:
                if t["origin_step"] > steps[0] and (t["class"] != first_agent or t["ruled"]):
                    rewritten = True; break
        # effective shares: a ruled machine word counts half for the human when the sentence was rewritten
        eff_h = h + (0.5 * m_ruled if rewritten else 0.0)
        eff_m = m - (0.5 * m_ruled if rewritten else 0.0)
        total = eff_h + eff_m
        both = (h and m) or (rewritten and m_ruled)
        if both and total and min(eff_h, eff_m) / total >= args.min_minority:
            mixv = round(2 * min(eff_h, eff_m) / total, 2); lean = round(eff_h / total, 2)
        else:
            mixv, lean = 0.0, None
        for i in s:
            out_tokens[i]["mix"] = mixv
            out_tokens[i]["lean"] = lean
            out_tokens[i]["sentence"] = sents.index(s)
            out_tokens[i]["rewritten"] = rewritten

    for sc in scars:
        i = sc["final_index"]
        other = sum(v for k, v in sc["of"].items() if k != sc["by"])     # the other hand's words in the cut
        sc["other_hand_words"] = other
        if 0 <= i < len(out_tokens):
            key = "cut_before"
        elif i == len(out_tokens):
            i = len(out_tokens) - 1; key = "cut_after"
        else:
            continue
        out_tokens[i][key] = out_tokens[i].get(key, 0) + sc["words"]
        out_tokens[i][key + "_other"] = out_tokens[i].get(key + "_other", 0) + other
        out_tokens[i].setdefault("cut_by", []).append(sc["by"])
    # loss per paragraph: the other hand's words cut inside it, summed
    loss = {}
    for sc in scars:
        i = min(sc["final_index"], len(out_tokens) - 1)
        pa = out_tokens[i]["para"]
        loss[pa] = loss.get(pa, 0) + sc["other_hand_words"]
    for t in out_tokens:
        t["para_loss"] = loss.get(t["para"], 0)
    for r in restorations:
        for i in range(r["final_index"], min(len(out_tokens), r["final_index"] + r["words"])):
            out_tokens[i]["restored"] = r["last_seen"]
    # heat: how many passes rewrote the sentence, plus cuts inside it
    for s_ in sents:
        steps = set(out_tokens[i]["origin_step"] for i in s_)
        cuts = sum(1 for i in s_ if out_tokens[i].get("cut_before"))
        heat = max(0, len(steps) - 1) + cuts
        for i in s_: out_tokens[i]["heat"] = heat

    n = len(out_tokens)
    by = {}
    for t in out_tokens:
        by[t["class"]] = by.get(t["class"], 0) + 1
    audit = []
    halting = []   # the two conditions spec 7 says stop the run with a question
    for step in range(1, len(drafts)):
        ev = [e for e in all_events if e["step"] == step]
        ins = sum(e["cur"][1] - e["cur"][0] for e in ev if e["op"] in ("insert", "replace"))
        dele = sum(e["prev"][1] - e["prev"][0] for e in ev if e["op"] in ("delete", "replace"))
        moves = sum(1 for e in ev if e["op"] == "move")
        n_prev = max(1, len(tokens[step - 1]))
        share = (ins + dele) / (2 * n_prev)
        flags = []
        if ins == 0 and dele == 0:
            flags.append("identical to the previous draft: a flattened export that lost tracked changes, or a duplicate file")
            halting.append((drafts[step]["label"], flags[-1]))
        if drafts[step]["agent"] == "human" and share > 0.5:
            flags.append("a human pass that changed more than half the text: check the label")
            halting.append((drafts[step]["label"], flags[-1]))
        if drafts[step]["agent"] == "machine" and 0 < ins + dele < 12:
            # a note, never a halt: spec 7 says a genuinely small pass passes
            flags.append("a very small machine pass: fine, but consider labelling it mechanical")
        audit.append({"pass": drafts[step]["label"], "agent": drafts[step]["agent"],
                      "words_in": ins, "words_out": dele, "share_changed": round(share, 4),
                      "moves": moves, "tracked_changes": drafts[step].get("tracked_changes", False), "flags": flags})

    # Spec 7: the audit prints before any render, and two of its conditions
    # halt the run with a question rather than deriving past them. The flags
    # phrase the question; this is what makes it stop. Rupture's V8 trips it,
    # which is the point, so re-deriving that chain is a deliberate act.
    if halting and not args.accept_audit:
        print(json.dumps({"title": man.get("title", ""), "audit": audit},
                         indent=2, ensure_ascii=False))
        sys.stderr.write("\nthe audit halts on %d question%s:\n"
                         % (len(halting), "" if len(halting) == 1 else "s"))
        for label, question in halting:
            sys.stderr.write("  %s: %s\n" % (label, question))
        sys.stderr.write("\nAnswer them, fix the manifest or the drafts, or re-run with "
                         "--accept-audit to record that the question was read and the "
                         "chain stands as it is. No record was written.\n")
        sys.exit(2)

    summary = {
        "title": man.get("title", ""),
        "audit": audit,
        "drafts": [{"label": d["label"], "agent": d["agent"], "words": len(tk), "tracked_changes": d.get("tracked_changes", False),
                    "ruled": {"value": ("ruled" if d.get("ruled") else ("unrecorded" if d.get("ruled_source", "unrecorded") == "unrecorded" else "unruled")),
                              "source": d.get("ruled_source", "unrecorded")}} for d, tk in zip(drafts, tokens)],
        "final_words": n,
        "share": {k: round(v / n, 3) for k, v in by.items()},
        "machine_words_approved_by_human": sum(1 for t in out_tokens if t["class"] == "machine" and t["approved"]),
        "moved_words": sum(1 for t in out_tokens if t["moved"]),
        "moves": sum(1 for e in all_events if e["op"] == "move"),
        "unattributed_words": by.get("unattributed", 0),
        "attested_words": attested,
        "mixed_sentences": sum(1 for s in sents if out_tokens[s[0]]["mix"] > 0),
        "rewritten_sentences": sum(1 for s in sents if out_tokens[s[0]].get("rewritten")),
        "ruled_words": sum(1 for t in out_tokens if t.get("ruled")),
        "sentences": len(sents),
        "note": "unattributed = introduced in a pass marked mixed; render as human (when in doubt, human).",
    }
    summary["scars"] = len(scars); summary["restorations"] = len(restorations)
    Path(args.out).write_text(json.dumps({"summary": summary, "tokens": out_tokens, "events": all_events,
                                          "scars": scars, "restorations": restorations}, indent=1, ensure_ascii=False),
                            encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

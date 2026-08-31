#!/usr/bin/env python3
"""scrub-gate.py: deterministic checks for the scrub gate (stage 7).

Counts the countable hallmark rows against a register profile's budgets
and reports. Part of Brinkman's craft files; the artifact definitions live
in hallmarks-and-the-scrub.md, the budgets in register-profiles.md, the
marked terms in machinelexicon.csv.

Two modes:
  gate mode (default): counts vs the active profile's budgets, verdict per row.
  --calibrate: rates only, no verdicts, TSV-friendly. This is the measuring
  half of the calibration protocol; run it across the three corpora.

Honesty notes, load-bearing:
  - Counters marked (heuristic) use pattern matching that has false positives
    and negatives. The gate proposes; the writer decides.
  - The counter cannot tell use from mention. Quoted examples of slop count
    as slop. Fine for calibration corpora; caveat for documents about slop.
  - Budgets are hard-coded from register-profiles.md, PROVISIONAL, July 2026.
    When the profiles change, this table must change with them.

July 2026 batch (post-eval): footnote-definition lines stripped before
segmentation; prepositional middles added to the triad post-filter; em dashes
counted as marks (runs), not characters, with run lengths reported; evidence
output falls back to the working directory when the input's directory is
read-only.

B0 dry-run fixes (July 2026): Tier 0 spans are masked before the H3.2
pass so a ban row cannot pay into the specificity floor; emphasis
stripping is confined to single-line, non-space-bounded spans so unpaired
asterisk art survives;
the stale H2.3 comment corrected (canon already reads sentence-initial).

V3.2 fixes (July 2026, bought by the B1 battery): sentence segmentation now
closes on em-dash-attached terminals and on no-space terminals between a
lowercase letter and a capital; evidence lines locate the matched text rather
than the base lemma's first word, which restores the audit lines that
stem-changing inflections used to drop and points phrase hits at the phrase.

Drift alignment (V3.2): the gated table now matches canon's default profile
exactly. H2.2 and H3.5 are still counted but reported as annotation vocabulary
rather than gated rows, because canon's default table does not declare them;
H1.5 and H3.3 are printed as the rule rows canon declares, for the reader to
judge, rather than silently omitted. `ship-check.py drift` compares this table
against register-profiles.md and fails on any divergence.

V3.3 (July 2026): the registry and the canon tables are separated, because
holding both in one dict is what let the V3.2 divergence hide. COUNTERS says
what this file can measure; PROFILES transcribes canon's tables, default in
full and each register as complete delta rows. Every classification is now
derived from those two rather than listed: a row declared with a band and
backed by a counter is gated, a row declared without one is a rule row judged
by hand, a row declared with a band and no counter reports as owed, and a
counter canon does not declare in the active profile reports as annotation
vocabulary. The hardcoded annotation list could not have expressed the
fairy-tale register, which declares H2.2 as a required closing formula.

Also V3.3: all six registers canon publishes are implemented, where three
were before. Verdict arithmetic is null-safe, since canon writes `n/a` for an
absent band and two registers use shapes that previously raised TypeError, a
floor with no band (satire H0.*) and a row stood down (llm-script H2.10). Two
declared rows had no entry at all before this pass and now report rather than
vanish: satire and fairy-tale declare H2.1, job-search declares H2.9, which
has no counter and prints as owed. Canon's name wins wherever a register
renames a row, since the rename usually carries the inversion. H1.1 evidence
no longer reports marks on footnote-definition lines, which the counting pass
strips: the audit file is the deliverable of record and must not name a match
the gate did not count. Container paths are out of the lexicon search.

Behavior check for this pass: counts, verdicts and flag totals are unchanged
for default, creative and job-search across the sample corpus. Row order now
follows canon's tables, and H1.5 and H3.3 print inline as rule rows rather
than in a trailing line.

V3.4.1 (July 2026): H3.2, a counted and gated floor row, recorded no evidence:
its matches were counted but never located, so the evidence file's claim to list
every pattern location was false for that one row, and it was missing from the
evidence section order entirely. Both passes now record each match at its found
position and H3.2 has a section. Counts, verdicts and flag totals are unchanged.

V3.4 (July 2026): the lexicon gains a `subset` column and profile rows gain an
optional subset selector, which closes a live defect and opens a row that was
declared but unenforced. The defect: job-search declares H1.2 as the flowery
subset, the gate had no way to express a subset, and so a resume was banned
from every one of the seventy-seven marked terms including the domain verbs
canon explicitly exempts. Flowery is now the noun and phrase clusters, twenty-
nine terms, which carries every term canon names by example. The opened row is
H2.9, symmetric hedging, declared by job-search since that register existed and
never counted; it ships as two subsets, dissolution and qualifier, both tagged
so they count in job-search and report nowhere else. See selected() for the
three-clause rule and the H2.9 catalog entry for why that scoping is not
optional: the lexical half of that row is a craft rule for employer-facing
prose, and the corpus evidence says hedge frequency does not indicate machine
authorship.

Known limit: canon's budget tables have no subset column, so the selector is a
gate-side detail that `ship-check.py drift` cannot see. A wrong selector is
caught by reading, not by the check.
"""

import argparse, csv, glob, os, re, statistics, sys

# ---------------------------------------------------------------- the registry
# What this file knows how to MEASURE. Membership here is a fact about the
# code, never about canon: a row appears because a counter exists for it.
# `label` is this file's display wording, which is sometimes more specific
# than canon's prose name; `unit` marks a row whose observation is not a
# per-1,000 rate; `display` marks a row that reports numbers and is never
# scored. Keeping this separate from the tables below is the whole point:
# conflating "has a counter" with "canon declares it" is what produced the
# drift the V3.2 alignment papered over.
COUNTERS = {
    "H0.*":  dict(label="leaked interaction artifacts"),
    "H1.1":  dict(label="em dash"),
    "H1.2":  dict(label="marked lexicon, aggregate"),
    "H1.3":  dict(label="negation-antithesis (heuristic)"),
    "H1.4":  dict(label="triads (heuristic)"),
    "H1.6":  dict(label="sycophancy/engagement strings"),
    "H2.2":  dict(label="summary-closer phrases"),
    "H2.3":  dict(label="sentence-initial formal connectives"),
    "H2.4":  dict(label="significance-inflation phrases"),
    "H2.5":  dict(label="trailing participial analysis (heuristic)"),
    "H2.9":  dict(label="symmetric hedging"),
    "H2.10": dict(label="uniformity: max same-length sentence run", unit="run"),
    "H3.2":  dict(label="specificity markers"),
    "H3.5":  dict(label="puffery terms"),
    "H4.3":  dict(label="typography: curly quotes / straight", display=True),
}

# ---------------------------------------------------------------- canon
# Transcribed from register-profiles.md. `default` is canon's table in full;
# every other profile is canon's delta list. Delta rows are written complete
# rather than partially, because `ship-check.py drift` compares each resolved
# table against canon's table for that profile literally, and a partial row
# would make the comparison depend on merge order.
#
# All six registers canon publishes are here. Three of them declare rows this
# file has no counter for (H2.1, H2.9); those report as owed rather than being
# silently dropped, which is how the H2.2 and H3.5 divergence stayed invisible.
PROFILES = {
    "default": {
        "H0.*":  dict(mode="count", dir="ceiling", target=0,  sd=0,    name="leaked interaction artifacts"),
        "H1.1":  dict(mode="count", dir="ceiling", target=3,  sd=2,    name="em dash"),
        "H1.2":  dict(mode="count", dir="ceiling", target=2,  sd=1,    name="marked lexicon, aggregate"),
        "H1.3":  dict(mode="count", dir="ceiling", target=1,  sd=1,    name="negation-antithesis"),
        "H1.4":  dict(mode="count", dir="ceiling", target=3,  sd=1,    name="triads"),
        "H1.5":  dict(mode="rule",  dir="ceiling", target=None, sd=None, name="bold-led label bullets"),
        "H1.6":  dict(mode="count", dir="ceiling", target=0,  sd=0,    name="sycophancy and engagement scaffolding"),
        "H2.3":  dict(mode="count", dir="ceiling", target=2,  sd=1,    name="sentence-initial formal connectives"),
        "H2.4":  dict(mode="count", dir="ceiling", target=1,  sd=1,    name="significance inflation"),
        "H2.5":  dict(mode="count", dir="ceiling", target=1,  sd=1,    name="trailing participial analysis"),
        "H2.10": dict(mode="rule",  dir="ceiling", target=4,  sd=1,    name="uniformity ceiling"),
        "H3.2":  dict(mode="count", dir="floor",   target=8,  sd=3,    name="specificity markers"),
        "H3.3":  dict(mode="rule",  dir="n/a",     target=None, sd=None, name="citations"),
        "H4.3":  dict(mode="rule",  dir="n/a",     target=None, sd=None, name="typography"),
    },
    "creative": {
        "H1.4":  dict(mode="count", dir="ceiling", target=4,  sd=1,    name="triads"),
        "H3.2":  dict(mode="count", dir="floor",   target=8,  sd=3,    name="specificity markers"),
        "H2.10": dict(mode="rule",  dir="ceiling", target=4,  sd=1,    name="uniformity ceiling"),
    },
    "job-search": {
        "H1.1":  dict(mode="count", dir="ceiling", target=0,  sd=0,    name="em dash"),
        "H1.2":  dict(mode="count", dir="ceiling", target=0,  sd=0,    name="marked lexicon, flowery subset",
                     subset="flowery"),
        "H1.5":  dict(mode="rule",  dir="ceiling", target=None, sd=None, name="bullets"),
        "H2.9":  dict(mode="count", dir="ceiling", target=0,  sd=0,    name="symmetric hedging"),
        "H3.2":  dict(mode="count", dir="floor",   target=12, sd=3,    name="specificity markers"),
        "H2.10": dict(mode="rule",  dir="ceiling", target=6,  sd=1,    name="uniformity ceiling"),
    },
    "satire": {
        "H0.*":  dict(mode="count", dir="floor",   target=0,  sd=None, name="leaked interaction artifacts"),
        "H1.1":  dict(mode="count", dir="floor",   target=6,  sd=2,    name="em dash"),
        "H1.2":  dict(mode="count", dir="floor",   target=8,  sd=2,    name="marked lexicon, aggregate"),
        "H1.3":  dict(mode="count", dir="floor",   target=3,  sd=1,    name="negation-antithesis"),
        "H1.4":  dict(mode="count", dir="floor",   target=5,  sd=1,    name="triads"),
        "H2.1":  dict(mode="rule",  dir="floor",   target=None, sd=None, name="throat-clearing opener"),
        "H2.4":  dict(mode="count", dir="floor",   target=3,  sd=1,    name="significance inflation"),
        "H2.10": dict(mode="rule",  dir="floor",   target=6,  sd=1,    name="uniformity"),
        "H3.3":  dict(mode="rule",  dir="n/a",     target=None, sd=None, name="citations"),
    },
    "fairy-tale": {
        "H1.4":  dict(mode="rule",  dir="floor",   target=None, sd=None, name="rule of three"),
        "H2.1":  dict(mode="rule",  dir="floor",   target=None, sd=None, name="opening formula"),
        "H2.2":  dict(mode="rule",  dir="floor",   target=None, sd=None, name="closing formula"),
        "H2.10": dict(mode="rule",  dir="ceiling", target=6,  sd=1,    name="uniformity ceiling"),
        "H3.2":  dict(mode="count", dir="floor",   target=8,  sd=3,    name="specificity markers"),
    },
    "llm-script": {
        "H0.*":  dict(mode="count", dir="ceiling", target=0,  sd=0,    name="leaked interaction artifacts"),
        "H1.4":  dict(mode="rule",  dir="ceiling", target=None, sd=None, name="triads"),
        "H1.5":  dict(mode="rule",  dir="ceiling", target=None, sd=None, name="bold-led label bullets"),
        "H2.10": dict(mode="rule",  dir="n/a",     target=None, sd=None, name="uniformity ceiling"),
        "H3.3":  dict(mode="rule",  dir="n/a",     target=None, sd=None, name="citations"),
        "H4.3":  dict(mode="rule",  dir="n/a",     target=None, sd=None, name="typography"),
    },
}

WPT = 1000.0  # rates are per 1,000 words

# ---------------------------------------------------------------- lexicon
# Beside the script, then beside the input, then the working directory. No
# absolute paths: this file ships in a public repo and a container path only
# ever confuses the reader who cloned it.
LEXICON_PATHS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "machinelexicon.csv"),
    "machinelexicon.csv", "machine-lexicon.csv",
]

def load_lexicon(path=None):
    paths = [path] if path else LEXICON_PATHS
    for p in paths:
        if p and os.path.exists(p):
            with open(p, newline="", encoding="utf-8") as f:
                rows = [r for r in csv.DictReader(f)]
            return p, rows
    sys.exit("lexicon CSV not found; tried: " + ", ".join(paths))

def lemma_variants(term):
    """Pragmatic inflection matcher: enough for the curated list, not a stemmer."""
    t = term.lower()
    v = {t, t + "s", t + "es", t + "ed", t + "ing"}
    if t.endswith("e"):
        v |= {t + "d", t[:-1] + "ing"}          # delve -> delved, delving
    if t.endswith("y") and len(t) > 3:
        v |= {t[:-1] + "ies", t[:-1] + "ied"}   # tapestry -> tapestries
    return v

def build_matchers(lex_rows):
    """Returns (string_patterns, word_matchers).
    string_patterns: [(tier, term)] matched case-insensitively as substrings (chat artifacts).
    word_matchers:   [(tier, term, subset, compiled_regex)] for words and phrases.
    `subset` is the lexicon's optional partition tag, empty for most rows; the
    active profile decides which partitions count. See selected()."""
    strings, words = [], []
    for r in lex_rows:
        term, cluster, tier = r["term"], r["cluster"], r["tier_id"]
        subset = (r.get("subset") or "").strip()
        if cluster == "chat-artifact":
            strings.append((tier, term))
        elif " " in term or "-" in term:
            pat = re.compile(r"\b" + re.escape(term.lower()).replace(r"\ ", r"\s+") + r"\b")
            words.append((tier, term, subset, pat))
        else:
            alts = sorted(lemma_variants(term), key=len, reverse=True)
            pat = re.compile(r"\b(?:" + "|".join(map(re.escape, alts)) + r")\b")
            words.append((tier, term, subset, pat))
    return strings, words


def selected(tier, subset, rows):
    """Does this lexicon row count under the active profile? Three clauses.

    A profile row with a `subset` selector takes that partition only: job-search
    declares H1.2 as the flowery subset, so a resume is not banned from saying
    `delve`, which the gate did until this rule existed.

    A profile row with no selector takes the whole tier, which is every other
    register's H1.2 and job-search's H2.9.

    A tier the profile does not declare at all is annotation vocabulary, and
    takes untagged rows only. Every H2.9 row is tagged, so hedging counts in
    job-search and reports nowhere else, which is the point: four corpus
    studies say hedge frequency does not indicate machine authorship, so
    surfacing it outside the one register that rules on it as craft would be
    reporting a signal against the evidence.
    """
    row = rows.get(tier)
    if row is None:
        return subset == ""
    sel = row.get("subset")
    return subset == sel if sel else True

# ---------------------------------------------------------------- text prep
# The two footnote-definition forms strip_markdown removes, hoisted so the
# evidence pass can exclude the same lines the counting pass never sees.
FOOTNOTE_DEF = re.compile(r"^(?:\[\^\d+\]|\\\[\\\^\d+\\\]):", re.M)

def strip_markdown(text):
    text = re.sub(r"^\[\^\d+\]:.*$", "", text, flags=re.M)          # footnote definitions
    text = re.sub(r"^\\\[\\\^\d+\\\]:.*$", "", text, flags=re.M)  # pandoc-escaped form
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.M)      # headers
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.M)    # bullets
    # Emphasis pairs cannot cross a line, and their content cannot begin or
    # end on whitespace (CommonMark flanking): Sterne's **** aposiopeses must
    # survive the strip rather than pairing with each other across prose.
    text = re.sub(r"\*\*([^\s*](?:[^*\n]*?[^\s*])?)\*\*", r"\1", text)  # bold
    text = re.sub(r"\*([^\s*](?:[^*\n]*?[^\s*])?)\*", r"\1", text)      # italics
    text = re.sub(r"`([^`]+)`", r"\1", text)                # code spans
    return text

# A terminal mark closes a sentence on whitespace, on an attached em-dash run
# (Sterne writes "Aposiopesis.--Just Heaven!" with real dashes), or, between a
# lowercase letter and a capital, on nothing at all (the "ready.I" typo common
# in raw dumps). The lowercase guard keeps initialisms and decimals intact:
# "U.S.A" and "3.5" do not split.
SENT_SPLIT = re.compile(
    r"(?<=[.!?])[\"')\]]*(?:\s+|\u2014+)"
    r"|(?<=[a-z][.!?])(?=[A-Z])"
)

def sentences(text):
    out = []
    for para in text.split("\n\n"):
        flat = " ".join(para.split())
        if not flat:
            continue
        for s in SENT_SPLIT.split(flat):
            s = s.strip()
            if s and len(s.split()) >= 2:
                out.append(s)
    return out

# ---------------------------------------------------------------- counters
NEG_ANTI = [
    re.compile(r"\bis(?:n't| not) (?:just|only|simply|merely|about)\b", re.I),
    re.compile(r"\b(?:it|this|that)(?:'s| is) not (?:just|only|simply|merely|about)\b", re.I),
    re.compile(r"\bnot only\b.{0,80}?\bbut(?: also)?\b", re.I | re.S),
    re.compile(r"\bno \w+, no \w+, just\b", re.I),
    re.compile(r"\bdon't just \w+\b.{0,40}?\b\w+\b", re.I),
]
# Serial comma required: the non-serial path ("X, Y and Z") was the dominant
# false-positive engine on real essays (pair appositions, clause joins), while
# the writer's genuine triads all carry the serial comma. Non-serial triads are
# an accepted false negative; forks writing non-serial hands restore ",?" here.
TRIAD = re.compile(r"\b[\w'’-]+(?:\s+[\w'’-]+){0,2},\s+[\w'’-]+(?:\s+[\w'’-]+){0,2},\s+(?:and|or)\s+[\w'’-]+", re.I)
CONNECTIVES = ("moreover", "furthermore", "additionally", "in addition", "consequently")
TRAIL_ING = re.compile(
    r",\s+(highlighting|underscoring|demonstrating|reflecting|showcasing|emphasizing|"
    r"signaling|signalling|suggesting|marking|cementing|solidifying|paving|ensuring|"
    r"illustrating|reinforcing|positioning|underlining|revealing)\b[^,;]{0,120}[.!?]\s*$", re.I)
TRIAD_SKIP = {"but", "so", "which", "though", "and", "or", "yet", "then",
              "however", "that", "because",
              # prepositional middles: comma parentheticals like "The machine's,
              # between one version and the next, is rupture". Anaphoric triads
              # ("in the attic, in the basement, and in the garage") survive via
              # the repeated-opener exception below; varied-preposition triads
              # are the accepted false-negative cost, visible in the evidence
              # file's rejected list.
              "between", "of", "in", "for", "with", "at", "on", "from", "by",
              "under", "over", "into", "through", "across", "during", "after",
              "before", "against", "without", "within", "to", "like"}
INTRODUCERS = {"moreover", "furthermore", "additionally", "however", "also",
               "first", "second", "third", "finally", "meanwhile", "instead",
               "today", "still", "indeed", "likewise", "similarly", "thus",
               "nonetheless", "nevertheless", "consequently", "therefore",
               "so", "then", "now", "here", "again", "yesterday", "tomorrow"}

def triad_scan(s):
    """Returns (kept, rejected) match spans for the sentence. Post-filters cut
    the main false-positive classes: tails of four-plus-item lists, comma
    parentheticals before a conjunction, and lone-adverb middles."""
    kept, rejected = [], []
    for m in TRIAD.finditer(s):
        pre = s[:m.start()]
        mm = re.search(r"([\w'’-]+),\s*$", pre)
        if mm and not (pre.strip().rstrip(",").lower() == mm.group(1).lower()
                       and mm.group(1).lower() in INTRODUCERS):
            rejected.append((m.group(), "list tail: four is a list, not a triad"))
            continue
        segs = m.group().split(",")
        first = segs[0].strip().split()
        mid = segs[1].strip().split()
        if mid and mid[0].lower() in TRIAD_SKIP and (not first or first[0].lower() != mid[0].lower()):
            rejected.append((m.group(), "parenthetical or clause join"))
            continue
        if len(mid) == 1 and mid[0].lower().endswith("ly") and not first[-1].lower().endswith("ly"):
            rejected.append((m.group(), "lone-adverb middle"))
            continue
        kept.append(m.group())
    return kept, rejected

def is_triad_sentence(s):
    return bool(triad_scan(s)[0])

PROPER = re.compile(r"\b[A-Z][a-zA-Z'’-]+\b")
NUMERIC = re.compile(r"\b\S*\d\S*\b")

def dispersion(positions, total_words):
    """Coefficient of variation of gaps between occurrences. Low CV at n>=3
    means evenly spaced (the machine pattern); higher means human clumping."""
    if len(positions) < 3 or total_words == 0:
        return None
    pts = sorted(positions) + [sorted(positions)[0] + total_words]
    gaps = [b - a for a, b in zip(pts, pts[1:])]
    m = statistics.mean(gaps)
    return round(statistics.pstdev(gaps) / m, 2) if m else None

def line_of(raw_low, needle, start=0):
    i = raw_low.find(needle, start)
    return (raw_low[:i].count("\n") + 1, i) if i >= 0 else (None, -1)

def analyze(raw, strings, words, rows):
    ev = {}  # hallmark id -> list of evidence strings
    def note(hid, msg):
        ev.setdefault(hid, []).append(msg)
    raw_low = raw.lower()
    text = strip_markdown(raw)
    low = text.lower()
    tokens = text.split()
    n_words = max(len(tokens), 1)
    sents = sentences(text)
    res = {"words": n_words, "sentences": len(sents)}

    # Tier 0 / H1.6 strings, with line numbers from the raw text
    hits0, hits16 = [], []
    for tier, term in strings:
        for m in re.finditer(re.escape(term.lower()), raw.lower()):
            line = raw[:m.start()].count("\n") + 1
            (hits0 if tier.startswith("H0") else hits16).append((tier, term, line))
    res["H0.*"], res["H0_detail"] = len(hits0), hits0
    res["H1.6"], res["H16_detail"] = len(hits16), hits16

    # Em dash: a run of consecutive dashes is one mark. Doubles are a print-era
    # counter-signal, so run lengths are reported alongside the mark count.
    # Evidence and count must draw on the same population. Footnote-definition
    # lines are stripped before counting, so a dash inside one is not counted
    # and the audit must not claim it: the evidence file is the deliverable of
    # record, and a line with no counted mark behind it is a false statement.
    dropped = {raw[:m.start()].count("\n") + 1 for m in FOOTNOTE_DEF.finditer(raw)}
    for m in re.finditer("—+", raw):
        ln = raw[:m.start()].count("\n") + 1
        if ln in dropped:
            continue
        ctx = raw[max(0, m.start() - 30):m.end() + 30].replace("\n", " ")
        note("H1.1", f"line {ln}: ...{ctx}...")
    runs = list(re.finditer("—+", text))
    dash_pos = [len(text[:m.start()].split()) for m in runs]
    res["H1.1"] = len(runs)
    res["H1.1_chars"] = text.count("—")
    from collections import Counter
    res["H1.1_runs"] = dict(sorted(Counter(len(m.group()) for m in runs).items()))
    res["H1.1_spaced"] = len(re.findall(r"(?<=\s)—+(?=\s)", text))
    res["H1.1_cv"] = dispersion(dash_pos, n_words)

    # Lexicon by tier bucket. Phrases match first and mask their spans so a
    # single stretch of text cannot pay into the budget twice.
    buckets = {"H1.2": [], "H2.2": [], "H2.4": [], "H2.9": [], "H3.5": []}
    lex_pos = []
    masked = low
    ordered = sorted(words, key=lambda w: -len(w[1]))
    for tier, term, subset, pat in ordered:
        if not selected(tier, subset, rows):
            continue
        hits = list(pat.finditer(masked))
        if hits and tier in buckets:
            buckets[tier].append((term, len(hits)))
            # Locate the matched text, not the lemma's first word: a stem-changing
            # inflection ("leveraging" for "leverage") is not findable by its lemma
            # and used to lose its audit line, and a phrase used to report at its
            # first word's position rather than the phrase's own.
            pos = 0
            for m in hits:
                ln, i = line_of(raw_low, m.group(), pos)
                if ln:
                    note(tier, f"'{term}' near line {ln}")
                    pos = i + 1
            if tier == "H1.2":
                lex_pos += [len(masked[:m.start()].split()) for m in hits]
            for m in hits:
                masked = masked[:m.start()] + "\x00" * (m.end() - m.start()) + masked[m.end():]
    for tier, pairs in buckets.items():
        res[tier] = sum(c for _, c in pairs)
        res[tier + "_terms"] = sorted(pairs, key=lambda x: -x[1])
    res["H1.2_cv"] = dispersion(lex_pos, n_words)

    # Negation-antithesis, triads, trailing participles: per sentence
    h13 = 0
    for s in sents:
        for p in NEG_ANTI:
            m = p.search(s)
            if m:
                note("H1.3", f'"{s[:110]}" (matched: {m.group()[:40]})')
                h13 += 1
                break
    res["H1.3"] = h13
    triad_flags = []
    for s in sents:
        kept, rejected = triad_scan(s)
        triad_flags.append(bool(kept))
        for k in kept:
            note("H1.4", f'"{k[:90]}" in: {s[:110]}')
        for rj, why in rejected:
            note("H1.4-filtered", f'"{rj[:90]}" rejected ({why})')
    res["H1.4"] = sum(triad_flags)
    res["H1.4_consecutive"] = any(a and b for a, b in zip(triad_flags, triad_flags[1:]))
    h25 = 0
    for s in sents:
        m = TRAIL_ING.search(s)
        if m:
            note("H2.5", f'"...{s[max(0, m.start() - 20):][:120]}"')
            h25 += 1
    res["H2.5"] = h25

    # Metronome connectives, counted sentence-initial, exactly as the profile
    # row reads ("counted at sentence heads"). An earlier version of this
    # comment misquoted canon and taught an eval instance to do the same.
    h23 = 0
    for s in sents:
        if s.lower().startswith(CONNECTIVES):
            note("H2.3", f'"{s[:100]}"')
            h23 += 1
    res["H2.3"] = h23

    # Uniformity: longest run of sentences whose lengths stay within a 4-word band
    lens, best, i = [len(s.split()) for s in sents], 1, 0
    for j in range(len(lens)):
        while max(lens[i:j + 1]) - min(lens[i:j + 1]) > 4:
            i += 1
        best = max(best, j - i + 1)
    res["H2.10"] = best if lens else 0
    if lens:
        note("H2.10", "sentence lengths (words): " + " ".join(map(str, lens)))
    res["sent_mean"] = round(statistics.mean(lens), 1) if lens else 0
    res["sent_sd"] = round(statistics.pstdev(lens), 1) if len(lens) > 1 else 0

    # Specificity: numerals + non-sentence-initial capitalized words.
    # Tier 0 spans are masked first so a leaked preamble or an unfilled
    # placeholder cannot pay into the floor; bracketed placeholders mask
    # through their closing bracket. One row's violation must not subsidize
    # another row's compliance (B0 dry run, July 2026). Residual, documented:
    # capitals that follow stripped bullet labels still count, and floors
    # compare per-1,000 rates, so small samples clear the floor on few hits.
    spec_text = text
    for tier, term in strings:
        if not tier.startswith("H0"):
            continue
        pat = re.escape(term)
        if term.startswith("["):
            pat += r"[^\]\n]{0,60}\]?"
        spec_text = re.sub(pat, lambda m: " " * len(m.group()), spec_text, flags=re.I)
    # Evidence must draw on exactly what the count draws on, so both passes
    # locate their matches in spec_text (Tier 0 already masked) and record each
    # one. H3.2 is a floor: the evidence is the proof the floor was cleared, and
    # for a long document that is a long list, which is correct.
    def h32_line(frag, start):
        i = spec_text.find(frag, start)
        return (spec_text[:i].count("\n") + 1, i) if i >= 0 else (None, -1)
    spec = 0
    pos = 0
    for m in NUMERIC.finditer(spec_text):
        spec += 1
        note("H3.2", f"numeral '{m.group()}' near line {spec_text[:m.start()].count(chr(10)) + 1}")
    starts = {re.sub(r"[^\w'’-]", "", s.split()[0]) for s in sents if s.split()}
    for m in PROPER.finditer(spec_text):
        w = m.group()
        if w not in starts and w != "I":
            spec += 1
            note("H3.2", f"proper noun '{w}' near line {spec_text[:m.start()].count(chr(10)) + 1}")
    res["H3.2"] = spec

    # Typography
    res["H4.3_curly"] = sum(text.count(c) for c in "\u201c\u201d\u2018\u2019")
    res["H4.3_straight"] = text.count('"')
    for tier, term, ln in hits0 + hits16:
        note(tier if tier.startswith("H0") else "H1.6", f"'{term}' line {ln}")
    res["_ev"] = ev
    return res

# ---------------------------------------------------------------- reporting
def rate(count, n_words):
    return round(count * WPT / n_words, 2)

def verdict(row, observed):
    """Null-safe. Canon writes `n/a` for an absent band, which arrives as None;
    a missing band is a band of zero, not a crash. A row with no target is not
    scoreable at all, per the writer's law: a counted cell always carries a
    numeric target, and a row with no number is a rule row by definition."""
    t, sd, d = row["target"], row["sd"], row["dir"]
    if t is None:
        return "info"
    sd = 0 if sd is None else sd
    if d == "ceiling":
        if t == 0 and sd == 0:
            return "BAN HIT" if observed > 0 else "ok"
        return "FLAG" if observed > t + sd else "ok"
    if d == "floor":
        # A floor of zero cannot be violated: satire unlocks H0.* this way,
        # meaning permitted rather than required.
        return "FLAG" if observed < t - sd else "ok"
    return "info"

def resolve(name):
    """Canon's table for this profile: the default table with the register's
    deltas applied. A delta may add a row canon declares only for that
    register (satire's H2.1, job-search's H2.9)."""
    rows = {k: dict(v) for k, v in PROFILES["default"].items()}
    for k, delta in PROFILES[name].items():
        rows.setdefault(k, {}).update(delta)
    return rows

def classify(rid, row):
    """Four outcomes, derived from canon and the registry rather than listed.
    Listing them was the defect: a hardcoded annotation list cannot know that
    fairy-tale declares H2.2 as a required closing formula."""
    if COUNTERS.get(rid, {}).get("display"):
        return "display"        # reports numbers, never scored
    if row["target"] is None:
        return "rule"           # declared without a band: judged, not counted
    if rid not in COUNTERS:
        return "owed"           # declared with a band, no counter exists yet
    return "gated"

def annotation_ids(rows):
    """Counters the active profile does not declare. Counted because the number
    informs the late reads, never scored because canon gives them no budget
    here. Membership follows the profile, so a row can be annotation vocabulary
    in one register and a ruled floor in another."""
    return [r for r in COUNTERS
            if r not in rows and not COUNTERS[r].get("display")]

def budget_str(row):
    if row["target"] is None:
        return "rule"
    sd = row["sd"]
    return f"{row['dir'][:4]} {row['target']}" + (f"\u00b1{sd}" if sd is not None else "")

def observation(rid, row, res):
    """(shown, compared). Bans and run-length rows compare raw counts; every
    other numeric row compares a per-1,000 rate."""
    obs = res.get(rid, 0)
    unit = COUNTERS.get(rid, {}).get("unit")
    r = rate(obs, res["words"])
    if unit == "run":
        return "run", obs
    if row["dir"] == "ceiling" and row["target"] == 0:
        return r, obs
    return r, r

def gated_ids(rows):
    return [rid for rid, row in rows.items() if classify(rid, row) == "gated"]

def row_label(rid, row):
    """Canon's name wins whenever the register renames the row, because the
    rename usually carries the inversion: fairy-tale's H2.2 is a required
    closing formula, not a summary closer, and printing the default wording
    there would state the opposite of the rule. Otherwise this file's label,
    which is often more specific about the counter's method."""
    base = PROFILES["default"].get(rid, {}).get("name")
    if row.get("name") and row["name"] != base:
        return row["name"]
    return COUNTERS.get(rid, {}).get("label") or row.get("name") or rid

def report(path, res, prof_name, rows):
    print(f"\n=== {path} ===")
    print(f"profile: {prof_name} (budgets PROVISIONAL, July 2026) | "
          f"{res['words']} words, {res['sentences']} sentences"
          + ("  [small sample: per-1,000 rates unstable]" if res["words"] < 500 else ""))
    print(f"{'id':6} {'artifact':42} {'count':>5} {'/1000':>7} {'budget':>12} {'verdict':>8}")
    flags, owed = 0, []
    # Canon's own row order. The table reads as a mirror of the register's
    # budget table, so a divergence is visible rather than inferred.
    for rid, row in rows.items():
        kind = classify(rid, row)
        label = row_label(rid, row)[:42]
        if kind == "display":
            print(f"{rid:6} {label:42} {res['H4.3_curly']:>5} {res['H4.3_straight']:>7} "
                  f"{'n/a':>12} {'info':>8}")
        elif kind == "rule":
            print(f"{rid:6} {label:42} {'-':>5} {'-':>7} {budget_str(row):>12} {'judge':>8}")
        elif kind == "owed":
            owed.append(rid)
            print(f"{rid:6} {label:42} {'-':>5} {'-':>7} {budget_str(row):>12} {'NO CTR':>8}")
        else:
            shown, compared = observation(rid, row, res)
            v = verdict(row, compared)
            if rid == "H1.4" and res.get("H1.4_consecutive"):
                v = "FLAG"
            tail = "  [consecutive]" if rid == "H1.4" and res.get("H1.4_consecutive") else ""
            print(f"{rid:6} {label:42} {res.get(rid, 0):>5} {shown:>7} "
                  f"{budget_str(row):>12} {v:>8}{tail}")
            flags += v not in ("ok", "info")
    print(f"sentence length mean {res['sent_mean']} sd {res['sent_sd']}"
          f" | em-dash marks: {res['H1.1']} ({res['H1.1_chars']} chars, runs {res['H1.1_runs']}),"
          f" {res['H1.1_spaced']} spaced"
          + (f" | dash gap CV {res['H1.1_cv']} (low = evenly spaced)" if res["H1.1_cv"] is not None else "")
          + (f" | lexicon gap CV {res['H1.2_cv']}" if res["H1.2_cv"] is not None else ""))
    for tier, label in (("H0_detail", "TIER 0 HITS (stop and report)"), ("H16_detail", "H1.6 strings")):
        if res[tier]:
            print(f"  {label}: " + "; ".join(f"{t} '{s}' line {ln}" for t, s, ln in res[tier]))
    for tier in ("H1.2", "H2.4", "H3.5", "H2.2", "H2.9"):
        if res.get(tier):
            tops = ", ".join(f"{t}×{c}" for t, c in res[tier + "_terms"][:8])
            print(f"  {tier} terms: {tops}")
    ann = [(i, res.get(i, 0)) for i in annotation_ids(rows) if res.get(i, 0)]
    if ann:
        print("  annotation vocabulary (counted, not declared in this profile; rides stages 5-6): "
              + "; ".join(f"{i} {c}" for i, c in ann))
    if owed:
        print("  declared with a budget, no counter in this file: " + ", ".join(owed)
              + " (judge by hand; the gate cannot score them)")
    print(f"summary: {flags} row(s) flagged. The gate proposes; the writer decides.")

def calibrate_line(path, res, rows, header=False):
    ids = gated_ids(rows)
    if header:
        print("file\twords\t" + "\t".join(i + "/1000" if i != "H2.10" else "H2.10run" for i in ids)
              + "\tsent_mean\tsent_sd")
    vals = [str(res.get(i, 0) if COUNTERS.get(i, {}).get("unit") == "run"
                else rate(res.get(i, 0), res["words"])) for i in ids]
    print(f"{path}\t{res['words']}\t" + "\t".join(vals) + f"\t{res['sent_mean']}\t{res['sent_sd']}")

def write_evidence(out_path, src_path, res, prof_name, rows):
    """Markdown audit: the gate report plus every match, its location, and what
    the post-filters rejected. This is the long form the hallmarks AI-note
    asks for (hallmark ID, location, count vs budget); the console report is
    its summary. Also the tuning surface for the heuristic counters."""
    L = [f"# Gate evidence: {os.path.basename(src_path)}", "",
         f"Profile: **{prof_name}** (budgets PROVISIONAL, July 2026). "
         f"{res['words']} words, {res['sentences']} sentences. "
         "Evidence lists every pattern location; counts de-overlap masked spans, "
         "so evidence lines can slightly exceed counts.", "",
         "| id | artifact | count | /1000 | budget | verdict |",
         "| --- | --- | --- | --- | --- | --- |"]
    for rid, row in rows.items():
        kind = classify(rid, row)
        label = row_label(rid, row)
        if kind == "display":
            L.append(f"| {rid} | {label} | {res['H4.3_curly']} | {res['H4.3_straight']} | n/a | info |")
        elif kind == "rule":
            L.append(f"| {rid} | {label} | - | - | {budget_str(row)} | judge |")
        elif kind == "owed":
            L.append(f"| {rid} | {label} | - | - | {budget_str(row)} | no counter |")
        else:
            shown, compared = observation(rid, row, res)
            v = verdict(row, compared)
            if rid == "H1.4" and res.get("H1.4_consecutive"):
                v = "FLAG (consecutive)"
            L.append(f"| {rid} | {label} | {res.get(rid, 0)} | {shown} | {budget_str(row)} | {v} |")
    L += ["", f"Sentence length mean {res['sent_mean']}, sd {res['sent_sd']}. "
              f"Em-dash marks {res['H1.1']} ({res['H1.1_chars']} chars, runs {res['H1.1_runs']}), "
              f"{res['H1.1_spaced']} spaced"
              + (f"; dash gap CV {res['H1.1_cv']}" if res['H1.1_cv'] is not None else "")
              + (f"; lexicon gap CV {res['H1.2_cv']}" if res['H1.2_cv'] is not None else "")
              + ". Low CV means evenly spaced, the machine pattern.", ""]
    order = ["H0.1", "H0.2", "H0.3", "H0.4", "H0.5", "H1.1", "H1.2", "H1.3",
             "H1.4", "H1.4-filtered", "H1.6", "H2.2", "H2.3", "H2.4", "H2.5",
             "H2.9", "H2.10", "H3.2", "H3.5"]
    ev = res.get("_ev", {})
    for hid in order:
        if ev.get(hid):
            title = "H1.4 candidates the post-filters rejected (not counted)"                 if hid == "H1.4-filtered" else hid
            L.append(f"## {title}")
            L += [f"- {line}" for line in ev[hid]]
            L.append("")
    L.append("The gate proposes; the writer decides.")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    return out_path

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="scrub gate: deterministic hallmark checks")
    ap.add_argument("files", nargs="+", help="text/markdown files (globs ok)")
    ap.add_argument("--profile", default="default", choices=sorted(PROFILES))
    ap.add_argument("--lexicon", default=None)
    ap.add_argument("--calibrate", action="store_true", help="rates only, TSV, no verdicts")
    ap.add_argument("--evidence", "--debug", nargs="?", const="auto", default=None,
                    metavar="FILE", help="also write a markdown evidence audit "
                    "(per-match locations, rejected candidates). FILE optional; "
                    "default <input>.evidence.md per input file")
    a = ap.parse_args()

    lex_path, lex = load_lexicon(a.lexicon)
    strings, words = build_matchers(lex)
    rows = resolve(a.profile)
    if not a.calibrate:
        print(f"lexicon: {lex_path} ({len(lex)} rows)")

    paths = [p for g in a.files for p in sorted(glob.glob(g))]
    for k, p in enumerate(paths):
        with open(p, encoding="utf-8") as f:
            res = analyze(f.read(), strings, words, rows)
        if a.calibrate:
            calibrate_line(p, res, rows, header=(k == 0))
        else:
            report(p, res, a.profile, rows)
        if a.evidence:
            if a.evidence == "auto" or len(paths) > 1:
                stem = os.path.splitext(os.path.basename(p))[0] + ".evidence.md"
                d = os.path.dirname(p) or "."
                out = os.path.join(d if os.access(d, os.W_OK) else os.getcwd(), stem)
            else:
                out = a.evidence
            print(f"evidence written: {write_evidence(out, p, res, a.profile, rows)}")

if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(0)  # downstream pipe closed (head, cut); not an error
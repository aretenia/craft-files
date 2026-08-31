#!/usr/bin/env python3
"""accept.py: the mechanical half of the v3 release acceptance test.

Run from the repository root. Everything here is checkable without judgment;
the parts that need a reader are in ACCEPTANCE.md, which is held outside the
repository because it names what each test watches for and would contaminate
any fresh reader who saw it first.

    python3 accept.py

Exits nonzero on any failure. This is a working document, not repo canon:
it verifies the release rather than being part of it.

Provenance: written by the library orchestrator, July 2026, at the writer's
direction, after a dogfood run found that every component passed its own tests
while the assembled system could not be started. The tests below are therefore
weighted toward seams and documented workflows rather than toward units.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PY = sys.executable
FAILS = []
CHECKS = [0]


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if cond:
        print(f"  ok    {name}")
    else:
        FAILS.append(name)
        print(f"  FAIL  {name}" + (f"\n          {detail}" if detail else ""))


def run(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def section(title):
    print(f"\n{title}")


# ------------------------------------------------------------------ structure
def test_structure():
    section("structure and naming")
    for d in ("pipeline", "craftgen", "grid", "skills"):
        check(f"{d}/ exists", os.path.isdir(d))
    for f in ("README.md", "CHANGELOG.md", "LICENSE", "scrub-gate.py",
              "ship-check.py", "machinelexicon.csv"):
        check(f"{f} at root", os.path.isfile(f))

    bad = []
    for root, _, files in os.walk("."):
        if ".git" in root:
            continue
        for f in files:
            if re.search(r"_\d+\.(md|py|json|csv)$", f) or "lanplighter" in f:
                bad.append(os.path.join(root, f))
    check("no platform-mangled filenames", not bad, str(bad))

    pyc = [os.path.join(r, f) for r, _, fs in os.walk(".") if ".git" not in r
           for f in fs if f.endswith(".pyc")]
    check("no committed bytecode", not pyc, str(pyc[:3]))


# ------------------------------------------------------------- cross-refs
def test_crossrefs():
    section("canon cross-references resolve")
    refs = set()
    for f in os.listdir("pipeline"):
        if not f.endswith(".md"):
            continue
        text = open(os.path.join("pipeline", f), encoding="utf-8").read()
        refs |= set(re.findall(r"`([a-z0-9-]+\.md)`", text))
    missing = [r for r in refs
               if not os.path.isfile(os.path.join("pipeline", r))
               and not os.path.isfile(os.path.join("grid", r))]
    check("every .md a canon file names exists", not missing, str(missing))


# ------------------------------------------------------------------- gate
def test_gate():
    section("the gate")
    r = run([PY, "scrub-gate.py", "pipeline/orwell-editing-rules.md"])
    check("runs from root and finds its lexicon", r.returncode == 0, r.stderr[:200])
    check("reports canon's fourteen rows", r.stdout.count("\nH") >= 14)

    profiles = ["default", "creative", "job-search", "satire", "fairy-tale", "llm-script"]
    for p in profiles:
        r = run([PY, "scrub-gate.py", "pipeline/orwell-editing-rules.md", "--profile", p])
        check(f"register {p} runs", r.returncode == 0, r.stderr[-200:])

    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "s.md")
        open(src, "w").write("A draft with 3 numerals and Proper Nouns in 2026.\n" * 5)
        r = run([PY, "scrub-gate.py", src, "--evidence", os.path.join(d, "e.md")])
        check("evidence mode writes an audit", os.path.isfile(os.path.join(d, "e.md")))
        if os.path.isfile(os.path.join(d, "e.md")):
            ev = open(os.path.join(d, "e.md"), encoding="utf-8").read()
            m = re.search(r"\| H3\.2 \|[^|]*\| (\d+) \|", ev)
            sec = re.search(r"## H3\.2\n(.*?)(?=\n## |\nThe gate)", ev, re.S)
            lines = len([l for l in sec.group(1).splitlines() if l.startswith("- ")]) if sec else 0
            check("H3.2 evidence count matches its table count",
                  m and int(m.group(1)) == lines, f"table={m and m.group(1)} lines={lines}")


# ------------------------------------------------------------------ drift
def test_drift():
    section("drift")
    r = run([PY, "ship-check.py", "drift", "--profiles", "pipeline/register-profiles.md",
             "--script", "scrub-gate.py"])
    check("clean across all six registers", r.returncode == 0 and "CLEAN" in r.stdout,
          r.stdout[-200:])

    # a check that cannot fail is worthless: inject a divergence
    with tempfile.TemporaryDirectory() as d:
        tmp = os.path.join(d, "scrub-gate.py")
        src = open("scrub-gate.py", encoding="utf-8").read()
        broken = src.replace('"H1.1":  dict(mode="count", dir="ceiling", target=3,',
                             '"H1.1":  dict(mode="count", dir="ceiling", target=9,', 1)
        open(tmp, "w", encoding="utf-8").write(broken)
        shutil.copy("machinelexicon.csv", d)
        r = run([PY, "ship-check.py", "drift", "--profiles",
                 os.path.abspath("pipeline/register-profiles.md"), "--script", tmp])
        check("catches an injected divergence", r.returncode != 0 and "drift:" in r.stdout)


# ------------------------------------------------------- class column / seed
def test_seed():
    section("the enforcement-class column and the seeder")
    rows, prof = {}, None
    for line in open("pipeline/register-profiles.md", encoding="utf-8"):
        s = line.strip()
        if s.startswith("## Profile:"):
            prof = re.sub(r"\([^)]*\)", "", s.split(":", 1)[1]).strip().split()[0]
        if s.startswith("| H") and prof:
            f = [x.strip() for x in s.strip("|").split("|")]
            if len(f) >= 7:
                rows.setdefault(prof, {})[f[0]] = f[6]
    allc = [c for p in rows.values() for c in p.values()]
    check("every budget row declares a class", allc and all(
        c in ("absolute", "budgeted", "informational") for c in allc),
        str(sorted(set(allc))))

    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "g.json")
        r = run([PY, "ship-check.py", "seed", "--desk", "craft-files",
                 "--profiles", "pipeline/register-profiles.md", "--out", out])
        check("seed emits a grid", r.returncode == 0, r.stderr[-200:])
        if os.path.isfile(out):
            seeded = json.load(open(out))["cells"]
            t0 = json.load(open("grid/grid-sample-t0.json"))["cells"]
            strip = lambda c: {k: {x: y for x, y in v.items() if x != "drift_note"}
                               for k, v in c.items()}
            check("seeded cells match the frozen t0 reference", strip(seeded) == strip(t0))


# ------------------------------------------------- the documented workflow
def test_workflow():
    section("the documented workflow, start to finish")
    with tempfile.TemporaryDirectory() as d:
        shutil.copytree("craftgen", os.path.join(d, "craftgen"))
        for f in ("ship-check.py", "machinelexicon.csv"):
            shutil.copy(f, d)
        shutil.copy("pipeline/register-profiles.md", d)
        grid = os.path.join(d, "grid.json")

        r = run([PY, "ship-check.py", "seed", "--desk", "acc", "--out", "grid.json"], cwd=d)
        check("step 1: a stranger can seed a desk", r.returncode == 0, r.stderr[-200:])

        tmpl = {
            "template_version": "1.0", "desk_id": "acc", "ratified_on": "2026-08-05",
            "author": "Proprietor", "artifact": "draft.md",
            "artifact_label": "machine pass output", "model": "m",
            "changes": [
                {"seq": 1, "machine_move": "closed a spaced em dash",
                 "human_move": "restored the spacing", "rule_id": "H1.1",
                 "direction": "human_strike", "evidence": "d.evidence.md#h11-1", "note": ""},
                {"seq": 2, "machine_move": None, "human_move": "cut a hedge",
                 "rule_id": None, "cluster_key": "hedging", "direction": "human_add",
                 "evidence": "draft.docx#rev-4", "note": ""},
            ],
        }
        json.dump(tmpl, open(os.path.join(d, "t1.json"), "w"))
        r = run([PY, "-m", "craftgen.cli", "generate", "--grid", "grid.json",
                 "--template", "t1.json", "--now", "2026-08-05T10:00:00Z",
                 "--out", "grid2.json", "--ledger", "led.json"], cwd=d)
        check("step 2: the template consumes", r.returncode == 0, r.stderr[-300:])

        if os.path.isfile(os.path.join(d, "grid2.json")):
            g = json.load(open(os.path.join(d, "grid2.json")))
            check("run counter advanced", g["run_counter"] == 1)
            check("the struck rule hardened", g["cells"]["H1.1"]["state"] == "validated")
            check("residue formed a cluster", len(g["undefined_region"]) == 1)
            check("one reel tuple per change", len(g["reel"]) == 2)

        # ledger persistence is cross-invocation, so it needs a second process
        r = run([PY, "-m", "craftgen.cli", "generate", "--grid", "grid.json",
                 "--template", "t1.json", "--now", "2026-08-05T10:00:00Z",
                 "--out", "grid3.json", "--ledger", "led.json"], cwd=d)
        check("step 3: double consumption refused across invocations",
              r.returncode == 2 and "already consumed" in r.stderr, r.stderr[-200:])


# --------------------------------------------------------- generator rules
def test_generator_invariants():
    section("generator invariants")
    sys.path.insert(0, os.getcwd())
    try:
        from craftgen import generate, Refusal
    except Exception as e:  # noqa: BLE001
        check("craftgen imports", False, str(e))
        return
    import copy
    grid = json.load(open("grid/grid-sample-t2.json"))
    base = dict(template_version="1.0", desk_id="craft-files", ratified_on="2026-08-05",
                author="Proprietor", artifact="e.md", artifact_label="x", model="m")

    def t(changes):
        d = dict(base)
        d["changes"] = changes
        return d

    g1, _ = generate(copy.deepcopy(grid), t([]), "2026-08-05T10:00:00Z")
    g2, _ = generate(copy.deepcopy(grid), t([]), "2026-08-05T10:00:00Z")
    check("determinism: identical inputs, identical output",
          json.dumps(g1, sort_keys=True) == json.dumps(g2, sort_keys=True))
    check("born-faded guardrail: a promoted cell keeps its evidence run",
          g1["cells"]["INF-002"]["last_fired_run"] == 1)

    strike = [{"seq": 1, "machine_move": "x", "human_move": "y", "rule_id": "H0.*",
               "direction": "stand", "evidence": None, "note": ""}]
    g3, _ = generate(copy.deepcopy(grid), t(strike), "2026-08-05T10:00:00Z")
    check("absolute endpoint pinned at 1.0", g3["cells"]["H0.*"]["weight"] == 1.0)

    info = [{"seq": 1, "machine_move": "x", "human_move": "y", "rule_id": "H4.3",
             "direction": "human_strike", "evidence": "a#1", "note": "typography"}]
    g4, _ = generate(copy.deepcopy(grid), t(info), "2026-08-05T10:00:00Z")
    check("informational endpoint pinned at 0.4", g4["cells"]["H4.3"]["weight"] == 0.4)

    refusals = [
        ("human_strike with no machine move",
         [{"seq": 1, "machine_move": None, "human_move": "y", "rule_id": "H1.1",
           "direction": "human_strike", "evidence": None, "note": ""}]),
        ("cluster_key beside a named rule",
         [{"seq": 1, "machine_move": None, "human_move": "y", "rule_id": "H1.1",
           "cluster_key": "k", "direction": "human_add", "evidence": None, "note": ""}]),
        ("rule_id naming no cell",
         [{"seq": 1, "machine_move": None, "human_move": "y", "rule_id": "H9.9",
           "direction": "human_add", "evidence": None, "note": ""}]),
        ("bandless row with an empty note",
         [{"seq": 1, "machine_move": None, "human_move": "y", "rule_id": "H3.3",
           "direction": "human_add", "evidence": None, "note": ""}]),
    ]
    for name, ch in refusals:
        try:
            generate(copy.deepcopy(grid), t(ch), "2026-08-05T10:00:00Z")
            check(f"refuses: {name}", False, "no refusal raised")
        except Refusal:
            check(f"refuses: {name}", True)


# ----------------------------------------------------------------- skills
def test_skills():
    section("skills")
    for s in ("scrub-gate", "canon-shipping"):
        p = f"skills/{s}/SKILL.md"
        check(f"{s}/SKILL.md present", os.path.isfile(p))
        if os.path.isfile(p):
            head = open(p, encoding="utf-8").read()[:600]
            check(f"{s} declares name and description in frontmatter",
                  head.startswith("---") and "name:" in head and "description:" in head)
    check("canon-shipping carries its companion",
          os.path.isfile("skills/canon-shipping/ship-check.py"))
    if os.path.isfile("skills/canon-shipping/ship-check.py"):
        a = open("skills/canon-shipping/ship-check.py", encoding="utf-8").read()
        b = open("ship-check.py", encoding="utf-8").read()
        check("the companion matches the governing root copy", a == b)

    # the skills describe the tools; the descriptions must not have gone stale
    txt = open("skills/canon-shipping/SKILL.md", encoding="utf-8").read()
    subs = set(re.findall(r"ship-check\.py (\w+)", txt))
    real = set(re.findall(r'add_parser\("(\w+)"', open("ship-check.py", encoding="utf-8").read()))
    check("every subcommand the skill names exists in the tool",
          subs <= real, f"named but absent: {sorted(subs - real)}")


def main():
    if not os.path.isfile("scrub-gate.py"):
        sys.exit("run this from the repository root")
    print("v3 release acceptance, mechanical half")
    test_structure()
    test_crossrefs()
    test_gate()
    test_drift()
    test_seed()
    test_workflow()
    test_generator_invariants()
    test_skills()
    print(f"\n{CHECKS[0] - len(FAILS)}/{CHECKS[0]} checks passed")
    if FAILS:
        print("failures:")
        for f in FAILS:
            print("  " + f)
        return 1
    print("\nMechanical half clean. The judgment half cannot be scripted: it needs")
    print("fresh readers, and its criteria are held outside the repo so they stay fresh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

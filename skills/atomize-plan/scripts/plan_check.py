#!/usr/bin/env python3
"""Check an atomization plan before any post is written.

  python3 plan_check.py plan.json
  python3 plan_check.py plan.json --source source.md --facts ../references/platform-facts.md
  python3 plan_check.py --init > plan.json

The plan is the cheap place to be wrong. This script fails it when:
  FAIL  no core insight, or the core insight is longer than 30 words
  FAIL  an atom has no "evidence" line, or (with --source) the evidence
        is not found in the source text, so the claim does not trace back
  FAIL  a platform is skipped without a reason
  FAIL  a thin source (under 500 words or under 3 atoms) gets more than
        3 pieces
  FAIL  a format that the platform does not have (e.g. "carousel" on X)
  FAIL  platform-facts.md is past last_verified + ttl_days (refresh first)
  WARN  more than 3 active platforms or more than 6 pieces without
        "wide": true
  WARN  a weak fit between the atoms and the format (a story as a carousel)
  WARN  two platforms share the same hook type
  WARN  atoms that no piece uses
Exit code 1 if any FAIL. Standard library only.
"""
import argparse
import datetime
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to a legacy code page

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FACTS = os.path.join(HERE, "..", "references", "platform-facts.md")

FORMATS = {
    "x": {"post", "thread", "long-post", "link-in-reply"},
    "threads": {"post", "mini-thread"},
    "linkedin": {"post", "carousel", "document"},
    "instagram": {"carousel", "reel-script", "caption"},
    "tiktok": {"video-script", "carousel"},
    "shorts": {"video-script"},
    "telegram": {"post", "long-post"},
    "newsletter": {"issue", "section"},
    "bluesky": {"post", "thread"},
    "reddit": {"post"},
}
TREATMENTS = {"native-deep", "native-light", "link-in-reply", "skip"}
KINDS = {"framework", "story", "data", "contrarian", "tutorial", "quote", "opinion", "step"}
# (atom kind, format) pairs that compress badly. From the fit table in references/idea-shapes.md
WEAK = {
    ("framework", "video-script"), ("framework", "reel-script"),
    ("story", "carousel"), ("story", "document"),
    ("data", "reel-script"),
    ("contrarian", "carousel"), ("contrarian", "document"),
    ("tutorial", "post"), ("tutorial", "mini-thread"),
    ("opinion", "carousel"), ("opinion", "video-script"),
}
HOOK_TYPES = {"time-transformation", "pain-mirror", "market-bomb", "outcome-first",
              "barrier-removal", "anti-pattern", "exclusion", "story-open", "question"}

INIT = {
    "source": {"title": "How we close the books in 3 days", "path": "source.md"},
    "core_insight": "One sentence a reader would repeat to a colleague.",
    "wide": False,
    "atoms": [
        {"id": "a1", "kind": "data", "text": "What the atom says, in your words",
         "evidence": "a short exact quote from the source"},
    ],
    "platforms": [
        {"platform": "x", "treatment": "native-light", "format": "post", "atoms": ["a1"],
         "hook_type": "outcome-first", "why": "the number stands alone"},
        {"platform": "instagram", "treatment": "skip", "why": "account not active"},
    ],
}


def norm(s):
    s = s.lower().replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[^a-z0-9%$.']+", " ", s).strip()


def facts_status(path, today):
    if not os.path.exists(path):
        return "WARN", "platform-facts file not found at %s" % path
    with open(path, encoding="utf-8") as f:
        head = f.read(800)
    lv = re.search(r"last_verified:\s*(\d{4}-\d{2}-\d{2})", head)
    ttl = re.search(r"ttl_days:\s*(\d+)", head)
    if not lv:
        return "WARN", "platform-facts has no last_verified date"
    d = datetime.date.fromisoformat(lv.group(1))
    days = int(ttl.group(1)) if ttl else 90
    exp = d + datetime.timedelta(days=days)
    if today > exp:
        return "FAIL", "platform-facts expired on %s (verified %s, ttl %d days). Refresh it before writing" % (exp, d, days)
    return "PASS", "platform-facts fresh until %s" % exp


def check(plan, source_text=None, facts=DEFAULT_FACTS, today=None):
    res = []
    add = lambda level, msg: res.append((level, msg))  # noqa: E731
    today = today or datetime.date.today()

    ci = (plan.get("core_insight") or "").strip()
    if not ci or ci.startswith("One sentence a reader"):
        add("FAIL", "no core_insight")
    elif len(ci.split()) > 30:
        add("FAIL", "core_insight is %d words; cut it to one sentence under 30" % len(ci.split()))
    else:
        add("PASS", "core insight: %r" % ci)

    atoms = plan.get("atoms") or []
    ids = {}
    src = norm(source_text) if source_text else None
    for a in atoms:
        aid = a.get("id", "?")
        ids[aid] = a
        if a.get("kind") not in KINDS:
            add("WARN", "atom %s kind %r not one of %s" % (aid, a.get("kind"), ", ".join(sorted(KINDS))))
        ev = (a.get("evidence") or "").strip()
        if not ev:
            add("FAIL", "atom %s has no evidence line; quote the source or drop the atom" % aid)
        elif src is not None and norm(ev) not in src:
            add("FAIL", "atom %s evidence not found in the source: %r" % (aid, ev[:60]))
    if atoms and not any(r[0] == "FAIL" and "atom" in r[1] for r in res):
        add("PASS", "%d atoms, each with evidence%s" % (len(atoms), " found in the source" if src is not None else ""))

    words = len(re.findall(r"\w+", source_text)) if source_text else plan.get("source", {}).get("words")
    thin = (words is not None and words < 500) or len(atoms) < 3

    active, pieces, hooks = [], 0, {}
    used = set()
    for p in plan.get("platforms") or []:
        name = (p.get("platform") or "").lower()
        tr = p.get("treatment")
        if name not in FORMATS:
            add("WARN", "unknown platform %r" % name)
        if tr not in TREATMENTS:
            add("FAIL", "%s: treatment %r, use one of %s" % (name, tr, ", ".join(sorted(TREATMENTS))))
            continue
        if tr == "skip":
            if not (p.get("why") or "").strip():
                add("FAIL", "%s skipped without a reason" % name)
            else:
                add("PASS", "%s skipped: %s" % (name, p["why"]))
            continue
        active.append(name)
        n = int(p.get("pieces", 1))
        pieces += n
        fmt = p.get("format")
        if name in FORMATS and fmt not in FORMATS[name]:
            add("FAIL", "%s has no format %r (use %s)" % (name, fmt, ", ".join(sorted(FORMATS[name]))))
        if not (p.get("why") or "").strip():
            add("WARN", "%s has no 'why' line" % name)
        for aid in p.get("atoms") or []:
            used.add(aid)
            a = ids.get(aid)
            if a is None:
                add("FAIL", "%s uses atom %s which does not exist" % (name, aid))
            elif (a.get("kind"), fmt) in WEAK:
                add("WARN", "%s: a %s atom as %s compresses badly (see references/idea-shapes.md)" % (name, a.get("kind"), fmt))
        ht = (p.get("hook_type") or "").lower()
        if ht and ht not in HOOK_TYPES:
            add("WARN", "%s hook_type %r is not a known type" % (name, ht))
        if ht:
            hooks.setdefault(ht, []).append(name)

    if thin and pieces > 3:
        add("FAIL", "thin source (%s words, %d atoms) but %d pieces planned; plan 1 to 3" % (words, len(atoms), pieces))
    elif thin:
        add("PASS", "thin source, %d piece(s) planned" % pieces)
    if not plan.get("wide") and (len(active) > 3 or pieces > 6):
        add("WARN", "%d platforms, %d pieces: over the default budget of 2-3 platforms and 3-6 pieces. Set \"wide\": true if asked for it" % (len(active), pieces))
    elif active:
        add("PASS", "%d active platform(s), %d piece(s)" % (len(active), pieces))
    if not active:
        add("FAIL", "no active platform")
    for ht, names in hooks.items():
        if len(names) > 1:
            add("WARN", "hook type %s used on %s; give each platform its own angle" % (ht, ", ".join(names)))
    unused = [a for a in ids if a not in used]
    if unused:
        add("INFO", "atoms not used by any piece: %s" % ", ".join(unused))

    if facts:
        add(*facts_status(facts, today))
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan", nargs="?", help="plan.json")
    ap.add_argument("--source", help="the source text, to check that every atom's evidence is in it")
    ap.add_argument("--facts", default=DEFAULT_FACTS, help="platform-facts.md with last_verified and ttl_days")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD), for tests")
    ap.add_argument("--init", action="store_true", help="print a starter plan.json")
    ap.add_argument("--json", action="store_true", help="print JSON")
    a = ap.parse_args()
    if a.init:
        print(json.dumps(INIT, indent=2))
        return
    if not a.plan:
        ap.error("plan.json is required (or --init)")
    with open(a.plan, encoding="utf-8") as f:
        plan = json.load(f)
    src = None
    path = a.source or (plan.get("source") or {}).get("path")
    if path and not os.path.isabs(path) and not a.source:
        path = os.path.join(os.path.dirname(os.path.abspath(a.plan)), path)
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            src = f.read()
    elif a.source:
        ap.error("source not found: %s" % a.source)
    today = datetime.date.fromisoformat(a.today) if a.today else None
    res = check(plan, src, a.facts, today)
    fails = sum(1 for r in res if r[0] == "FAIL")
    if a.json:
        print(json.dumps({"fails": fails, "results": [{"level": l, "msg": m} for l, m in res]}, indent=1))
    else:
        for level, msg in res:
            print("%-4s %s" % (level, msg))
        print("\n%s: %d fail(s), %d warning(s)" % ("BLOCKED" if fails else "OK", fails, sum(1 for r in res if r[0] == "WARN")))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

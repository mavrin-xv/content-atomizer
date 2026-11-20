#!/usr/bin/env python3
"""Rank the comments on a post, so replies go to the ones that matter first.

  python3 triage_replies.py comments.txt -o replies.md
  python3 triage_replies.py comments.txt --known "dana_k,lee.ops" -o replies.md
  python3 triage_replies.py --check replies.md

comments.txt: one comment per line as "author: text". Lines that start
with whitespace continue the comment above. Blank lines are ignored.

Tiers (a default order; read the comments, then move rows if needed):
  1 question       asks something you can answer with new information
  2 disagreement   pushes back with a reason
  3 experience     shares their own numbers or story
  4 peer           from someone on the --known list, or a repeat commenter
  5 praise         short thanks or applause (batch a few varied replies)
  6 skip           bait, abuse, spam, all caps. No reply, with the reason
Flags:
  NEEDS A PERSON   the comment asks about price, refunds, dates, guarantees,
                   legal or medical questions, or anything private. The
                   draft must not promise; a person answers
  RELATIONSHIP     repeat commenter, --known peer, or someone who shares
                   their own data. Worth a follow or a DM, not just a reply

--check reads a filled replies.md and FAILs on: a draft longer than 3
sentences, a draft under a tier 6 comment, a NEEDS A PERSON row whose draft
promises a price, date or result, two identical drafts, bait in a draft, or
an empty draft for tiers 1-3. Exit code 1 if any FAIL.
Standard library only.
"""
import argparse
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to a legacy code page

TIER_NAMES = {1: "question", 2: "disagreement", 3: "experience", 4: "peer", 5: "praise", 6: "skip"}
DISAGREE = r"\b(disagree|not true|doesn't work|does not work|wrong|but (we|i|in my)|actually|i'd push back|not sure that|that's not|never worked|in my experience it|counterpoint)\b"
EXPERIENCE = r"\b(we (tried|did|went|cut|use|used|saw|got)|i (tried|did|went|cut|use|used|saw|got|run|ran)|our (team|shop|numbers|close)|for us|in my shop|last (month|year|quarter))\b"
PRAISE = r"^(great|love|amazing|awesome|so good|this is gold|thanks|thank you|fire|nice|well said|100%|facts|needed this|saved)\b"
QUESTION = r"\?|^(how|what|why|which|when|where|can|could|does|do|is|are|would|should)\b"
SKIP = r"\b(dm me for|check my profile|crypto signals|follow back|f4f|idiot|scam|clown|garbage|trash)\b|https?://"
PERSON = r"\b(price|pricing|cost|how much|refund|discount|coupon|deadline|when (will|does|is)|date|guarantee|legal|lawyer|tax advice|medical|my account|invoice|contract|password)\b"
PROMISE = r"(\$\s?\d|\b\d+\s?(dollars|usd|eur|%)\b|\bguarantee|\bby (monday|tuesday|wednesday|thursday|friday|tomorrow|next week)\b|\bwill (definitely|always)\b|\bfree for you\b)"
BAIT = ["follow for more", "thoughts?", "rt if", "like if", "check my profile", "link in bio"]


def parse(text):
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        if line[:1].isspace() and rows:
            rows[-1]["text"] += " " + line.strip()
            continue
        m = re.match(r"^\s*([^:]{1,40}):\s*(.+)$", line)
        if m:
            rows.append({"author": m.group(1).strip().lstrip("@"), "text": m.group(2).strip()})
        else:
            rows.append({"author": "unknown", "text": line.strip()})
    return rows


def classify(rows, known=()):
    known = {k.strip().lstrip("@").lower() for k in known if k.strip()}
    counts = {}
    for r in rows:
        counts[r["author"].lower()] = counts.get(r["author"].lower(), 0) + 1
    for i, r in enumerate(rows):
        t = r["text"]
        low = t.lower()
        letters = [c for c in t if c.isalpha()]
        caps = letters and sum(c.isupper() for c in letters) / float(len(letters)) > 0.7 and len(letters) > 12
        r["idx"] = i + 1
        r["flags"] = []
        if re.search(SKIP, low) or caps:
            r["tier"], r["reason"] = 6, "spam, abuse or a link drop" if not caps else "all caps shouting"
        elif re.search(DISAGREE, low) and len(t.split()) >= 6:
            r["tier"], r["reason"] = 2, "pushes back with a reason"
        elif re.search(QUESTION, low):
            r["tier"], r["reason"] = 1, "asks a question"
        elif re.search(EXPERIENCE, low) or (re.search(r"\d", t) and len(t.split()) >= 8):
            r["tier"], r["reason"] = 3, "shares their own data or story"
        elif r["author"].lower() in known or counts[r["author"].lower()] > 1:
            r["tier"], r["reason"] = 4, "known peer or repeat commenter"
        elif re.search(PRAISE, low) or len(t.split()) <= 5:
            r["tier"], r["reason"] = 5, "short praise"
        else:
            r["tier"], r["reason"] = 4, "substantive comment, no clear type"
        if re.search(PERSON, low) and r["tier"] != 6:
            r["flags"].append("NEEDS A PERSON")
        why = []
        if r["author"].lower() in known:
            why.append("on your known list")
        if counts[r["author"].lower()] > 1:
            why.append("%d comments on this post" % counts[r["author"].lower()])
        if r["tier"] == 3:
            why.append("shared their own data")
        if r["tier"] != 6 and why:
            r["flags"].append("RELATIONSHIP")
            r["rel"] = ", ".join(why)
    return sorted(rows, key=lambda r: (r["tier"], r["idx"]))


def to_md(rows):
    out = ["# Replies", "", "Ranked by tier. Write each draft in 1 to 3 sentences that add something the post did not say.",
           "Tier 6 rows get no reply. Rows flagged NEEDS A PERSON get a holding reply with no price, date or promise.", ""]
    for r in rows:
        flags = (" | " + ", ".join(r["flags"])) if r["flags"] else ""
        out.append("## %d. tier %d %s | @%s%s" % (r["idx"], r["tier"], TIER_NAMES[r["tier"]], r["author"], flags))
        out.append("> %s" % r["text"])
        out.append("")
        out.append("Why: %s" % r["reason"])
        out.append("Draft: %s" % ("(no reply)" if r["tier"] == 6 else ""))
        out.append("")
    rel = [r for r in rows if "RELATIONSHIP" in r["flags"]]
    out.append("## Relationship flags")
    out.append("")
    if rel:
        seen = set()
        for r in rel:
            if r["author"] in seen:
                continue
            seen.add(r["author"])
            out.append("- @%s: %s" % (r["author"], r["rel"]))
    else:
        out.append("- none")
    out.append("")
    return "\n".join(out)


def sentences(s):
    s = re.sub(r"\b(e\.g|i\.e|vs|etc)\.", r"\1", s)
    return len([x for x in re.split(r"(?<=[.!?])\s+", s.strip()) if x.strip()])


def check(md):
    fails, warns = 0, 0
    blocks = re.split(r"^## ", md, flags=re.M)[1:]
    drafts = {}
    for b in blocks:
        head = b.splitlines()[0]
        m = re.match(r"(\d+)\. tier (\d)", head)
        if not m:
            continue
        idx, tier = m.group(1), int(m.group(2))
        dm = re.search(r"^Draft:\s*(.*(?:\n(?!Why:|## ).+)*)", b, re.M)
        draft = (dm.group(1).strip() if dm else "")
        if draft == "(no reply)":
            draft = ""
        if tier == 6 and draft:
            print("FAIL #%s: tier 6 (skip) has a draft; do not reply" % idx)
            fails += 1
        if tier in (1, 2, 3) and not draft:
            print("FAIL #%s: tier %d needs a draft" % (idx, tier))
            fails += 1
        if not draft:
            continue
        n = sentences(draft)
        if n > 3:
            print("FAIL #%s: draft is %d sentences; keep to 3" % (idx, n))
            fails += 1
        if "NEEDS A PERSON" in head and re.search(PROMISE, draft.lower()):
            print("FAIL #%s: NEEDS A PERSON but the draft promises a price, date or result" % idx)
            fails += 1
        if any(x in draft.lower() for x in BAIT):
            print("FAIL #%s: bait in the draft" % idx)
            fails += 1
        key = re.sub(r"\W+", " ", draft.lower()).strip()
        if key in drafts:
            print("FAIL #%s: same draft as #%s; vary the replies" % (idx, drafts[key]))
            fails += 1
        drafts[key] = idx
        if "—" in draft or "–" in draft:
            print("WARN #%s: em/en dash in the draft" % idx)
            warns += 1
    print("\n%s: %d draft(s), %d fail(s), %d warning(s)" % ("BLOCKED" if fails else "OK", len(drafts), fails, warns))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="comments.txt, or replies.md with --check")
    ap.add_argument("-o", "--out", help="write replies.md here (default: print)")
    ap.add_argument("--known", default="", help="comma-separated handles of peers or customers")
    ap.add_argument("--check", action="store_true", help="check a filled replies.md")
    a = ap.parse_args()
    with open(a.file, encoding="utf-8") as f:
        text = f.read()
    if a.check:
        sys.exit(check(text))
    rows = classify(parse(text), a.known.split(","))
    md = to_md(rows)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(md)
        counts = {}
        for r in rows:
            counts[r["tier"]] = counts.get(r["tier"], 0) + 1
        print("wrote %s: %d comments, %s" % (a.out, len(rows), ", ".join("tier %d x%d" % (k, v) for k, v in sorted(counts.items()))))
    else:
        print(md)


if __name__ == "__main__":
    main()

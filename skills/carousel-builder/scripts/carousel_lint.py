#!/usr/bin/env python3
"""Check carousel slide copy (slides.json) before it is rendered.

  python3 carousel_lint.py slides.json
  python3 carousel_lint.py slides.json --json
  python3 carousel_lint.py --init value-stack > slides.json

Frameworks and their slide ranges (references/frameworks.md):
  value-stack 4-14, problem-proof 6-10, hack-list 6-10,
  rant-callout 4-8, demo-walkthrough 3-11

  FAIL  slide count outside the framework's range
  FAIL  slide 1 is not role "hook", has body text or a list, or its title
        wraps to more than 3 lines at headline size
  FAIL  a slide body over 150 characters (split it into two slides)
  FAIL  a line break forced mid-sentence (<br> in copy)
  FAIL  the last slide is not role "cta", or it asks for nothing, or it
        only says "follow for more"
  FAIL  framework parts missing: problem-proof needs a "proof" slide with
        an image or a number; hack-list needs "bad" and "good" on every
        hack; rant-callout needs a "pivot" slide; demo-walkthrough needs an
        image on every "step"
  FAIL  engagement bait
  WARN  nothing defines the topic for a cold reader by slide 3
  WARN  no "close" slide right before the CTA
  WARN  over 45 words on a slide, two short slides in a row (merge them),
        size that does not match the platform, hype words, dashes
Exit code 1 if any FAIL. Standard library only.
"""
import argparse
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to a legacy code page

RANGES = {"value-stack": (4, 14), "problem-proof": (6, 10), "hack-list": (6, 10),
          "rant-callout": (4, 8), "demo-walkthrough": (3, 11)}
SIZES = {"instagram": "1080x1350", "linkedin": "1080x1350", "tiktok": "1080x1920", "threads": "1080x1350"}
ROLES = {"hook", "define", "problem", "point", "proof", "hack", "pivot", "step", "close", "cta"}
ASK = re.compile(r"\b(save|comment|follow|send|get|download|reply|dm|subscribe|join|grab|book|try|read|write)\b", re.I)
BAIT = ["follow for more", "like if", "tag a friend", "smash", "you won't believe", "thoughts?", "agree?"]
HYPE = ["unlock", "seamless", "game-changer", "game changer", "supercharge", "revolutionize", "effortless",
        "in today's world", "skyrocket", "secret sauce", "next level"]

INIT = {
    "value-stack": [
        {"role": "hook", "title": "How to [outcome] in [time] without [pain]", "sub": "One line that says who it is for"},
        {"role": "define", "title": "What [the thing] is", "body": "One or two plain sentences."},
        {"role": "point", "kicker": "01", "title": "First point", "body": "Why it matters, one example."},
        {"role": "point", "kicker": "02", "title": "Second point", "body": "Why it matters, one example."},
        {"role": "close", "title": "The one line to remember", "body": "The idea in a sentence."},
        {"role": "cta", "title": "Save this for your next [moment]", "body": "Comment WORD and I will send you [exact deliverable]."},
    ],
}


def wrap_lines(text, chars):
    lines, cur = 0, 0
    for w in text.split():
        if cur == 0:
            cur = len(w)
            lines += 1
        elif cur + 1 + len(w) <= chars:
            cur += 1 + len(w)
        else:
            lines += 1
            cur = len(w)
    return lines


def chars_per_line(px, width=920, ratio=0.56):
    return max(8, int(width / (ratio * px)))


def text_of(s):
    parts = [s.get("title", ""), s.get("sub", ""), s.get("body", ""), s.get("bad", ""), s.get("good", "")]
    parts += s.get("items") or []
    return " ".join(p for p in parts if p)


def lint(deck):
    res = []
    add = lambda level, msg: res.append((level, msg))  # noqa: E731
    fw = deck.get("framework")
    slides = deck.get("slides") or []
    n = len(slides)
    if fw not in RANGES:
        add("FAIL", "framework %r unknown; use %s" % (fw, ", ".join(RANGES)))
    else:
        lo, hi = RANGES[fw]
        add("PASS" if lo <= n <= hi else "FAIL", "%d slides for %s (range %d-%d)" % (n, fw, lo, hi))
    plat = deck.get("platform", "instagram")
    size = deck.get("size") or SIZES.get(plat, "1080x1350")
    if plat in SIZES and size != SIZES[plat]:
        add("WARN", "size %s on %s; native is %s" % (size, plat, SIZES[plat]))
    if not slides:
        return res
    for i, s in enumerate(slides, 1):
        if s.get("role") not in ROLES:
            add("WARN", "slide %d role %r unknown" % (i, s.get("role")))

    # slide 1
    s1 = slides[0]
    width = int(size.split("x")[0]) - 160
    hl = wrap_lines(s1.get("title", ""), chars_per_line(92, width))
    if s1.get("role") != "hook":
        add("FAIL", "slide 1 must be role 'hook'")
    if s1.get("body") or s1.get("items"):
        add("FAIL", "slide 1 carries body text or a list; keep it to the hook and one subline")
    if hl > 3:
        add("FAIL", "slide 1 title wraps to about %d lines at 92px; 3 is the most a thumbnail holds" % hl)
    elif s1.get("title"):
        add("PASS", "slide 1 title about %d line(s): %r" % (hl, s1["title"]))
    if len(s1.get("sub", "")) > 90:
        add("WARN", "slide 1 subline is %d chars; keep it to one line" % len(s1["sub"]))

    # cold reader
    if n >= 3 and not any(s.get("role") in ("define", "problem") for s in slides[1:3]):
        add("WARN", "no 'define' or 'problem' slide by slide 3; a cold reader may not know what this is")

    # per slide
    for i, s in enumerate(slides, 1):
        body = s.get("body", "")
        if len(body) > 150:
            add("FAIL", "slide %d body is %d chars; over 150, split it" % (i, len(body)))
        words = len(re.findall(r"[\w']+", text_of(s)))
        if words > 45:
            add("WARN", "slide %d has %d words; readable in one second means under 45" % (i, words))
        for field in ("title", "sub", "body", "bad", "good"):
            v = s.get(field, "")
            if "<br" in v.lower():
                add("FAIL", "slide %d %s has a forced <br>; let the text wrap" % (i, field))
            for m in re.finditer(r"\n", v):
                if v[:m.start()].rstrip()[-1:] not in ".:!?":
                    add("WARN", "slide %d %s breaks a line mid-sentence" % (i, field))
                    break
        if i > 1 and s.get("role") not in ("hook", "cta"):
            prev = slides[i - 2]
            if prev.get("role") not in ("hook", "cta") and len(text_of(prev)) < 40 and len(text_of(s)) < 40:
                add("WARN", "slides %d and %d are both under 40 chars; merge them" % (i - 1, i))

    # ending
    last = slides[-1]
    lt = text_of(last).lower()
    if last.get("role") != "cta":
        add("FAIL", "last slide must be role 'cta'")
    elif not ASK.search(lt):
        add("FAIL", "CTA slide asks for nothing; name the action and the exact thing they get")
    elif re.fullmatch(r"\s*(follow( me)? for more[.!]?)\s*", lt):
        add("FAIL", "CTA is only 'follow for more'; name the deliverable")
    else:
        add("PASS", "CTA: %r" % text_of(last)[:80])
    if n >= 4 and slides[-2].get("role") != "close":
        add("WARN", "slide %d (before the CTA) is not a 'close'; land the idea before you ask" % (n - 1))

    # framework parts
    roles = [s.get("role") for s in slides]
    if fw == "problem-proof":
        proofs = [s for s in slides if s.get("role") == "proof"]
        ok = [s for s in proofs if s.get("image") or re.search(r"\d", text_of(s))]
        add("PASS" if ok else "FAIL", "problem-proof: %d proof slide(s) with an image or a number" % len(ok))
    if fw == "hack-list":
        hacks = [i for i, s in enumerate(slides, 1) if s.get("role") == "hack"]
        bad = [i for i in hacks if not (slides[i - 1].get("bad") and slides[i - 1].get("good"))]
        if not hacks:
            add("FAIL", "hack-list has no 'hack' slides")
        elif bad:
            add("FAIL", "hack slide(s) %s need both 'bad' and 'good'" % ", ".join(map(str, bad)))
        else:
            add("PASS", "%d hacks, each with bad and good" % len(hacks))
    if fw == "rant-callout":
        add("PASS" if "pivot" in roles else "FAIL", "rant-callout %s a 'pivot' (fairness) slide" % ("has" if "pivot" in roles else "needs"))
    if fw == "demo-walkthrough":
        steps = [i for i, s in enumerate(slides, 1) if s.get("role") == "step"]
        noimg = [i for i in steps if not slides[i - 1].get("image")]
        if noimg:
            add("FAIL", "demo step slide(s) %s have no screenshot ('image')" % ", ".join(map(str, noimg)))
        elif steps:
            add("PASS", "%d steps, each with a screenshot" % len(steps))
        for i in steps:
            if len(re.findall(r"[\w']+", slides[i - 1].get("body", ""))) > 10:
                add("WARN", "demo step %d caption over 10 words" % i)

    alltext = " ".join(text_of(s) for s in slides)
    low = alltext.lower()
    b = [x for x in BAIT if x in low and x != "follow for more"]
    if b:
        add("FAIL", "engagement bait: %s" % ", ".join(b))
    h = [x for x in HYPE if x in low]
    if h:
        add("WARN", "hype words: %s" % ", ".join(h))
    d = alltext.count("—") + alltext.count("–")
    if d:
        add("WARN", "%d em/en dash(es)" % d)
    add("INFO", "%d slides, %d words" % (n, len(re.findall(r"[\w']+", alltext))))
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slides", nargs="?", help="slides.json")
    ap.add_argument("--init", metavar="FRAMEWORK", help="print a starter slides.json (value-stack)")
    ap.add_argument("--json", action="store_true", help="print JSON")
    a = ap.parse_args()
    if a.init:
        print(json.dumps({"framework": "value-stack", "platform": "instagram", "theme": "dark",
                          "footer": "Your Name", "slides": INIT["value-stack"]}, indent=2))
        return
    if not a.slides:
        ap.error("slides.json is required (or --init)")
    with open(a.slides, encoding="utf-8") as f:
        deck = json.load(f)
    res = lint(deck)
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

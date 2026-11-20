#!/usr/bin/env python3
"""Check a set of platform posts written from one source, before anyone sees them.

  python3 post_check.py pieces.md
  python3 post_check.py pieces.md --source source.md --json

pieces.md has one section per piece, headed "## <platform>: <format>":

  ## x: thread           posts separated by a line with only ---
  ## x: link-in-reply    a line starting "Reply:" holds the first reply (the link)
  ## threads: post       ## linkedin: post     ## telegram: post
  ## instagram: caption  ## newsletter: section
  ## tiktok: video-script  beats as "[0-3s] spoken words", plus
                           "ON SCREEN: ..." and "CAPTION: ..." lines

Text inside ``` fences is a note and is ignored.

Per piece:
  FAIL  over the platform's character limit (per post for threads)
  FAIL  a link in the body of an X post (put it in the first reply)
  FAIL  a link in an Instagram or TikTok caption (not clickable there)
  FAIL  engagement bait ("thoughts?", "RT if", "follow for more", ...)
  FAIL  video: first beat ends after 3 s, or the hook has more than
        9 spoken words, or the script runs over --max-seconds at 2.5
        words per second
  FAIL  (with --source) a number that is not in the source text
  WARN  too many hashtags, more than one kind of ask, hook line too long
        for the fold, thread length outside the usual range, hype words,
        em or en dashes
Across pieces:
  FAIL  two pieces share more than 35% of their 3-word phrases (a
        rephrased cross-post, which rankers demote)
  WARN  over 20% shared, or two pieces open with the same three words
Exit code 1 if any FAIL. Standard library only.
"""
import argparse
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to a legacy code page

# platform: (limit per post or piece, hashtag max, fold chars for the hook line or None)
LIMITS = {
    "x": (280, 2, None),
    "threads": (500, 1, None),
    "bluesky": (300, 2, None),
    "linkedin": (3000, 5, 210),
    "instagram": (2200, 5, 125),
    "tiktok": (2200, 5, 100),
    "shorts": (5000, 3, 100),
    "telegram": (4096, 3, None),
    "newsletter": (None, 0, None),
    "reddit": (40000, 0, None),
}
NO_LINK = {"instagram", "tiktok"}
THREAD_RANGE = {"x": (3, 12), "threads": (2, 6), "bluesky": (2, 8)}
BAIT = ["thoughts?", "agree?", "rt if", "like if", "follow for more", "smash that", "drop a comment",
        "comment below", "don't forget to like", "tag a friend", "you won't believe", "let that sink in",
        "read that again", "here's what i learned", "a thread \U0001f9f5", "\U0001f9f5\U0001f447", "who else",
        "like and share", "share if you agree"]
HYPE = ["unlock", "seamless", "game-changer", "game changer", "supercharge", "revolutionize", "effortless",
        "in today's world", "skyrocket", "next level", "secret sauce", "mind-blowing", "insane results"]
ASKS = {
    "comment": r"\bcomment\b",
    "follow": r"\bfollow\b",
    "subscribe": r"\bsubscribe\b",
    "link": r"\blink in (bio|the first reply|comments)\b|\bclick\b",
    "dm": r"\bdm me\b|\bsend me a dm\b",
    "save": r"\bsave this\b|\bsave it\b",
    "share": r"\bshare (this|it)\b|\brepost\b",
    "reply": r"\breply with\b",
}
URL = re.compile(r"https?://\S+|\b[a-z0-9-]+\.(com|io|co|org|net|dev|app)/\S*", re.I)
BEAT = re.compile(r"^\[(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*s\]\s*(.*)$")
NUM = re.compile(r"(?<![\w/])\$?\d[\d,]*(?:\.\d+)?%?")


def strip_fences(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


def parse(md):
    pieces, cur = [], None
    for line in strip_fences(md).splitlines():
        m = re.match(r"^##\s+([a-z]+)\s*:\s*(.+?)\s*$", line, re.I)
        if m:
            cur = {"platform": m.group(1).lower(), "format": m.group(2).lower(), "lines": []}
            pieces.append(cur)
        elif cur is not None and not line.startswith("# "):
            cur["lines"].append(line)
    for p in pieces:
        body = "\n".join(p["lines"]).strip()
        p["reply"] = "\n".join(l[6:].strip() for l in p["lines"] if l.startswith("Reply:"))
        body = "\n".join(l for l in body.splitlines() if not l.startswith("Reply:")).strip()
        p["body"] = body
        p["posts"] = [x.strip() for x in re.split(r"^\s*---\s*$", body, flags=re.M) if x.strip()]
    return pieces


def xlen(text):
    return len(URL.sub("x" * 23, text))


def shingles(text):
    w = re.findall(r"[a-z0-9']+", text.lower())
    return {" ".join(w[i:i + 3]) for i in range(len(w) - 2)}


def spoken(p):
    beats, other = [], []
    for line in p["body"].splitlines():
        m = BEAT.match(line.strip())
        if m:
            beats.append((float(m.group(1)), float(m.group(2)), m.group(3)))
        elif beats and line.strip() and not re.match(r"^(ON SCREEN|CAPTION|SHOT|B-ROLL)\s*:", line.strip(), re.I):
            beats[-1] = (beats[-1][0], beats[-1][1], beats[-1][2] + " " + line.strip())
        else:
            other.append(line)
    return beats, other


def caption_of(p):
    caps = [l.split(":", 1)[1].strip() for l in p["body"].splitlines() if re.match(r"^\s*CAPTION\s*:", l, re.I)]
    return "\n".join(caps)


def check_piece(p, add, source_nums, max_seconds):
    name = "%s: %s" % (p["platform"], p["format"])
    plat = p["platform"]
    if plat not in LIMITS:
        add("WARN", "%s: unknown platform, only generic checks run" % name)
    limit, tags_max, fold = LIMITS.get(plat, (None, 3, None))
    is_video = "script" in p["format"]
    text = p["body"]
    low = text.lower()

    if is_video:
        beats, _ = spoken(p)
        if not beats:
            add("FAIL", "%s: no timed beats like '[0-3s] ...'" % name)
        else:
            s0, e0, hook = beats[0]
            hw = len(re.findall(r"[\w']+", hook))
            if e0 > 3:
                add("FAIL", "%s: first beat ends at %gs; the hook must land by 3s" % (name, e0))
            if hw > 9:
                add("FAIL", "%s: hook has %d spoken words; 9 is the most you can say in 3s" % (name, hw))
            if e0 <= 3 and hw <= 9:
                add("PASS", "%s: hook lands in %gs with %d words" % (name, e0, hw))
            words = sum(len(re.findall(r"[\w']+", b[2])) for b in beats)
            est = words / 2.5
            if est > max_seconds:
                add("FAIL", "%s: %d spoken words is about %ds, over %ds" % (name, words, est, max_seconds))
            else:
                add("PASS", "%s: about %ds spoken (%d words)" % (name, est, words))
            if est > beats[-1][1] + 5:
                add("WARN", "%s: timestamps end at %gs but the words need about %ds" % (name, beats[-1][1], est))
        overlays = [l.split(":", 1)[1].strip() for l in text.splitlines() if re.match(r"^\s*ON SCREEN\s*:", l, re.I)]
        for o in overlays:
            if len(o.split()) > 6:
                add("WARN", "%s: on-screen text over 6 words: %r" % (name, o))
        cap = caption_of(p)
        if cap and limit and len(cap) > limit:
            add("FAIL", "%s: caption %d chars, limit %d" % (name, len(cap), limit))
        if cap and plat in NO_LINK and URL.search(cap):
            add("FAIL", "%s: link in the caption is not clickable on %s" % (name, plat))
    else:
        posts = p["posts"] if plat in THREAD_RANGE or plat == "threads" else [text]
        if plat in THREAD_RANGE and ("thread" in p["format"]):
            lo, hi = THREAD_RANGE[plat]
            if not lo <= len(posts) <= hi:
                add("WARN", "%s: %d posts, usual range %d-%d" % (name, len(posts), lo, hi))
            for i, post in enumerate(posts[1:], 2):
                if re.match(r"^(and|but also|also|so|this)\b", post, re.I):
                    add("WARN", "%s: post %d leans on the one before (%r); each post must stand alone" % (name, i, post[:25]))
        over = []
        for i, post in enumerate(posts, 1):
            n = xlen(post) if plat == "x" else len(post)
            if limit and n > limit:
                over.append("post %d is %d chars" % (i, n) if len(posts) > 1 else "%d chars" % n)
        if over:
            add("FAIL", "%s: over the %d limit: %s" % (name, limit, "; ".join(over)))
        elif limit:
            add("PASS", "%s: within %d chars%s" % (name, limit, " per post" if len(posts) > 1 else ""))
        if plat == "x" and URL.search(text):
            add("FAIL", "%s: link in the post body costs reach on X; move it to a 'Reply:' line" % name)
        if p["format"] == "link-in-reply" and not URL.search(p["reply"]):
            add("FAIL", "%s: link-in-reply piece has no link in its 'Reply:' line" % name)
        if plat in NO_LINK and URL.search(text):
            add("FAIL", "%s: link is not clickable on %s; say where the link is instead" % (name, plat))
        if fold:
            first = text.splitlines()[0] if text else ""
            if len(first) > fold:
                add("WARN", "%s: first line is %d chars; only about %d show before 'more'" % (name, len(first), fold))
        if plat in ("telegram", "newsletter") and len(URL.findall(text)) > 2:
            add("WARN", "%s: %d links; give one clear next step" % (name, len(URL.findall(text))))

    tags = re.findall(r"(?<!\w)#\w+", strip_fences(text))
    if len(tags) > tags_max:
        add("WARN", "%s: %d hashtags, keep to %d" % (name, len(tags), tags_max))
    bait = [b for b in BAIT if b in low]
    if bait:
        add("FAIL", "%s: engagement bait: %s" % (name, ", ".join(bait)))
    kinds = [k for k, rx in ASKS.items() if re.search(rx, low)]
    if len(kinds) > 1:
        add("WARN", "%s: %d kinds of ask (%s); keep one" % (name, len(kinds), ", ".join(kinds)))
    hype = [h for h in HYPE if h in low]
    if hype:
        add("WARN", "%s: hype words: %s" % (name, ", ".join(hype)))
    d = text.count("—") + text.count("–")
    if d:
        add("WARN", "%s: %d em/en dash(es)" % (name, d))
    if source_nums is not None:
        body = re.sub(r"\[\d+(?:\.\d+)?\s*-\s*\d+(?:\.\d+)?\s*s\]", " ", text)
        body = re.sub(r"(?m)^\s*\d+/\s*", " ", body)
        body = URL.sub(" ", body)
        missing = sorted({n for n in (x.replace(",", "").lstrip("$").rstrip("%").rstrip(".") for x in NUM.findall(body))
                          if n and n not in source_nums})
        if missing:
            add("FAIL", "%s: numbers not in the source: %s (cite them or cut them)" % (name, ", ".join(missing)))


def check(md, source_text=None, max_seconds=60):
    res = []
    add = lambda level, msg: res.append((level, msg))  # noqa: E731
    pieces = parse(md)
    if not pieces:
        add("FAIL", "no '## platform: format' sections found")
        return res
    nums = None
    if source_text is not None:
        nums = {x.replace(",", "").lstrip("$").rstrip("%").rstrip(".") for x in NUM.findall(source_text)}
    for p in pieces:
        check_piece(p, add, nums, max_seconds)
    sh = [(p, shingles(p["body"])) for p in pieces]
    worst = 0.0
    for i in range(len(sh)):
        for j in range(i + 1, len(sh)):
            a, b = sh[i][1], sh[j][1]
            if not a or not b:
                continue
            jac = len(a & b) / float(len(a | b))
            worst = max(worst, jac)
            pair = "%s:%s and %s:%s" % (sh[i][0]["platform"], sh[i][0]["format"], sh[j][0]["platform"], sh[j][0]["format"])
            if jac > 0.35:
                add("FAIL", "%s share %d%% of their phrases: a rephrased cross-post. Rewrite one from the atom" % (pair, jac * 100))
            elif jac > 0.20:
                add("WARN", "%s share %d%% of their phrases" % (pair, jac * 100))
    if len(sh) > 1:
        add("INFO", "highest phrase overlap between two pieces: %d%%" % (worst * 100))
    opens = {}
    for p in pieces:
        first = " ".join(re.findall(r"[a-z0-9']+", p["body"].lower())[:3])
        if first:
            opens.setdefault(first, []).append("%s:%s" % (p["platform"], p["format"]))
    for o, names in opens.items():
        if len(names) > 1:
            add("WARN", "%s all open with %r; vary the hook" % (", ".join(names), o))
    add("INFO", "%d piece(s) checked" % len(pieces))
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pieces", help="pieces.md")
    ap.add_argument("--source", help="source text; every number in the posts must appear in it")
    ap.add_argument("--max-seconds", type=int, default=60, help="longest allowed video script (default 60)")
    ap.add_argument("--json", action="store_true", help="print JSON")
    a = ap.parse_args()
    with open(a.pieces, encoding="utf-8") as f:
        md = f.read()
    src = None
    if a.source:
        with open(a.source, encoding="utf-8") as f:
            src = f.read()
    res = check(md, src, a.max_seconds)
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

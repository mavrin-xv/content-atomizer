#!/usr/bin/env python3
"""Render slides.json to one HTML file, and optionally to PNG slides or a PDF.

  python3 render_carousel.py slides.json -o carousel.html
  python3 render_carousel.py slides.json -o carousel.html --png out/
  python3 render_carousel.py slides.json -o carousel.html --pdf carousel.pdf
  python3 render_carousel.py slides.json -o carousel.html --theme light --accent "#2f6f4f"

Themes: dark, light, editorial (white, numbered, serif headlines),
paper (warm off-white, handwritten-style headline font if installed).
Sizes come from the platform: 1080x1350 (Instagram, LinkedIn, Threads),
1080x1920 (TikTok). Override with "size" in slides.json.

The HTML opens in any browser as a scrollable preview. --png and --pdf need
the Playwright package for Python and its Chromium:
  pip install playwright && python3 -m playwright install chromium
PNG files are named 01.png, 02.png, ... at full size. The PDF has one page
per slide, which is the format LinkedIn uses for document posts.
Copy is HTML-escaped. Titles keep their last two words together so no
headline ends on one orphan word. Standard library only for the HTML.
"""
import argparse
import html
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to a legacy code page

SIZES = {"instagram": "1080x1350", "linkedin": "1080x1350", "threads": "1080x1350", "tiktok": "1080x1920"}
THEMES = {
    "dark": {"bg": "#111214", "fg": "#f4f4f2", "muted": "#a3a3a0", "accent": "#4cc9f0", "line": "#2a2b2f",
             "head": "Inter, 'Helvetica Neue', Arial, sans-serif", "body": "Inter, 'Helvetica Neue', Arial, sans-serif"},
    "light": {"bg": "#ffffff", "fg": "#141414", "muted": "#5f6368", "accent": "#1d6fe0", "line": "#e6e6e6",
              "head": "Inter, 'Helvetica Neue', Arial, sans-serif", "body": "Inter, 'Helvetica Neue', Arial, sans-serif"},
    "editorial": {"bg": "#fbfaf7", "fg": "#151515", "muted": "#66625b", "accent": "#c2410c", "line": "#e7e2d8",
                  "head": "Georgia, 'Times New Roman', serif", "body": "Inter, 'Helvetica Neue', Arial, sans-serif"},
    "paper": {"bg": "#f6f1e7", "fg": "#2b2620", "muted": "#6e665a", "accent": "#b4442a", "line": "#ddd3c1",
              "head": "'Patrick Hand', 'Segoe Print', 'Comic Neue', cursive", "body": "'Patrick Hand', 'Segoe Print', Georgia, serif"},
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{background:#777;font-family:var(--body);padding:24px;display:flex;flex-direction:column;align-items:center;gap:24px}
body.print{background:var(--bg);padding:0;gap:0}
.slide{width:var(--w);height:var(--h);background:var(--bg);color:var(--fg);position:relative;overflow:hidden;
  display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:120px 80px 140px}
body:not(.print) .slide{zoom:var(--zoom)}
.kicker{font:700 40px var(--body);color:var(--accent);letter-spacing:.04em;margin-bottom:28px}
h1,h2{font-family:var(--head);font-weight:800;line-height:1.05;text-wrap:balance;max-width:920px}
h1{font-size:104px}
h2{font-size:92px;margin-bottom:36px}
.sub{font-size:44px;color:var(--muted);margin-top:36px;max-width:900px;text-wrap:balance;line-height:1.25}
.body{font-size:44px;line-height:1.3;max-width:900px;text-wrap:pretty}
ul{list-style:none;font-size:42px;line-height:1.3;max-width:900px;text-align:left;margin-top:12px}
li{padding:14px 0;border-bottom:3px solid var(--line)}
li:last-child{border-bottom:0}
li::before{content:"\\2192\\00a0";color:var(--accent);font-weight:700}
.pair{width:100%;max-width:900px;text-align:left;font-size:40px;line-height:1.3}
.pair p{padding:22px 0}
.pair b{display:block;font-size:30px;letter-spacing:.06em;text-transform:uppercase;margin-bottom:8px}
.pair .bad b{color:var(--muted)}
.pair .good b{color:var(--accent)}
.pair .bad{border-bottom:3px solid var(--line);color:var(--muted)}
img{max-width:900px;max-height:620px;border-radius:18px;margin-top:28px;object-fit:contain}
.hl{color:var(--accent);white-space:nowrap}
.foot{position:absolute;left:80px;right:80px;bottom:56px;display:flex;justify-content:space-between;
  font:500 30px var(--body);color:var(--muted)}
.swipe{position:absolute;right:80px;bottom:110px;font:700 32px var(--body);color:var(--accent)}
.cta h2{color:var(--accent)}
"""

FIT_JS = """
document.querySelectorAll('.slide').forEach(function(s){
  var t=s.querySelector('h1,h2'); if(!t) return;
  var size=parseFloat(getComputedStyle(t).fontSize), min=72;
  while(s.scrollHeight>s.clientHeight && size>min){size-=4; t.style.fontSize=size+'px';}
});
"""


def esc(s):
    """Escape, then turn **word** into an accent highlight."""
    out = html.escape(s or "")
    parts = out.split("**")
    return "".join(('<span class="hl">%s</span>' % p) if i % 2 else p for i, p in enumerate(parts))


def keep_tail(s):
    words = (s or "").rsplit(" ", 1)
    return words[0] + " " + words[1] if len(words) == 2 and len(words[1]) < 12 else (s or "")


def slide_html(s, i, n, footer, base):
    role = s.get("role", "point")
    out = ['<section class="slide %s">' % html.escape(role)]
    if s.get("kicker"):
        out.append('<div class="kicker">%s</div>' % esc(s["kicker"]))
    tag = "h1" if i == 1 else "h2"
    if s.get("title"):
        out.append("<%s>%s</%s>" % (tag, esc(keep_tail(s["title"])), tag))
    if s.get("sub"):
        out.append('<p class="sub">%s</p>' % esc(s["sub"]))
    if s.get("body"):
        out.append('<p class="body">%s</p>' % esc(s["body"]))
    if s.get("items"):
        out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % esc(x) for x in s["items"]))
    if s.get("bad") or s.get("good"):
        out.append('<div class="pair"><p class="bad"><b>%s</b>%s</p><p class="good"><b>%s</b>%s</p></div>' % (
            esc(s.get("bad_label", "Instead of")), esc(s.get("bad", "")), esc(s.get("good_label", "Do this")), esc(s.get("good", ""))))
    if s.get("image"):
        src = s["image"]
        if not src.startswith(("http://", "https://", "data:")):
            src = os.path.relpath(os.path.join(base, src), base).replace(os.sep, "/")
        out.append('<img src="%s" alt="%s">' % (html.escape(src), html.escape(s.get("alt", ""))))
    if i == 1 and n > 1:
        out.append('<div class="swipe">%s →</div>' % esc(s.get("swipe", "Swipe")))
    out.append('<div class="foot"><span>%s</span><span>%d/%d</span></div>' % (esc(footer), i, n))
    out.append("</section>")
    return "".join(out)


def render(deck, base, theme=None, accent=None, print_mode=False):
    plat = deck.get("platform", "instagram")
    w, h = (deck.get("size") or SIZES.get(plat, "1080x1350")).split("x")
    t = dict(THEMES.get(theme or deck.get("theme", "dark"), THEMES["dark"]))
    if accent or deck.get("accent"):
        t["accent"] = accent or deck["accent"]
    slides = deck.get("slides") or []
    n = len(slides)
    vars_ = ";".join("--%s:%s" % (k, v) for k, v in t.items())
    vars_ += ";--w:%spx;--h:%spx;--zoom:%s" % (w, h, "0.4")
    body = "".join(slide_html(s, i, n, deck.get("footer", ""), base) for i, s in enumerate(slides, 1))
    return ("<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width\">"
            "<title>%s</title><style>:root{%s}%s</style></head><body class=\"%s\">%s<script>%s</script></body></html>") % (
        html.escape((slides[0].get("title") if slides else "carousel") or "carousel"), vars_, CSS,
        "print" if print_mode else "", body, FIT_JS)


def export(deck, base, out_html, png_dir=None, pdf=None, theme=None, accent=None):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("--png/--pdf need Playwright: pip install playwright && python3 -m playwright install chromium")
    plat = deck.get("platform", "instagram")
    w, h = [int(x) for x in (deck.get("size") or SIZES.get(plat, "1080x1350")).split("x")]
    tmp = out_html + ".print.html"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(render(deck, base, theme, accent, print_mode=True))
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            page = b.new_page(viewport={"width": w, "height": h})
            page.goto("file:///" + os.path.abspath(tmp).replace(os.sep, "/"))
            page.wait_for_timeout(300)
            if png_dir:
                os.makedirs(png_dir, exist_ok=True)
                for i, el in enumerate(page.query_selector_all(".slide"), 1):
                    path = os.path.join(png_dir, "%02d.png" % i)
                    el.screenshot(path=path)
                    print("wrote %s" % path)
            if pdf:
                page.pdf(path=pdf, width="%dpx" % w, height="%dpx" % h, print_background=True)
                print("wrote %s" % pdf)
            b.close()
    finally:
        os.remove(tmp)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slides", help="slides.json")
    ap.add_argument("-o", "--out", default="carousel.html", help="HTML preview to write")
    ap.add_argument("--theme", choices=sorted(THEMES), help="override the theme in slides.json")
    ap.add_argument("--accent", help="accent colour, e.g. '#2f6f4f'")
    ap.add_argument("--png", metavar="DIR", help="also write one PNG per slide (needs Playwright)")
    ap.add_argument("--pdf", metavar="FILE", help="also write a PDF, one page per slide (needs Playwright)")
    a = ap.parse_args()
    with open(a.slides, encoding="utf-8") as f:
        deck = json.load(f)
    base = os.path.dirname(os.path.abspath(a.out))
    src_base = os.path.dirname(os.path.abspath(a.slides))
    for s in deck.get("slides") or []:
        if s.get("image") and not s["image"].startswith(("http://", "https://", "data:")):
            s["image"] = os.path.relpath(os.path.join(src_base, s["image"]), base)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(render(deck, base, a.theme, a.accent))
    print("wrote %s (%d slides)" % (a.out, len(deck.get("slides") or [])))
    if a.png or a.pdf:
        export(deck, base, a.out, a.png, a.pdf, a.theme, a.accent)


if __name__ == "__main__":
    main()

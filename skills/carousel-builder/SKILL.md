---
name: carousel-builder
description: Builds swipe carousels for Instagram, LinkedIn, Threads and TikTok photo mode from one idea - picks one of five frameworks (value-stack, problem-proof, hack-list, rant-callout, demo-walkthrough), writes slide copy as slides.json, lints it against slide rules (hook-only first slide that fits in 3 lines, 150-character body limit, a definition by slide 3, a close and a specific CTA, the parts each framework needs), renders it to HTML and to PNG slides or a PDF with neutral themes, and runs a visual QA loop with a blind read. Use when the user says "make a carousel", "turn this into slides", "Instagram carousel", "LinkedIn document post", "swipe post", "carousel from this article", or after atomize-plan picks a carousel.
---

# Carousel builder

A carousel is read one slide at a time, on a phone, in about a second each. Most fail on slide 1 (a paragraph instead of a promise) or on the last slide (no ask). This skill picks a structure, writes copy that survives a one-second read, renders the slides and checks them with eyes, not just with a script.

## Inputs

- The atoms for the carousel from `atoms/<slug>/plan.json`, or one idea from the person.
- The platform, which sets the size: 1080x1350 for Instagram, LinkedIn and Threads, 1080x1920 for TikTok.
- Optional: an accent color, a footer name, images for proof or demo slides.

## Procedure

1. **Pick the framework** with [references/frameworks.md](references/frameworks.md). Swaps are a hack-list, evidence-heavy claims are problem-proof, screenshots are a demo-walkthrough, arguments are a rant-callout, everything else is a value-stack.
2. **Write slides.json** in `atoms/<slug>/` (start from `templates/slides.example.json` or `python3 scripts/carousel_lint.py --init value-stack`). Follow [references/slide-rules.md](references/slide-rules.md): hook-only slide 1, one idea per slide, a close, then a CTA that names what the reader gets.
3. **Lint:**
   ```
   python3 scripts/carousel_lint.py atoms/<slug>/slides.json
   ```
   Fix every FAIL before rendering.
4. **Render:**
   ```
   python3 scripts/render_carousel.py atoms/<slug>/slides.json -o atoms/<slug>/carousel.html --png atoms/<slug>/png
   ```
   `--pdf file.pdf` makes a LinkedIn document. `--theme dark|light|editorial|paper` and `--accent "#hex"` set the look ([references/design-rules.md](references/design-rules.md)). PNG and PDF need Playwright for Python; without it you get the HTML preview and can screenshot it.
5. **Run the QA loop** in [references/qa-loop.md](references/qa-loop.md): look at every PNG against the visual checklist, then do a blind read with someone (or a fresh session) who sees only the images. Fix slides.json and render again. Three rounds at most.
6. **Write the caption** with platform-writer (`## instagram: caption`), so the caption is checked with the other pieces.

## Hard rules

- Slide 1 is the hook and nothing else.
- Every number on a slide is in the source.
- The last slide asks for one thing and says what the reader gets. "Follow for more" alone fails.
- Fix copy in slides.json, never in the generated HTML.
- Look at the rendered slides before calling it done. The linter cannot see a broken line or a cramped slide.
- This skill renders files. It never posts.

## Output

`atoms/<slug>/slides.json`, `carousel.html`, and PNG slides or a PDF, with the QA checklist passed.

## Files

- [references/frameworks.md](references/frameworks.md): the five frameworks with slide maps
- [references/slide-rules.md](references/slide-rules.md): copy rules and the slides.json format
- [references/design-rules.md](references/design-rules.md): themes, sizes, contrast
- [references/qa-loop.md](references/qa-loop.md): visual checklist and blind read
- `scripts/carousel_lint.py`: copy linter (`--help`)
- `scripts/render_carousel.py`: HTML, PNG and PDF renderer (`--help`)

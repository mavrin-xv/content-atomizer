# Slide rules

A carousel is read one slide at a time, on a phone, in about a second per slide. Every rule here comes from that.

## Slide 1

- Hook only. A title and at most one short subline (90 characters or fewer). No body text, no list. `carousel_lint.py` fails a body or list on slide 1.
- The title wraps to three lines or fewer at headline size. If it does not fit, it is two ideas.
- It promises something specific: a number, an outcome, a named mistake. "Some thoughts on bookkeeping" promises nothing.
- Highlight the one or two words that carry the promise with `**double asterisks**`. The renderer colors them and keeps them on one line.

## Slide 2

A cold reader who swiped once needs to know what this is about and whether it is for them. Use a `define` or `problem` slide by slide 3; the linter warns when there is none.

## Middle slides

- One idea per slide. A body over 150 characters fails; split it into two slides.
- Under 45 words per slide, or the reader stops swiping.
- No forced line breaks (`<br>`). Let the text wrap. The renderer balances lines and keeps the last two words together so no word sits alone on the last line.
- Two very short slides in a row (under 40 characters each) should be one slide.
- Number the points in the title ("3. Close on a calendar") so the reader knows where they are.

## The last two slides

- The second to last is a `close`: what the points add up to, or what they do not fix. Honest limits belong here.
- The last slide is a `cta` that asks for one specific action and names what the reader gets. "Save this for month end" or "Try the 10-minute match for two weeks" pass. "Follow for more" alone fails.

## Copy

- Plain words. The hype list in the linter warns on "unlock", "game-changer" and similar.
- No dashes as punctuation; the linter warns.
- Numbers as digits on slides.
- Every number traces to the source. Run `post_check.py --source` on the caption, and read the slides against the source yourself.

## slides.json

```json
{
  "framework": "hack-list",
  "platform": "instagram",
  "theme": "editorial",
  "footer": "Northwind Books",
  "slides": [
    {"role": "hook", "title": "Close the month in **3 days**, not 9", "sub": "Four habits. No software."},
    {"role": "problem", "title": "Why month end takes 9 days", "body": "One or two lines."},
    {"role": "hack", "title": "1. Reconcile every morning", "bad": "One big match at month end", "good": "10 minutes a day"},
    {"role": "close", "title": "...", "body": "..."},
    {"role": "cta", "title": "Start with the 10 minutes", "body": "Save this for month end."}
  ]
}
```

Roles: hook, define, problem, point, proof, hack, pivot, step, close, cta. Optional fields: `kicker` (a small label above the title, like "01"), `sub`, `body`, `items` (a short list), `bad`, `good`, `image` (a path relative to slides.json). Deck fields: `platform` sets the size (instagram, linkedin and threads 1080x1350, tiktok 1080x1920), or set `size` yourself; `theme` and `accent` set the look.

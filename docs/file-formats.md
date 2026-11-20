# File formats

Every file the scripts read is plain text. Start from the files in `templates/` or the `--init` options.

## plan.json

Written by atomize-plan, read by `plan_check.py`. Fields: `source` (`title`, `path` relative to plan.json), `core_insight`, `wide` (true only when a full fan-out was asked for) with an optional `wide_reason`, `atoms` (`id`, `kind`, `text`, `evidence`) and `platforms` (`platform`, `treatment`, `format`, `atoms`, `hook_type`, `why`, optional `pieces`). Full description in the atomize-plan skill, `references/extraction.md`. Starter: `templates/plan.example.json`.

## pieces.md

Written by platform-writer, read by `post_check.py`.

- One section per piece: `## <platform>: <format>`, for example `## x: thread`.
- Threads: `---` on its own line between posts. A line starting `Reply:` is the first reply, where links go.
- Video scripts: lines starting with a time range like `[0-3s]` are spoken; `ON SCREEN:` and `CAPTION:` lines are not counted as speech.
- Anything inside a code fence is ignored, so notes and scores can live there.

Starter: `templates/pieces.md`.

## slides.json

Written by carousel-builder, read by `carousel_lint.py` and `render_carousel.py`. Deck fields: `framework`, `platform`, `theme`, `footer`, `accent`, `size`. Slide fields: `role`, `title`, `kicker`, `sub`, `body`, `items`, `bad`, `good`, `image`. Wrap a word or two in `**double asterisks**` to color them with the accent. Full rules in the carousel-builder skill, `references/slide-rules.md`. Starter: `templates/slides.example.json`.

## hooks.csv

Read and written by `hook_bank.py`. Columns: `date` (YYYY-MM-DD), `source` (own or a note on where it came from), `platform`, `hook_type` (one of nine ids), `hook`, `pattern`, `why`, `metric`, `value` (a number or empty). Starter: `templates/hooks.csv`.

## comments.txt

Read by `triage_replies.py`. One comment per line as `author: text`. A line that starts with spaces continues the comment above. Blank lines are ignored.

## replies.md

Written by `triage_replies.py`, then edited by hand, then checked with `--check`. Each comment is a `## ` heading with its tier and flags, a quote, a `Why:` line and a `Draft:` line. Keep the headings as they are; the check reads them.

## brief.md

Optional, read by people and the model, not by scripts: who you are, which accounts are active, voice, asks and limits. Starter: `templates/brief.md`.

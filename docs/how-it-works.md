# How it works

The pack splits repurposing into a plan, the writing, and the follow-up, with a script checking each step. The model makes the judgement calls. The scripts count things, so the same mistake is caught every time.

## 1. Plan before writing (atomize-plan)

The source goes into `atoms/<slug>/source.md`. The model writes one core insight and pulls atoms: data points, stories, frameworks, contrarian takes, quotable lines. Each atom carries an exact quote from the source as evidence.

Then it picks a treatment per platform:

- **native-deep**: the full idea rebuilt for the platform (a thread, a long Telegram post, a carousel).
- **native-light**: one atom, one short post.
- **link-in-reply**: a short post with the value in it, and the link in the first reply.
- **skip**: with a reason. Most plans skip something.

The default budget is 2 to 3 platforms and 3 to 6 pieces. A wide fan-out has to be asked for. A thin source (under about 500 words or fewer than three atoms) gets three pieces at most.

`plan_check.py` reads plan.json and the source. It fails a plan when an atom's evidence is not in the source, a skip has no reason, a platform gets a format it does not have, the budget is blown on a thin source, or the platform facts file is past its verify date. It warns when two platforms share a hook type.

## 2. Write each piece for its room (platform-writer, carousel-builder)

platform-writer writes `pieces.md`, one section per piece. Each platform gets its own reader line, angle and hook type from the plan. The X piece keeps the link out of the body. The Telegram or newsletter piece is the full version with caveats. The video script has a spoken hook in the first 3 seconds, timed beats, on-screen text and a caption.

`post_check.py` checks limits per platform, link rules, the 3-second hook, spoken length, bait and hype words, phrase overlap between pieces, and any digit in a piece that is not in the source. Then the model scores each piece on hook, native fit, substance, voice and ask, and ships at an average of 8 with nothing under 7.

carousel-builder picks one of five frameworks, writes `slides.json`, lints it with `carousel_lint.py`, renders it with `render_carousel.py` to HTML and PNG or PDF, and then looks at the images. A blind read by someone who sees only the slides is the last check.

## 3. Learn from the results (hook-library, reply-triage)

hook-library keeps `hooks.csv`: your first lines with a type, a slot pattern and one metric. `hook_bank.py patterns` ranks frames used three or more times by median result. Those frames are the ones to reuse.

reply-triage ranks the comments on a live post into six tiers, flags the ones that need a person (price, refund, dates, legal), and checks the drafts before anyone posts them.

## Files in a run

```
atoms/
  hooks.csv              hook-library, shared across sources
  <slug>/
    source.md            the input
    plan.json            atomize-plan
    pieces.md            platform-writer
    slides.json          carousel-builder
    carousel.html, png/  render_carousel.py
    comments.txt         pasted after posting
    replies.md           reply-triage
```

## Why scripts and a model

A model asked to "check the limits" will usually say it did. A script that counts 281 characters will not. The reverse holds for judgement: no script can tell whether a hook is interesting. The pack keeps each half where it is reliable.

## What the scripts do not do

They do not post, schedule, fetch analytics or call any API. `render_carousel.py` uses Playwright, if installed, only to screenshot a local HTML file.

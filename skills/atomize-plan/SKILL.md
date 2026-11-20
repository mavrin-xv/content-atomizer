---
name: atomize-plan
description: Plans how one source (an article, transcript, talk, newsletter or long post) becomes native posts across platforms. Extracts the core insight and the atoms (data, stories, frameworks, contrarian takes, quotable lines) with exact evidence from the source, then decides per platform whether to write a deep native piece, a light one, a link-in-reply post or to skip with a reason, and writes plan.json. A checker verifies every atom's evidence is really in the source, flags weak format fits, thin sources, over-budget plans, repeated hook types and stale platform facts. Use when the user says "atomize this", "repurpose this article", "turn this into posts", "one topic many platforms", "what can I post from this", "content plan from this transcript", or before platform-writer and carousel-builder.
---

# Atomize plan

Most repurposing fails before the writing starts: the same paragraph gets pasted into five apps, or a thin source gets stretched into ten posts that repeat one sentence. This skill decides first what the source actually says, then where each idea fits, and writes that down so the writing skills have a brief.

## Inputs

- The source as text: an article, a transcript, notes from a talk. Save it as `atoms/<slug>/source.md`.
- The platforms the person posts on. Read `templates/brief.md` if they filled it; otherwise ask once, or plan for the platforms they named.
- Whether they want a full fan-out. The default is 2 to 3 platforms and 3 to 6 pieces.

## Procedure

1. **Write the core insight** in one sentence of 30 words or fewer. If the source has no point you can state, say so and stop.
2. **Extract atoms** with [references/extraction.md](references/extraction.md). Each atom gets an id, a kind, your own wording and the exact sentence from the source as `evidence`. Six good atoms beat twelve thin ones.
3. **Judge the source size.** Under about 500 words or fewer than three atoms is thin: plan at most three pieces.
4. **Pick a treatment per platform** with the fit table in [references/idea-shapes.md](references/idea-shapes.md): native-deep, native-light, link-in-reply, or skip with a one-line reason. Skip where the atom fits badly or the account is inactive.
5. **Give each platform its own hook type** from the hook-library skill's type list, so the same source does not open the same way everywhere.
6. **State the plan to the person in 3 to 5 lines** before any writing: which platforms, which atoms, what gets skipped and why. Wait for a yes or a change if they are present.
7. **Write `atoms/<slug>/plan.json`** (start from `templates/plan.example.json` or `python3 scripts/plan_check.py --init`).
8. **Check:**
   ```
   python3 scripts/plan_check.py atoms/<slug>/plan.json
   ```
   Fix every FAIL: evidence not found in the source, a skip with no reason, a format the platform does not have, too many pieces for a thin source, an expired `references/platform-facts.md`. Read the WARN lines and either fix them or say why not.

## Hard rules

- No atom without evidence copied from the source. No numbers the source does not contain.
- Skips are allowed and expected. Never fill a platform just because the account exists.
- A full fan-out only when the person asks; set `"wide": true` and record why.
- Platform facts are hypotheses with a date. When the checker says they expired, re-verify before planning.
- This skill plans. It does not write the posts and never publishes.

## Output

`atoms/<slug>/plan.json`, checked, and a 3 to 5 line summary for the person. Then hand over to platform-writer for posts and scripts and to carousel-builder for carousels.

## Modes

- **Analyze only:** extract atoms and stop. Useful to see what a source can carry before deciding anything.
- **Single platform:** one source, one platform. Still write plan.json with the others skipped, so the next run knows what was used.

## Files

- [references/extraction.md](references/extraction.md): how to pull atoms and the plan.json fields
- [references/idea-shapes.md](references/idea-shapes.md): atom kinds, fit table, budget, the four treatments
- [references/platform-facts.md](references/platform-facts.md): limits and ranking hypotheses with a verify date
- `scripts/plan_check.py`: the checker (`--help` for options)

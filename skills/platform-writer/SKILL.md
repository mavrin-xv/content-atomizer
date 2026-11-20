---
name: platform-writer
description: Writes the native posts from an atomize plan - an X thread or post with the link in the first reply, a Telegram channel or newsletter piece that is the full version, Threads, Bluesky and LinkedIn posts, Instagram captions and short video scripts with timed beats, on-screen text and a caption - each with its own angle and hook for the platform. A checker enforces character limits, link rules per platform, a 3-second spoken hook, spoken length, numbers that trace back to the source, engagement bait and phrase overlap between pieces, then a five-dimension score decides what ships. Use when the user says "write the thread", "write the posts from this plan", "Telegram post from this article", "newsletter version", "TikTok script from this", "LinkedIn post", or after atomize-plan.
---

# Platform writer

A thread, a newsletter and a video script made from one article should read like the same person talking in three rooms. Usually they read like one paragraph cut three ways. This skill writes each piece for its room from the plan, then checks the mechanical rules and scores the rest.

## Inputs

- `atoms/<slug>/plan.json` from atomize-plan. If there is none, run atomize-plan first; writing without a plan is how pieces end up repeating each other.
- `atoms/<slug>/source.md`, for evidence and numbers.
- `templates/brief.md` if filled: voice, words to avoid, where links live.

## Procedure

1. **Read the plan.** Write only the platforms that are not skipped, with the atoms and hook type listed for each.
2. **Say who this reader is** in one line per platform before writing: what they came to that app for.
3. **Write each piece** in `atoms/<slug>/pieces.md` with the shapes in [references/platform-formats.md](references/platform-formats.md). Start from `templates/pieces.md`. One `## <platform>: <format>` section per piece.
   - X: the value in the post, the link in a `Reply:` line. Threads: each post stands alone.
   - Telegram or newsletter: the full version, with the caveats and what it did not fix.
   - Video: `[0-3s]` spoken hook of nine words or fewer, timed beats, `ON SCREEN:` and `CAPTION:` lines. Script only, no production.
4. **Check:**
   ```
   python3 scripts/post_check.py atoms/<slug>/pieces.md --source atoms/<slug>/source.md
   ```
   Fix every FAIL: over a limit, a link in an X body, a clickable link promised on Instagram or TikTok, a hook that lands after 3 seconds, a video longer than `--max-seconds`, a number not in the source, bait, two pieces that overlap too much.
5. **Score** each piece on hook, native fit, substance, voice and ask with [references/quality-gate.md](references/quality-gate.md). Ship at an average of 8 with nothing under 7. Rewrite only the weak dimension, three rounds at most, then go back to the plan.
6. **Run the voice test:** read the shortest and the longest piece side by side. Same opinions, same words for things, different length.
7. **Cut the patterns** in [references/slop-patterns.md](references/slop-patterns.md) that the script cannot see.

## Hard rules

- Every number comes from the source. Spelled-out numbers too; the script only catches digits.
- One ask per piece, and it fits the platform.
- No two platforms open with the same hook type or the same first three words.
- No engagement bait, no fake urgency, no invented testimonials.
- Drafts only. This skill never posts.

## Output

`atoms/<slug>/pieces.md`, checked, with the five scores in a fenced block under each piece. Carousels go to carousel-builder; the Instagram caption for a carousel lives here.

## Files

- [references/platform-formats.md](references/platform-formats.md): per-platform shapes, thread structures, video beat format
- [references/quality-gate.md](references/quality-gate.md): five dimensions, ship bar, rewrite cap
- [references/slop-patterns.md](references/slop-patterns.md): bait, hype and shapes to rewrite
- `scripts/post_check.py`: the checker (`--help` for limits and options)

# Platform formats

Same person, different room. The voice stays yours; the length, the opening and what you ask for change with the room. Before you write a piece, say in one line what this reader came to this platform for.

## pieces.md layout

```
## x: thread
First post text

---
Second post text
Reply: https://example.com/full-article

## telegram: long-post
Full text

## tiktok: video-script
[0-3s] Spoken hook line.
ON SCREEN: short overlay
[3-15s] Next beat.
CAPTION: the caption under the video
```

Each piece starts with `## <platform>: <format>`. In a thread, `---` on its own line separates posts. `Reply:` holds the first reply. Fenced code blocks are ignored by `post_check.py`, so notes to yourself go inside them.

## X

- **Post.** One idea, the value in the post itself. Under 280 characters. No link in the body.
- **Thread.** The first post carries most of the reach, so it has to work alone: the outcome or the tension plus a reason to read on. Each later post makes one point and would make sense if someone saw only that post. Five to eight posts is plenty; end with the one action, not "follow me".
- **Link-in-reply.** A complete native post, then the link in `Reply:`.

Five thread shapes that work for most sources:

| Shape | First post | Body |
|---|---|---|
| Numbered habits | before and after with a number | one habit per post |
| Story | the moment things went wrong | what happened, what changed, the lesson |
| Myth list | the belief most people hold | one myth per post with the evidence |
| Teardown | "I looked at X so you do not have to" | one observation per post |
| How-to | the result and the time it takes | one step per post, the last one is the first action |

## Threads and Bluesky

The take, not the lecture. One opinion with one reason, under 500 characters on Threads and 300 on Bluesky. A two or three post mini-thread is the upper limit. Questions at the end should be real questions you want answered.

## LinkedIn

The first two lines are all most people see. Put the outcome or the tension there, not a greeting. Short paragraphs, one idea each. A personal angle (what you did, what you saw) works better than general advice. Links go in the first comment. Three to five hashtags at most, or none.

## Instagram

Visual first. The carousel carries the content (see the carousel-builder skill), the caption carries the hook in its first line and one reason to save it. Links in captions do not click; say where the link is instead.

## TikTok, Reels and Shorts scripts

One idea per video. The format the checker reads:

```
[0-3s] Spoken hook, 9 words or fewer.
ON SCREEN: 2 to 6 words
[3-15s] The problem or the setup.
[15-40s] The one idea, shown or explained.
[40-50s] The close: what to do next.
CAPTION: one or two lines
```

- The spoken hook and the on-screen text land in the first three seconds and say the same thing in different words.
- At about 2.5 spoken words per second, 60 seconds is about 150 words. `post_check.py` estimates the length and fails over `--max-seconds`.
- Write numbers as words when they are spoken ("nine days"), digits when they are on screen ("9 days").
- No production notes about cameras or editing here. This pack stops at the script.

## Telegram channel and newsletter

The full version. Readers already chose you, so this is where the reasoning, the caveats and the "what it did not fix" part go. Bold the first words of each point so it can be skimmed. One ask at the end, and make it specific: try X for two weeks, reply with Y.

## Reddit

Community first. Read the subreddit's rules, write for that community's question, and do not link your own site unless the rules allow it. Most sources should skip Reddit unless you already take part there.

## The voice test

Read the X post and the newsletter piece side by side. They should sound like the same person in two rooms: same opinions, same words for things, different length and pace. If one sounds like a press release and the other like a friend, rewrite the press release.

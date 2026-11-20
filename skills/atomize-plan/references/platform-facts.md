---
last_verified: 2026-11-20
ttl_days: 90
---

# Platform facts

Every line here is a working assumption, not a law. Platforms change ranking without notice. `plan_check.py` fails when `last_verified + ttl_days` is in the past, so somebody re-reads this file at least once a quarter. When you verify a fact, update the date; when you cannot verify it, mark it "unverified" instead of deleting it.

## Limits used by the checkers

| Platform | Post length | Notes |
|---|---|---|
| X | 280 characters per post on a free account, a link counts as 23 | long posts exist on paid accounts |
| Threads | 500 characters | |
| Bluesky | 300 characters | |
| LinkedIn | 3000 characters | about 210 characters show before "see more" |
| Instagram caption | 2200 characters | about 125 characters show before "more" |
| TikTok caption | 2200 characters | |
| YouTube Shorts description | 5000 characters | |
| Telegram post | 4096 characters with no media, 1024 as a media caption | |

Sources: each platform's help pages. Check them when you update `last_verified`.

## Ranking signals (hypotheses)

**X.** In 2023 X published the weights of its home timeline ranker in the `twitter/the-algorithm-ml` repository (`projects/home/recap/README.md`). In that snapshot a like counted 0.5, a repost 1.0, a reply 13.5, a profile click that led to engagement 12.0, a reply that the author engaged with 75.0, and negative feedback -74.0, a report -369.0. The working takeaway: replies, especially conversations the author joins, were worth far more than likes, and anything that makes people hide the post cost more than any gain. Treat these numbers as a 2023 snapshot. The current ranker may differ.

**X links.** Posts with a link in the body are widely reported to get less reach than posts without one. Put the value in the post and the link in the first reply. This is practitioner consensus, not a published rule.

**LinkedIn.** The first two or three lines decide whether anyone clicks "see more". Practitioners report that external links in the post body reduce reach; the common workaround is the link in the first comment. Unverified by the platform.

**Instagram.** Saves and shares are the signals the platform has publicly said it weighs for reach. Carousels get a second chance in the feed when someone skips the first slide, according to practitioner reports. Links in captions are not clickable.

**TikTok and Shorts.** Watch time and completion dominate. The first two to three seconds decide whether someone stays, so the spoken hook and the on-screen text both land there.

**Threads.** Replies and reposts carry conversation; the platform favours takes over lectures. Unverified.

**Telegram and newsletters.** No ranking feed. Readers already chose you, so the piece can be the full version, with the reasoning and the caveats.

## What to do with this file

Read it when you plan, not when you write. If a decision in the plan depends on a line marked "unverified", say so in the plan's `why` field.

---
name: reply-triage
description: Sorts the comments on a published post into six tiers (questions, disagreement with a reason, shared experience, peers and repeat commenters, praise, skip) so replies go to the ones that start conversations first, flags comments that need a person (price, refunds, dates, guarantees, legal or account questions) and relationship candidates, writes a ranked replies.md with a slot for each draft, then checks the drafts - 1 to 3 sentences, no reply to spam, no promises under a needs-a-person flag, no identical replies, no bait. Use when the user says "help me reply to comments", "triage these replies", "which comments should I answer", "draft replies", "comments on my post", or after a piece from this pack goes live.
---

# Reply triage

The hour after a post goes up is when replies count most, and it usually goes to answering "great post" while a real question waits. This skill ranks the comments, drafts short replies that add something, and stops anything that promises a price or a date in public.

## Inputs

- The comments, pasted or exported, one per line as `author: text`, saved as `atoms/<slug>/comments.txt`. Indented lines continue the comment above.
- Optional: handles of peers or customers you know, for `--known`.
- The post and its source, so replies can add a detail the post did not have.

## Procedure

1. **Rank:**
   ```
   python3 scripts/triage_replies.py atoms/<slug>/comments.txt --known "handle1,handle2" -o atoms/<slug>/replies.md
   ```
2. **Read the ranking** and move rows the keyword rules got wrong: sarcasm, jokes, other languages. The tier rules are in [references/tiers.md](references/tiers.md).
3. **Draft replies** under each `Draft:` line, tier 1 first:
   - Questions: the answer plus one detail from the source.
   - Disagreement: agree with the right part, give your reason, do not try to win.
   - Experience: a specific question about their numbers.
   - Praise: short and varied, or just a like.
   - Tier 6: leave "(no reply)".
   - NEEDS A PERSON: a holding reply with no price, date, percentage or guarantee.
4. **Check:**
   ```
   python3 scripts/triage_replies.py --check atoms/<slug>/replies.md
   ```
   Fix every FAIL.
5. **Hand the list to the person**, with the relationship flags at the bottom as follow or DM candidates.

## Hard rules

- Drafts only. A person reads and posts every reply.
- Never promise a price, date, refund or result in a public reply. Flagged rows go to someone who can commit.
- No reply to tier 6. No arguing with trolls.
- One to three sentences, each reply different.
- Do not quote a commenter in a future post without asking them.

## Output

`atoms/<slug>/replies.md`, ranked, with drafts that pass `--check`, and a short list of people worth a follow-up.

## Files

- [references/tiers.md](references/tiers.md): the six tiers, flags, draft rules, reply windows
- `scripts/triage_replies.py`: ranker and draft checker (`--help`)

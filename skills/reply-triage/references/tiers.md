# Reply tiers

Replies are where a post earns its reach. In X's 2023 ranker a reply that the author engaged with weighed 75, against 0.5 for a like (see `platform-facts.md` in the atomize-plan skill). Reply first to the comments that start a conversation.

## The six tiers

| Tier | Comment | Reply with | Time |
|---|---|---|---|
| 1 question | asks something you can answer | the answer, plus one detail the post did not have | within the first hour |
| 2 disagreement | pushes back with a reason | agree with the part that is right, then your reason, without winning | within the first hour |
| 3 experience | shares their own numbers or story | a specific follow-up question about their numbers | same day |
| 4 peer | someone you know, or a repeat commenter | a real reply, not a thanks | same day |
| 5 praise | "great post", "love this" | short and varied, or a like; never the same text twice | when you have time |
| 6 skip | bait, abuse, spam, link drops, all caps | nothing. Hide or report if the platform allows | none |

`triage_replies.py` assigns tiers with keyword rules. It will misfile sarcasm, jokes and comments in other languages. Read the list and move rows before you write drafts.

## Flags

**NEEDS A PERSON.** Price, refunds, dates, deadlines, guarantees, contracts, legal, tax or medical questions, account problems. The draft is a holding reply that promises nothing: "Good question, I will message you today." A person who can make the commitment answers. `--check` fails a flagged draft that contains a price, a percentage, a guarantee or a weekday deadline.

**RELATIONSHIP.** On your known list, more than one comment on the post, or shared their own data. Note these at the bottom of replies.md. They are candidates for a follow, a DM, or a quote in a future post (ask first).

## Writing a draft

- One to three sentences. `--check` fails at four.
- Add something: a number, a step, a source, a question about their case. "Thanks!" adds nothing.
- Answer the question asked, then stop.
- No links unless they asked for one.
- No bait, no "follow for more".
- Vary the praise replies. Identical drafts fail the check.

## Reply windows

Block 20 to 30 minutes after each post for replies. Same-platform posts at least a day apart, so you are not answering two threads at once. If a post gets more comments than you can answer, answer tiers 1 to 3 and like the rest.

## Never

- Post replies automatically. The pack drafts; a person reads and posts.
- Promise prices, dates or results in a public reply.
- Argue with tier 6.

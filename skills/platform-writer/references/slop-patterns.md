# Patterns to cut

These make a post read as generated or as bait. `post_check.py` fails on the bait list and warns on hype words and dashes. The rest you catch by reading.

## Bait (fails the check)

"let that sink in", "read that again", "you won't believe", "here's what I learned", "agree?", "thoughts?", "who else", "drop a comment", "comment below", "like if", "RT if", "like and share", "share if you agree", "tag a friend", "smash that", "follow for more". Also by hand: "nobody talks about this", "this will change your life", "comment YES to get it" when nothing is sent.

Why it matters: X's 2023 ranker gave negative feedback a weight of -74 against 0.5 for a like (see `platform-facts.md` in atomize-plan). Bait that gets a few cheap likes and a few "show less of this" clicks loses.

## Hype words (warns)

Flagged by the script: unlock, seamless, game-changer, supercharge, revolutionize, effortless, in today's world, skyrocket, next level, secret sauce, mind-blowing, insane results. Catch by hand: ultimate, crush it, powerful, incredible. Replace each with the specific result, or delete it.

## Shapes to rewrite

| Shape | Example | Rewrite as |
|---|---|---|
| "It's not X, it's Y" | "It's not about software, it's about habits" | "We changed four habits. None of them is software." |
| Three adjectives in a row | "simple, fast and powerful" | the one that matters, with a number |
| Throat-clearing opener | "In today's world, bookkeeping is..." | start at the outcome |
| Rhetorical question chain | "Tired? Overwhelmed? Behind?" | one concrete situation |
| Fake suspense | "Here's the thing nobody tells you..." | say the thing |
| Summary close | "In conclusion, habits matter." | the next action |
| Em and en dashes | "close fast, fix later" written with a dash | a comma, a colon or two sentences |

## Repetition across pieces

The same hook pattern on every platform is the most common atomizing mistake. Give each platform its own hook type in the plan, and check the opening three words of every piece; `post_check.py` warns when two pieces open the same way.

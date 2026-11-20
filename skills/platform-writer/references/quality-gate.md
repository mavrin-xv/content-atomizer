# Quality gate

Run `post_check.py` first; it catches the mechanical failures. Then score every piece on five dimensions by reading it as the reader would.

## Five dimensions, 1 to 10 each

| Dimension | 9-10 | 5-6 | 1-3 |
|---|---|---|---|
| Hook | the first line alone makes the reader stop, with a specific outcome or tension | a clear topic with no reason to care yet | a greeting, a stock question, or bait |
| Native fit | written for this platform's reader and length | a decent post moved from somewhere else | a paragraph pasted from the article |
| Substance | every line adds a fact, a step or a reason | some filler between good lines | could be about any business |
| Voice | sounds like the same person as the other pieces | slightly generic | sounds like a template |
| Ask | one specific next step that fits the platform | a vague "let me know" | no ask, or "follow for more", or bait |

## Ship bar

- Average 8 or more, and no dimension under 7.
- Below the bar: rewrite only the weak dimension, then score again.
- Three rewrites at most. If a piece still fails, it is the atom or the platform that is wrong. Go back to the plan and skip that platform, or pick a different atom.

## Things that fail regardless of score

- A number that is not in the source (`post_check.py --source` catches digits; read for spelled-out numbers yourself).
- A claim about results the source does not make.
- Two pieces whose lines overlap heavily. `post_check.py` fails over 35% shared three-word phrases and warns over 20%.
- Engagement bait, listed in `slop-patterns.md`.
- A link in an X post body, or a clickable-link promise on Instagram or TikTok.

## Record the scores

Write the five scores under each piece in a fenced block so they stay out of the checker:

```
hook 8 | fit 9 | substance 8 | voice 8 | ask 7 | avg 8.0 | ship
```

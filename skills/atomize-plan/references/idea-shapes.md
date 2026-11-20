# Idea shapes and where they fit

Pick formats from the shape of each atom, not from the list of accounts you have. An atom that does not fit a platform gets skipped there, with a reason.

## Atom kinds

| Kind | What it looks like | Example from a bookkeeping article |
|---|---|---|
| framework | a named set of steps or parts | "Four habits: daily match, one inbox, fixed calendar, one-page report" |
| step | one step you can do today | "Open the bank feed every morning and match yesterday's lines" |
| tutorial | how to do one thing, start to finish | "The 10-minute daily match, with a one-line note for anything odd" |
| data | a number with a before and after | "Missing receipts went from about 30 a month to under 5" |
| story | something that happened to someone | "Two clients still have a cash problem; they see it 6 days earlier" |
| contrarian | a claim most readers will push back on | "Close even when something is missing" |
| opinion | a view without a fight attached | "The call matters more than the report" |
| quote | one line that stands alone | "You cannot fix a number you see too late" |

## Fit table

Rows are atom kinds, columns are formats. Strong means the format carries the atom without losing its point. Weak means it compresses badly; `plan_check.py` warns on the weak pairs.

| Kind | Thread | Short post | Long post / newsletter | Carousel | Video script |
|---|---|---|---|---|---|
| framework | strong | weak | strong | strong | weak (pick one part) |
| step | ok | strong | ok | ok | strong |
| tutorial | strong | weak | strong | strong | strong |
| data | ok | strong | ok | ok (one number per slide) | ok |
| story | ok | weak | strong | weak | strong |
| contrarian | strong | strong | ok | weak | ok |
| opinion | ok | strong | ok | weak | ok |
| quote | weak | strong | weak | ok (quote card) | weak |

## Default budget

Two to three platforms and three to six pieces per source. A full fan-out to every account is allowed only when the person asks for it; set `"wide": true` in the plan and say why. More pieces from one source mean more repetition, and readers who follow you on two platforms notice.

## Thin sources

Under about 500 words, or fewer than three atoms, is a thin source. Make at most three pieces, usually one native piece on the best-fit platform plus one short post. Padding a thin source produces three posts that say the same sentence.

## The four treatments

| Treatment | When | What it means |
|---|---|---|
| native-deep | the atom fits and the platform matters to you | a full piece written for that platform |
| native-light | the atom fits but the platform is secondary | one short native post, no thread or carousel |
| link-in-reply | the source itself is the point (a long article, a video) | a native post that stands alone, with the link in the first reply |
| skip | weak fit, inactive account, or nothing new to say there | no piece, and one line saying why |

Skips are part of the plan. A plan with no skips across five platforms is usually a plan that did not look at fit.

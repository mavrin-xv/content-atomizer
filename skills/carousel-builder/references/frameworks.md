# Five carousel frameworks

Pick the framework from the atom, not from habit. Each one has a slide range that `carousel_lint.py` enforces and a required part it checks.

| Framework | Use it for | Slides | Required part |
|---|---|---|---|
| value-stack | a set of points that each stand alone | 4-14 | numbered points, one per slide |
| problem-proof | a claim that needs evidence to be believed | 6-10 | a `proof` slide with a number or an image |
| hack-list | habits or swaps, "instead of this, do that" | 6-10 | `bad` and `good` on every `hack` slide |
| rant-callout | a strong opinion against common practice | 4-8 | a `pivot` slide that turns the rant into advice |
| demo-walkthrough | a process shown step by step | 3-11 | an image on every `step` slide, captions of 10 words or fewer |

## value-stack

```
1 hook      the promise with a number: "7 checks before you send an invoice"
2 define    who this is for, or what the problem costs
3-n point   one point per slide, numbered, a title and one or two lines
n-1 close   the one point to start with, or the pattern behind them all
n cta       the specific next step
```

## problem-proof

```
1 hook      the claim
2 problem   what goes wrong today, in the reader's words
3 problem   why the usual fix does not work
4 proof     a number, a before and after, or a screenshot
5-7 point   what to do instead
8 close     the result restated with the proof
9 cta       the next step
```

## hack-list

```
1 hook      "Close the month in 3 days, not 9"
2 problem   why the current way hurts
3-n hack    title, then "Instead of" (bad) and "Do this" (good)
n-1 close   what the swaps add up to, or what they do not fix
n cta       the next step
```

## rant-callout

```
1 hook      the opinion, stated flatly
2 problem   what people do now
3 problem   what it costs them
4 pivot     "So do this instead"
5 point     the replacement
6 cta       the next step
```

## demo-walkthrough

```
1 hook      the result and the time it takes
2 define    what you need before you start
3-n step    one screenshot or photo per step, a caption of 10 words or fewer
n cta       the next step
```

## Choosing between them

- If every point is an "instead of", use hack-list.
- If the reader will not believe you without seeing evidence, use problem-proof.
- If you can only say it with screenshots, use demo-walkthrough.
- If you are arguing, use rant-callout, and keep it short.
- Everything else is a value-stack.

Start a deck with `carousel_lint.py --init value-stack > slides.json` and change the framework and slides from there.

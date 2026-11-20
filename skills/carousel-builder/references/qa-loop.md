# QA loop

Lint the copy, render, look at the pictures, fix, repeat. Three rounds at most; if round three still fails, the framework or the atom is wrong.

## One round

1. `python3 scripts/carousel_lint.py slides.json` until it prints OK.
2. `python3 scripts/render_carousel.py slides.json -o carousel.html --png out/` to render.
3. Open each PNG and check the visual list below. Write down every failure with its slide number before fixing anything.
4. Fix the copy in slides.json, not in the HTML. The HTML is regenerated every time.

## Visual checklist

| Check | Fails when |
|---|---|
| Hook read in one second | you have to read slide 1 twice to get the promise |
| No orphan word | one word alone on the last line of a title |
| Highlight intact | a highlighted phrase is split across two lines |
| Nothing cut off | text touches the edge or overlaps the footer |
| Even density | one slide is crowded while the next is nearly empty |
| Images readable | a screenshot's text is too small to read on a phone |
| Swipe reason | a slide ends without a reason to see the next one |
| CTA clear | the last slide does not say what to do and what you get |

## Blind read

After the visual pass, give only the PNGs (not the source, not the plan) to someone who has not seen them, or to a fresh agent session. Ask three questions:

1. What is this carousel about, after slide 1 only?
2. Which slide would you save or screenshot?
3. What does the last slide ask you to do?

If the answers do not match what you meant, fix the slides that caused the miss. This catches what a writer cannot see in their own work: the context in your head that is not on the slide.

## Done when

- `carousel_lint.py` prints OK with no FAIL.
- The visual checklist has no failure.
- The blind read gets all three answers right.

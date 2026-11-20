# Design rules

The renderer ships four neutral themes so a first carousel looks clean without a designer. Use your own colors and fonts with `--accent` and by editing the theme block at the top of `render_carousel.py`.

## Themes

| Theme | Look | Good for |
|---|---|---|
| dark | near-black background, white heavy sans, bright accent | bold claims, short titles |
| light | white background, dark sans | data and steps |
| editorial | off-white, serif titles, sans body | opinions and essays |
| paper | warm paper, handwritten-style system font | personal notes, casual tone |

All themes use fonts that ship with the operating system, so nothing is downloaded and the output is the same offline. Fonts differ between Windows, macOS and Linux, so check the PNGs on the machine you export from.

## Rules the renderer applies

- Size per platform: 1080x1350 (4:5) for Instagram, LinkedIn and Threads; 1080x1920 for TikTok.
- Safe margins of 80 pixels on each side. The footer sits inside them.
- Titles shrink to fit, down to 72 pixels, and use balanced wrapping.
- The highlight color goes on the words inside `**...**` only. One highlight per slide is enough.
- Slide 1 gets a "Swipe" cue; every slide gets "n/total" in the footer.
- Hack slides render "Instead of" in a muted tone and "Do this" in the accent color.

## Rules for you

- Contrast: body text needs at least 4.5:1 against the background. The four themes meet it; check your own colors with any contrast checker before you post.
- One accent color. Two accents read as noise at phone size.
- Images: use real screenshots or photos for proof and demo slides, cropped to the content. Stock photos of people pointing at laptops add nothing.
- Keep the footer to a name or handle. No logos bigger than the footer text.
- Look at every PNG before you post. The linter checks the copy; only your eyes check the picture.

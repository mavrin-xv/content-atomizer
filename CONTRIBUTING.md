# Contributing

Issues and pull requests are welcome.

- **Bug:** include the command, the input file (or a short version of it) and the full output.
- **Platform rule changed:** update the limit in `post_check.py` and the row in `skills/atomize-plan/references/platform-facts.md`, with a link to the platform's own docs and a new `last_verified` date.
- **New carousel framework:** add it to `skills/carousel-builder/references/frameworks.md`, its slide range and checks to `carousel_lint.py`, and a starter to `INIT` there.
- **New hook type:** add the regex to `TYPES` in `hook_bank.py` and a row with an example to `skills/hook-library/references/hook-types.md`.
- **Skill changes:** show a before and after output on the invented data in `examples/`.
- Scripts stay standard-library only, so the pack installs with nothing but Python. Playwright stays optional.
- Plain English in docs. No invented numbers in examples; example companies are fictional.

By contributing you agree your work is released under the MIT license.

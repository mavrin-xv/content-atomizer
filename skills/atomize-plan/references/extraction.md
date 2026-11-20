# Extracting atoms

Atomize ideas, not paragraphs. An atom is one idea that can carry a piece on its own. Copying paragraph three into a tweet is excerpting; turning the idea in paragraph three into a tweet is atomizing.

## Read in this order

1. **Core insight.** One sentence, 30 words or fewer, that says what the source proves. If you cannot write it, the source does not have one yet. Say so and stop; atomizing a source with no point produces five pieces with no point.
2. **Supporting points.** Three to seven. Each one is a reason the core insight is true.
3. **Evidence.** Numbers with their before and after, named examples, results. Copy the exact sentence from the source into the atom's `evidence` field. `plan_check.py` looks for it in the source and fails the plan if it is not there.
4. **Stories.** Anything that happened to a person or a business, with a moment of change.
5. **Contrarian takes.** Claims a reader in this field would argue with. These carry threads and short posts.
6. **Quotable lines.** Sentences under 30 words that stand alone without context.
7. **Action items.** What the reader can do today. Every platform piece should point at one.

## Rules

- Write the atom's `text` in your own words. Keep the `evidence` field verbatim.
- No number goes into an atom unless it is in the source. If the source says "about 30", the atom says "about 30", not 30.
- Mark the kind honestly. A list of tips is not a framework unless the parts depend on each other.
- Stop at the atoms the source supports. Six good atoms beat twelve thin ones.
- Note what the source does not cover, for the honest-limits line in long pieces.

## plan.json fields

```json
{
  "source": {"title": "...", "path": "source.md"},
  "core_insight": "one sentence, 30 words or fewer",
  "wide": false,
  "atoms": [
    {"id": "a1", "kind": "data", "text": "your words", "evidence": "exact sentence from the source"}
  ],
  "platforms": [
    {"platform": "x", "treatment": "native-deep", "format": "thread", "atoms": ["a1"],
     "hook_type": "outcome-first", "why": "one line"},
    {"platform": "linkedin", "treatment": "skip", "why": "the reason"}
  ]
}
```

`source.path` is resolved relative to plan.json. Add `"pieces": 2` to a platform entry when it gets more than one piece. Hook types are listed in the hook-library skill (hook-types.md there); give each platform a different one.

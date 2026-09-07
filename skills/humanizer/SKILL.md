---
name: humanizer
description: |
  Manual-only skill. Use only when the user explicitly invokes humanizer,
  $humanizer, /humanizer, or asks to use the humanizer skill. Do not trigger
  automatically for ordinary editing, copywriting, localization, marketing,
  App Store copy, or text review. When invoked, remove signs of AI-generated
  English writing from text and make it sound more natural while preserving
  meaning.
license: MIT
metadata:
  version: "2.8.3"
---

# Humanizer

Use only when the user explicitly invokes humanizer, `$humanizer`, `/humanizer`, or asks to use this skill. Keep `agents/openai.yaml` explicit-only. Ordinary editing requests do not activate it.

Edit English prose to sound natural while preserving the author's intent and voice. The patterns below are editing heuristics, not a reliable way to determine whether a person or AI wrote a text. Do not label authorship from style alone.

## Editorial contract

- Preserve meaning, factual coverage, stance, sentiment, and uncertainty. Do not invent facts, sources, concrete details, first-person experiences, or opinions to make prose livelier.
- Preserve useful structure and any requested format. Merge or split paragraphs when that improves flow; paragraph count is not a requirement. Cut empty repetition without dropping substantive content.
- Match the audience and register. Technical, legal, encyclopedic, and reference prose may appropriately be neutral. Preserve personality already present in personal writing without manufacturing quirks, tangents, or emotion.
- When a writing sample is supplied, use its vocabulary, rhythm, transitions, and punctuation as evidence of the desired voice. Without a sample, infer voice from the input and request.
- Treat isolated transitions, dashes, curly quotes, formal vocabulary, lists, or polished grammar as normal writing. Revise patterns when they make the passage vague, repetitive, inflated, or awkward, not to satisfy a stylistic quota.
- Preserve quotations, titles, proper names, code, and examples that discuss the watched phrases. Retain necessary qualifications and meaningful punctuation. User style requirements take precedence over these defaults.

## Workflow and output

Read the input and identify the specific passages that need improvement. If there is little to fix, make a small edit or say no humanization is needed; do not force a rewrite.

Draft the revision, then compare it with the input for factual or tonal drift. Check natural flow and remaining filler in context. The draft and review are internal by default; return only the final rewritten text unless the user asks for explanations or intermediate drafts.

Return text in the conversation. Edit files only when the user explicitly requests an in-place file edit.

## Pattern references

Read only the reference matching a problem present in the input:

- [Content patterns](references/content-patterns.md): inflated significance, promotion, vague attribution, and generic conclusions about challenges.
- [Language patterns](references/language-patterns.md): repetitive vocabulary, awkward constructions, forced triplets, synonym cycling, and unclear subjects.
- [Style patterns](references/style-patterns.md): excessive punctuation, emphasis, headings, lists, emoji, and typography.
- [Communication patterns](references/communication-patterns.md): chatbot framing, speculative filler, hedging, generic closers, and manufactured drama.

## Attribution

Adapted from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. Its observations are context for editing, not proof of authorship. License metadata is preserved above.

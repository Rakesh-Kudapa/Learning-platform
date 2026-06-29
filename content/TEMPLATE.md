# Module Content Template

> **Purpose.** This is pure subject-matter content, written by the SME (Rakesh,
> with Claude's research help). It contains **zero code**. Claude Code's job is
> to take a filled-out copy of this template and wire it into `templates/course.html`
> (as a new `modN()` function, following the exact pattern of `mod1()`/`mod2()`)
> and into `course_data.py` (`MODULE_TITLES`, `MODULE_CONTEXT`). Claude Code should
> NOT invent or alter facts — only format/structure them into the existing patterns.

---

## Module number & title
`Module 0X — <Title>`

## Eyebrow / kicker
Short tag line shown above the H1, e.g. `MODULE 0X • <Section name>`

## Headline (H1) + lead paragraph
The big title (can use one **emphasized** word/phrase) + a 1-2 sentence hook
that frames why this module matters.

## Narration script
Plain text, 80-150 words, written to be *read aloud* (no headers/bullets) —
this is what the "Listen" button speaks. Should summarize the module's key
point in a friendly, spoken tone.

## Body sections
One or more `### Subheading` blocks. Each should be short paragraphs a true
beginner can follow — no unexplained jargon, define every term on first use.
Use **bold** for key terms, and short bullet lists where useful.

## Video script (Steve.ai)
A separate, shorter script for the AI explainer video — written in natural,
spoken language, pre-broken into short numbered **scenes** (1-3 sentences
each) so Steve.ai's auto-scene-split lands cleanly. Keep total length to
~60-90 seconds of spoken audio (roughly 130-180 words total).
- **Suggested context tag** (1-2 words, for Steve.ai's "what's this video
  about" field): e.g. `healthcare data`
- **Suggested style:** animated 2D explainer / presenter-avatar template
- **Scenes:**
  1. ...
  2. ...
  3. ...

## Diagram spec (if applicable)
Describe the diagram in words — what boxes/steps/arrows it needs, what each
label says, what it's trying to show. Claude Code (or Claude in chat) turns
this into an inline SVG matching the existing visual style (teal→violet→
magenta gradient, rounded boxes, IBM Plex Mono labels). Do not write SVG code
here — just the content of the diagram.

## Callout(s)
Optional short highlight box(es): a memory hook, a common-mistake warning,
or an "Excelra connection" line tying the concept back to Excelra's business.

## Knowledge check(s)
Scale the number of questions to the module's length/content depth — a
dense module (e.g. 20 terminologies) warrants more questions than a short
one. As a guide: 3 questions for lighter modules, 4-5 for denser ones.
Each question unlocks the next module once **all** questions in the module
have been answered (right or wrong) — correct answers award full XP,
incorrect award half XP, matching the existing single-question modules.

### Question 1
- **Question:**
- **Options (4):** A / B / C / D
- **Correct answer:** (letter)
- **Explanation:** 1-2 sentences explaining why the correct answer is right
  (and ideally why a tempting wrong option is wrong).
- **XP:** 15 (lower than the old flat 20, since multiple questions now add
  up per module — adjust if a module has very few questions)

### Question 2
(same structure — add as many `### Question N` blocks as the module needs)

## XP value
Sum of all questions' XP above (informational — not required to total an
exact number, just keep it consistent with the per-question values).
Default `20` unless this module's check should be weighted differently.

---
*Fill one copy of this per module as `content/module-0X-<slug>.md`.*

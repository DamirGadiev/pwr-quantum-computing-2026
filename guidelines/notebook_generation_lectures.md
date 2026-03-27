# Notebook Generation Guidelines (Lectures)

Lecture notebooks are narrative-first and concept-first. They are designed for live presentation and self-study.

## 1. Lecture Design Goals

- Teach concepts through visual narrative, not proof-heavy derivations.
- Keep each section centered on one conceptual question.
- Use short markdown blocks between code cells to maintain flow during live teaching.

## 2. Required Section Structure

Each lecture section should contain:

1. Concept question
2. Small executable model
3. Dominant figure
4. Theory vs practice contrast
5. Recap sentence
6. Discussion prompt

## 3. Content Expectations

- Start from familiar examples, then generalize to abstract classes/frameworks.
- Distinguish clearly between:
  - asymptotic intuition,
  - measured behavior,
  - system-level overhead.
- Include misconception guards where students commonly overgeneralize.

## 4. Visual Narrative Constraints

- One central figure per section; avoid figure clutter.
- Follow the shared style in `utilities/complexity_utils.py`.
- Ensure all figures are readable when projected in a classroom.
- Place interpretation immediately after each figure.

## 5. Lecture-Level Rigor

- Definitions should be accurate but course-level (intuition-first).
- Explicitly mark toy models and what they leave out.
- Do not present toy simulation numbers as hardware predictions.

## 6. End-of-Notebook Closure

Include:

- concise recap of key lessons,
- list of student discussion questions,
- bridge statement to next lecture/lab activity.

# Notebook Generation Guidelines (Common)

These rules apply to all notebooks in this project, including lectures and labs.

## 1. Teaching Philosophy

- Prefer evidence-first explanations: claims must be supported by a computation, table, or plot.
- Build intuition progressively: motivate, model, visualize, compare, recap.
- Keep notebooks runnable top-to-bottom on a student laptop without network access.
- Use simplifications deliberately and label them as pedagogical approximations.

## 2. Standard Notebook Rhythm

For each major section, follow this flow:

1. Motivating question
2. Minimal model/algorithm code
3. One dominant visual
4. Compact comparison (table or bullet contrast)
5. Short takeaway
6. Prompt question for students

## 3. Evidence-First Rules

- Every non-trivial claim about complexity or performance must be tied to one of:
  - operation counting,
  - measured runtime (with caveats),
  - memory/representation comparison,
  - scaling plot.
- Keep theory and measurement explicitly separated in markdown.
- State assumptions that affect interpretation (input size definition, hardware, simplifications).

## 4. Visual and Plot Quality

- Use consistent style and plotting helpers from `utilities/complexity_utils.py`.
- Plots must have clear titles, axis labels, readable legends, and units where relevant.
- Prefer one clear message per figure over dense multi-purpose charts.
- Use projector-friendly sizing and font scales.
- Keep color choices consistent and accessible; avoid low-contrast defaults.

## 5. Code Organization in Notebooks

- Reuse shared utilities; do not re-implement style/plot helpers in each notebook.
- Keep algorithm code short and transparent; avoid unnecessary abstraction.
- Separate setup cells, model cells, plotting cells, and interpretation markdown.
- Seed randomness where reproducibility matters.
- Ensure all imports are explicit and minimal.

## 6. Complexity Assessment Framework (Project Default)

Use this framework in both lectures and labs when assessing algorithms or advantage claims:

1. Input model: what is `n` and why?
2. Representation: data structure/topology and memory implications.
3. Core growth: asymptotic behavior and dominant terms.
4. End-to-end costs: preprocessing, mapping/routing, measurement, post-processing.
5. Baseline fairness: comparison against a strong and honest classical baseline.
6. Practical limits: constants, overheads, and measurement noise.

## 7. Quality Gate Before Finalizing a Notebook

- Runs from first to last cell without manual intervention.
- No broken references to helper functions or utilities.
- Every section has at least one explicit takeaway.
- Every key plot has an interpretation paragraph directly below it.
- Student prompts are present and aligned with the section objective.

## 8. Best Agentic Practices for Notebook Generation

- Start with a compact section plan before writing cells (question -> model -> evidence -> takeaway).
- Reuse existing project utilities first; only add new helpers when required by repeated use.
- Implement in small, verifiable increments and re-run affected cells immediately.
- Prefer deterministic outputs for teaching artifacts (fixed seeds, stable sample sizes).
- Validate pedagogical alignment after technical correctness: does each section answer its motivating question?
- End with a checklist pass for reproducibility, evidence quality, and visual readability.

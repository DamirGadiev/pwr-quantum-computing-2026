# AGENTS.md

This file defines default instructions for agentic work in this repository.

## Scope

These instructions apply to all agent tasks unless the user gives an explicit override.

## Source of Truth for Notebook Generation

Use the following files as the primary standards:

- `guidelines/notebook_generation_common.md`
- `guidelines/notebook_generation_lectures.md`
- `guidelines/notebook_generation_labs.md`

When generating or editing notebooks, follow these documents directly.

## Project Context

- The repository contains both **lectures** and **labs**.
- Both share a common pedagogical approach: evidence-first, visual-first, and reproducible.
- Lecture notebooks are narrative-first; lab notebooks are workflow-first and assignment-oriented.

## Required Notebook Practices

- Support key claims with computation, measurements, tables, or plots.
- Keep theory and measured behavior explicitly separated.
- Use visually clear, projection-friendly plots with explicit labels and readable legends.
- Reuse helper code from `utilities/complexity_utils.py` instead of duplicating plotting/style code.
- Keep cells modular: setup, model, plot, interpretation.
- Ensure deterministic behavior where relevant (fixed seeds, stable sampling setup).

## Complexity Assessment Framework (Default)

Apply this framework when assessing algorithmic or quantum-advantage claims:

1. Input model (`n` definition and assumptions)
2. Representation and memory implications
3. Core asymptotic growth and dominant terms
4. End-to-end overheads (pre/post-processing, mapping/routing, measurement)
5. Baseline fairness and comparison quality
6. Practical constraints (constants, noise, execution environment)

## Agentic Workflow

Use this sequence for substantial notebook work:

1. Plan section structure (`question -> model -> evidence -> takeaway`)
2. Implement in small increments
3. Re-run affected cells immediately
4. Interpret outputs directly under plots/tables
5. Perform final quality gate pass

## Definition of Done

Before marking work complete:

- Notebook runs top-to-bottom without hidden-state dependency.
- No broken references to utilities or helper functions.
- Every major section has a takeaway and at least one student-facing prompt.
- Plots/figures are readable and aligned with the section question.
- Conclusions are evidence-backed and include caveats when needed.


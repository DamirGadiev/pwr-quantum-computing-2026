# Notebook Generation Guidelines (Labs)

Lab notebooks are practice-first and execution-first. They should guide students through methodical, reproducible analysis.

## 1. Lab Design Goals

- Turn lecture concepts into hands-on workflows.
- Show each step needed to evaluate a complexity or advantage claim.
- Train students to justify conclusions using evidence, not slogans.

## 2. Required Lab Flow

Each lab unit should follow:

1. Task objective and expected output
2. Starter code/context
3. Guided step-by-step implementation
4. Evidence collection (tables/plots/measurements)
5. Interpretation questions
6. Mini conclusion and checkpoint

## 3. Assignment-Oriented Structure

- Separate clearly:
  - instructor-guided examples,
  - student TODO sections,
  - final independent tasks.
- Provide explicit deliverable criteria (what must be shown and explained).
- Include rubric-friendly checkpoints tied to the complexity framework.

## 4. Evidence and Fair Comparison Rules

- Require students to state:
  - input model,
  - baseline choice,
  - assumptions and caveats.
- Require at least one plot/table per major claim.
- Ban unsupported conclusions such as "algorithm X is better" without measured/theoretical justification.

## 5. Utility Reuse and Technical Consistency

- Use plotting and formatting helpers from `utilities/complexity_utils.py`.
- Keep student-facing code cells concise and runnable.
- Use deterministic seeds for stochastic experiments.
- Ensure notebook execution is linear and does not depend on hidden state.

## 6. Lab Closing Block

End each lab with:

- a short "What we validated" summary,
- a short "Where conclusions may fail" limitations block,
- next-assignment handoff instructions.

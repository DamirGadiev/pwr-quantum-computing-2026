# Team B — Translation Symmetry, Bloch Momentum, and the Order-Finding Core Behind Shor

## Challenge Brief

Your team will investigate a **periodic lattice system** and use it to uncover the mathematical structure that sits at the heart of **Shor’s algorithm**.

The system is not cryptographic. It is physical.

You will study a **1D periodic tight-binding ring**, analyze its **translation symmetry**, recover the eigenphases of the translation operator, and connect those phases to a finite-order unitary. Then you will show why this is mathematically the same kind of order-finding problem that Shor exploits in modular arithmetic.

Your job is to:

1. build a periodic lattice model,
2. solve it classically,
3. use QFT to move between site and momentum representations,
4. use QPE to recover translation eigenphases,
5. explain why this is the physics analogue of the order-finding engine inside Shor.

The key point is that the interesting unitary is not the Hamiltonian itself but the **translation operator**:
$$
T|j\rangle = |j+1 \bmod 8\rangle.
$$

This operator shifts every site label by one step around the ring. Because the geometry is periodic, applying the same shift eight times returns every basis state to where it started:
$$
T^8 = I.
$$

That finite-order structure is the exact reason QPE becomes relevant.

---

## Why this problem matters

Translation symmetry is one of the most fundamental ideas in condensed matter and lattice physics.

For a periodic lattice:

- translation is a unitary symmetry,
- momentum / Bloch states diagonalize the translation operator,
- the allowed phases are discrete roots of unity,
- a finite periodic system has a finite translation order.

That is exactly the bridge to Shor:

- Shor’s quantum core is an **order-finding problem**,
- finite-order unitary operators have eigenphases of the form \(s/r\),
- QPE can recover those phases,
- from the phase structure one can infer the order.

So this challenge lets you study Shor’s skeleton in a genuine physics setting.

---

## Ring picture

The physical picture should stay visible throughout the whole notebook: one particle can occupy any of 8 sites, and the translation operator moves that occupation one step clockwise.

![8-site periodic ring with labeled sites and one-step translation](team_b_ring_diagram.svg)

What this picture means mathematically:

- the Hilbert space basis states are the site occupations $|0\rangle,\dots,|7\rangle$,
- the ring geometry makes site 7 adjacent to site 0,
- translation by one site is a symmetry because every bond looks identical after the shift,
- repeated translations generate a finite cyclic group: $I, T, T^2, \dots, T^7$.

---

## Explicit input

Use the following fixed model.

### Periodic ring
- number of lattice sites: \(N = 8\)
- hopping amplitude: \(J = 1\)
- periodic boundary conditions

### Basis
Use the site basis:
\[
|0\rangle, |1\rangle, \dots, |7\rangle.
\]

### Translation operator
Define:
\[
T |j\rangle = |j+1 \bmod 8\rangle.
\]

### Tight-binding Hamiltonian
Define:
\[
H = -J \sum_{j=0}^{7}
\left(
|j+1\rangle\langle j|
+
|j\rangle\langle j+1|
\right),
\]
with all indices taken modulo 8.

This is a fully explicit physical model with no external data dependency.

---

## Mathematical model

### Translation symmetry
Because the system is periodic:
\[
T^8 = I.
\]

So \(T\) is a finite-order unitary of order 8.

### Which symmetry are we actually looking for?

The central symmetry in this workshop is **discrete translation symmetry**.

We are not looking for:

- reflection symmetry,
- spin symmetry,
- particle-exchange symmetry.

We are looking for the statement that a rigid shift of the whole lattice leaves the physics unchanged. In operator form:
$$
T^m |j\rangle = |j+m \bmod 8\rangle,
$$
and the tight-binding Hamiltonian satisfies
$$
[H,T] = 0.
$$

This commutator is the compact way of saying that the Hamiltonian and translation operator can be diagonalized in the same symmetry-adapted basis. That basis is the Bloch or momentum basis.

Its eigenstates are momentum / Bloch states:
\[
|k_n\rangle =
\frac{1}{\sqrt{8}}
\sum_{j=0}^{7} e^{i 2\pi n j / 8} |j\rangle,
\qquad n = 0,1,\dots,7.
\]

These satisfy:
\[
T|k_n\rangle = e^{-i 2\pi n/8} |k_n\rangle.
\]

So the eigenphases are discrete fractions:
\[
\phi_n = \frac{n}{8}
\quad \text{(up to sign convention and modulo 1).}
\]

### Tight-binding energies
The same Bloch states diagonalize the nearest-neighbor Hamiltonian:
\[
H |k_n\rangle = E_n |k_n\rangle,
\]
with
\[
E_n = -2J \cos\left(\frac{2\pi n}{8}\right).
\]

This gives the team both:

- a symmetry operator \(T\),
- a physical Hamiltonian \(H\).

---

## Classical baseline

You must implement the following classical steps first.

1. Build the explicit \(8\times8\) matrix for \(T\).
2. Verify numerically that:
   \[
   T^8 = I.
   \]
3. Diagonalize \(T\) and list its eigenvalues.
4. Construct the Bloch states explicitly.
5. Verify numerically that the Bloch states diagonalize \(T\).
6. Build and diagonalize the tight-binding Hamiltonian \(H\).
7. Verify:
   - \([H,T] = 0\),
   - the energy formula
     \[
     E_n = -2\cos(2\pi n/8).
     \]

This classical solution is the benchmark and the physics anchor.

---

## Quantum mapping

This challenge has two natural quantum layers.

### Layer 1 — QFT as momentum transform
The site basis is position-like. The Fourier basis is momentum-like.

Applying QFT on the 3-qubit site register gives a discrete momentum representation. This is physically meaningful because the momentum basis diagonalizes translation on the ring.

Use QFT to show:

- a site-localized state becomes spread over momentum sectors,
- a momentum eigenstate has a sharp phase interpretation,
- Fourier structure is not decorative here; it is the natural symmetry basis.

### Layer 2 — QPE on the translation operator
Apply QPE to the unitary \(T\).

If the system is prepared in a translation eigenstate \(|k_n\rangle\), then QPE recovers the phase corresponding to:
\[
e^{-i2\pi n/8}.
\]

That means QPE reveals the discrete fraction \(n/8\), i.e. the hidden order structure of the unitary.

### Why order and QPE are connected

The connection is completely general.

If a unitary $U$ has finite order $r$, then
$$
U^r = I.
$$

Any eigenvalue $\lambda$ of $U$ must therefore satisfy
$$
\lambda^r = 1,
$$
so it has to be an $r$th root of unity:
$$
\lambda = e^{i2\pi s/r}
$$
for some integer $s$.

Now apply QPE to an eigenstate $|\psi_s\rangle$ of $U$:
$$
U|\psi_s\rangle = e^{i2\pi s/r} |\psi_s\rangle.
$$

QPE estimates the phase
$$
\phi = \frac{s}{r}.
$$

So QPE does not directly output the order $r$. It outputs a rational phase whose denominator is tied to the order. Recovering that denominator from the measured phase is the classical post-processing step that turns phase estimation into order finding.

For this ring problem:

- the unitary is $T$,
- the order is $r=8$,
- the eigenphases are multiples of $1/8$,
- QPE should recover numbers of the form $n/8$ modulo sign convention and modulo 1.

This is the exact type of object that appears in Shor:
- a finite-order unitary,
- root-of-unity eigenphases,
- phase estimation,
- order recovery.

---

## Recommended technical stack

- Python
- NumPy / SciPy
- Qiskit

Optional:
- Jupyter notebook
- statevector simulator
- inline SVG / HTML visualizations

---

## Explicit task list

### Part 1 — Build the physical model
1. Construct the matrix of the translation operator \(T\).
2. Verify numerically that \(T^8 = I\).
3. Construct the tight-binding Hamiltonian \(H\).
4. Check numerically that \([H,T]=0\).

### Part 2 — Solve the model classically
5. Diagonalize \(T\).
6. List its eigenvalues as roots of unity.
7. Construct the Bloch states \(|k_n\rangle\) analytically.
8. Verify numerically that:
   \[
   T |k_n\rangle = e^{-i2\pi n/8}|k_n\rangle.
   \]
9. Diagonalize \(H\) and compare its eigenvectors to the Bloch states.
10. Verify the dispersion relation:
    \[
    E_n = -2\cos(2\pi n/8).
    \]

### Part 3 — Use QFT as a physics tool
11. Encode the 8-site Hilbert space on 3 qubits.
12. Prepare one site-localized state, for example \(|3\rangle\).
13. Apply QFT and interpret the output distribution in the momentum basis.
14. Prepare one or two superpositions in the site basis and repeat.
15. Explain how QFT is acting as a basis change from position-like to momentum-like representation.

### Part 4 — Use QPE to estimate translation phases
16. Build a QPE circuit for the unitary \(T\).
17. Use:
    - 3 system qubits,
    - 5–7 phase qubits.
18. Prepare a known Bloch state \(|k_n\rangle\).
19. Run QPE and recover the corresponding phase.
20. Convert the measured phase into the integer label \(n\) or the fraction \(n/8\).

### Part 5 — Connect to Shor
21. Explain why \(T\) is a finite-order unitary.
22. Explain why its eigenphases are fractions with denominator 8.
23. Explain why recovering the denominator is an order-finding problem.
24. Write a short comparison:
    - physical translation symmetry,
    - modular multiplication in Shor.

---

## Stretch tasks

1. Extend the ring to \(N=16\) sites if simulator performance allows.
2. Start from a superposition of several momentum sectors and analyze the QPE output distribution.
3. Add a weak on-site defect potential and study what happens when exact translation symmetry is broken.
4. Compare direct QFT-based momentum analysis to QPE-based phase extraction.
5. Build a toy modular-order example and explicitly compare it to the translation-order case.

---

## Qubit budget

Safe configuration:

- 3 system qubits for the 8-site ring
- 5–7 phase qubits for QPE

Total:
- **8–10 qubits**

Even the \(N=16\) extension only needs 4 system qubits.

This fits comfortably inside a 10–15 qubit simulator budget.

---

## Deliverables

Prepare a short report or slide deck containing:

1. **Physical model**
   - ring geometry,
   - translation operator,
   - Hamiltonian.

2. **Classical solution**
   - eigenvalues of \(T\),
   - Bloch states,
   - tight-binding energies.

3. **Quantum solution**
   - QFT as momentum transform,
   - QPE on the translation operator,
   - measured phases.

4. **Interpretation**
   - what the measured phases mean physically,
   - why this is an order-finding problem,
   - how this mirrors the logic behind Shor.

---

## Suggested figures

Include at least 3 of the following:

- matrix representation of \(T\)
- eigenvalues of \(T\) on the complex unit circle
- dispersion plot \(E_n\) vs \(k_n\)
- QFT circuit diagram
- QPE circuit diagram
- histogram of measured QPE outcomes
- side-by-side picture: site basis vs momentum basis

---

## Guiding questions

1. Why do periodic boundary conditions force discrete momentum values?
2. Why do translation eigenvalues lie on the unit circle?
3. Why is QFT the natural basis change for this system?
4. What does QPE recover that a direct site-basis measurement does not?
5. In what precise sense is this the same type of problem as the order-finding core in Shor?

---

## Suggested division of labor inside the team

- **Theory lead** — translation symmetry, Bloch states, dispersion
- **Classical lead** — matrix construction and diagonalization
- **Quantum lead** — QFT and QPE circuits
- **Skeptic / integrator** — checks assumptions and builds the Shor connection

---

## References

1. IBM Quantum Learning — Quantum Phase Estimation  
   https://quantum.cloud.ibm.com/learning/courses/utility-scale-quantum-computing/quantum-phase-estimation

2. IBM Quantum Learning — Phase Estimation and Factoring  
   https://quantum.cloud.ibm.com/learning/courses/fundamentals-of-quantum-algorithms/phase-estimation-and-factoring/introduction

3. Periodic lattice and Bloch-theory lecture notes  
   https://home.uni-leipzig.de/stp/quantum_mechanics_2_ws2223/lecturetranscript_QM2.pdf

4. Bloch / periodic-potential lecture notes  
   https://bohr.physics.berkeley.edu/classes/221/9697/blochban.pdf

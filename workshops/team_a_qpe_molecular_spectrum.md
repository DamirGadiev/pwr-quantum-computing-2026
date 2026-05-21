# Team A — Molecular Spectrum Estimation with Quantum Phase Estimation

## Challenge Brief

Your team will investigate a compact quantum-simulation workflow for **molecular energy estimation with Quantum Phase Estimation (QPE)**.

To keep the workshop self-contained and compatible with the existing UV environment, you will **not** generate molecules with an external chemistry package. Instead, you will work with **explicit effective qubit Hamiltonians** that capture the structure of small active-space molecular models.

The main target is **hydrogen \(\mathrm{H}_2\)**, with additional comparison tasks for **\(\mathrm{LiH}\)** and **\(\mathrm{BeH}_2\)**.

Your job is to:

1. build the supplied qubit Hamiltonians,
2. solve them classically,
3. implement a QPE workflow on a simulator,
4. recover molecular energy estimates from measured phases,
5. compare how the workflow behaves across \(\mathrm{H}_2\), \(\mathrm{LiH}\), and \(\mathrm{BeH}_2\),
6. explain what is physically meaningful and what remains difficult in realistic chemistry.

This is still a genuine eigenvalue-estimation problem: QPE extracts phases of time evolution, and those phases encode molecular energies.

---

## Why this problem matters

Estimating eigenenergies is central in:

- molecular physics,
- quantum chemistry,
- materials modeling,
- many-body quantum simulation.

The basic idea is:

\[
\hat H |E_j\rangle = E_j |E_j\rangle
\]

If we define

\[
U = e^{-i \hat H \tau},
\]

then

\[
U |E_j\rangle = e^{-i E_j \tau} |E_j\rangle = e^{2\pi i \phi_j} |E_j\rangle,
\]

so the phase \(\phi_j\) measured by QPE contains the energy:

\[
\phi_j = -\frac{E_j \tau}{2\pi} \pmod 1.
\]

Your job is to recover that phase and convert it back into an energy estimate.

---

## Explicit input

Use the following **effective two-qubit molecular Hamiltonians**:

\[
\hat H =
c_{II}\, I\otimes I
+ c_{ZI}\, Z\otimes I
+ c_{IZ}\, I\otimes Z
+ c_{ZZ}\, Z\otimes Z
+ c_{XX}\, X\otimes X.
\]

### Molecule 1 — \(\mathrm{H}_2\)

\[
\hat H_{\mathrm{H}_2}
=
-1.05\, II
+0.39\, ZI
+0.39\, IZ
-0.01\, ZZ
+0.18\, XX
\]

### Molecule 2 — \(\mathrm{LiH}\)

\[
\hat H_{\mathrm{LiH}}
=
-2.20\, II
+0.18\, ZI
+0.12\, IZ
-0.35\, ZZ
+0.28\, XX
\]

### Molecule 3 — \(\mathrm{BeH}_2\)

\[
\hat H_{\mathrm{BeH}_2}
=
-3.60\, II
+0.25\, ZI
+0.31\, IZ
-0.48\, ZZ
+0.41\, XX
\]

Interpret these as fixed effective active-space models chosen for this workshop.

This assignment is deliberately self-contained:

- no external chemistry package is required,
- no molecular integral generation is required,
- all inputs needed for the quantum workflow are given explicitly.

---

## Mathematical model

For each molecule, start from the supplied qubit Hamiltonian \(\hat H\) and define

\[
U = e^{-i \hat H \tau}.
\]

If the system register is prepared in an eigenstate \(|E_j\rangle\), then QPE estimates the corresponding phase \(\phi_j\), from which you reconstruct

\[
E_j = -\frac{2\pi}{\tau}\phi_j
\]

up to the modulo-1 ambiguity.

In practice, it is often convenient to shift the Hamiltonian by a scalar multiple of the identity:

\[
\hat H' = \hat H - s I,
\]

because this only adds a global phase to the original dynamics. Then

\[
U' = e^{-i \hat H' \tau}
\]

has the same eigenvectors, and the recovered energy is

\[
E_j = s - \frac{2\pi}{\tau}\phi_j.
\]

This shift is a practical way to keep all relevant phases inside a convenient interval.

---

## Classical baseline

You must implement a classical solution first.

Required classical tasks:

1. build each qubit Hamiltonian from Pauli matrices,
2. diagonalize it exactly,
3. extract:
   - ground-state energy,
   - first excited-state energy,
   - at least one energy gap,
4. analyze the overlap of a simple reference state with the true ground state,
5. compare the three molecules on the same classical benchmark.

This classical solution is your correctness benchmark.

---

## Quantum mapping

Your quantum circuit should contain:

- a **phase register** of \(m\) qubits,
- a **system register** holding the molecular state,
- controlled powers of \(U\),
- an inverse QFT on the phase register,
- a measurement of the phase register.

Recommended precision range:

- \(m = 5\) to \(7\) phase qubits

Recommended system setup:

- use the two-qubit effective molecular register directly,
- start with either:
  - an exact eigenstate prepared from classical diagonalization, or
  - a simple computational-basis reference state such as \(|11\rangle\).

### Suggested implementation path

#### Option A — clarity first
Prepare an exact eigenstate from the classical solution and run QPE.

This isolates the phase-estimation logic and makes the energy recovery step clean.

#### Option B — realism first
Prepare a simple reference state and observe that QPE returns several eigenphases with probabilities determined by state overlap.

This is closer to realistic workflows, where state preparation is the hard part.

---

## Recommended technical stack

- Python
- NumPy / SciPy
- Qiskit
- Qiskit Aer

Optional:
- Jupyter notebook
- statevector simulator
- inline SVG / HTML visualizations

---

## Explicit task list

### Part 1 — Build the molecular model
1. Encode Pauli matrices \(I, X, Z\).
2. Build the three supplied Hamiltonians \(\hat H_{\mathrm{H}_2}\), \(\hat H_{\mathrm{LiH}}\), and \(\hat H_{\mathrm{BeH}_2}\).
3. Convert each Hamiltonian to a \(4\times4\) matrix.
4. Print and inspect the Pauli coefficients and matrix forms.

### Part 2 — Solve the benchmark classically
5. Diagonalize each Hamiltonian exactly.
6. Record:
   - ground-state energy,
   - first excited-state energy,
   - corresponding eigenvectors,
   - at least one energy gap.
7. Compare the three spectra in one table or plot.
8. Evaluate the overlap of the basis state \(|11\rangle\) with each true ground state.

### Part 3 — Set up QPE
9. Choose a scalar shift \(s\) and a time parameter \(\tau\) that avoid phase aliasing.
10. Build \(U' = e^{-i(H-sI)\tau}\).
11. Build controlled powers:
    - \(U'\),
    - \((U')^2\),
    - \((U')^4\),
    - and so on up to the number of phase qubits used.
12. Build the inverse QFT on the phase register.

### Part 4 — Run quantum estimation for \(\mathrm{H}_2\)
13. Prepare one target input state for \(\mathrm{H}_2\).
14. Run QPE.
15. Extract the measured bitstring distribution.
16. Convert the dominant measured phase into an energy estimate.
17. Compare against exact diagonalization.

### Part 5 — Extend to \(\mathrm{LiH}\) and \(\mathrm{BeH}_2\)
18. Repeat the workflow for \(\mathrm{LiH}\) and \(\mathrm{BeH}_2\).
19. Compare:
   - exact ground-state energies,
   - recovered QPE energies,
   - dominant output phases,
   - overlaps of \(|11\rangle\) with the ground state.
20. Discuss which molecule is easiest to estimate accurately in this reduced model and why.

### Part 6 — Analyze limitations
21. Discuss the role of:
   - state preparation,
   - finite phase precision,
   - choice of \(\tau\),
   - the cost of implementing \(e^{-iHt}\),
   - the difference between these small effective models and full chemistry Hamiltonians.

---

## Stretch tasks

1. Compare exact-eigenstate initialization to \(|11\rangle\) initialization for all three molecules.
2. Estimate more than one energy level for at least one molecule.
3. Study how the energy error changes with the number of phase qubits.
4. Discuss why Hamiltonian simulation, not inverse QFT, is usually the real heavy part.
5. Compare textbook QPE with iterative / recursive phase-estimation ideas.

---

## Qubit budget

A realistic simulator configuration for this workshop:

- 2 system qubits
- 5–7 phase qubits

Total:
- about **7–9 qubits**

This fits comfortably inside a small simulator budget.

---

## Deliverables

Prepare a short report or slide deck containing:

1. **Problem definition**
   - what quantity is being estimated,
   - why phase estimation is relevant to chemistry.

2. **Classical model**
   - Hamiltonian construction,
   - exact diagonalization results,
   - comparison across \(\mathrm{H}_2\), \(\mathrm{LiH}\), and \(\mathrm{BeH}_2\).

3. **Quantum model**
   - definition of \(U' = e^{-i(H-sI)\tau}\),
   - QPE circuit structure,
   - phase-to-energy mapping.

4. **Results**
   - exact energies,
   - QPE energy estimates,
   - error table.

5. **Interpretation**
   - what worked,
   - what assumptions were required,
   - where the true practical bottlenecks lie.

---

## Suggested figures

Include at least 3 of the following:

- Pauli-coefficient comparison across molecules
- energy spectrum table or plot
- QPE circuit diagram
- measurement histogram on the phase register
- energy error vs number of phase qubits
- overlap comparison for different initial states

---

## Guiding questions

1. Why is molecular energy estimation naturally an eigenvalue problem?
2. Why does QPE estimate phase rather than energy directly?
3. What determines whether QPE collapses onto the desired eigenstate?
4. What is gained by increasing the number of phase qubits?
5. What part of this workflow is easy in a reduced simulator model but hard in realistic chemistry?

---

## Suggested division of labor inside the team

- **Physics lead** — explains the energy model and physical interpretation
- **Classical lead** — exact diagonalization and benchmarking
- **Quantum lead** — QPE circuit and simulation
- **Skeptic / integrator** — checks assumptions, approximations, and interpretation

---

## References

1. Abrams, D. S., and Lloyd, S. *A quantum algorithm providing exponential speed increase for finding eigenvalues and eigenvectors.*  
   https://arxiv.org/abs/quant-ph/9807070

2. Aspuru-Guzik, A. et al. *Simulated Quantum Computation of Molecular Energies.*  
   https://arxiv.org/abs/quant-ph/0604193

3. IBM Quantum Learning — Quantum Phase Estimation  
   https://quantum.cloud.ibm.com/learning/courses/utility-scale-quantum-computing/quantum-phase-estimation

4. IBM Quantum Learning — Introduction to quantum chemistry with qubit Hamiltonians  
   https://learning.quantum.ibm.com/

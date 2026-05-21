from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


NOTEBOOK_METADATA = {
    "kernelspec": {
        "display_name": ".venv",
        "language": "python",
        "name": "python3",
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.10",
    },
}


def markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": dedent(source).strip("\n").splitlines(keepends=True),
    }


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(source).strip("\n").splitlines(keepends=True),
    }


TEAM_A_IMPORTS = r"""
import os
import warnings
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd() / ".mpl-cache"))
Path(os.environ["MPLCONFIGDIR"]).mkdir(exist_ok=True)
os.environ.setdefault("XDG_CACHE_HOME", str(Path.cwd() / ".cache"))
Path(os.environ["XDG_CACHE_HOME"]).mkdir(exist_ok=True)
os.environ.setdefault("MPLBACKEND", "Agg")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import expm
from IPython.display import Markdown, display
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import QFTGate
from qiskit.circuit.library.generalized_gates import UnitaryGate

warnings.filterwarnings("ignore", message="FigureCanvasAgg is non-interactive, and thus cannot be shown")

np.set_printoptions(precision=5, suppress=True)
pd.options.display.float_format = "{:.6f}".format
plt.style.use("tableau-colorblind10")
"""


TEAM_B_IMPORTS = r"""
import os
import warnings
from fractions import Fraction
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path.cwd() / ".mpl-cache"))
Path(os.environ["MPLCONFIGDIR"]).mkdir(exist_ok=True)
os.environ.setdefault("XDG_CACHE_HOME", str(Path.cwd() / ".cache"))
Path(os.environ["XDG_CACHE_HOME"]).mkdir(exist_ok=True)
os.environ.setdefault("MPLBACKEND", "Agg")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Markdown, display
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import QFTGate
from qiskit.circuit.library.generalized_gates import UnitaryGate

warnings.filterwarnings("ignore", message="FigureCanvasAgg is non-interactive, and thus cannot be shown")

np.set_printoptions(precision=5, suppress=True)
pd.options.display.float_format = "{:.6f}".format
plt.style.use("tableau-colorblind10")
"""


def team_a_solution_cells() -> list[dict]:
    return [
        markdown_cell(
            r"""
            # Team A Solution — Molecular Spectrum Estimation with Quantum Phase Estimation

            We solve the workshop exactly in the reduced, self-contained setting:

            1. write down the three effective two-qubit molecular Hamiltonians,
            2. diagonalize them classically,
            3. build a QPE circuit for $\mathrm{H}_2$,
            4. recover an energy estimate from the dominant measured phase,
            5. repeat the same logic for $\mathrm{LiH}$ and $\mathrm{BeH}_2$.

            The central phase-to-energy relation is

            $$
            U' = e^{-i(H-sI)\tau},
            \qquad
            E = s - \frac{2\pi}{\tau}\phi.
            $$

            In this notebook, every major algebraic step is followed by the exact code used to implement it.
            """
        ),
        code_cell(TEAM_A_IMPORTS),
        markdown_cell(
            r"""
            ## Step 1 — Define the Pauli Matrices and the Molecular Coefficients

            Each molecule is modeled by

            $$
            H = c_{II}II + c_{ZI}ZI + c_{IZ}IZ + c_{ZZ}ZZ + c_{XX}XX.
            $$

            We first record the coefficients exactly as given in the workshop statement.
            """
        ),
        code_cell(
            r"""
            I = np.eye(2, dtype=complex)
            X = np.array([[0, 1], [1, 0]], dtype=complex)
            Z = np.array([[1, 0], [0, -1]], dtype=complex)

            h2_coeffs = {"II": -1.05, "ZI": 0.39, "IZ": 0.39, "ZZ": -0.01, "XX": 0.18}
            lih_coeffs = {"II": -2.20, "ZI": 0.18, "IZ": 0.12, "ZZ": -0.35, "XX": 0.28}
            beh2_coeffs = {"II": -3.60, "ZI": 0.25, "IZ": 0.31, "ZZ": -0.48, "XX": 0.41}

            coefficient_table = pd.DataFrame(
                [
                    ["H2", *h2_coeffs.values()],
                    ["LiH", *lih_coeffs.values()],
                    ["BeH2", *beh2_coeffs.values()],
                ],
                columns=["Molecule", "II", "ZI", "IZ", "ZZ", "XX"],
            )
            display(coefficient_table)
            """
        ),
        markdown_cell(
            r"""
            ## Step 2 — Build the Three Hamiltonian Matrices Explicitly

            Now we translate the coefficient dictionaries into actual $4\times 4$ matrices.

            This is the point where the abstract Pauli expansion becomes a concrete matrix eigenvalue problem.
            """
        ),
        code_cell(
            r"""
            H_h2 = (
                h2_coeffs["II"] * np.kron(I, I)
                + h2_coeffs["ZI"] * np.kron(Z, I)
                + h2_coeffs["IZ"] * np.kron(I, Z)
                + h2_coeffs["ZZ"] * np.kron(Z, Z)
                + h2_coeffs["XX"] * np.kron(X, X)
            )

            H_lih = (
                lih_coeffs["II"] * np.kron(I, I)
                + lih_coeffs["ZI"] * np.kron(Z, I)
                + lih_coeffs["IZ"] * np.kron(I, Z)
                + lih_coeffs["ZZ"] * np.kron(Z, Z)
                + lih_coeffs["XX"] * np.kron(X, X)
            )

            H_beh2 = (
                beh2_coeffs["II"] * np.kron(I, I)
                + beh2_coeffs["ZI"] * np.kron(Z, I)
                + beh2_coeffs["IZ"] * np.kron(I, Z)
                + beh2_coeffs["ZZ"] * np.kron(Z, Z)
                + beh2_coeffs["XX"] * np.kron(X, X)
            )

            print("H2 Hamiltonian:")
            print(H_h2)
            print("\nLiH Hamiltonian:")
            print(H_lih)
            print("\nBeH2 Hamiltonian:")
            print(H_beh2)
            """
        ),
        markdown_cell(
            r"""
            ## Step 3 — Diagonalize the Hamiltonians Classically

            Since QPE is an eigenvalue algorithm, the exact classical diagonalization is our benchmark.

            We extract:

            - the four exact energies for each molecule,
            - the ground-to-first-excited gap,
            - the overlap of the simple reference state $|11\rangle$ with the exact ground state.
            """
        ),
        code_cell(
            r"""
            h2_evals, h2_evecs = np.linalg.eigh(H_h2)
            lih_evals, lih_evecs = np.linalg.eigh(H_lih)
            beh2_evals, beh2_evecs = np.linalg.eigh(H_beh2)

            ket_11 = np.array([0, 0, 0, 1], dtype=complex)
            h2_overlaps = np.abs(h2_evecs.conj().T @ ket_11) ** 2
            lih_overlaps = np.abs(lih_evecs.conj().T @ ket_11) ** 2
            beh2_overlaps = np.abs(beh2_evecs.conj().T @ ket_11) ** 2

            spectrum_table = pd.DataFrame(
                [
                    ["H2", h2_evals[0], h2_evals[1], h2_evals[1] - h2_evals[0], h2_overlaps[0]],
                    ["LiH", lih_evals[0], lih_evals[1], lih_evals[1] - lih_evals[0], lih_overlaps[0]],
                    ["BeH2", beh2_evals[0], beh2_evals[1], beh2_evals[1] - beh2_evals[0], beh2_overlaps[0]],
                ],
                columns=["Molecule", "Ground energy", "1st excited", "Gap E1-E0", "Ground overlap of |11>"],
            )
            display(spectrum_table)

            level_table = pd.DataFrame(
                {
                    "Level": ["E0", "E1", "E2", "E3"],
                    "H2": h2_evals,
                    "LiH": lih_evals,
                    "BeH2": beh2_evals,
                }
            )
            display(level_table)
            """
        ),
        markdown_cell(
            r"""
            ## Step 4 — Visualize the Exact Spectra

            The left panel compares the exact energy levels across the three effective molecular models.

            The right panel shows why $|11\rangle$ is a good teaching-state choice: it already has strong ground-state overlap in all three models.
            """
        ),
        code_cell(
            r"""
            molecule_positions = np.arange(3)

            fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

            for level_index, level_name, color in zip(
                range(4),
                ["E0", "E1", "E2", "E3"],
                ["#1d4ed8", "#ea580c", "#0f766e", "#7c3aed"],
            ):
                axes[0].plot(
                    molecule_positions,
                    [h2_evals[level_index], lih_evals[level_index], beh2_evals[level_index]],
                    marker="o",
                    linewidth=2,
                    label=level_name,
                    color=color,
                )

            axes[0].set_xticks(molecule_positions, ["H2", "LiH", "BeH2"])
            axes[0].set_ylabel("Energy")
            axes[0].set_title("Exact energy spectra", loc="left")
            axes[0].grid(alpha=0.25)
            axes[0].legend()

            axes[1].bar(
                ["H2", "LiH", "BeH2"],
                [h2_overlaps[0], lih_overlaps[0], beh2_overlaps[0]],
                color=["#2563eb", "#ea580c", "#0f766e"],
            )
            axes[1].set_ylim(0, 1.05)
            axes[1].set_ylabel(r"$|\langle E_0 | 11 \rangle|^2$")
            axes[1].set_title("Ground-state support of |11>", loc="left")
            axes[1].grid(axis="y", alpha=0.25)

            fig.tight_layout()
            display(fig)
            plt.close(fig)
            """
        ),
        markdown_cell(
            r"""
            ## Step 5 — Shift the Hamiltonian for QPE

            QPE returns a phase, not an energy directly.

            To keep the phase map clean, we shift the Hamiltonian by a scalar:

            $$
            H' = H - sI,
            \qquad
            s = E_{\max} + 0.10.
            $$

            We use $\tau = 0.70$ and inspect the exact phases that should be seen for $\mathrm{H}_2$.
            """
        ),
        code_cell(
            r"""
            tau = 0.70
            phase_qubits = 6

            h2_shift = float(h2_evals.max() + 0.10)
            H_h2_shifted = H_h2 - h2_shift * np.eye(4)
            U_h2 = expm(-1j * H_h2_shifted * tau)
            h2_shifted_phases = -(h2_evals - h2_shift) * tau / (2 * np.pi)

            expected_phase_table = pd.DataFrame(
                {
                    "Level": ["E0", "E1", "E2", "E3"],
                    "Exact energy": h2_evals,
                    "Expected phase": h2_shifted_phases,
                }
            )
            display(expected_phase_table)
            """
        ),
        markdown_cell(
            r"""
            ## Step 6 — Build the Exact-Eigenstate QPE Circuit for $\mathrm{H}_2$

            This is the clean reference case:

            - the phase register starts in a uniform superposition,
            - the system register starts in the exact ground-state eigenvector,
            - controlled powers of $U' = e^{-i(H-sI)\tau}$ are applied,
            - inverse QFT decodes the phase into a bitstring.
            """
        ),
        code_cell(
            r"""
            h2_exact_qpe = QuantumCircuit(phase_qubits + 2)
            for q in range(phase_qubits):
                h2_exact_qpe.h(q)

            h2_exact_qpe.initialize(h2_evecs[:, 0], [phase_qubits, phase_qubits + 1])

            for q in range(phase_qubits):
                powered_gate = UnitaryGate(np.linalg.matrix_power(U_h2, 2**q), label=f"U^{2**q}")
                h2_exact_qpe.append(powered_gate.control(1), [q, phase_qubits, phase_qubits + 1])

            h2_exact_qpe.append(QFTGate(phase_qubits).inverse(), range(phase_qubits))

            print(h2_exact_qpe.draw(output="text"))
            """
        ),
        markdown_cell(
            r"""
            ## Step 7 — Run Exact-Eigenstate QPE and Decode the Energy

            If the input is an exact eigenstate, the histogram should collapse sharply onto one dominant phase bitstring.
            """
        ),
        code_cell(
            r"""
            h2_exact_statevector = Statevector.from_instruction(h2_exact_qpe)
            h2_exact_distribution = h2_exact_statevector.probabilities_dict(qargs=list(range(phase_qubits)))

            h2_exact_top = sorted(
                [(str(bitstring), float(probability)) for bitstring, probability in h2_exact_distribution.items()],
                key=lambda item: item[1],
                reverse=True,
            )[:8]

            h2_exact_rows = []
            for bitstring, probability in h2_exact_top:
                phase = int(bitstring, 2) / (2**phase_qubits)
                energy = h2_shift - (2 * np.pi / tau) * phase
                h2_exact_rows.append([bitstring, phase, probability, energy])

            h2_exact_table = pd.DataFrame(
                h2_exact_rows,
                columns=["Bitstring", "Phase", "Probability", "Recovered energy"],
            )
            display(h2_exact_table)

            fig, ax = plt.subplots(figsize=(8.5, 4.2))
            ax.bar(h2_exact_table["Bitstring"], h2_exact_table["Probability"], color="#2563eb")
            ax.set_title("H2 QPE histogram from exact ground-state initialization", loc="left")
            ax.set_xlabel("Measured phase bitstring")
            ax.set_ylabel("Probability")
            ax.grid(axis="y", alpha=0.25)
            plt.xticks(rotation=45)
            plt.tight_layout()
            display(fig)
            plt.close(fig)

            dominant_bitstring = h2_exact_table.loc[0, "Bitstring"]
            dominant_phase = h2_exact_table.loc[0, "Phase"]
            dominant_energy = h2_exact_table.loc[0, "Recovered energy"]
            dominant_probability = h2_exact_table.loc[0, "Probability"]

            display(Markdown(
                rf'''
                Dominant result:

                - bitstring: `{dominant_bitstring}`
                - phase: `{dominant_phase:.6f}`
                - probability: `{dominant_probability:.6f}`
                - recovered energy: `{dominant_energy:.6f}`
                - exact ground energy: `{h2_evals[0]:.6f}`
                - absolute error: `{abs(dominant_energy - h2_evals[0]):.6f}`
                '''
            ))
            """
        ),
        markdown_cell(
            r"""
            ## Step 8 — Build the Reference-State QPE Circuit from $|11\rangle$

            This is the more realistic teaching example: we no longer prepare an exact eigenvector.

            Instead, we begin with the simple computational basis state $|11\rangle$, so the QPE histogram reflects the decomposition

            $$
            |11\rangle = \sum_j c_j |E_j\rangle.
            $$
            """
        ),
        code_cell(
            r"""
            h2_reference_qpe = QuantumCircuit(phase_qubits + 2)
            for q in range(phase_qubits):
                h2_reference_qpe.h(q)

            h2_reference_qpe.x(phase_qubits)
            h2_reference_qpe.x(phase_qubits + 1)

            for q in range(phase_qubits):
                powered_gate = UnitaryGate(np.linalg.matrix_power(U_h2, 2**q), label=f"U^{2**q}")
                h2_reference_qpe.append(powered_gate.control(1), [q, phase_qubits, phase_qubits + 1])

            h2_reference_qpe.append(QFTGate(phase_qubits).inverse(), range(phase_qubits))

            print(h2_reference_qpe.draw(output="text"))
            """
        ),
        markdown_cell(
            r"""
            ## Step 9 — Run Reference-State QPE and Compare with Exact Overlaps

            Now the phase histogram should reveal the eigenstate weights of the reference state.

            We compare the observed QPE distribution with the exact overlap values $|\langle E_j|11\rangle|^2$.
            """
        ),
        code_cell(
            r"""
            h2_reference_statevector = Statevector.from_instruction(h2_reference_qpe)
            h2_reference_distribution = h2_reference_statevector.probabilities_dict(qargs=list(range(phase_qubits)))

            h2_reference_top = sorted(
                [(str(bitstring), float(probability)) for bitstring, probability in h2_reference_distribution.items()],
                key=lambda item: item[1],
                reverse=True,
            )[:8]

            h2_reference_rows = []
            for bitstring, probability in h2_reference_top:
                phase = int(bitstring, 2) / (2**phase_qubits)
                energy = h2_shift - (2 * np.pi / tau) * phase
                h2_reference_rows.append([bitstring, phase, probability, energy])

            h2_reference_table = pd.DataFrame(
                h2_reference_rows,
                columns=["Bitstring", "Phase", "Probability", "Recovered energy"],
            )
            display(h2_reference_table)

            overlap_table = pd.DataFrame(
                {
                    "Level": ["E0", "E1", "E2", "E3"],
                    "Exact energy": h2_evals,
                    "Overlap with |11>": h2_overlaps,
                }
            )
            display(overlap_table)

            fig, axes = plt.subplots(1, 2, figsize=(13, 4.2))

            axes[0].bar(h2_reference_table["Bitstring"], h2_reference_table["Probability"], color="#ea580c")
            axes[0].set_title("H2 QPE histogram from |11> initialization", loc="left")
            axes[0].set_xlabel("Measured phase bitstring")
            axes[0].set_ylabel("Probability")
            axes[0].grid(axis="y", alpha=0.25)
            axes[0].tick_params(axis="x", rotation=45)

            axes[1].bar(overlap_table["Level"], overlap_table["Overlap with |11>"], color="#0f766e")
            axes[1].set_ylim(0, 1.05)
            axes[1].set_title("Exact overlap of |11> with the H2 eigenbasis", loc="left")
            axes[1].set_ylabel("Weight")
            axes[1].grid(axis="y", alpha=0.25)

            fig.tight_layout()
            display(fig)
            plt.close(fig)
            """
        ),
        markdown_cell(
            r"""
            ## Step 10 — Repeat Ground-State QPE for $\mathrm{LiH}$ and $\mathrm{BeH}_2$

            We now run the same exact-eigenstate QPE logic for all three molecules and compare the recovered ground-state energies.

            We also track how the absolute error changes as the number of phase qubits increases from 4 to 7.
            """
        ),
        code_cell(
            r"""
            molecule_names = ["H2", "LiH", "BeH2"]
            hamiltonians = [H_h2, H_lih, H_beh2]
            eigenvalues = [h2_evals, lih_evals, beh2_evals]
            eigenvectors = [h2_evecs, lih_evecs, beh2_evecs]
            overlaps = [h2_overlaps, lih_overlaps, beh2_overlaps]

            summary_rows = []
            error_rows = []

            for molecule_name, H_matrix, evals, evecs, ref_overlaps in zip(
                molecule_names, hamiltonians, eigenvalues, eigenvectors, overlaps
            ):
                shift = float(evals.max() + 0.10)
                U_matrix = expm(-1j * (H_matrix - shift * np.eye(4)) * tau)

                qpe_circuit = QuantumCircuit(phase_qubits + 2)
                for q in range(phase_qubits):
                    qpe_circuit.h(q)
                qpe_circuit.initialize(evecs[:, 0], [phase_qubits, phase_qubits + 1])
                for q in range(phase_qubits):
                    powered_gate = UnitaryGate(np.linalg.matrix_power(U_matrix, 2**q), label=f"U^{2**q}")
                    qpe_circuit.append(powered_gate.control(1), [q, phase_qubits, phase_qubits + 1])
                qpe_circuit.append(QFTGate(phase_qubits).inverse(), range(phase_qubits))

                distribution = Statevector.from_instruction(qpe_circuit).probabilities_dict(qargs=list(range(phase_qubits)))
                dominant_bitstring, dominant_probability = max(
                    ((str(bitstring), float(probability)) for bitstring, probability in distribution.items()),
                    key=lambda item: item[1],
                )
                dominant_phase = int(dominant_bitstring, 2) / (2**phase_qubits)
                recovered_energy = shift - (2 * np.pi / tau) * dominant_phase

                summary_rows.append(
                    [
                        molecule_name,
                        evals[0],
                        dominant_bitstring,
                        dominant_phase,
                        recovered_energy,
                        abs(recovered_energy - evals[0]),
                        ref_overlaps[0],
                    ]
                )

                row = {"Molecule": molecule_name}
                for m in [4, 5, 6, 7]:
                    qpe_circuit = QuantumCircuit(m + 2)
                    for q in range(m):
                        qpe_circuit.h(q)
                    qpe_circuit.initialize(evecs[:, 0], [m, m + 1])
                    for q in range(m):
                        powered_gate = UnitaryGate(np.linalg.matrix_power(U_matrix, 2**q), label=f"U^{2**q}")
                        qpe_circuit.append(powered_gate.control(1), [q, m, m + 1])
                    qpe_circuit.append(QFTGate(m).inverse(), range(m))

                    distribution = Statevector.from_instruction(qpe_circuit).probabilities_dict(qargs=list(range(m)))
                    dominant_bitstring, dominant_probability = max(
                        ((str(bitstring), float(probability)) for bitstring, probability in distribution.items()),
                        key=lambda item: item[1],
                    )
                    dominant_phase = int(dominant_bitstring, 2) / (2**m)
                    recovered_energy = shift - (2 * np.pi / tau) * dominant_phase
                    row[f"{m} qubits"] = abs(recovered_energy - evals[0])

                error_rows.append(row)

            summary_table = pd.DataFrame(
                summary_rows,
                columns=[
                    "Molecule",
                    "Exact ground energy",
                    "Dominant bitstring",
                    "Phase",
                    "Recovered energy",
                    "Absolute error",
                    "Ground overlap of |11>",
                ],
            )
            display(summary_table)

            error_table = pd.DataFrame(error_rows)
            display(error_table)
            """
        ),
        markdown_cell(
            r"""
            ## Step 11 — Visual Comparison Across the Three Molecules

            The first panel compares the exact and recovered ground-state energies.

            The second panel shows how the QPE error changes with phase-register size.
            """
        ),
        code_cell(
            r"""
            fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

            x = np.arange(len(summary_table))
            width = 0.36

            axes[0].bar(x - width / 2, summary_table["Exact ground energy"], width=width, label="Exact", color="#334155")
            axes[0].bar(x + width / 2, summary_table["Recovered energy"], width=width, label="QPE", color="#2563eb")
            axes[0].set_xticks(x, summary_table["Molecule"])
            axes[0].set_title("Exact versus recovered ground-state energies", loc="left")
            axes[0].set_ylabel("Energy")
            axes[0].grid(axis="y", alpha=0.25)
            axes[0].legend()

            phase_sizes = [4, 5, 6, 7]
            for molecule_name, color in zip(["H2", "LiH", "BeH2"], ["#2563eb", "#ea580c", "#0f766e"]):
                row = error_table.loc[error_table["Molecule"] == molecule_name].iloc[0]
                axes[1].plot(
                    phase_sizes,
                    [row["4 qubits"], row["5 qubits"], row["6 qubits"], row["7 qubits"]],
                    marker="o",
                    linewidth=2,
                    label=molecule_name,
                    color=color,
                )

            axes[1].set_xticks(phase_sizes)
            axes[1].set_xlabel("Number of phase qubits")
            axes[1].set_ylabel("Absolute ground-state error")
            axes[1].set_title("QPE error versus phase-register size", loc="left")
            axes[1].grid(alpha=0.25)
            axes[1].legend()

            fig.tight_layout()
            display(fig)
            plt.close(fig)
            """
        ),
        markdown_cell(
            r"""
            ## Step 12 — Final Interpretation

            The workshop logic is now complete:

            - the molecular models are explicit,
            - the exact spectra are known,
            - QPE is implemented directly on the shifted time-evolution operator,
            - the recovered phase is converted back into an energy estimate,
            - the behavior across $\mathrm{H}_2$, $\mathrm{LiH}$, and $\mathrm{BeH}_2$ can be compared quantitatively.

            The main scientific lesson is unchanged:

            - QPE genuinely estimates eigenvalues through phase,
            - classical diagonalization is the correctness benchmark,
            - these reduced two-qubit models are pedagogically useful,
            - realistic chemistry remains hard because of state preparation and Hamiltonian simulation cost.
            """
        ),
    ]


def team_b_solution_cells() -> list[dict]:
    return [
        markdown_cell(
            r"""
            # Team B Solution — Translation Symmetry, Bloch Momentum, and the Order-Finding Core Behind Shor

            We solve the workshop in four explicit stages:

            1. build the translation operator and tight-binding Hamiltonian,
            2. verify the Bloch-momentum picture classically,
            3. use QFT as the position-to-momentum basis change,
            4. use QPE to recover the translation eigenphase and connect it to Shor’s order-finding logic.

            The key operator identities are

            $$
            T|j\rangle = |j+1 \bmod 8\rangle,
            \qquad
            T^8 = I,
            $$

            and the Bloch states satisfy

            $$
            T|k_n\rangle = e^{-i2\pi n/8}|k_n\rangle.
            $$
            """
        ),
        code_cell(TEAM_B_IMPORTS),
        markdown_cell(
            r"""
            ## Step 1 — Build the Translation Operator and the Tight-Binding Hamiltonian

            The physical system is an 8-site periodic ring with nearest-neighbor hopping amplitude $J=1$.

            We first write the matrices $T$ and $H$ explicitly in the site basis.
            """
        ),
        code_cell(
            r"""
            N = 8
            J = 1.0

            T = np.zeros((N, N), dtype=complex)
            for j in range(N):
                T[(j + 1) % N, j] = 1.0

            H = np.zeros((N, N), dtype=complex)
            for j in range(N):
                H[(j + 1) % N, j] -= J
                H[j, (j + 1) % N] -= J

            print("Translation operator T:")
            print(T)
            print("\nTight-binding Hamiltonian H:")
            print(H)
            """
        ),
        markdown_cell(
            r"""
            ## Step 2 — Construct the Bloch States and the Analytic Energies

            For each momentum label $n=0,\dots,7$, the Bloch state is

            $$
            |k_n\rangle = \frac{1}{\sqrt{8}}\sum_{j=0}^{7} e^{i2\pi nj/8}|j\rangle.
            $$

            The corresponding tight-binding energy is

            $$
            E_n = -2\cos\left(\frac{2\pi n}{8}\right).
            $$
            """
        ),
        code_cell(
            r"""
            bloch_states = []
            translation_eigenvalues = []
            analytic_energies = []

            for n in range(N):
                sites = np.arange(N)
                bloch_vector = np.exp(1j * 2 * np.pi * n * sites / N) / np.sqrt(N)
                bloch_states.append(bloch_vector)
                translation_eigenvalues.append(np.exp(-1j * 2 * np.pi * n / N))
                analytic_energies.append(-2 * J * np.cos(2 * np.pi * n / N))

            bloch_states = np.column_stack(bloch_states)
            translation_eigenvalues = np.array(translation_eigenvalues)
            analytic_energies = np.array(analytic_energies)

            translation_table = pd.DataFrame(
                {
                    "n": np.arange(N),
                    "Eigenvalue of T": translation_eigenvalues,
                    "Analytic energy": analytic_energies,
                }
            )
            display(translation_table)
            """
        ),
        markdown_cell(
            r"""
            ## Step 3 — Verify the Symmetry Relations Numerically

            The classical benchmark checks are:

            - $T^8 = I$,
            - $[H,T] = 0$,
            - the Bloch states line up with the exact Hamiltonian eigenvectors.
            """
        ),
        code_cell(
            r"""
            ring_checks = pd.DataFrame(
                [
                    ["||T^8 - I||", np.linalg.norm(np.linalg.matrix_power(T, 8) - np.eye(N))],
                    ["||[H,T]||", np.linalg.norm(H @ T - T @ H)],
                ],
                columns=["Check", "Value"],
            )
            display(ring_checks)

            H_evals, H_evecs = np.linalg.eigh(H)

            overlap_rows = []
            for n in range(N):
                overlaps = np.abs(H_evecs.conj().T @ bloch_states[:, n]) ** 2
                overlap_rows.append([n, analytic_energies[n], overlaps.max()])

            overlap_table = pd.DataFrame(
                overlap_rows,
                columns=["Momentum label n", "Analytic energy", "Best overlap with exact eigenbasis"],
            )
            display(overlap_table)
            """
        ),
        markdown_cell(
            r"""
            ## Step 4 — Visualize the Translation Spectrum

            The left panel places the translation eigenvalues on the complex unit circle.

            The right panel shows the tight-binding dispersion relation $E_n$ across the 8 allowed momentum labels.
            """
        ),
        code_cell(
            r"""
            fig, axes = plt.subplots(1, 2, figsize=(13, 5))

            axes[0].scatter(translation_eigenvalues.real, translation_eigenvalues.imag, s=90, color="#d97706")
            circle = plt.Circle((0, 0), 1.0, color="#cbd5e1", fill=False, linewidth=1.5)
            axes[0].add_patch(circle)
            for n, eig in enumerate(translation_eigenvalues):
                axes[0].text(eig.real + 0.04, eig.imag + 0.04, f"n={n}", fontsize=10)
            axes[0].axhline(0, color="#94a3b8", linewidth=1)
            axes[0].axvline(0, color="#94a3b8", linewidth=1)
            axes[0].set_aspect("equal")
            axes[0].set_xlim(-1.25, 1.25)
            axes[0].set_ylim(-1.25, 1.25)
            axes[0].set_title("Translation eigenvalues on the unit circle", loc="left")
            axes[0].set_xlabel("Real part")
            axes[0].set_ylabel("Imaginary part")

            axes[1].plot(np.arange(N), analytic_energies, marker="o", linewidth=2, color="#2563eb")
            axes[1].set_xticks(np.arange(N))
            axes[1].set_xlabel("Momentum label n")
            axes[1].set_ylabel("Energy")
            axes[1].set_title("Tight-binding dispersion", loc="left")
            axes[1].grid(alpha=0.25)

            fig.tight_layout()
            display(fig)
            plt.close(fig)
            """
        ),
        markdown_cell(
            r"""
            ## Step 5 — Use the QFT as the Momentum Transform

            A site-localized state does not have a sharp momentum label.

            The QFT converts site-basis information into momentum-basis amplitudes and phases, so we study:

            - $|3\rangle$,
            - the superposition $(|0\rangle + |1\rangle)/\sqrt{2}$.
            """
        ),
        code_cell(
            r"""
            qft_gate = QFTGate(3)

            site_state_3 = np.zeros(N, dtype=complex)
            site_state_3[3] = 1.0
            qft_of_site_3 = Statevector(site_state_3).evolve(qft_gate)

            qft_site_table = pd.DataFrame(
                {
                    "Momentum index": np.arange(N),
                    "Amplitude": qft_of_site_3.data,
                    "Probability": np.abs(qft_of_site_3.data) ** 2,
                    "Phase / pi": np.angle(qft_of_site_3.data) / np.pi,
                }
            )
            display(qft_site_table)

            superposition_state = (np.eye(N, dtype=complex)[0] + np.eye(N, dtype=complex)[1]) / np.sqrt(2)
            qft_of_superposition = Statevector(superposition_state).evolve(qft_gate)

            qft_superposition_table = pd.DataFrame(
                {
                    "Momentum index": np.arange(N),
                    "Probability": np.abs(qft_of_superposition.data) ** 2,
                    "Phase / pi": np.angle(qft_of_superposition.data) / np.pi,
                }
            )
            display(qft_superposition_table)
            """
        ),
        markdown_cell(
            r"""
            ## Step 6 — Plot the QFT Output Distributions

            We want to see both probabilities and phases.

            For a site state, the probability spread is flat, while the phase pattern carries the positional information.
            For a superposition state, interference changes the probability distribution itself.
            """
        ),
        code_cell(
            r"""
            fig, axes = plt.subplots(2, 2, figsize=(13, 7))

            axes[0, 0].bar(np.arange(N), np.abs(qft_of_site_3.data) ** 2, color="#d97706")
            axes[0, 0].set_title("QFT(|3>) probabilities", loc="left")
            axes[0, 0].set_ylabel("Probability")
            axes[0, 0].set_xticks(np.arange(N))
            axes[0, 0].grid(axis="y", alpha=0.25)

            axes[0, 1].bar(np.arange(N), np.angle(qft_of_site_3.data) / np.pi, color="#92400e")
            axes[0, 1].set_title("QFT(|3>) phases / π", loc="left")
            axes[0, 1].set_ylabel("Phase / π")
            axes[0, 1].set_xticks(np.arange(N))
            axes[0, 1].grid(axis="y", alpha=0.25)

            axes[1, 0].bar(np.arange(N), np.abs(qft_of_superposition.data) ** 2, color="#2563eb")
            axes[1, 0].set_title(r"QFT((|0\rangle + |1\rangle)/\sqrt{2}) probabilities", loc="left")
            axes[1, 0].set_xlabel("Momentum index")
            axes[1, 0].set_ylabel("Probability")
            axes[1, 0].set_xticks(np.arange(N))
            axes[1, 0].grid(axis="y", alpha=0.25)

            axes[1, 1].bar(np.arange(N), np.angle(qft_of_superposition.data) / np.pi, color="#1d4ed8")
            axes[1, 1].set_title(r"QFT((|0\rangle + |1\rangle)/\sqrt{2}) phases / π", loc="left")
            axes[1, 1].set_xlabel("Momentum index")
            axes[1, 1].set_ylabel("Phase / π")
            axes[1, 1].set_xticks(np.arange(N))
            axes[1, 1].grid(axis="y", alpha=0.25)

            fig.tight_layout()
            display(fig)
            plt.close(fig)
            """
        ),
        markdown_cell(
            r"""
            ## Step 7 — Build the QPE Circuit for a Known Bloch State

            We choose the Bloch sector $n=3$.

            Since

            $$
            T|k_3\rangle = e^{-i2\pi\cdot 3/8}|k_3\rangle,
            $$

            QPE should return

            $$
            \phi = -\frac{3}{8}\pmod 1 = \frac{5}{8}.
            $$
            """
        ),
        code_cell(
            r"""
            phase_qubits = 6
            target_n = 3
            target_bloch_state = bloch_states[:, target_n]

            qpe_translation = QuantumCircuit(phase_qubits + 3)
            for q in range(phase_qubits):
                qpe_translation.h(q)

            qpe_translation.initialize(target_bloch_state, [phase_qubits, phase_qubits + 1, phase_qubits + 2])

            for q in range(phase_qubits):
                powered_gate = UnitaryGate(np.linalg.matrix_power(T, 2**q), label=f"T^{2**q}")
                qpe_translation.append(powered_gate.control(1), [q, phase_qubits, phase_qubits + 1, phase_qubits + 2])

            qpe_translation.append(QFTGate(phase_qubits).inverse(), range(phase_qubits))

            print(qpe_translation.draw(output="text"))
            """
        ),
        markdown_cell(
            r"""
            ## Step 8 — Run QPE and Decode the Phase

            We now extract the phase-register distribution and translate the dominant phase back into the momentum label.
            """
        ),
        code_cell(
            r"""
            translation_distribution = Statevector.from_instruction(qpe_translation).probabilities_dict(qargs=list(range(phase_qubits)))

            translation_top = sorted(
                [(str(bitstring), float(probability)) for bitstring, probability in translation_distribution.items()],
                key=lambda item: item[1],
                reverse=True,
            )[:8]

            translation_rows = []
            for bitstring, probability in translation_top:
                phase = int(bitstring, 2) / (2**phase_qubits)
                inferred_n = (-round(phase * N)) % N
                exact_fraction = Fraction(int(bitstring, 2), 2**phase_qubits).limit_denominator(8)
                translation_rows.append([bitstring, phase, probability, inferred_n, str(exact_fraction)])

            translation_qpe_table = pd.DataFrame(
                translation_rows,
                columns=["Bitstring", "Phase", "Probability", "Recovered n", "Phase as fraction"],
            )
            display(translation_qpe_table)

            fig, ax = plt.subplots(figsize=(8.5, 4.2))
            ax.bar(translation_qpe_table["Bitstring"], translation_qpe_table["Probability"], color="#0f766e")
            ax.set_title("QPE histogram for the Bloch state with n = 3", loc="left")
            ax.set_xlabel("Measured phase bitstring")
            ax.set_ylabel("Probability")
            ax.grid(axis="y", alpha=0.25)
            plt.xticks(rotation=45)
            plt.tight_layout()
            display(fig)
            plt.close(fig)

            dominant_row = translation_qpe_table.iloc[0]
            display(Markdown(
                rf'''
                Dominant result:

                - bitstring: `{dominant_row['Bitstring']}`
                - phase: `{dominant_row['Phase']:.6f} = {dominant_row['Phase as fraction']}`
                - recovered momentum label: `{int(dominant_row['Recovered n'])}`

                This matches the prepared Bloch state with $n=3$.
                '''
            ))
            """
        ),
        markdown_cell(
            r"""
            ## Step 9 — Use a Superposition of Momentum Sectors

            Finally, we prepare a superposition of two Bloch states.

            The purpose is to show that QPE resolves the finite-order phase structure into multiple peaks, exactly as one expects in order-finding problems.
            """
        ),
        code_cell(
            r"""
            mixed_state = (bloch_states[:, 2] + bloch_states[:, 5]) / np.sqrt(2)

            mixed_qpe = QuantumCircuit(phase_qubits + 3)
            for q in range(phase_qubits):
                mixed_qpe.h(q)

            mixed_qpe.initialize(mixed_state, [phase_qubits, phase_qubits + 1, phase_qubits + 2])

            for q in range(phase_qubits):
                powered_gate = UnitaryGate(np.linalg.matrix_power(T, 2**q), label=f"T^{2**q}")
                mixed_qpe.append(powered_gate.control(1), [q, phase_qubits, phase_qubits + 1, phase_qubits + 2])

            mixed_qpe.append(QFTGate(phase_qubits).inverse(), range(phase_qubits))

            mixed_distribution = Statevector.from_instruction(mixed_qpe).probabilities_dict(qargs=list(range(phase_qubits)))

            mixed_top = sorted(
                [(str(bitstring), float(probability)) for bitstring, probability in mixed_distribution.items()],
                key=lambda item: item[1],
                reverse=True,
            )[:10]

            mixed_rows = []
            for bitstring, probability in mixed_top:
                phase = int(bitstring, 2) / (2**phase_qubits)
                inferred_n = (-round(phase * N)) % N
                mixed_rows.append([bitstring, phase, probability, inferred_n])

            mixed_table = pd.DataFrame(
                mixed_rows,
                columns=["Bitstring", "Phase", "Probability", "Recovered n"],
            )
            display(mixed_table)
            """
        ),
        markdown_cell(
            r"""
            ## Step 10 — Plot the Superposition Histogram and State the Shor Analogy

            The superposition histogram is the visual cue that this is a finite-order phase problem.

            The structural comparison with Shor is:

            - a finite-order unitary,
            - rational eigenphases,
            - QPE to recover the phase,
            - classical inference of the hidden order.
            """
        ),
        code_cell(
            r"""
            comparison_table = pd.DataFrame(
                [
                    ["Unitary", "Spatial translation T", "Modular multiplication U_a"],
                    ["Finite order", "T^8 = I", "U_a^r = I on the cyclic subspace"],
                    ["Eigenphases", "-n/8 mod 1", "s/r"],
                    ["Quantum primitive", "QPE on T", "QPE on modular multiplication"],
                    ["Recovered structure", "Momentum / order 8", "Order r"],
                ],
                columns=["Feature", "Translation ring", "Shor core"],
            )
            display(comparison_table)

            fig, ax = plt.subplots(figsize=(8.5, 4.2))
            ax.bar(mixed_table["Bitstring"], mixed_table["Probability"], color="#7c3aed")
            ax.set_title("QPE histogram for a superposition of two momentum sectors", loc="left")
            ax.set_xlabel("Measured phase bitstring")
            ax.set_ylabel("Probability")
            ax.grid(axis="y", alpha=0.25)
            plt.xticks(rotation=45)
            plt.tight_layout()
            display(fig)
            plt.close(fig)
            """
        ),
        markdown_cell(
            r"""
            ## Step 11 — Final Interpretation

            We have now completed the workshop step by step:

            1. the translation symmetry was written explicitly,
            2. the Bloch basis was verified numerically,
            3. the QFT was shown as a genuine momentum transform,
            4. QPE recovered the translation phase,
            5. the superposition case exposed the same multi-peak logic that underlies Shor’s order-finding core.

            The conceptual conclusion is precise:

            > Shor’s core is not special because it is about arithmetic.  
            > It is special because it is a phase-estimation method for a finite-order unitary.

            Translation symmetry on a periodic ring is one of the cleanest physics examples of that structure.
            """
        ),
    ]


def write_notebook(path: Path, cells: list[dict]) -> None:
    notebook = {
        "cells": cells,
        "metadata": NOTEBOOK_METADATA,
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    workshop_dir = Path(__file__).resolve().parent
    outputs = {
        workshop_dir / "team_a_qpe_molecular_spectrum_solution.ipynb": team_a_solution_cells(),
        workshop_dir / "team_b_translation_symmetry_order_finding_solution.ipynb": team_b_solution_cells(),
    }
    for path, cells in outputs.items():
        write_notebook(path, cells)
        print(f"Generated {path.relative_to(workshop_dir.parent)}")


if __name__ == "__main__":
    main()

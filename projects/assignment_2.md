# Asian Option Pricing Using Quantum Amplitude Estimation

## Introduction

Derivatives portfolio management is a critical task for banks, funds, and other financial institutions. Accurate and timely pricing of derivative products is essential for risk management, hedging, and trading decisions.

Asian options are a representative example of path-dependent derivatives whose fair pricing often relies on Monte Carlo simulation. This approach is flexible and widely used in practice, but it can become computationally expensive, especially when pricing must be repeated many times per day across large portfolios or under many market scenarios.

The core computational challenge is therefore one of statistical estimation: given a stochastic model of the underlying asset, estimate the expected discounted payoff of the option with sufficient accuracy. This makes Asian option pricing a natural candidate for studying Quantum Amplitude Estimation (QAE), one of the best-known quantum alternatives to classical Monte Carlo methods.

The purpose of this challenge is to investigate the potential advantages and limitations of quantum computing for fast and accurate Asian option pricing, with the main focus on Quantum Amplitude Estimation.

## Quantum Perspective

Decomposing the problem of Asian option pricing, the most relevant tasks are:

1. Identify how the option-pricing problem can be formulated as an expectation-estimation problem.
2. Study the classical Monte Carlo baseline, including its computational complexity and practical bottlenecks.
3. Investigate whether Quantum Amplitude Estimation can provide a meaningful asymptotic advantage for estimating the expected payoff.
4. Assess the practical feasibility of the solution, including circuit depth, qubit requirements, and the hardware assumptions needed for any potential advantage.

The key observation is that Asian option pricing is naturally expressed as an expected value under a probability distribution over asset paths. Classical Monte Carlo approximates this expectation using repeated sampling. QAE is relevant because it can, in principle, reduce the number of required oracle calls from `O(1/epsilon^2)` to `O(1/epsilon)` for additive error `epsilon`, assuming ideal quantum access to the relevant probability distribution and payoff function.

For a discretely monitored Asian call option, a standard mathematical formulation is:

```text
Price = exp(-rT) * E[max((1/M) * sum_{i=1}^M S_i - K, 0)]
```

where:

1. `r` is the risk-free rate,
2. `T` is the maturity,
3. `S_i` is the asset price at observation time `i`,
4. `M` is the number of monitoring dates,
5. `K` is the strike price.

This makes the computational core of the assignment an expectation-estimation problem rather than a prediction or model-training problem.

## Classical Monte Carlo Pricing

An Asian option is a type of option whose payoff depends on the average price of the underlying asset over a set of observation times, rather than only on the terminal price. For example, for an arithmetic-average Asian call option, the payoff can be written as:

```text
payoff = max((1/M) * sum_{i=1}^M S_i - K, 0)
```

where:

1. `S_i` is the asset price at observation time `i`,
2. `M` is the number of observation dates,
3. `K` is the strike price.

The fair price is the discounted expectation of this payoff under the chosen pricing model. In the classical setting, this is typically estimated by:

1. sampling many asset-price paths,
2. computing the payoff for each path,
3. averaging the discounted payoffs.

This method is robust and general, but its convergence rate is slow. To achieve additive error `epsilon`, Monte Carlo typically requires `O(1/epsilon^2)` samples.

## Quantum Alternative: QAE

Quantum Amplitude Estimation is one of the most studied quantum algorithms for accelerating Monte Carlo-type estimation tasks. In the context of Asian option pricing, the target quantity is the expected payoff or a suitably normalized version of it.

At a high level, the quantum workflow should:

1. encode the probability distribution of asset-price paths,
2. compute the payoff associated with each path,
3. map the normalized payoff into an amplitude,
4. use QAE to estimate that amplitude, and
5. recover the option price from the estimated amplitude.

This makes QAE a natural fit for the problem. The core difficulty here is not prediction from data or model training, but efficient estimation of an expectation. That is why QAE should be the primary algorithmic direction in this assignment.

## Suggested Project Scope

For this use case, we propose the following workflow:

1. Define a simplified Asian option pricing problem, for example under a Black-Scholes-style model with discretized time steps.
2. Implement a classical Monte Carlo baseline for pricing the option.
3. Formulate the pricing problem as an amplitude-estimation task by specifying how the distribution over price paths is encoded, how the payoff is computed, and how the payoff is normalized into a quantum amplitude.
4. Implement a proof-of-concept quantum workflow, either as a small circuit simulation, a pseudocode-level oracle construction, or a resource-estimation study if full simulation is too costly.
5. Prepare a feasibility study for the proposed approach, assuming the selected quantum method.
6. Prepare a short pitch or presentation describing the solution, assumptions, and expected value.

You may start from a simplified model with:

1. a small number of time steps,
2. a discretized distribution over asset returns,
3. a normalized payoff function,
4. a small instance that is easy to explain and simulate.

## Solution Properties

The feasibility study should contain:

1. Executive summary, a clear one-pager describing the points below.
2. Mathematical problem definition.
3. Overview of classical tools used to solve the given problem, including theoretical computational complexity, performance estimate, and bottlenecks.
4. Overview of quantum algorithms suitable for the given problem, with emphasis on QAE, including a system-design exercise, computational complexity comparison to classical Monte Carlo, resource estimates, and a feasibility horizon in years.
5. Estimate of economic viability as a roadmap, with projected hardware expectations for the technology and the accuracy required.

The success of your proof-of-concept implementation will be evaluated based on achieving one or more of the following milestones:

1. Implement an Asian option pricing workflow using quantum computing methods centered on Quantum Amplitude Estimation.
2. Demonstrate consistency with a classical pricing baseline, such as Monte Carlo simulation, up to a tolerable approximation error.
3. Provide a correct mapping from expected payoff estimation to the QAE formalism.
4. Compare the theoretical scaling of the classical and quantum approaches.
5. Provide a realistic assessment of the assumptions under which a quantum advantage could emerge.

## References

1. Nikitas Stamatopoulos et al. "Option Pricing using Quantum Computers". In: Quantum 4 (2020), p. 291. doi: https://doi.org/10.22331/q-2020-07-06-291
2. Daniel J. Egger et al. "Quantum Computing for Finance: State of the Art and Future Prospects". IEEE Transactions on Quantum Engineering 1 (2020). doi: https://doi.org/10.1109/TQE.2020.3030314
3. Steven Herbert. "A threshold for quantum advantage in derivative pricing". Quantum 5 (2021), p. 513. https://quantum-journal.org/papers/q-2021-06-01-463/pdf
4. Brassard, Gilles, Peter Hoyer, Michele Mosca, and Alain Tapp. "Quantum Amplitude Amplification and Estimation." Contemporary Mathematics 305 (2002). https://arxiv.org/abs/quant-ph/0005055
5. Montanaro, Ashley. "Quantum speedup of Monte Carlo methods." Proceedings of the Royal Society A 471.2181 (2015): 20150301. https://pmc.ncbi.nlm.nih.gov/articles/PMC4614442/
6. Carrera Vazquez, Adrián, and Stefan Woerner. "Efficient State Preparation for Quantum Amplitude Estimation." Physical Review Applied 15, 034027 (2021). https://journals.aps.org/prapplied/abstract/10.1103/PhysRevApplied.15.034027

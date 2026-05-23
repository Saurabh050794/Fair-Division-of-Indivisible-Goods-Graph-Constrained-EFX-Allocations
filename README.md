# Fair Division of Indivisible Goods

**M.Tech Project — Computing and Mathematics**  
**Indian Institute of Technology Palakkad**  
**Author:** Saurabh Kumar (112402005)  
**Supervisor:** Dr. Pratik Ghosal, Dept. of Computer Science & Engineering, IIT Palakkad  
**Submitted:** May 2026

---

## Overview

This project investigates the fair allocation of indivisible goods among agents whose interactions are restricted by a graph structure. The central fairness concept studied is **EFX (Envy-Freeness up to Any Good)** — one of the strongest and most studied relaxations of envy-freeness for discrete settings.

In the **Graph-EFX** model, agents are represented as vertices in a graph and fairness is only enforced between neighboring agents (connected by edges). This captures real-world settings such as social networks, hierarchical organizations, and geographically distributed groups.

---

## Problem Statement

Given:
- A set of **n agents** with additive valuation functions
- A set of **m indivisible goods**
- An **envy graph** G = (N, E) representing which agent pairs must satisfy fairness

Find an allocation A = (A₁, ..., Aₙ) such that for every edge (i, j) ∈ E and every good g ∈ Aⱼ:

> vᵢ(Aᵢ) ≥ vᵢ(Aⱼ \ {g})   **(Graph-EFX condition)**

---

## Fairness Concepts Covered

| Concept | Definition |
|---|---|
| **EF** (Envy-Free) | Every agent values their bundle at least as much as any other |
| **EF1** (Envy-Free up to 1 Good) | Envy eliminated by removing *some* good from the envied bundle |
| **EFX** (Envy-Free up to Any Good) | Envy eliminated by removing *any* good from the envied bundle |
| **MNW** (Maximum Nash Welfare) | Maximizes product of utilities; known to guarantee EF1 + Pareto optimality |
| **MMS** (Maximin Share) | Each agent receives at least what they'd guarantee themselves by dividing goods into n bundles |
| **Graph-EFX** | EFX enforced only between graph-adjacent agents |

---

## Algorithms Implemented

### 1. Classical Algorithms (Phase 1)
- **Round-Robin** — Guarantees EF1; agents pick in turns
- **Envy-Cycle Elimination (ECE)** — Guarantees EF1; eliminates directed envy cycles
- **Leximin++** — Guarantees EFX under identical valuations

### 2. Graph-Constrained Algorithms (Phase 2)

#### Sweeping Algorithm (Path Graphs)
Computes a G-EFX allocation on a **path graph Pₙ**:
1. Initialize: all goods assigned to agent 1
2. Repeat until no strong envy exists:
   - **Forward sweep** (left → right): apply `LocalEFX` on each adjacent pair
   - **Backward sweep** (right → left): apply `LocalEFX` on each adjacent pair
3. Return allocation if no strong envy remains; else report failure

#### Tree-Based EFX Algorithm (Proposed)
Extends the sweeping approach to arbitrary **tree graphs** using DFS traversal:
1. Initialize: all goods assigned to root agent
2. Compute DFS pre-order and post-order edge sequences
3. Repeat until no strong envy exists:
   - **Forward pass** (root → leaves): apply `LocalEFX` along DFS pre-order edges
   - **Backward pass** (leaves → root): apply `LocalEFX` along DFS post-order edges
4. Return G-EFX allocation or report failure

Both algorithms use a shared `LocalEFX` subroutine — a greedy two-agent EFX procedure based on the cut-and-choose principle.

---

## Key Theoretical Results

- **EFX always exists** for two agents (divide-and-choose), three agents (pseudo-polynomial), identical valuations (Leximin++), bi-valued valuations, and ordered valuations (ECE)
- **MNW allocations** are both EF1 and Pareto optimal (Caragiannis et al.)
- **Graph-EFX** is guaranteed to exist on star graphs, path graphs (P₄), core-outer structures, and graphs with diameter ≥ 4 (for mixed goods/chores under lexicographic valuations)
- General EFX existence for arbitrary graphs and valuations remains **open**

---

## Repository Structure

```
fair-division-efx/
│
├── phase1_report.pdf          # Phase 1: Classical fair division (EF1, EFX, MNW)
├── phase2_report.pdf          # Phase 2: Graph-constrained EFX, algorithms, results
│
├── sweeping_algorithm.py      # Sweeping Algorithm for path graphs
├── tree_efx_algorithm.py      # Tree-Based EFX Allocation Algorithm
│
└── README.md
```

---

## How to Run

### Requirements
- Python 3.x (no external libraries required)

### Sweeping Algorithm (Path Graph)

```bash
python sweeping_algorithm.py
```

You will be prompted to enter:
- Number of agents `n`
- Number of goods `m`

Valuations are randomly generated. The algorithm prints each iteration's forward/backward sweeps, envy checks, and the final allocation.

**Sample Output:**
```
Number of agents (n): 3
Number of goods  (m): 4

Goods : {g1, g2, g3, g4}
Agents: {Agent-1, Agent-2, Agent-3}

Valuations:
  Agent 1:  {'g1': 8, 'g2': 5, 'g3': 3, 'g4': 1}
  Agent 2:  {'g1': 4, 'g2': 9, 'g3': 6, 'g4': 2}
  Agent 3:  {'g1': 7, 'g2': 3, 'g3': 5, 'g4': 8}

...

Success: Strong envy eliminated.

========================================
FINAL ALLOCATION
========================================
Agent 1 gets: {'g1'}
  Value: 8
Agent 2 gets: {'g2', 'g3'}
  Value: 15
Agent 3 gets: {'g4'}
  Value: 8
```

### Tree-Based EFX Algorithm

```bash
python tree_efx_algorithm.py
```

You will be prompted to enter:
- Number of agents `n`
- Number of goods `m`

A random tree is generated automatically. The algorithm prints the tree structure, DFS traversal order, each iteration's passes, envy checks, and the final allocation.

---

## Correctness Guarantees

- **Sweeping Algorithm:** If it terminates, the output is a valid G-EFX allocation for the path graph (correctness proven; termination open in general).
- **Tree Algorithm:** If it terminates, the output is a valid G-EFX allocation for the tree graph (correctness proven; full termination proof is an open problem).
- Both algorithms detect failure (stuck state) and report it explicitly.

---

## Open Problems

- Proving **termination** of both algorithms under all inputs (a strictly decreasing potential function is unknown)
- Existence of EFX allocations on **arbitrary graphs** under general valuations
- Efficient EFX computation for **submodular** valuations
- Complexity of deciding whether a G-EFX allocation exists for a given graph

---

## References

1. Plaut, B. and Roughgarden, T. *Almost Envy-Freeness with General Valuations.* SIAM Journal on Discrete Mathematics, 2020.
2. Caragiannis, I. et al. *The Unreasonable Fairness of Maximum Nash Welfare.* ACM Transactions on Economics and Computation, 2019.
3. Chaudhury, B. R. et al. *EFX Exists for Three Agents.* ACM EC, 2020.
4. Payan, A., Sengupta, S., and Viswanathan, K. *Graph-Constrained Fair Division.* 2022.
5. Hosseini, H., Searns, A., and Segal-Halevi, E. *Fair Division of Indivisible Goods Under Constraints.* IJCAI, 2022.
6. Mahara, R. *Extension of Additive Valuations to General Valuations on the Existence of EFX.* Preprint, 2021.

---

## License

This project was developed as an M.Tech thesis at IIT Palakkad. Feel free to use the code for academic and research purposes with appropriate attribution.

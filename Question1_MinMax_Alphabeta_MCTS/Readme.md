# Game Search Algorithms Implementation for Tic-Tac-Toe

A Python implementation of four classical Artificial Intelligence (AI) game-tree search algorithms using **Tic-Tac-Toe** as the test environment. The project demonstrates how different search techniques make decisions in adversarial games and compares their performance.

## Implemented Algorithms

### 1. Minimax Search
The Minimax algorithm explores the complete game tree and assumes both players play optimally.

**Features**
- Exhaustive search
- Guaranteed optimal move
- No pruning

**Complexity**
- Time: O(b^d)
- Space: O(d)

Where:
- `b` = branching factor
- `d` = search depth

---

### 2. Alpha-Beta Pruning
An optimized version of Minimax that eliminates branches that cannot influence the final decision.

**Features**
- Produces the same result as Minimax
- Explores fewer nodes
- Faster execution

**Complexity**
- Worst Case: O(b^d)
- Best Case: O(b^(d/2))

---

### 3. Heuristic Alpha-Beta Search
A depth-limited Alpha-Beta search that uses a heuristic evaluation function when the cutoff depth is reached.

**Features**
- Suitable for larger game trees
- Configurable search depth
- Uses board evaluation instead of exhaustive search

**Heuristic Evaluation**
- +10 : X has two in a row and one empty cell
- -10 : O has two in a row and one empty cell
- +1 : X has one mark in a line
- -1 : O has one mark in a line
- 0 : Blocked line

---

### 4. Monte Carlo Tree Search (MCTS)
A probabilistic search algorithm that builds a partial game tree through repeated simulations.

**MCTS Phases**
1. Selection
2. Expansion
3. Simulation (Rollout)
4. Backpropagation

**Features**
- No heuristic required
- Anytime algorithm
- Widely used in modern game AI

---

## Project Structure

```text
game_search_algorithms.py

├── TicTacToe
│   ├── Game State Representation
│   ├── Move Generation
│   ├── Winner Detection
│   └── Terminal State Checking
│
├── MinimaxSearch
├── AlphaBetaSearch
├── HeuristicAlphaBetaSearch
├── MCTSNode
├── MCTSSearch
│
├── run_tests()
└── performance_comparison()
```

---

## Requirements

- Python 3.8+
- No external dependencies

Standard libraries used:

```python
math
random
time
copy
collections
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/game-search-algorithms.git
cd game-search-algorithms
```

---

## Usage

Run the program:

```bash
python game_search_algorithms.py
```

The script automatically executes:

```python
run_tests()
performance_comparison()
```

---

## Example Output

```text
============================================================
RUNNING TEST SUITE
============================================================

[PASS] TTT: X wins top row
[PASS] TTT: O wins left column
[PASS] Minimax: value = +1
[PASS] AlphaBeta: same value as Minimax
...

============================================================
RESULTS: ALL TESTS PASSED
============================================================
```

---

## Performance Comparison

The program compares:

- Best move selected
- Evaluation value
- Nodes explored
- Execution time

Example:

```text
Minimax                  nodes=549946
Alpha-Beta               nodes=18296
Heuristic AB (d=4)       nodes=500
MCTS (2000 iters)        nodes=2000
```

This demonstrates how pruning and heuristics significantly reduce computational cost.

---

## Testing

The included test suite verifies:

### Tic-Tac-Toe Engine
- Winner detection
- Draw detection
- Legal move generation
- Terminal state detection

### Minimax
- Optimal move selection
- Winning move discovery
- Blocking opponent wins

### Alpha-Beta
- Consistency with Minimax
- Reduced node exploration

### Heuristic Alpha-Beta
- Correct heuristic evaluation
- Depth-limited functionality

### MCTS
- Legal move generation
- Winning move selection
- Blocking opponent threats
- Performance against random players

---

## Learning Objectives

This project is useful for understanding:

- Adversarial Search
- Game Trees
- Minimax Algorithm
- Alpha-Beta Pruning
- Heuristic Evaluation Functions
- Monte Carlo Tree Search (MCTS)
- Artificial Intelligence in Board Games

---

## References

1. Russell, S. & Norvig, P. *Artificial Intelligence: A Modern Approach*
2. Kocsis, L. & Szepesvári, C. *Bandit Based Monte-Carlo Planning (2006)*
3. Classical Game Tree Search Literature

---

## Author

Developed as an educational implementation of classical AI game search algorithms using Tic-Tac-Toe as a benchmark environment.

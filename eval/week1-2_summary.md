# AI Chess Bot — Phase 0 Evaluation Summary

## 1. Objective

Phase 0 establishes a working Python chess environment and two reproducible baseline agents before neural-network training:

- **Random Bot:** selects a uniformly random legal move.
- **Material Minimax Bot:** uses a material-count heuristic and a **2-ply minimax search**, selecting the move with the best worst-case material evaluation.

The primary question is whether shallow search with a simple evaluation function can outperform random legal moves.

## 2. Implementation

| Component | Role |
|---|---|
| `search/random_bot.py` | Random legal move selection via `python-chess` |
| `eval/material.py` | Material-only position evaluation (positive favors White) |
| `search/minimax.py` | Two-ply minimax search and move selection |
| `main.py` | Runs an individual game between agents |
| `eval/random_baseline.py` | Random-versus-random self-play evaluation |
| `eval/minimax_baseline.py` | Minimax-versus-random head-to-head tournament |
| `tests/` | Correctness and Stockfish integration tests |

The material heuristic uses piece values of pawn = 100, knight = 320, bishop = 330, rook = 500, and queen = 900. Minimax uses large terminal scores for checkmate and zero for draws. The head-to-head tournament alternates the minimax agent's color every game.

## 3. Experimental Setup

Two distinct experiments were run, each consisting of **100 games**:

1. **Random self-play:** Random Bot versus Random Bot, to check basic functionality and characterize game outcomes.
2. **Head-to-head:** 2-ply Material Minimax Bot versus Random Bot, with Minimax playing White in 50 games and Black in 50 games.

The scripts record game result, termination reason, game length in plies, and time spent selecting moves. The results below are calculated from the supplied CSV exports, `random_baseline_results.csv` and `minimax_baseline_results.csv`.

**Interpretation note:** The two datasets are different experimental conditions. Random self-play describes baseline behavior; the direct head-to-head experiment measures the minimax agent's performance against Random.

## 4. Random Bot Self-Play Results

| Metric | Result |
|---|---:|
| Games completed | 100 |
| White wins | 10 (10%) |
| Black wins | 5 (5%) |
| Draws | 85 (85%) |
| Average game length | 346.83 plies |
| Median game length | 359.50 plies |
| Minimum / maximum game length | 76 / 610 plies |
| Mean White move-selection time | 0.0301 ms |
| Mean Black move-selection time | 0.0312 ms |

### Game termination reasons

| Termination | Games | Share |
|---|---:|---:|
| Insufficient material | 47 | 47% |
| Fifty-move rule | 18 | 18% |
| Threefold repetition | 15 | 15% |
| Checkmate | 15 | 15% |
| Stalemate | 5 | 5% |
| **Total** | **100** | **100%** |

**Interpretation.** Most random-versus-random games ended in draws (85%), especially because of insufficient material (47%). Without purposeful attacking or checkmating play, random games often continue until a draw condition is reached. The 15 checkmates demonstrate that random legal play can occasionally produce a decisive result, but this experiment does **not** measure strength against a strategic opponent.

## 5. Minimax vs. Random Results

| Metric | Result |
|---|---:|
| Games completed | 100 |
| Minimax wins | 100 (100%) |
| Random wins | 0 (0%) |
| Draws | 0 (0%) |
| Minimax as White | 50 games, 50 wins |
| Minimax as Black | 50 games, 50 wins |
| Average game length | 64.86 plies |
| Median game length | 55.50 plies |
| Minimum / maximum game length | 5 / 205 plies |
| Checkmate terminations | 100 (100%) |
| Mean Minimax move-selection time | 270.66 ms |
| Mean Random move-selection time | 0.0558 ms |
| Total recorded Minimax move-selection time | 884.50 s |
| Total recorded Random move-selection time | 0.18 s |

### Score rate

Chess score rate counts one point per win and half a point per draw:

\[
\text{Score Rate} = \frac{\text{Wins} + 0.5\times\text{Draws}}{\text{Games}}
\]

For Minimax, this is `(100 + 0.5 × 0) / 100 = 1.00`, or **100%**.

**Interpretation.** The 2-ply material-based minimax agent defeated the random agent in every recorded head-to-head game, regardless of color. All games ended in checkmate. This is strong evidence that material evaluation plus shallow lookahead provides a decisive advantage over random legal move selection in this test setting. It does not establish the bot's Elo rating or imply that it would perform similarly against stronger opponents.

## 6. Comparative Analysis

| Metric | Random vs. Random | Minimax vs. Random |
|---|---:|---:|
| Games | 100 | 100 |
| Draws | 85 | 0 |
| Checkmates | 15 | 100 |
| Average plies per game | 346.83 | 64.86 |

Games in the head-to-head tournament averaged **281.97 fewer plies**, approximately **81.3% shorter** than random self-play. This is a comparison of game lengths under two different matchups, **not** a controlled measure of Minimax's speed advantage.

### Computation trade-off

Minimax averaged **270.66 milliseconds per move**, compared with **0.0558 milliseconds per move** for Random in the head-to-head tournament. The difference is expected: Random selects a legal move, whereas Minimax explores candidate moves and opponent replies. These timings depend on hardware, Python environment, and the distribution of board positions, so they should be treated as measurements from this run rather than general engine benchmarks.

## 7. Limitations

- **Opponent strength:** Random is a very weak opponent. A 100% score against Random does not imply competitive play against human players or established chess engines.
- **Shallow search:** A depth-2 search sees only one move by each player and can miss longer tactics.
- **Material-only evaluation:** The heuristic ignores positional concepts such as king safety, mobility, pawn structure, development, and center control.
- **No statistical generalization across opponents:** Only one opponent policy was used for the head-to-head test.
- **Draw handling:** The evaluation uses `claim_draw=True`, allowing games to end under claimable threefold-repetition and fifty-move conditions.
- **Reproducibility:** The supplied CSVs do not include a random seed, package versions, hardware details, or per-game move histories. Preserve these in future experiments to support exact reruns.
- **Test verification:** The CSV results show that games completed; they do not independently establish that all automated unit tests or the Stockfish connection test passed.

## 8. Phase 0 Conclusion

**The core baseline objective was achieved:** both agents produced complete games, and the 2-ply material minimax bot scored **100/100** against the random-move bot. The comparison provides a clear reference point for future neural-network evaluation. The baseline also reveals a meaningful speed–strength trade-off: minimax made stronger decisions against Random, but required substantially more computation per move.

Before marking the entire Phase 0 setup complete, confirm that the Stockfish executable is available, the automated tests pass, and the repository contains the required source code, dependency list, and documentation. These setup checks cannot be verified from the two CSV files alone.

## 9. Next Steps — Phase 1

1. Obtain chess positions and Stockfish evaluation labels from a suitable dataset.
2. Deduplicate positions and define a consistent train/validation split.
3. Convert evaluations into training targets and encode board positions for a neural network.
4. Retain the Phase 0 tournament configuration so future models can be compared fairly.

## Data Sources

- `data/random_baseline_results.csv` — 100 random self-play games.
- `data/minimax_baseline_results.csv` — 100 Minimax-versus-Random games.

All numeric results in this report were computed from these two CSV files. No tournament values were estimated or fabricated.

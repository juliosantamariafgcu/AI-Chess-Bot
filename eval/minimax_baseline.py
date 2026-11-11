from collections import Counter
from pathlib import Path
import csv
import time

import chess

from search.minimax import select_best_move
from search.random_bot import select_random_move


def play_game(minimax_color: chess.Color, depth: int = 2) -> dict:
    board = chess.Board()
    plies = 0
    minimax_time = 0.0
    random_time = 0.0
    minimax_moves = 0
    random_moves = 0

    while not board.is_game_over(claim_draw=True):
        is_minimax = board.turn == minimax_color
        start = time.perf_counter()
        move = (
            select_best_move(board, depth=depth)
            if is_minimax
            else select_random_move(board)
        )
        elapsed = time.perf_counter() - start

        if move is None or move not in board.legal_moves:
            raise RuntimeError(f"Bot returned an invalid move: {move!r} at {board.fen()}")

        if is_minimax:
            minimax_time += elapsed
            minimax_moves += 1
        else:
            random_time += elapsed
            random_moves += 1

        board.push(move)
        plies += 1

    outcome = board.outcome(claim_draw=True)
    if outcome is None:
        raise RuntimeError("Game ended without a recognized outcome")

    if outcome.winner is None:
        winner = "draw"
    elif outcome.winner == minimax_color:
        winner = "minimax"
    else:
        winner = "random"

    return {
        "minimax_color": "White" if minimax_color == chess.WHITE else "Black",
        "winner": winner,
        "result": board.result(claim_draw=True),
        "termination": outcome.termination.name,
        "plies": plies,
        "minimax_moves": minimax_moves,
        "random_moves": random_moves,
        "minimax_time_seconds": round(minimax_time, 6),
        "random_time_seconds": round(random_time, 6),
    }


def evaluate_minimax(num_games: int = 10, depth: int = 2) -> list[dict]:
    if num_games < 1 or depth < 1:
        raise ValueError("num_games and depth must both be positive")

    results = []
    start = time.perf_counter()
    for game_index in range(num_games):
        color = chess.WHITE if game_index % 2 == 0 else chess.BLACK
        result = play_game(minimax_color=color, depth=depth)
        result = {"game": game_index + 1, **result}
        results.append(result)
        print(
            f"Game {game_index + 1}/{num_games}: "
            f"Minimax={result['minimax_color']}, "
            f"winner={result['winner']}, "
            f"plies={result['plies']}, "
            f"termination={result['termination']}",
            flush=True,
        )

    counts = Counter(r["winner"] for r in results)
    terminations = Counter(r["termination"] for r in results)
    total_plies = sum(r["plies"] for r in results)
    minimax_moves = sum(r["minimax_moves"] for r in results)
    random_moves = sum(r["random_moves"] for r in results)
    minimax_seconds = sum(r["minimax_time_seconds"] for r in results)
    random_seconds = sum(r["random_time_seconds"] for r in results)

    print("\n=== MINIMAX VS RANDOM BASELINE ===")
    print(f"Games played: {num_games}")
    print(f"Search depth: {depth} plies")
    print(f"Minimax wins: {counts['minimax']} ({100 * counts['minimax'] / num_games:.1f}%)")
    print(f"Random wins: {counts['random']} ({100 * counts['random'] / num_games:.1f}%)")
    print(f"Draws: {counts['draw']} ({100 * counts['draw'] / num_games:.1f}%)")
    print(f"Minimax score (win=1, draw=0.5): {(counts['minimax'] + 0.5 * counts['draw']) / num_games:.3f}")
    print(f"Average plies per game: {total_plies / num_games:.2f}")
    print(f"Average minimax decision time: {minimax_seconds / minimax_moves:.4f} s" if minimax_moves else "No minimax moves")
    print(f"Average random decision time: {random_seconds / random_moves:.6f} s" if random_moves else "No random moves")
    print(f"Tournament runtime: {time.perf_counter() - start:.2f} s")

    print("\n=== GAME TERMINATION REASONS ===")
    for reason, count in terminations.most_common():
        print(f"{reason}: {count} ({100 * count / num_games:.1f}%)")

    output = Path("data") / "minimax_baseline_results.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved game results to: {output}")
    return results


if __name__ == "__main__":
    evaluate_minimax(num_games=100, depth=2)
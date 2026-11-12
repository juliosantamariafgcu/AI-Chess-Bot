## This file tests and gives a baseline for two bots using the random mehtod to chose moves.

from collections import Counter
from pathlib import Path
import csv
import time

import chess

from search.random_bot import select_random_move


def play_game() -> dict:
    board = chess.Board()
    plies = 0
    white_time = 0.0
    black_time = 0.0
    white_moves = 0
    black_moves = 0

    while not board.is_game_over(claim_draw=True):
        color = board.turn
        start = time.perf_counter()
        move = select_random_move(board)
        elapsed = time.perf_counter() - start

        if move is None or move not in board.legal_moves:
            raise RuntimeError(f"Random bot returned an invalid move: {move!r} at {board.fen()}")

        if color == chess.WHITE:
            white_time += elapsed
            white_moves += 1
        else:
            black_time += elapsed
            black_moves += 1

        board.push(move)
        plies += 1

    outcome = board.outcome(claim_draw=True)
    if outcome is None:
        raise RuntimeError("Game ended without a recognized outcome")

    winner = "draw" if outcome.winner is None else ("White" if outcome.winner == chess.WHITE else "Black")
    return {
        "winner": winner,
        "result": board.result(claim_draw=True),
        "termination": outcome.termination.name,
        "plies": plies,
        "white_moves": white_moves,
        "black_moves": black_moves,
        "white_time_seconds": round(white_time, 6),
        "black_time_seconds": round(black_time, 6),
    }


def evaluate_random_bot(num_games: int = 100) -> list[dict]:
    if num_games < 1:
        raise ValueError("num_games must be positive")

    results = []
    start = time.perf_counter()
    for game_index in range(num_games):
        result = {"game": game_index + 1, **play_game()}
        results.append(result)
        print(
            f"Game {game_index + 1}/{num_games}: "
            f"winner={result['winner']}, "
            f"plies={result['plies']}, "
            f"termination={result['termination']}",
            flush=True,
        )

    counts = Counter(r["winner"] for r in results)
    terminations = Counter(r["termination"] for r in results)
    total_plies = sum(r["plies"] for r in results)
    white_moves = sum(r["white_moves"] for r in results)
    black_moves = sum(r["black_moves"] for r in results)
    white_seconds = sum(r["white_time_seconds"] for r in results)
    black_seconds = sum(r["black_time_seconds"] for r in results)

    print("\n=== RANDOM BOT SELF-PLAY BASELINE ===")
    print(f"Games played: {num_games}")
    print(f"White wins: {counts['White']} ({100 * counts['White'] / num_games:.1f}%)")
    print(f"Black wins: {counts['Black']} ({100 * counts['Black'] / num_games:.1f}%)")
    print(f"Draws: {counts['draw']} ({100 * counts['draw'] / num_games:.1f}%)")
    print(f"Average plies per game: {total_plies / num_games:.2f}")
    print(f"Average White decision time: {white_seconds / white_moves:.6f} s" if white_moves else "No White moves")
    print(f"Average Black decision time: {black_seconds / black_moves:.6f} s" if black_moves else "No Black moves")
    print(f"Tournament runtime: {time.perf_counter() - start:.2f} s")

    print("\n=== GAME TERMINATION REASONS ===")
    for reason, count in terminations.most_common():
        print(f"{reason}: {count} ({100 * count / num_games:.1f}%)")

    output = Path("data") / "random_baseline_results.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved game results to: {output}")
    return results


if __name__ == "__main__":
    evaluate_random_bot(num_games=100)
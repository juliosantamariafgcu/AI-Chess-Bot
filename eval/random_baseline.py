import chess
from collections import Counter
from search.random_bot import select_random_move


def evaluate_random_bot(num_games=100):
    results = {
        "white_wins": 0,
        "black_wins": 0,
        "draws": 0,
        "total_moves": 0
    }

    termination_counts = Counter()

    for game in range(num_games):
        board = chess.Board()
        move_count = 0

        while not board.is_game_over(claim_draw=True):
            move = select_random_move(board)

            assert move in board.legal_moves

            board.push(move)
            move_count += 1

        result = board.result(claim_draw=True)
        outcome = board.outcome(claim_draw=True)

        # Count the reason the game ended
        termination_counts[outcome.termination.name] += 1

        if result == "1-0":
            results["white_wins"] += 1
        elif result == "0-1":
            results["black_wins"] += 1
        else:
            results["draws"] += 1

        results["total_moves"] += move_count

    print("\n=== RANDOM BOT EVALUATION ===")
    print(f"Games Played: {num_games}")
    print(f"White Wins: {results['white_wins']}")
    print(f"Black Wins: {results['black_wins']}")
    print(f"Draws: {results['draws']}")
    print(
        f"Average Plies Per Game: "
        f"{results['total_moves'] / num_games:.2f}"
    )

    print("\n=== GAME TERMINATION REASONS ===")
    for reason, count in termination_counts.most_common():
        percentage = (count / num_games) * 100
        print(f"{reason}: {count} ({percentage:.1f}%)")


if __name__ == "__main__":
    evaluate_random_bot(100)
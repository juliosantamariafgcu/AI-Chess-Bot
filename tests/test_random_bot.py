import chess
from search.random_bot import select_random_move


def test_random_bot():
    board = chess.Board()
    move_count = 0

    while not board.is_game_over(claim_draw=True):
        legal_moves = list(board.legal_moves)

        move = select_random_move(board)

        # Check that the selected move is legal
        assert move in legal_moves, f"Illegal move: {move}"

        board.push(move)
        move_count += 1

        # Prevent extremely long games
        assert move_count < 1000, "Game exceeded move limit"

    print("Random Bot Test Completed")
    print("Total Moves:", move_count)
    print("Final Result:", board.result(claim_draw=True))
    print("Final Board:")
    print(board)


if __name__ == "__main__":
    test_random_bot()
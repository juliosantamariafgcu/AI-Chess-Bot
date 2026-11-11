import chess
from search.minimax import select_best_move


def test_minimax():
    board = chess.Board()

    move = select_best_move(board, depth=2)

    assert move in board.legal_moves

    print("Selected move:", move)
    print("Move is legal:", move in board.legal_moves)


if __name__ == "__main__":
    test_minimax()
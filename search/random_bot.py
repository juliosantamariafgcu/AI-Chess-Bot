
import random
import chess

## Sends back Random Moves if they are legal (simplest bot possible)
def select_random_move(board: chess.Board):
    legal_moves = list(board.legal_moves)

    if not legal_moves:
        return None

    return random.choice(legal_moves)
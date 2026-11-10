import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
}

## Simplest evaluation of "Score" (Tells who is in the lead and current scores)
## Function evaluates the score from the WHITE perspective, with a positive score meaning
# an advantage for WHITE and a negative score meaning an advantage for BLACK.

def evaluate_material(board: chess.Board) -> int:
    score = 0

    for piece_type, value in PIECE_VALUES.items():
        white_count = len(
            board.pieces(piece_type, chess.WHITE)
        )
        black_count = len(
            board.pieces(piece_type, chess.BLACK)
        )

        score += value * (white_count - black_count)

    return score
import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
}

## Simplest Evaluation of "Score" (Tells who is in the lead and current scores)

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
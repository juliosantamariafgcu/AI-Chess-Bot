import chess
import random
from eval.material import evaluate_material

## Functions define the decision tree of the AI-Chess-Bot

# The bot is using a 2-ply search to start,
# and chooses the move that gives the best score

# This function is the desision tree and returns the move with the best score
def minimax(board, depth):
    if board.is_checkmate():
        return -100000 if board.turn == chess.WHITE else 100000

    if board.is_game_over(claim_draw=True):
        return 0

    if depth == 0:
        return evaluate_material(board)

    if board.turn == chess.WHITE:
        best = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            best = max(best, minimax(board, depth - 1))
            board.pop()
        return best

    best = float("inf")
    for move in board.legal_moves:
        board.push(move)
        best = min(best, minimax(board, depth - 1))
        board.pop()
    return best

# This function selects the best possible move for the current player and returns that move
def select_best_move(board, depth=2):
    best_moves = []
    maximizing = board.turn == chess.WHITE
    best_score = float("-inf") if maximizing else float("inf")

    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1)
        board.pop()

        if (maximizing and score > best_score) or (
            not maximizing and score < best_score
        ):
            best_score = score
            best_moves = [move]

        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves) if best_moves else None
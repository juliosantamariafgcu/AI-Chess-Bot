import chess

from search.random_bot import select_random_move
from search.minimax import select_best_move

## Plays a game between the AI-Chess_Bot and the random-bot
def play_game(minimax_color=chess.WHITE):
    board = chess.Board()
    move_count = 0

    while not board.is_game_over(claim_draw=True):

        if board.turn == minimax_color:
            move = select_best_move(board, depth=2)
        else:
            move = select_random_move(board)

        if move is None:
            break

        assert move in board.legal_moves

        board.push(move)
        move_count += 1

    outcome = board.outcome(claim_draw=True)
    result = board.result(claim_draw=True)

    print("Game Result:", result)
    print("Termination:", outcome.termination.name)
    print("Total Plies:", move_count)
    print("\nFinal Board:")
    print(board)

    return {
        "result": result,
        "termination": outcome.termination.name,
        "plies": move_count,
        "minimax_color": minimax_color
    }


if __name__ == "__main__":
    play_game()
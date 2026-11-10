import chess

from search.random_bot import select_random_move
from search.minimax import select_best_move

## Plays a game between the AI-Chess_Bot and the random-bot
def play_game():
    board = chess.Board()

    while not board.is_game_over(claim_draw=True):
        if board.turn == chess.WHITE:
            move = select_best_move(board, depth=2)
        else:
            move = select_random_move(board)

        if move is None:
            break

        board.push(move)

    print("Game result:", board.result(claim_draw=True))
    print(board)


if __name__ == "__main__":
    play_game()
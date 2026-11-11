import chess
import chess.engine

STOCKFISH_PATH = "engines/stockfish/stockfish.exe"

engine = chess.engine.SimpleEngine.popen_uci(
    STOCKFISH_PATH
)

board = chess.Board()

result = engine.analyse(
    board,
    chess.engine.Limit(depth=10)
)

print("Stockfish Evaluation:", result["score"])

engine.quit()
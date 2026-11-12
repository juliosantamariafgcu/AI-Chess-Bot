import chess
import chess.engine

STOCKFISH_PATH = "engines/stockfish/stockfish.exe"


def test_stockfish():
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    try:
        board = chess.Board()

        result = engine.analyse(
            board,
            chess.engine.Limit(depth=10)
        )

        print("Stockfish Evaluation:", result["score"])

        assert "score" in result
        assert result["score"] is not None

    finally:
        engine.quit()
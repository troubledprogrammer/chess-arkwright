import pytest
from chess import Board
from constants import *

@pytest.mark.parametrize(
    "fen",
    [
        START_FEN,
        "r2qk1nr/pp1b1ppp/2p5/2Pp4/2P5/3B1N2/P4PPP/RNBQK2R b KQkq - 0 9",
        "r1b1k2r/pp2nppp/2p1p3/8/5B2/8/PPP1PNPP/2KR1B1R w - - 1 11",
    ]
)
def test_game_state_no_result(fen):
    b = Board(fen)
    assert b.get_win_state() == NO_RESULT

@pytest.mark.parametrize(
    "fen",
    [
        "r1bqkbnr/p1pp1Qpp/1pn5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4",
        "rnbqkbnr/ppppp2p/5p2/6pQ/3PP3/8/PPP2PPP/RNB1KBNR b KQkq - 1 3",
        "rnbqkb1r/3pnppp/pppNp3/8/8/8/PPPPPPPP/RNBQKB1R b KQkq - 0 1",
        "2k1R3/pp3p2/3K2b1/1p1p1r2/P2R4/8/8/8 b - - 1 60",
    ]
)
def test_game_state_white_win(fen):
    b = Board(fen)
    assert b.get_win_state() == WHITE

@pytest.mark.parametrize(
    "fen",
    [
        "rnb1kbnr/pppp1ppp/8/4p3/5PPq/8/PPPPP2P/RNBQKBNR w KQkq - 1 3",
        "8/8/8/2p3k1/1p6/pP5b/P6P/K3q3 w - - 0 37",
        "r1b3k1/pp1p2bp/2n2rp1/3p1P2/6Q1/8/PPP3PP/R1B2q1K w - - 0 18",
        "k7/pp6/2p2qP1/3pK3/4n3/1P6/P1P5/8 w - - 2 51",
    ]
)
def test_game_state_black_win(fen):
    b = Board(fen)
    assert b.get_win_state() == BLACK

@pytest.mark.parametrize(
    "fen",
    [
        "8/8/2q5/K7/2k5/8/8/8 w - - 0 1",
        "8/5p2/3p4/2b2p2/p4k1p/7P/1r4PK/3r4 w - - 0 48",
        "8/8/6p1/7k/6n1/7K/5q2/8 w - - 0 60",
    ]
)
def test_game_state_stalemate(fen):
    b = Board(fen)
    assert b.get_win_state() == DRAW

@pytest.mark.parametrize(
    ("fen", "moves"),
    [
        (START_FEN, 20),
        ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1", 20),
        ("R6R/3Q4/1Q4Q1/4Q3/2Q4Q/Q4Q2/pp1Q4/kBNNK1B1 w - - 0 1", 216),
        ("r1bq1rk1/pppp1ppp/3n1b2/8/8/2N5/PPPP1PPP/R1BQRBK1 b - - 4 10", 26),
    ]
)
def test_legal_moves(fen, moves):
    b = Board(fen)
    assert len(b.get_legal_moves()) == moves
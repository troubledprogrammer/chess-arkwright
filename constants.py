START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

LETTERS = "abcdefgh"
NUMBERS = "12345678"

WHITE = 1
BLACK = -1
DRAW = 0
NO_RESULT = 2

KING = 10
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 5
QUEEN = 9

# Unicode characters for chess pieces
# https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode#Unicode_characters
# PIECES = {
#     PAWN: ["", "\u2659", "\u265F"],
#     KNIGHT: ["", "\u2658", "\u265E"],
#     BISHOP: ["", "\u2657", "\u265D"],
#     ROOK: ["", "\u2656", "\u265C"],
#     QUEEN: ["", "\u2655", "\u265B"],
#     KING: ["", "\u2654", "\u265A"],
# }

PIECES = {
    PAWN: {WHITE: "P", BLACK: "p"},
    KNIGHT: {WHITE: "N", BLACK: "n"},
    BISHOP: {WHITE: "B", BLACK: "b"},
    ROOK: {WHITE: "R", BLACK: "r"},
    QUEEN: {WHITE: "Q", BLACK: "q"},
    KING: {WHITE: "K", BLACK: "k"},
}

LEGAL_PROMOTE_PIECES = [
    KNIGHT,
    BISHOP,
    ROOK,
    QUEEN
]
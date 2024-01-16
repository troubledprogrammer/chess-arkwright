from __future__ import annotations

from copy import deepcopy

from constants import *
from conversions import *


class Square:
    def __init__(self, pos: int = 0, piece: Piece = None) -> None:
        """
        Creates a square object that holds a position and piece
        :param pos: index of square starting from a8
        :param piece: Piece on square
        """
        self.index = pos
        self.piece = piece

    def has_piece(self) -> bool:
        """
        Checks if square holds a piece
        :return: true if contains a piece
        """
        return self.piece is not None

    def has_ally_piece(self, colour: int) -> bool:
        """
        Checks if square holds a piece of the same colour specified
        :param colour: -1 for black, 1 for white; Note: Use WHITE and BLACK constants for readability
        :return: true if contains an ally piece
        """
        if not self.has_piece(): return False
        return self.piece.colour == colour

    def has_enemy_piece(self, colour: int) -> bool:
        """
        Checks if square holds a piece of the opposite colour specified
        :param colour: -1 for black, 1 for white; Note: Use WHITE and BLACK constants for readability
        :return: true if contains an enemy piece
        """
        if not self.has_piece(): return False
        return self.piece.colour != colour

    def __str__(self):
        return index_to_algebraic(self.index)

    def __eq__(self, s):
        if not isinstance(s, Square):
            raise NotImplemented
        return s.index == self.index


class Piece:
    def __init__(self, piece_type: int, colour: int) -> None:
        """
        Creates a piece from a colour and type
        :param piece_type: use PAWN, KNIGHT etc. constants
        :param colour: -1 for black, 1 for white; Note: Use WHITE and BLACK constants for readability
        """
        self.colour = colour
        self.type = piece_type

        self.printable = PIECES[self.type][self.colour]

    @staticmethod
    def from_str(char: str) -> Piece:
        """
        Creates a piece form a FEN piece character
        :param char: FEN character
        :return: an instance of piece
        """
        colour = WHITE if char.isupper() else BLACK
        match char.lower():
            case "p":
                piece_type = PAWN
            case "n":
                piece_type = KNIGHT
            case "b":
                piece_type = BISHOP
            case "r":
                piece_type = ROOK
            case "q":
                piece_type = QUEEN
            case "k":
                piece_type = KING
            case _:
                raise Exception(f"Invalid piece: {char} is not a valid piece")
        return Piece(piece_type, colour)

    def __str__(self):
        return self.printable

    def is_attacking(self, board: Board, cur_pos: int, target_pos: int) -> bool:
        """
        Checks if a piece is attacking a square
        :param board: Board instance
        :param cur_pos: index of current square
        :param target_pos: index of target square
        :return: true if piece is threatening position
        """
        cc, cr = index_to_coordinate(cur_pos)
        nc, nr = index_to_coordinate(target_pos)
        if self.type == PAWN and self.colour == WHITE:
            if nr - cr == -1 and abs(nc - cc) == 1:
                if board.position[target_pos].has_enemy_piece(self.colour):
                    return True
        if self.type == PAWN and self.colour == BLACK:
            if nr - cr == 1 and abs(nc - cc) == 1:
                if board.position[target_pos].has_enemy_piece(self.colour):
                    return True
        if self.type == KNIGHT:
            t = index_to_coordinate(target_pos)
            c = index_to_coordinate(cur_pos)
            o = t[0] - c[0], t[1] - c[1]
            if o in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)] and not board.position[
                target_pos].has_ally_piece(self.colour):
                return True
        if self.type == BISHOP:
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                col, row = index_to_coordinate(cur_pos)
                while 0 <= row <= 7 and 0 <= col <= 7:
                    if not coordinate_to_index((col, row)) == cur_pos:
                        if coordinate_to_index((col, row)) == target_pos:
                            if not board.position[coordinate_to_index((col, row))].has_ally_piece(self.colour):
                                return True
                        if board.position[coordinate_to_index((col, row))].has_piece():
                            break
                    row += direction[0]
                    col += direction[1]
        if self.type == ROOK:
            for direction in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                col, row = index_to_coordinate(cur_pos)
                while 0 <= row <= 7 and 0 <= col <= 7:
                    cur_checking = coordinate_to_index((col, row))
                    if not cur_checking == cur_pos:
                        if cur_checking == target_pos:
                            if not board.position[cur_checking].has_ally_piece(self.colour):
                                return True
                        if board.position[cur_checking].has_piece():
                            break
                    row += direction[0]
                    col += direction[1]
        if self.type == QUEEN:
            for direction in [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]:
                col, row = index_to_coordinate(cur_pos)
                while 0 <= row <= 7 and 0 <= col <= 7:
                    if not coordinate_to_index((col, row)) == cur_pos:
                        if coordinate_to_index((col, row)) == target_pos:
                            if not board.position[coordinate_to_index((col, row))].has_ally_piece(self.colour):
                                return True
                        if board.position[coordinate_to_index((col, row))].has_piece():
                            break
                    row += direction[0]
                    col += direction[1]
        if self.type == KING:
            t = index_to_coordinate(target_pos)
            c = index_to_coordinate(cur_pos)
            o = t[0] - c[0], t[1] - c[1]
            if o in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)] and not board.position[
                target_pos].has_ally_piece(self.colour):
                return True
            if self.colour == 1:
                if target_pos == 62 and board.castling[0]:
                    if not board.position[62].has_piece() and not board.position[61].has_piece():
                        return True
                if target_pos == 28 and board.castling[1]:
                    if not board.position[59].has_piece() and not board.position[58].has_piece() and not board.position[
                        57].has_piece():
                        return True
                if target_pos == 6 and board.castling[2]:
                    if not board.position[6].has_piece() and not board.position[5].has_piece():
                        return True
                if target_pos == 2 and board.castling[3]:
                    if not board.position[1].has_piece() and not board.position[2].has_piece() and not board.position[
                        3].has_piece():
                        return True
        # print(f"{self} cannot move to {indexToAlgebraic(target_pos)}")
        return False

    def can_move(self, board: Board, cur_pos: int, target_pos: int) -> bool:
        """
        Checks if making a move is legal
        :param board: Board instance
        :param cur_pos: index of current square
        :param target_pos: index of target square
        :return: true if piece can move to given position
        """
        if board.turn != self.colour:
            # c = ["", "White", "Black"][board.turn]
            # print(f"{self} cannot move because it is {c}'s turn")
            return False
        if self.type == PAWN and self.colour == WHITE:
            if cur_pos - target_pos == 8:
                if not board.position[target_pos].has_piece():
                    return True
            elif cur_pos - target_pos == 16 and cur_pos > 47:
                if not board.position[target_pos].has_piece() and not board.position[cur_pos - 8].has_piece():
                    return True
            elif (cur_pos - target_pos == 7 or cur_pos - target_pos == 9) and board.en_passant.index == target_pos:
                    return True
        if self.type == PAWN and self.colour == BLACK:
            if cur_pos - target_pos == -8:
                if not board.position[target_pos].has_piece():
                    return True
            elif cur_pos - target_pos == -16 and cur_pos < 16:
                if not board.position[target_pos].has_piece() and not board.position[cur_pos + 8].has_piece():
                    return True
            elif cur_pos - target_pos == -7 or cur_pos - target_pos == -9:
                if board.position[target_pos].has_enemy_piece(self.colour):
                    return True
                elif board.en_passant.index == target_pos:
                    return True
        return self.is_attacking(board, cur_pos, target_pos)


class Move:
    def __init__(self, start_pos: int, target_pos: int, promotion_piece: Piece = None) -> None:
        """
        Creates an instance of a move holding a start and end pos
        :param start_pos: index of starting square
        :param target_pos: index of target square
        :param promotion_piece: Piece to promote to
        """
        self.current_pos = start_pos
        self.target_pos = target_pos
        self.promotion_piece = promotion_piece

    def __str__(self):
        promotion = ""
        if self.promotion_piece is not None:
            promotion = f" = {self.promotion_piece.printable}"
        return f"{index_to_algebraic(self.current_pos)} > {index_to_algebraic(self.target_pos)}{promotion}"

    def __eq__(self, move):
        if not isinstance(move, Move):
            raise NotImplemented
        return move.current_pos == self.current_pos and move.target_pos == self.target_pos

    def is_valid(self, board: Board) -> bool:
        """
        Checks if move is legal on board
        :param board: Board instance
        :return: true if the move is legal
        """
        try:
            if not board.position[self.current_pos].has_piece():
                return False
            if not board.position[self.current_pos].piece.can_move(board, self.current_pos, self.target_pos):
                return False
        except AttributeError:
            print("Tried to move a piece that didn't exist")
            return False
        
        # set promotion piece to queen if no piece specified
        if index_to_coordinate(self.target_pos)[1] in [0, 7]:
            if self.promotion_piece == None:
                self.promotion_piece = Piece(QUEEN, board.position[self.current_pos].piece.colour)

        board.make_move(self)
        is_check = board.is_check(-board.turn)
        board.unmake_move()
        if is_check:
            # print(f"Invalid move: {-board.turn} would be in check")
            return False
        target_rank = index_to_coordinate(self.target_pos)[1]
        if board.position[self.current_pos].piece.type == PAWN and (target_rank == 0 or target_rank == 7):
            if self.promotion_piece.colour != board.turn: return False
            if self.promotion_piece.type == KING: return False
        return True


class Board:
    def __init__(self, fen: str = START_FEN) -> None:
        """
        Creates an instance of the game
        :param fen: the FEN string for the position to load
        """
        self.position = [Square()] * 64  # empty board
        self.turn = WHITE
        self.castling = [False] * 4
        self.en_passant = Square(-1)  # no en passant square
        self.halfmoves = 0  # counts to 100 halfmoves (50 move rule)
        self.moves = 0

        self.saves = []

        self.load_fen(fen)

    def load_fen(self, fen_to_load: str) -> None:
        """
        Loads a FEN notation onto the board
        :param fen_to_load: the FEN string to load onto the board
        """
        fen_string = fen_to_load.split(" ")
        # pieces
        pieces = []
        index = 0
        for char in fen_string[0]:
            if char.isnumeric():
                for _ in range(int(char)):
                    pieces.append(Square(index))
                    index += 1
            else:
                if not char == "/":
                    p = Piece.from_str(char)
                    pieces.append(Square(index, p))
                    index += 1
        self.position = pieces
        # turn
        turn = WHITE
        if fen_string[1] == "b": turn = BLACK
        self.turn = turn
        # castling
        self.castling = [False] * 4
        for char in fen_string[2]:
            if char == "K": self.castling[0] = True
            if char == "Q": self.castling[1] = True
            if char == "k": self.castling[2] = True
            if char == "q": self.castling[3] = True
        # en passant
        if fen_string[3] == "-":
            self.en_passant = Square(-1)
        else:
            self.en_passant = Square(algebraic_to_index(fen_string[3]))
        # 50 move timer
        self.halfmoves = int(fen_string[4])
        # moves
        self.moves = int(fen_string[5]) * 2 - 2
        if not self.turn: self.moves += 1

    def __str__(self):
        t = "\n    a   b   c   d   e   f   g   h  \n  +---+---+---+---+---+---+---+---+\n8 | # | # | # | # | # | # | " \
            "# | # | 8\n  +---+---+---+---+---+---+---+---+\n7 | # | # | # | # | # | # | # | # | 7\n  " \
            "+---+---+---+---+---+---+---+---+\n6 | # | # | # | # | # | # | # | # | 6\n  " \
            "+---+---+---+---+---+---+---+---+\n5 | # | # | # | # | # | # | # | # | 5\n  " \
            "+---+---+---+---+---+---+---+---+\n4 | # | # | # | # | # | # | # | # | 4\n  " \
            "+---+---+---+---+---+---+---+---+\n3 | # | # | # | # | # | # | # | # | 3\n  " \
            "+---+---+---+---+---+---+---+---+\n2 | # | # | # | # | # | # | # | # | 2\n  " \
            "+---+---+---+---+---+---+---+---+\n1 | # | # | # | # | # | # | # | # | 1\n  " \
            "+---+---+---+---+---+---+---+---+\n    a   b   c   d   e   f   g   h  \n"
        for square in self.position:
            if not square.has_piece():
                t = t.replace("#", " ", 1)
            else:
                t = t.replace("#", square.piece.printable, 1)
        return t

    def make_move(self, move: Move) -> None:
        """
        Makes a move on the board
        :param move: Move instance to make
        """

        self.saves.append(SaveState(self))

        p = self.position[move.current_pos].piece

        # print(p,self.board[move.target_pos], sep="")

        # en passant
        if self.en_passant.index == move.target_pos:
            self.position[move.target_pos + 8 * p.colour].piece = None
        if p.type == PAWN and abs(move.current_pos - move.target_pos) == 16:
            self.en_passant = Square(move.target_pos + 8 * p.colour)
        else:
            self.en_passant = Square(-1)

        # castling
        if p.type == KING:
            if p.colour == WHITE:
                self.castling[0] = False
                self.castling[1] = False
            if p.colour == BLACK:
                self.castling[2] = False
                self.castling[3] = False
        if p.type == ROOK:
            if p.colour == WHITE:
                if move.current_pos == 63: self.castling[0] = False
                if move.current_pos == 56: self.castling[1] = False
            if p.colour == BLACK:
                if move.current_pos == 7: self.castling[2] = False
                if move.current_pos == 0: self.castling[3] = False
        if p.type == KING and abs(move.current_pos - move.target_pos) == 2:
            if move.target_pos == 62:  # White KS
                self.position[61].piece = self.position[63].piece
                self.position[63].piece = None
            if move.target_pos == 58:  # White QS
                self.position[59].piece = self.position[56].piece
                self.position[56].piece = None
            if move.target_pos == 6:  # Black KS
                self.position[5].piece = self.position[5].piece
                self.position[7].piece = None
            if move.target_pos == 2:  # Black QS
                self.position[3].piece = self.position[0].piece
                self.position[0].piece = None

        self.position[move.target_pos].piece = self.position[move.current_pos].piece
        self.position[move.current_pos].piece = None

        self.turn *= -1
        self.moves += 1
        self.halfmoves += 1

        if p.type == PAWN: self.halfmoves = 0
        if self.is_check(self.turn): self.halfmoves = 0

        if p.type == PAWN:
            if p.colour == WHITE and index_to_coordinate(move.target_pos)[1] == 0:
                self.position[move.target_pos].piece = move.promotion_piece
            if p.colour == BLACK and index_to_coordinate(move.target_pos)[1] == 7:
                self.position[move.target_pos].piece = move.promotion_piece

    def unmake_move(self) -> None:
        """
        Unmakes the last move unless there are no previous recorded positions
        """
        if len(self.saves) == 0: raise Exception("Cannot undo move: No previous position exists")
        self.load_state(self.saves.pop())

    def load_state(self, state: SaveState) -> None:
        """
        Loads a previous position onto the board
        :param state: The save instance to go back to
        """
        self.position = deepcopy(state.position)
        self.turn = state.turn
        self.castling = state.castling
        self.en_passant = state.en_passant
        self.halfmoves = state.halfmoves
        self.moves = state.moves

    def get_win_state(self) -> int:
        """
        Checks if game has ended
        :return: Constant: either WHITE, BLACK, DRAW or NO_RESULT
        """
        l = self.get_legal_moves()
        if len(l) == 0:
            if self.is_check(self.turn):
                return -self.turn
            else:
                return DRAW
        if self.halfmoves >= 100: return 0
        return NO_RESULT

    def get_legal_moves(self) -> list[Move]:
        """
        Gets an array of all legal moves
        :return: a list of all the legal moves as move instances
        """
        moves = []
        for si in range(64):
            for ti in range(64):
                start_square = self.position[si]
                if start_square.has_piece():
                    target_rank = index_to_coordinate(ti)[1]
                    if start_square.piece.type == PAWN and (target_rank == 0 or target_rank == 7):
                        for piece_type in LEGAL_PROMOTE_PIECES:
                            move = Move(si, ti, Piece(piece_type, self.turn))
                            if move.is_valid(self):
                                moves.append(move)
                    else:
                        move = Move(si, ti)
                        if move.is_valid(self):
                            moves.append(move)
        return moves

    def is_check(self, colour: WHITE | BLACK) -> bool:
        """
        Checks if specified colour's king is in check
        :param colour: WHITE or BLACK constant of specified king
        :return: true if given king is in check
        """
        king_pos = None
        for square in self.position:
            if square.has_piece():
                if square.piece.type == KING and square.piece.colour == colour:
                    king_pos = square.index
                    break
        for square in self.position:
            if square.has_piece() and square.piece.colour == -colour:
                if square.piece.is_attacking(self, square.index, king_pos):
                    return True
        return False

    def clone(self) -> Board:
        """
        Copies all the data in the board
        :return: a different identical instance of Board
        """
        return deepcopy(self)


class SaveState:
    def __init__(self, board: Board) -> None:
        """
        Creates a save instance from a position
        :param board: Board instance to save
        """
        self.position = deepcopy(board.position)
        self.turn = board.turn
        self.castling = board.castling.copy()
        self.en_passant = board.en_passant
        self.halfmoves = board.halfmoves
        self.moves = board.moves

    def __eq__(self, other):
        if not isinstance(other, (SaveState, Board)):
            return NotImplemented
        return self.position == other.position

    __str__ = Board.__str__


if __name__ == '__main__':
    b = Board() #Board(fen="rnbqkbnr/2pppppp/pp6/8/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1")
    r = NO_RESULT

    while r == NO_RESULT:
        print(b)
        print(f"{['', 'White', 'Black'][b.turn]} to move:")

        valid_move = False
        while not valid_move:
            try:
                m = input("--> ").lower().split(" ")
                mv = Move(algebraic_to_index(m[0]), algebraic_to_index(m[1]))
                valid_move = True
            except:
                print("invalid move format: should be 'start end' i.e 'e2 e4'")

        if mv.is_valid(b):
            b.make_move(mv)
            r = b.get_win_state()
        else:
            print(f"{mv} is not legal")

    print(["Draw", "White won", "Black won"][r])

# Alternate main for benchmarking move generation
#if __name__ == "__main__":
#    import time
#    b = Board()  # change fen to benchmark different positions
#    t1 = time.time()
#    b.get_legal_moves()
#    t2 = time.time()
#    print(f"Total time = {t2-t1}")

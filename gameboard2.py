import io
import os
import sys
import itertools
import unicodedata


BLACK,WHITE = ("BLACK","WHITE")

def main():

    checkers = CheckersBoard()
    print(checkers)

    # chess = ChessBoard()
    # print(chess)

def console(char, background):
    return "\x1B[{}m{}\x1B[0m".format(
            43 if background == BLACK else 47, char or " ")

class AbstractBoard:

    def __init__(self, rows, columns):
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.populate_board()


    def populate_board(self):
        raise NotImplementedError()


    def __str__(self):
        squares = []
        for y, row in enumerate(self.board):
            for x, piece in enumerate(row):
                square = console(piece, BLACK if (y + x) % 2 else WHITE)
                squares.append(square)
            squares.append("\n")
        return "".join(squares)

class CheckersBoard(AbstractBoard):

    def __init__(self):
        super().__init__(10, 10)


    def populate_board(self):
        for x in range(0, 9, 2):
            for y in range(4):
                column = x + ((y + 1) % 2)
                for row, color in ((y, "black"), (y + 6, "white")):
                    self.board[row][column] = create_piece("draught",
                            color)


def create_piece(kind, color):
    if kind == "draught":
        return eval("{}{}()".format(color.title(), kind.title()))
    return eval("{}Chess{}()".format(color.title(), kind.title()))

class Piece(str):
    __slots__ = ()

for code in itertools.chain((0x26C0, 0x26C2), range(0x2654, 0x2660)):
    char = chr(code)
    name = unicodedata.name(char).title().replace(" ", "")
    if name.endswith("sMan"):
        name = name[:-4]
    exec("""\
class {}(Piece):

    __slots__ = ()

    def __new__(Class):
        return super().__new__(Class, "{}")""".format(name, char))
    # Using exec() is risky


if __name__ == "__main__":
    main()

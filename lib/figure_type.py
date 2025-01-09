import enum as Enum


class Figure_type(Enum.Enum):
    w_king = "K"
    w_queen = "Q"
    w_rook = "R"
    w_bishop = "B"
    w_knight = "N"
    w_pawn = "P"

    b_king = "k"
    b_queen = "q"
    b_rook = "r"
    b_bishop = "b"
    b_knight = "n"
    b_pawn = "p"

    empty = False

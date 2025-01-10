import enum as Enum


class Castling(Enum.Enum):
    WHITE = "KQ"
    BLACK = "kq"
    Both = "KQkq"
    NoneCastling = "_"

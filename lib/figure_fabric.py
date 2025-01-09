from lib.bishop import Bishop
from lib.figure_type import Figure_type
from lib.move import Move
from lib.figure import Figure
from lib.king import King
from lib.knight import Knight
from lib.pawn import Pawn
from lib.queen import Queen
from lib.rook import Rook


class FigureFabric:

    def __init__(self, chess) -> None:
        self.chess = chess

    def create_figure(self, figure: Figure_type, position: Move) -> Figure | None:
        """
        Метод создания фигуры на доске.

        :param figure: Тип фигуры (Figure_type).
        :param position: Позиция фигуры на доске (Move).
        """

        if figure == Figure_type.w_king or figure == Figure_type.b_king:
            return King(figure, position, self.chess)

        if figure == Figure_type.w_queen or figure == Figure_type.b_queen:
            return Queen(figure, position, self.chess)

        if figure == Figure_type.w_rook or figure == Figure_type.b_rook:
            return Rook(figure, position, self.chess)

        if figure == Figure_type.w_bishop or figure == Figure_type.b_bishop:
            return Bishop(figure, position, self.chess)

        if figure == Figure_type.w_knight or figure == Figure_type.b_knight:
            return Knight(figure, position, self.chess)

        if figure == Figure_type.w_pawn or figure == Figure_type.b_pawn:
            return Pawn(figure, position, self.chess)

        return None

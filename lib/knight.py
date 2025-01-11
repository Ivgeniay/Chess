from lib.figure_type import Figure_type
from lib.move import Move
from lib.figure import Figure


class Knight(Figure):
    def __init__(self, figure_type: Figure_type, position: Move, chess) -> None:
        super().__init__(figure_type, position, chess)

    def is_possible_move(self, move: Move) -> bool:
        # NOTE: Общие проверки
        if self.is_own_cell(move) or self.is_not_own_move() or self.is_frendly_cell(move):
            return False

        if self.chess.is_kingcheck_after_move(self, move):
            return False

        posible_moves = self.get_possible_moves()
        return move in posible_moves

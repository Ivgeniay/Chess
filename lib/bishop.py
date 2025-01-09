from lib.figure import Figure
from lib.figure_type import Figure_type
from lib.move import Move


class Bishop(Figure):

    def __init__(self, figure_type: Figure_type, position: Move, chess) -> None:
        super().__init__(figure_type, position, chess)

    def get_possible_moves(self, is_under_protection_figure: bool = False) -> list[Move]:
        possible_moves = []
        row, col = self.position.value

        # ТNOTE: Обход диагоналей
        self.traverse_direction(
            1, 1, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(
            1, -1, row, col, possible_moves, is_under_protection_figure)
        self.traverse_direction(-1, 1, row, col,
                                possible_moves, is_under_protection_figure)
        self.traverse_direction(-1, -1, row, col,
                                possible_moves, is_under_protection_figure)

        return possible_moves

    def is_possible_move(self, move: Move) -> bool:
        # NOTE: Общие проверки
        if self.is_own_cell(move) or self.is_not_own_move() or self.is_frendly_cell(move):
            return False

        posible_moves = self.get_possible_moves()
        return move in posible_moves

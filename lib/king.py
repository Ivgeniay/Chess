from lib.figure_type import Figure_type
from lib.move import Move
from lib.figure import Figure
from lib.rook import Rook


class King(Figure):

    def __init__(self, figure_type: Figure_type, position: Move, chess) -> None:
        super().__init__(figure_type, position, chess)

    def is_possible_move(self, move: Move) -> bool:
        # NOTE: Общие проверки
        if self.is_own_cell(move) or self.is_not_own_move():
            return False

        # if self.is_frendly_cell(move)
        #     return False
        other = self.chess.board[move.value[0]][move.value[1]]
        if other != None and other.side == self.side and isinstance(other, Rook):
            pass
        else:
            if self.is_frendly_cell(move):
                return False

        if self.chess.is_cell_under_attack(move, self.side):
            return False

        possible_moves = self.get_possible_moves()
        return move in possible_moves

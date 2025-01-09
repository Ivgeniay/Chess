from lib.figure_type import Figure_type
from lib.move import Move
from lib.figure import Figure


class King(Figure):

    def __init__(self, figure_type: Figure_type, position: Move, chess) -> None:
        super().__init__(figure_type, position, chess)

    def get_possible_moves(self, is_under_protection_figure: bool = False) -> list[Move]:
        possible_moves = []
        row, col = self.position.value
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                other_figure = self.chess.board[r][c]
                move_key = Move((r, c))

                # NOTE: Клетка свободна или занята фигурой противника
                if other_figure is None or other_figure.side != self.side:
                    possible_moves.append(move_key)

        return possible_moves

    def is_possible_move(self, move: Move) -> bool:
        # NOTE: Общие проверки
        if self.is_own_cell(move) or self.is_not_own_move() or self.is_frendly_cell(move):
            return False

        if self.chess.is_cell_under_attack(move, self.side):
            return False

        possible_moves = self.get_possible_moves()
        return move in possible_moves

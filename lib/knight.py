from lib.figure_type import Figure_type
from lib.move import Move
from lib.figure import Figure


class Knight(Figure):
    def __init__(self, figure_type: Figure_type, position: Move, chess) -> None:
        super().__init__(figure_type, position, chess)

    def get_possible_moves(self, is_under_protection_figure: bool = False) -> list[Move]:
        possible_moves = []
        row, col = self.position.value

        # Все возможные смещения для хода коня
        knight_moves = [
            (-2, -1), (-2, 1),  # Верхние ходы
            (-1, -2), (-1, 2),  # Ходы слева и справа
            (1, -2), (1, 2),    # Ходы снизу слева и справа
            (2, -1), (2, 1)     # Нижние ходы
        ]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc

            # Проверяем, что клетка находится в пределах доски
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                move = Move((new_row, new_col))
                cell = self.chess.board[new_row][new_col]

                # Если клетка пуста или занята фигурой противника, добавляем ход
                if cell is None or cell.side != self.side:
                    possible_moves.append(move)
                elif is_under_protection_figure:
                    possible_moves.append(move)

        return possible_moves

    def is_possible_move(self, move: Move) -> bool:
        # NOTE: Общие проверки
        if self.is_own_cell(move) or self.is_not_own_move() or self.is_frendly_cell(move):
            return False

        posible_moves = self.get_possible_moves()
        return move in posible_moves

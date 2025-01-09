from lib.figure_type import Figure_type
from lib.move import Move
from lib.side import Side
from lib.figure import Figure


class Pawn(Figure):
    def __init__(self, figure_type: Figure_type, position: Move, chess) -> None:
        super().__init__(figure_type, position, chess)
        self.is_enpassant: bool = False
        self.can_enpassant: bool = True

    def get_possible_moves(self, is_under_protection_figure: bool = False) -> list[Move]:
        possible_moves = []
        row, col = self.position.value

        # NOTE: Определяем направление движения в зависимости от стороны
        direction = 1 if self.side == Side.WHITE else -1

        # Ход на одну клетку вперёд
        new_row = row + direction
        # Клетка должна быть пустой
        if 0 <= new_row < 8 and self.chess.board[new_row][col] is None:
            possible_moves.append(Move((new_row, col)))

            # Ход на две клетки вперёд со стартовой позиции
            if self.can_enpassant and ((self.side == Side.WHITE and row == 1) or (self.side == Side.BLACK and row == 6)):
                two_step_row = row + 2 * direction
                # Проверяем, что обе клетки свободны
                if self.chess.board[two_step_row][col] is None:
                    possible_moves.append(Move((two_step_row, col)))

        # Диагональные ходы (возможны только при атаке)
        for dc in (-1, 1):  # Влево и вправо по диагонали
            diag_row, diag_col = row + direction, col + dc
            if 0 <= diag_row < 8 and 0 <= diag_col < 8:
                cell = self.chess.board[diag_row][diag_col]
                # NOTE: Если есть фигура противника
                if cell is not None and cell.side != self.side:
                    possible_moves.append(Move((diag_row, diag_col)))
                # NOTE: Если есть фигура игрока и нужно вернуть данные о фигурах под защитой
                elif is_under_protection_figure:
                    possible_moves.append(Move((diag_row, diag_col)))

        return possible_moves

    def pawn_attacks(self, pawn: Figure) -> set[Move]:
        attack_cells = set()
        row, col = pawn.position.value

        if pawn.side == Side.WHITE:
            # NOTE: Белая пешка атакует выше и влево/вправо
            # attack_positions = [(row - 1, col - 1), (row - 1, col + 1)]
            attack_positions = [(row + 1, col - 1), (row + 1, col + 1)]
        else:
            # NOTE: Чёрная пешка атакует ниже и влево/вправо
            # attack_positions = [(row + 1, col - 1), (row + 1, col + 1)]
            attack_positions = [(row - 1, col - 1), (row - 1, col + 1)]

        for r, c in attack_positions:
            # NOTE: Проверка на выход за пределы доски
            if 0 <= r < 8 and 0 <= c < 8:
                attack_move = Move((r, c))
                if pawn.side == Side.WHITE:
                    attack_cells.add(attack_move)
                else:
                    attack_cells.add(attack_move)
        return attack_cells

    # NOTE: Переопределение метода для пешки поскольку у неё есть дополнительные возможности
    # нужно рассчитать тут был ли ход сделан на 2 клетки вперед, если да то здесь будет проходить
    # управление булевыми переменными is_enpassant и can_enpassant
    def last_action(self) -> None:
        self.can_enpassant = False
        if abs(self.positions[-1].value[0] - self.positions[-2].value[0]) == 2:
            self.is_enpassant = True
        pass

    # TODO: доделать возможность брать на проходе сейчас не работает
    # TODO: доделать возможность превращения пешки
    # TODO: доделать проверку на шах
    # TODO: доделать проверку на мат
    # TODO: убрать из метода self.can_enpassant = False поскольку метод будет использоваться для подсвечивания возможных ходов
    def is_possible_move(self, move: Move) -> bool:
        # NOTE: Общие проверки
        if self.is_own_cell(move) or self.is_not_own_move() or self.is_frendly_cell(move):
            return False

        possible_moves = self.get_possible_moves()
        return move in possible_moves

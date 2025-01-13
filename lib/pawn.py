from lib.figure_type import Figure_type
from lib.move import Move
from lib.side import Side
from lib.figure import Figure


class Pawn(Figure):
    def __init__(self, figure_type: Figure_type, position: Move, chess) -> None:
        super().__init__(figure_type, position, chess)
        self.is_enpassant: bool = False
        self.can_enpassant: bool = True

    def pawn_attacks(self, pawn: Figure) -> set[Move]:
        attack_cells = set()
        row, col = pawn.position.value

        if pawn.side == Side.WHITE:
            # NOTE: Белая пешка атакует выше и влево/вправо
            attack_positions = [(row + 1, col - 1), (row + 1, col + 1)]
        else:
            # NOTE: Чёрная пешка атакует ниже и влево/вправо
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

    def last_action(self) -> None:
        if self.can_enpassant and abs(self.positions_list[-1].value[0] - self.positions_list[-2].value[0]) == 2:
            self.is_enpassant = True
        self.can_enpassant = False

    # TODO: доделать возможность превращения пешки
    def is_possible_move(self, move: Move) -> bool:
        # NOTE: Общие проверки
        if self.is_own_cell(move) or self.is_not_own_move() or self.is_frendly_cell(move) or self.chess.is_stop_figure_moving:
            return False

        if self.chess.is_kingcheck_after_move(self, move):
            return False

        possible_moves = self.get_possible_moves()

        return move in possible_moves

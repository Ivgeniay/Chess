from lib.figure_type import Figure_type
from lib.move import Move
from lib.side import Side

from abc import ABC, abstractmethod


class Figure(ABC):

    def __init__(self, figure_type: Figure_type, position: Move, chess) -> None:
        from lib.chess import Chess
        self.figure_type: Figure_type = figure_type
        self.position: Move = position
        self.chess: Chess = chess
        self.side: Side = Side.WHITE if figure_type.name.lower().startswith(
            "w") else Side.BLACK
        self.rect = (0, 0)
        self.positions: list[Move] = [self.position]

    def get_chess_position(self) -> Move:
        """
        Возвращает текущую позицию фигуры на доске в формате Move.
        """
        return self.position

    @ abstractmethod
    def is_possible_move(self, move: Move) -> bool:
        """
        Процедура проверки возможности хода фигуры на указанную клетку.

        :param move: Клетка, на которую пытается сделать ход фигура.
        """
        return True

    def get_possible_moves(self, is_under_protection_figure: bool = False) -> list[Move]:
        """
        Возвращает все возможные вертикальные и горизонтальные ходы, 
        отсеивая невозможные перемещения в соответствии с правилами.
        """
        return self.chess.get_figure_possible_moves(self, is_under_protection_figure)

    def set_new_position(self, move: Move) -> None:
        """
        Устанавливает новую позицию фигуры на доске.

        :param move: Клетка, на которую пытается сделать ход фигура.
        """
        self.position = move
        self.positions.append(move)

    def last_action(self) -> None:
        """
        Метод вызываемый после успешного хода фигуры. Позволяет реализовать дополнительные действия, связанные с ходом фигуры.

        :param move: Клетка, на которую пытается сделать ход фигура.
        """
        pass

    def destroy(self) -> None:
        """
        Метод уничтожения фигуры. Удаляет фигуру с доски.
        """
        # self.chess.board[self.position.value[0]][self.position.value[1]] = None
        pass

    def is_own_cell(self, move: Move) -> bool:
        """ 
        Проверка на то, что фигура не пытается ходить на свою клетку 

        :param move: Клетка, на которую пытается сделать ход фигура
        """
        owner = self.chess.board[move.value[0]][move.value[1]]
        return owner == self

    def is_not_own_move(self):
        """ Проверка соответствие цветов фигуры и стороны хода """
        return self.chess.controll_side != self.side

    def is_cell_empty(self, move: Move) -> bool:
        """
        Проверка на пустоту клетки

        :param move: Клетка, на которую пытается сделать ход фигура
        """
        return self.chess.board[move.value[0]][move.value[1]] == None

    def is_frendly_cell(self, move: Move) -> bool:
        """
        Проверка на то, что фигура не пытается съесть свою фигуру

        :param move: Клетка, на которую пытается сделать ход фигура
        """
        return self.chess.board[move.value[0]][move.value[1]] != None and self.chess.board[move.value[0]][move.value[1]].side == self.side

    def traverse_direction(self, dr: int, dc: int, row: int, col: int, possible_moves: list, is_under_protection_figure: bool = False) -> None:
        """
        Вспомогательный метод для обхода клеток в указанном направлении.

        :param dr: Смещение по вертикали.
        :param dc: Смещение по горизонтали.
        :param row: Начальная строка.
        :param col: Начальный столбец.
        :param possible_moves: Список возможных ходов.
        :param with_guard_figure: Флаг, указывающий на необходимость добавления клеток с фигурами того же цвета для включения в список, как 'под защитой фигуры'.
        """
        from lib.king import King
        r, c = row + dr, col + dc
        while 0 <= r < 8 and 0 <= c < 8:
            other_figure = self.chess.board[r][c]
            move_key = Move((r, c))

            # NOTE: Клетка пустая
            if other_figure is None:
                possible_moves.append(move_key)
            elif isinstance(other_figure, King) and other_figure.side != self.side:
                # NOTE: Если фигура противника - король, добавляем клетку и продолжаем обход
                possible_moves.append(move_key)
            else:
                # NOTE: Если фигура того же цвета
                if other_figure.side == self.side:
                    # NOTE: Если фигура находится под защитой, добавляем клетку и прерываем обход
                    if is_under_protection_figure:
                        possible_moves.append(move_key)
                    break
                # NOTE: Если фигура противника, добавляем клетку и прерываем обход
                possible_moves.append(move_key)
                break

            r += dr
            c += dc

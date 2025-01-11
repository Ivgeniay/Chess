from lib.moveModel import MoveModel
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
        self.positions_list: list[Move] = [self.position]
        self.attacked_cells: set[Move] = set()
        self.possible_moves: set[Move] = set()

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
        self.positions_list.append(move)
        move_from = self.positions_list[len(
            self.positions_list) - 2] if len(self.positions_list) > 1 else None
        self.chess.moves.append(MoveModel(self.figure_type,
                                          move_from,
                                          move,
                                          self.side))

    def last_action(self) -> None:
        """
        Метод вызываемый после успешного хода фигуры. Позволяет реализовать дополнительные действия, связанные с ходом фигуры.
        """
        pass

    def destroy(self) -> None:
        """
        Метод вызываемый в момент уничтожения фигуры.
        """
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


from game.entities.abstract.IDrawable import IDrawable
from lib.move import Move
from lib.chess import Chess
from game.settings import *
import pygame as pg


class Board(IDrawable):
    def __init__(self) -> None:
        self.rect = (BOARD_OFFSET, BOARD_OFFSET, 8*SQUARE_SIZE *
                     SQUARE_SCALE, 8*SQUARE_SIZE*SQUARE_SCALE)

    def draw(self, surface: pg.Surface) -> None:
        self.draw_board(surface)

    def draw_board(self, surface: pg.Surface) -> None:
        """
        Отрисовка доски.

        :param surface: Поверхность, на которой будет отрисована доска.
        """

        size = 8
        for row in range(size):
            for col in range(size):
                color = WHITE if (row + col) % 2 == 0 else BLACK_SOFT
                rect_pos = self.get_cell_infos_by_chess_coord(col, row)
                rect = pg.Rect(rect_pos[0], rect_pos[1],
                               rect_pos[2], rect_pos[3])
                pg.draw.rect(surface, color, rect)

    def ouline_cell(self, surface: pg.Surface, move: Move, color: pg.Color = RED) -> None:
        cell_info = self.get_cell_info_by_move(move)
        pg.draw.rect(surface, color, pg.Rect(
            cell_info[0], cell_info[1], cell_info[2], cell_info[3]))

    def get_cell_by_absolut_screen_coord(self, x: int, y: int) -> Move | None:
        """
        Преобразует абсолютные координаты игрового окна в шахматные координаты.

        :param x: Абсолютная X-координата.
        :param y: Абсолютная Y-координата.
        :return: Координаты клетки в формате Move (например, Move.e2).
        """

        x_relative = x - BOARD_OFFSET[0]
        y_relative = y - BOARD_OFFSET[1]

        if x_relative < 0 or y_relative < 0:
            return None

        col = x_relative // (SQUARE_SIZE // SQUARE_SCALE)
        row = y_relative // (SQUARE_SIZE // SQUARE_SCALE)
        row = 7 - row

        if not (0 <= col < 8 and 0 <= row < 8):
            return None

        col_letter = chr(ord('a') + col)
        row_number = row + 1

        return Move[f"{col_letter}{row_number}"]

    def get_cell_infos_by_chess_coord(self, x: int, y: int) -> tuple[int, int, int, int]:
        """ 
        Принимает координаты доски вида (X, Y) и возвращет координаты верхнего левого угла клетки и ее размеры

        :param x: Координата клетки по горизонтали
        :param y: Координата клетки по вертикали
        :return: Кортеж с координатами верхнего левого угла клетки и ее размерами
        """
        adjusted_y = 7 - y  # Инверсия по вертикали
        x = x * SQUARE_SIZE
        adjusted_y = adjusted_y * SQUARE_SIZE
        return (x // SQUARE_SCALE + BOARD_OFFSET[0],
                adjusted_y // SQUARE_SCALE + BOARD_OFFSET[1],
                SQUARE_SIZE // SQUARE_SCALE,
                SQUARE_SIZE // SQUARE_SCALE)

    def get_cell_info_by_move(self, move: Move) -> tuple[int, int, int, int]:
        """
        Принимает шахматные координаты вида "Move.e2" и возвращает координаты верхнего левого угла клетки и ее размеры

        :param move: Ход вида "Move.e2"
        :return: Кортеж с координатами верхнего левого угла клетки и ее размерами
        """
        return self.get_cell_infos_by_chess_coord(move.value[1], move.value[0])

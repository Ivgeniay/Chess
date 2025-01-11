from game.entities.abstract.ISurfaceble import ISurfaceble
from game.entities.abstract.IUpdatable import IUpdatable
from game.entities.abstract.IDrawable import IDrawable
from game.entities.board import Board
from game.services.input import Input
from game.services.service_locator import ServiceLocator
from lib.move import Move
from lib.figure import Figure
from game.settings import *
import pygame as pg


class FigureDisplayManager(IDrawable, IUpdatable, ISurfaceble):
    from lib.chess import Chess

    # def __init__(self, chess: Chess, board: Board, input: Input, surface: pg.Surface) -> None:
    def __init__(self, surface: pg.Surface) -> None:
        from lib.chess import Chess
        self.chess = ServiceLocator.get(Chess)
        self.figures = self.chess.get_figure_list()
        self.board = ServiceLocator.get(Board)
        self.input = ServiceLocator.get(Input)
        self._surface = surface

        self.download_sprites()
        self.initialize_figures()

        self.dragging_object: Figure = None

        # self.input.mouse_left_down_register(self.start_dragging)
        # self.input.mouse_left_up_register(self.stop_dragging)
        self.input.mouse_left_down_register_ui(self, self.start_dragging)
        self.input.mouse_left_up_register_ui(self, self.stop_dragging)

    @property
    def surface(self) -> pg.Surface:
        return self._surface

    def restart(self):
        self.recall_figures(self.chess)

    def download_sprites(self) -> None:
        """
        Вспомогательный метод для загрузки спрайтов фигур.
        """
        self.w_pawn_pic = pg.image.load(
            "game/resources/sprites/white_pawn.png").convert_alpha()
        self.b_pawn_pic = pg.image.load(
            "game/resources/sprites/black_pawn.png").convert_alpha()
        self.w_bigshop_pic = pg.image.load(
            "game/resources/sprites/white_bishop.png").convert_alpha()
        self.b_bigshop_pic = pg.image.load(
            "game/resources/sprites/black_bishop.png").convert_alpha()
        self.w_knight_pic = pg.image.load(
            "game/resources/sprites/white_knight.png").convert_alpha()
        self.b_knight_pic = pg.image.load(
            "game/resources/sprites/black_knight.png").convert_alpha()
        self.w_rook_pic = pg.image.load(
            "game/resources/sprites/white_rook.png").convert_alpha()
        self.b_rook_pic = pg.image.load(
            "game/resources/sprites/black_rook.png").convert_alpha()
        self.w_queen_pic = pg.image.load(
            "game/resources/sprites/white_queen.png").convert_alpha()
        self.b_queen_pic = pg.image.load(
            "game/resources/sprites/black_queen.png").convert_alpha()
        self.w_king_pic = pg.image.load(
            "game/resources/sprites/white_king.png").convert_alpha()
        self.b_king_pic = pg.image.load(
            "game/resources/sprites/black_king.png").convert_alpha()

    def initialize_figures(self) -> None:
        """
        Метод для инициализации фигур на доске и добавления им праильного rect-позиционирования согласно их шахматного положения.
        """
        for figure in self.figures:
            coord: Move = figure.get_chess_position()
            cell_info: tuple[int, int, int,
                             int] = self.board.get_cell_info_by_move(coord)
            figure.rect = (cell_info[0], cell_info[1])

    def recall_figures(self, chess: Chess) -> None:
        """
        Метод для обновления списка фигур на доске и правильного их позиционирования.
        """
        self.figures = chess.get_figure_list()
        self.initialize_figures()

    def draw(self, surface: pg.surface.Surface) -> None:

        for figure in self.figures:
            if figure.figure_type == figure.figure_type.w_pawn:
                scaled_piece = pg.transform.scale(
                    self.w_pawn_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.b_pawn:
                scaled_piece = pg.transform.scale(
                    self.b_pawn_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.w_bishop:
                scaled_piece = pg.transform.scale(
                    self.w_bigshop_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.b_bishop:
                scaled_piece = pg.transform.scale(
                    self.b_bigshop_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.w_knight:
                scaled_piece = pg.transform.scale(
                    self.w_knight_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.b_knight:
                scaled_piece = pg.transform.scale(
                    self.b_knight_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.w_rook:
                scaled_piece = pg.transform.scale(
                    self.w_rook_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.b_rook:
                scaled_piece = pg.transform.scale(
                    self.b_rook_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.w_queen:
                scaled_piece = pg.transform.scale(
                    self.w_queen_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.b_queen:
                scaled_piece = pg.transform.scale(
                    self.b_queen_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.w_king:
                scaled_piece = pg.transform.scale(
                    self.w_king_pic, (SQUARE_SIZE, SQUARE_SIZE))

            elif figure.figure_type == figure.figure_type.b_king:
                scaled_piece = pg.transform.scale(
                    self.b_king_pic, (SQUARE_SIZE, SQUARE_SIZE))

            surface.blit(scaled_piece, figure.rect)

    def update(self) -> None:
        if self.input.is_mouse_left and self.dragging_object:
            self.dragging_object.rect = (
                DRAGGABLE_OFFSET[0] + self.input.mouse[0], DRAGGABLE_OFFSET[1] + self.input.mouse[1])

    def start_dragging(self) -> None:
        pos: Move | None = self.board.get_cell_by_absolut_screen_coord(
            self.input.mouse_x, self.input.mouse_y)
        if pos:
            self.dragging_object = next(
                (figure for figure in self.figures if figure.position == pos), None)

    def stop_dragging(self) -> None:
        if self.dragging_object:
            new_pos: Move | None = self.board.get_cell_by_absolut_screen_coord(
                self.input.mouse_x, self.input.mouse_y)
            if new_pos:
                if self.dragging_object.is_possible_move(new_pos):

                    pos = self.board.get_cell_info_by_move(new_pos)
                    self.dragging_object.rect = (pos[0], pos[1])
                    self.chess.move_figure(self.dragging_object, new_pos)
                else:
                    self.dragging_object.rect = self.board.get_cell_info_by_move(
                        self.dragging_object.position)
        self.dragging_object = None

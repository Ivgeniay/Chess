from game.services.resourse_service import ResourcesService
from game.entities.abstract.ISurfaceble import ISurfaceble
from game.entities.abstract.IUpdatable import IUpdatable
from game.services.service_locator import ServiceLocator
from game.entities.abstract.IDrawable import IDrawable
from game.entities.board import Board
from game.services.input import Input
from lib.figure_type import Figure_type
from lib.move import Move
from lib.figure import Figure
from game.settings import *
import pygame as pg


class FigureDisplayManager(IDrawable, IUpdatable, ISurfaceble):
    from lib.chess import Chess

    def __init__(self, surface: pg.Surface) -> None:
        from lib.chess import Chess
        self.chess: Chess = ServiceLocator.get(Chess)
        self.board: Board = ServiceLocator.get(Board)
        self.figures: list[Figure] = self.chess.get_figure_list()
        self.input: Input = ServiceLocator.get(Input)
        self._surface: pg.Surface = surface

        self.download_sprites()
        self.initialize_figures()

        self.dragging_object: Figure = None

        self.input.mouse_left_down_register(self, self.start_dragging)
        self.input.mouse_left_up_register(self, self.stop_dragging)

    @property
    def surface(self) -> pg.Surface:
        return self._surface

    def restart(self) -> None:
        self.recall_figures(self.chess)

    def download_sprites(self) -> None:
        """
        Вспомогательный метод для загрузки спрайтов фигур.
        """
        resourcesService: ResourcesService = ServiceLocator.get(
            ResourcesService)

        self.w_pawn_pic = resourcesService.get_resource(
            Figure_type.w_pawn.name)
        self.b_pawn_pic = resourcesService.get_resource(
            Figure_type.b_pawn.name)
        self.w_bigshop_pic = resourcesService.get_resource(
            Figure_type.w_bishop.name)
        self.b_bigshop_pic = resourcesService.get_resource(
            Figure_type.b_bishop.name)
        self.w_knight_pic = resourcesService.get_resource(
            Figure_type.w_knight.name)
        self.b_knight_pic = resourcesService.get_resource(
            Figure_type.b_knight.name)
        self.w_rook_pic = resourcesService.get_resource(
            Figure_type.w_rook.name)
        self.b_rook_pic = resourcesService.get_resource(
            Figure_type.b_rook.name)
        self.w_queen_pic = resourcesService.get_resource(
            Figure_type.w_queen.name)
        self.b_queen_pic = resourcesService.get_resource(
            Figure_type.b_queen.name)
        self.w_king_pic = resourcesService.get_resource(
            Figure_type.w_king.name)
        self.b_king_pic = resourcesService.get_resource(
            Figure_type.b_king.name)

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

                    pos: tuple[int, int, int,
                               int] = self.board.get_cell_info_by_move(new_pos)
                    self.dragging_object.rect = (pos[0], pos[1])
                    self.chess.move_figure(self.dragging_object, new_pos)
                else:
                    self.dragging_object.rect = self.board.get_cell_info_by_move(
                        self.dragging_object.position)
        self.dragging_object = None

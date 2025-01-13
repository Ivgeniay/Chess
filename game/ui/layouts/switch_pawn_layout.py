from re import S
from game.entities.FiguresManager import FigureDisplayManager
from game.services.resourse_service import ResourcesService
from game.services.service_locator import ServiceLocator
from game.settings import *
from game.ui.button import Button
from game.ui.layouts.layout import Layout

import pygame as pg

from game.ui.uielement import UiElement
from lib.chess import Chess
from lib.figure_type import Figure_type
from lib.pawn import Pawn
from lib.side import Side


class SwitchPawnLayout(Layout):
    def __init__(self, x: int, y: int, width: int, height: int, content: list[UiElement] = None, surface: pg.Surface = None, fill_color=BLACK) -> None:
        super().__init__(x, y, width, height, content, fill_color=fill_color)
        self.is_open = False
        self.switch_pawn: Pawn = None
        self.get_sprites()

        self.chess: Chess = ServiceLocator.get(Chess)
        self.chess.register_switch_pawn_handler(self.switch_pawn_handler)
        self.figure_dis_manager: FigureDisplayManager = ServiceLocator.get(
            FigureDisplayManager)

        queen_btn = Button(0, 0, 100, 100, text="Queen", action=lambda x: self.choose_figure(
            Figure_type.w_queen if self.switch_pawn.side == Side.WHITE else Figure_type.b_queen), surface=self._surface)
        rook_btn = Button(0, 0, 100, 100, text="Rook",
                          action=lambda x: self.choose_figure(Figure_type.w_rook if self.switch_pawn.side == Side.WHITE else Figure_type.b_rook), surface=self._surface)
        bishop_btn = Button(0, 0, 100, 100, text="Bishop",
                            action=lambda x: self.choose_figure(Figure_type.w_bishop if self.switch_pawn.side == Side.WHITE else Figure_type.b_bishop), surface=self._surface)
        knight_btn = Button(0, 0, 100, 100, text="Knight",
                            action=lambda x: self.choose_figure(Figure_type.w_knight if self.switch_pawn.side == Side.WHITE else Figure_type.b_knight), surface=self._surface)

        queen_btn.change_picture(self.w_queen_pic)
        queen_btn.change_hover_picture(self.w_queen_shine_pic)

        rook_btn.change_picture(self.w_rook_pic)
        rook_btn.change_hover_picture(self.w_rook_shine_pic)

        bishop_btn.change_picture(self.w_bigshop_pic)
        bishop_btn.change_hover_picture(self.w_bishop_shine_pic)

        knight_btn.change_picture(self.w_knight_pic)
        knight_btn.change_hover_picture(self.w_knight_shine_pic)

        self.add_element(queen_btn)
        self.add_element(rook_btn)
        self.add_element(bishop_btn)
        self.add_element(knight_btn)

    def choose_figure(self, figure: Figure_type) -> None:
        self.chess.switch_pawn(figure)
        self.close()
        self.figure_dis_manager.recall_figures(self.chess)

    def get_sprites(self) -> None:
        resourcesService: ResourcesService = ServiceLocator.get(
            ResourcesService)
        self.w_bigshop_pic: pg.Surface = resourcesService.get_resource(
            Figure_type.w_bishop.name)
        self.b_bigshop_pic: pg.Surface = resourcesService.get_resource(
            Figure_type.b_bishop.name)
        self.w_knight_pic: pg.Surface = resourcesService.get_resource(
            Figure_type.w_knight.name)
        self.b_knight_pic: pg.Surface = resourcesService.get_resource(
            Figure_type.b_knight.name)
        self.w_rook_pic: pg.Surface = resourcesService.get_resource(
            Figure_type.w_rook.name)
        self.b_rook_pic: pg.Surface = resourcesService.get_resource(
            Figure_type.b_rook.name)
        self.w_queen_pic: pg.Surface = resourcesService.get_resource(
            Figure_type.w_queen.name)
        self.b_queen_pic: pg.Surface = resourcesService.get_resource(
            Figure_type.b_queen.name)
        self.w_king_pic: pg.Surface = resourcesService.get_resource(
            Figure_type.w_king.name)
        self.b_king_pic: pg.Surface = resourcesService.get_resource(
            Figure_type.b_king.name)

        self.w_queen_shine_pic: pg.Surface = resourcesService.get_resource(
            "w_queen_shine")
        self.w_knight_shine_pic: pg.Surface = resourcesService.get_resource(
            "w_knight_shine")
        self.w_bishop_shine_pic: pg.Surface = resourcesService.get_resource(
            "w_bishop_shine")
        self.w_rook_shine_pic: pg.Surface = resourcesService.get_resource(
            "w_rook_shine")

    def switch_pawn_handler(self, figure: Pawn) -> None:
        self.switch_pawn: Pawn = figure
        self.open()

    def open(self) -> None:
        super().open()

    def close(self) -> None:
        super().close()

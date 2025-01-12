from game.entities.FiguresManager import FigureDisplayManager
from game.entities.abstract.IUpdatable import IUpdatable
from game.entities.abstract.IDrawable import IDrawable
from game.entities.abstract.Entity import Entity
from game.entities.board import Board
from game.services.input import Input
from game.services.resourse_service import ResourcesService
from game.services.service_locator import ServiceLocator
from game.settings import *
from game.ui.layouts.switch_pawn_layout import SwitchPawnLayout
from game.ui.surface.surface_manager import SurfaceManager
from game.ui.button import Button
from game.ui.text import TextUI

from game.ui.uielement import UiElement
from lib.chess import Chess

import pygame as pg


class Application:
    def __init__(self) -> None:
        pg.init()
        pg.display.set_caption(WINDOW_TITLE)

        self.screen: pg.Surface = pg.display.set_mode((WIDTH, HEIGHT))
        self.updatable: list[IUpdatable] = []
        self.drawable: list[IDrawable] = []
        self.running: bool = False

        ServiceLocator.register(Application, self)
        ServiceLocator.register(ResourcesService, ResourcesService())
        ServiceLocator.register(Chess, Chess())
        ServiceLocator.register(SurfaceManager, SurfaceManager())
        ServiceLocator.register(Board, Board())
        ServiceLocator.register(Input, Input())
        ServiceLocator.register(
            FigureDisplayManager, FigureDisplayManager(self.screen))

        self.restart_btn = Button(
            BTN_POSITION[0], BTN_POSITION[1], BTN_WIDTH, BTN_HEIGHT, text="Restart", action=self.restart, surface=self.screen)
        self.qunt_moves_textui = TextUI(
            BTN_POSITION[0] - BTN_WIDTH/2, BTN_POSITION[1] - BTN_HEIGHT/2 + 75, SCORE_WIDTH, SCORE_HEIGHT, text="100 : 100", font=pg.font.Font(None, 60))
        self.layout = SwitchPawnLayout(0, HEIGHT/3, WIDTH, HEIGHT/4)
        # self.layout2 = SwitchPawnLayout(WIDTH/2, HEIGHT/2, WIDTH/5, HEIGHT/5, fill_color=YELLOW)
        # self.layout3 = SwitchPawnLayout(0, 0, WIDTH/1.2, HEIGHT/4, fill_color=GREEN)

        self.entity_register(ServiceLocator.get(Input))
        self.entity_register(ServiceLocator.get(Board))
        self.entity_register(ServiceLocator.get(FigureDisplayManager))
        self.entity_register(self.restart_btn)
        self.entity_register(self.qunt_moves_textui)

        ServiceLocator.get(SurfaceManager).add_surface(
            self.screen, self.screen.get_rect(), 0, is_main=True)
        ServiceLocator.get(Input).quit_down_register(self.application_quit)
        ServiceLocator.get(Chess).register_next_turn_handler(
            ServiceLocator.get(FigureDisplayManager).recall_figures)
        ServiceLocator.get(Chess).register_next_turn_handler(lambda chess: self.qunt_moves_textui.set_text(
            f"{chess.half_move_number} : {chess.move_number}"))

    def restart(self, sender: UiElement) -> None:
        ServiceLocator.get(Chess).restart()
        ServiceLocator.get(FigureDisplayManager).restart()

    def run(self) -> None:
        self.running = True
        ServiceLocator.get(Chess).start()

        # NOTE: FEN sample
        # fen = "r3k2r/3b4/pqn1pnp1/1ppp1p1p/PbPP1PBP/BPNQPNP1/8/R3K2R b KQkq - 13 14"
        # fen = "rnbqkbnr/ppppp1pp/8/P7/5p2/8/1PPPPPPP/RNBQKBNR w KQkq - 2 2"
        fen = "rnbqkbnr/2ppppPP/8/8/8/8/ppPPPP2/RNBQKBNR w KQkq - 8 8"
        ServiceLocator.get(Chess).from_fen(fen)
        ServiceLocator.get(FigureDisplayManager).restart()
        ServiceLocator.get(Chess).start(False)

        while self.running:
            self.screen.fill(BLACK)
            self.draw()
            self.update()
            if self.running:
                pg.display.flip()

    def update(self) -> None:
        for updatable in self.updatable:
            if isinstance(updatable, IUpdatable):
                updatable.update()

    def draw(self) -> None:
        for idrawable in self.drawable:
            if isinstance(idrawable, IDrawable):
                idrawable.draw(self.screen)

        ServiceLocator.get(SurfaceManager).draw_surfaces()
        pass

    def entity_register(self, entity: Entity) -> None:
        if isinstance(entity, IUpdatable):
            self.updatable.append(entity)
        if isinstance(entity, IDrawable):
            self.drawable.append(entity)

    def entity_unregister(self, entity: Entity) -> None:
        if isinstance(entity, IUpdatable):
            self.updatable.remove(entity)
        if isinstance(entity, IDrawable):
            self.drawable.remove(entity)

    def application_quit(self) -> None:
        self.running = False
        pg.quit()

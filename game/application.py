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
        self.resources_service: ResourcesService = ServiceLocator.register(
            ResourcesService, ResourcesService())
        self.chess: Chess = ServiceLocator.register(Chess, Chess())
        self.surface_manager: SurfaceManager = ServiceLocator.register(
            SurfaceManager, SurfaceManager())
        self.board: Board = ServiceLocator.register(Board, Board())
        self.input: Input = ServiceLocator.register(
            Input, Input(self.surface_manager))
        self.figure_dmanager: FigureDisplayManager = ServiceLocator.register(
            FigureDisplayManager, FigureDisplayManager(self.screen))

        self.restart_btn = Button(
            BTN_POSITION[0], BTN_POSITION[1], BTN_WIDTH, BTN_HEIGHT, text="Restart", action=self.chess.restart, surface=self.screen)
        self.qunt_moves_textui = TextUI(BTN_POSITION[0] - BTN_WIDTH/2, BTN_POSITION[1] - BTN_HEIGHT /
                                        2 + 75, SCORE_WIDTH, SCORE_HEIGHT, text="100 : 100", font=pg.font.Font(None, 60))
        self.status_textui = TextUI(BTN_POSITION[0] - BTN_WIDTH/2, BTN_POSITION[1] - BTN_HEIGHT /
                                    2 + 110, SCORE_WIDTH, SCORE_HEIGHT, text="100 : 100", font=pg.font.Font(None, 30))
        self.layout = SwitchPawnLayout(0, HEIGHT/3, WIDTH, HEIGHT/4)

        self.entity_register(self.input)
        self.entity_register(self.board)
        self.entity_register(self.figure_dmanager)
        self.entity_register(self.restart_btn)
        self.entity_register(self.qunt_moves_textui)
        self.entity_register(self.status_textui)

        self.surface_manager.add_surface(
            self.screen, self.screen.get_rect(), 0, is_main=True)
        self.input.quit_down_register(self.application_quit)
        self.chess.register_next_turn_handler(
            self.figure_dmanager.recall_figures)
        self.chess.register_next_turn_handler(lambda chess: self.qunt_moves_textui.set_text(
            f"{chess.half_move_number} : {chess.move_number}"))
        self.chess.register_chess_message_handler(
            lambda message: self.status_textui.set_text(message))
        self.chess.register_chess_restart_handler(
            self.figure_dmanager.restart)

    def run(self) -> None:
        self.running = True
        self.chess.start()

        # NOTE: FEN sample
        # # хаос
        # fen = "r3k2r/3b4/pqn1pnp1/1ppp1p1p/PbPP1PBP/BPNQPNP1/8/R3K2R b KQkq - 13 14"
        # мат или пат черному
        fen = "k7/P2P3P/5P2/2Q2P2/8/8/8/2BQKBNR w KQkq - 27 27"
        # # детский мат черному
        # fen = "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 3 3"
        # превращение пешек на следующем ходу
        # fen = "rnbqkbnr/2ppppPP/8/8/8/8/ppPPPP2/RNBQKBNR w KQkq - 8 8"
        self.chess.from_fen(fen)
        self.figure_dmanager.restart(self.chess)
        self.chess.start(False)

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
        self.surface_manager.draw_surfaces()

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

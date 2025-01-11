from game.entities.FiguresManager import FigureDisplayManager
from game.entities.abstract.IUpdatable import IUpdatable
from game.entities.abstract.IDrawable import IDrawable
from game.entities.abstract.Entity import Entity
from game.entities.board import Board
from game.drawer import Drawer
from game.services.input import Input
from game.services.service_locator import ServiceLocator
from game.settings import *
from game.ui.button import Button
from game.ui.layout import Layout
from game.ui.surface_manager import SurfaceManager
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
        ServiceLocator.register(Chess, Chess())
        ServiceLocator.register(Drawer, Drawer(self.screen))
        ServiceLocator.register(SurfaceManager, SurfaceManager())
        ServiceLocator.register(Board, Board())
        ServiceLocator.register(Input, Input())
        ServiceLocator.register(
            FigureDisplayManager, FigureDisplayManager(self.screen))

        self.restart_btn = Button(BTN_POSITION[0], BTN_POSITION[1], BTN_WIDTH,
                                  BTN_HEIGHT, text="Restart", action=self.restart)
        self.qunt_moves_textui = TextUI(
            BTN_POSITION[0] - BTN_WIDTH/2, BTN_POSITION[1] - BTN_HEIGHT/2 + 75, SCORE_WIDTH, SCORE_HEIGHT, text="100 : 100", font=pg.font.Font(None, 60))
        self.layout = Layout(WIDTH/3, HEIGHT/3, WIDTH/3, HEIGHT/3)

        self.entity_register(ServiceLocator.get(Input))
        self.entity_register(ServiceLocator.get(Board))
        self.entity_register(ServiceLocator.get(FigureDisplayManager))
        self.entity_register(self.restart_btn)
        self.entity_register(self.qunt_moves_textui)
        self.entity_register(self.layout)

        ServiceLocator.get(SurfaceManager).add_surface(
            self.screen, self.screen.get_rect(), 0)
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
        fen = "r3k2r/3b4/pqn1pnp1/1ppp1p1p/PbPP1PBP/BPNQPNP1/8/R3K2R b KQkq - 13 14"
        # fen = "rnbqkbnr/ppppp1pp/8/P7/5p2/8/1PPPPPPP/RNBQKBNR w KQkq - 2 2"
        ServiceLocator.get(Chess).from_fen(fen)
        ServiceLocator.get(FigureDisplayManager).restart()
        ServiceLocator.get(Chess).start(False)

        while self.running:
            ServiceLocator.get(Drawer).clear()
            self.draw()
            self.update()
            if self.running:
                pg.display.flip()

    def update(self) -> None:
        for updatable in self.updatable:
            if isinstance(updatable, IUpdatable):
                updatable.update()

    def draw(self) -> None:
        for d in self.drawable:
            if isinstance(d, IDrawable):
                ServiceLocator.get(Drawer).draw(d)

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

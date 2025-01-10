from game.entities.FiguresManager import FigureDisplayManager
from game.entities.abstract.IUpdatable import IUpdatable
from game.entities.abstract.IDrawable import IDrawable
from game.entities.abstract.Entity import Entity
from game.entities.board import Board
from game.drawer import Drawer
from game.input import Input
from game.settings import *
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
        self.drawer: Drawer = Drawer(self.screen)
        self.running: bool = False

        self.chess: Chess = Chess()
        self.input: Input = Input()
        self.board: Board = Board()
        self.figureManager = FigureDisplayManager(
            self.chess, self.board, self.input)

        self.restart_btn = Button(BTN_POSITION[0], BTN_POSITION[1], BTN_WIDTH,
                                  BTN_HEIGHT, self.input, text="Restart", action=self.restart)
        self.qunt_moves_textui = TextUI(
            BTN_POSITION[0] - BTN_WIDTH/2, BTN_POSITION[1] - BTN_HEIGHT/2 + 75, SCORE_WIDTH, SCORE_HEIGHT, self.input, text="100 : 100", font=pg.font.Font(None, 60))

        self.input.quit_down_register(self.application_quit)

        self.entity_register(self.input)
        self.entity_register(self.board)
        self.entity_register(self.figureManager)
        self.entity_register(self.restart_btn)
        self.entity_register(self.qunt_moves_textui)

        self.chess.register_next_turn_handler(
            self.figureManager.recall_figures)
        self.chess.register_next_turn_handler(lambda chess: self.qunt_moves_textui.set_text(
            f"{chess.half_move_number} : {chess.move_number}"))

    def restart(self, sender: UiElement) -> None:
        self.chess.restart()
        self.figureManager.restart()

    def run(self) -> None:
        self.running = True
        self.chess.start()

        # NOTE: FEN sample
        # fen = "r3k2r/3b4/pqn1pnp1/1ppp1p1p/PbPP1PBP/BPNQPNP1/8/R3K2R b KQkq - 13 14"
        fen = "rnbqkbnr/ppppp1pp/8/P7/5p2/8/1PPPPPPP/RNBQKBNR w KQkq - 2 2"
        self.chess.from_fen(fen)
        self.figureManager.restart()
        self.chess.start(False)

        while self.running:
            self.drawer.clear()
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
                self.drawer.draw(d)

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

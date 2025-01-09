from game.entities.abstract.IDrawable import IDrawable
from game.settings import *
import pygame as pg


class Drawer:
    def __init__(self, screen: pg.Surface):
        self.screen = screen

    def clear(self):
        self.screen.fill(BLACK)

    def draw(self, idrawable: IDrawable):
        idrawable.draw(self.screen)

    def draw_text(self, text: str, x: int, y: int, size: int, color: pg.color.Color):
        font = pg.font.Font(None, size)
        text = font.render(text, True, color)
        self.screen.blit(text, (x, y))

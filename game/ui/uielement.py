from game.entities.abstract.IDrawable import IDrawable
from game.input import Input
from game.settings import *

from abc import ABC, abstractmethod
import pygame as pg


class UiElement(ABC, IDrawable):

    def __init__(self, x: int, y: int, width: int, height: int, input: Input, font: pg.font.Font = None, text: str = ""):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.font: pg.font.Font = font
        self.input: Input = input
        self.is_hovered: bool = False
        self.rect: pg.Rect = pg.Rect(self.x, self.y, self.width, self.height)
        if self.font is None:
            self.font = pg.font.Font(None, 36)
        self.text_surface = self.font.render(text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(
            center=(self.rect.centerx, self.rect.centery))

        self.input.mouse_pos_register(self.on_mouse_pos_change)
        self.input.mouse_left_down_register(self.on_click)

    @abstractmethod
    def draw(self, surface):
        pass

    def on_hover(self, value: bool):
        pass

    def on_click(self):
        pass

    def on_mouse_pos_change(self, pos: tuple[int, int]):
        is_collided = self.rect.collidepoint(pos)
        if is_collided != self.is_hovered:
            self.is_hovered = is_collided
            self.on_hover(self.is_hovered)

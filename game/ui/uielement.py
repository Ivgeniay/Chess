from game.entities.abstract.ISurfaceble import ISurfaceble
from game.entities.abstract.IDrawable import IDrawable
from game.services.input import Input
from game.services.service_locator import ServiceLocator
from game.settings import *

from abc import ABC, abstractmethod
import pygame as pg


class UiElement(ABC, IDrawable, ISurfaceble):

    def __init__(self, x: int, y: int, width: int, height: int, font: pg.font.Font = None, text: str = "", surface: pg.Surface = None):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self._surface: pg.Surface = surface
        self.font: pg.font.Font = font
        self.input: Input = ServiceLocator.get(Input)
        self.is_hovered: bool = False
        self.rect: pg.Rect = pg.Rect(self.x, self.y, self.width, self.height)
        if self.font is None:
            self.font = pg.font.Font(None, 36)
        self.text_surface = self.font.render(text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(
            center=(self.rect.centerx, self.rect.centery))

        self.input.mouse_pos_register(self.on_mouse_pos_change)
        self.input.mouse_left_down_register_ui(self, self.on_click)

    def surface(self) -> pg.Surface:
        return self._surface

    @abstractmethod
    def draw(self, surface):
        self.surface = surface
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

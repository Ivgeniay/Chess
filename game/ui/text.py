from game.ui.uielement import UiElement
from game.settings import *

import pygame as pg


class TextUI(UiElement):

    def __init__(self, x: int, y: int, width: int, height: int, text: str, font: pg.font.Font = None, surface: pg.Surface = None):
        super().__init__(x, y, width, height, font, text, surface)
        self.text_surface = self.font.render(text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(
            center=(self.rect.centerx, self.rect.centery))

    def draw(self, surface):
        super().draw(surface)
        surface.blit(self.text_surface, self.text_rect)

    def set_text(self, text: str):
        self.text_surface = self.font.render(text, True, WHITE)
        self.text_rect = self.text_surface.get_rect(
            center=(self.rect.centerx, self.rect.centery))

    def on_hover(self, value: bool):
        pass

    def on_click(self):
        pass

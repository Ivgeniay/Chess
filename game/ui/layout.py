from game.services.service_locator import ServiceLocator
from game.ui.surface_manager import SurfaceManager
from game.ui.uielement import UiElement
from game.services.input import Input
from game.settings import *

import pygame as pg


class Layout(UiElement):
    def __init__(self, x: int, y: int, width: int, height: int, font: pg.font.Font = None, content: list[UiElement] = None) -> None:
        self._surface = pg.Surface((width, height))
        super().__init__(x, y, width, height, font, "", self._surface)
        self.content = content
        self.is_open = False
        # ServiceLocator.get(SurfaceManager).add_surface(
        #     self._surface, self.rect)
        ServiceLocator.get(Input).mouse_pos_register(self.test)

    def draw(self, surface: pg.Surface) -> None:
        if not self.is_open:
            return

        surface.blit(self._surface, (self.x, self.y))
        if self.content is not None:
            for element in self.content:
                element.draw(self._surface)

    def test(self, pos: tuple[int, int]) -> None:
        if pos[0] > 700 and pos[0] > 700:
            self.open()
        else:
            self.close()

    def open(self) -> None:
        if not self.is_open:
            ServiceLocator.get(SurfaceManager).add_surface(
                self._surface, self.rect)
        self.is_open = True

    def close(self) -> None:
        if self.is_open:
            ServiceLocator.get(SurfaceManager).remove_surface(self._surface)
        self.is_open = False

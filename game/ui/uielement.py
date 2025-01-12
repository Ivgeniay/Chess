from game.entities.abstract.ISurfaceble import ISurfaceble
from game.entities.abstract.IDrawable import IDrawable
from game.services.input import Input
from game.services.service_locator import ServiceLocator
from game.settings import *

from abc import ABC, abstractmethod
import pygame as pg

from game.ui.surface.surface_manager import SurfaceManager


class UiElement(ABC, IDrawable, ISurfaceble):

    def __init__(self, x: int, y: int, width: int, height: int, font: pg.font.Font = None, text: str = "", surface: pg.Surface = None) -> None:
        self.x: int = x
        self.start_x: int = x
        self.y: int = y
        self.start_y: int = y
        self.width: int = width
        self.start_width: int = width
        self.height: int = height
        self.start_height: int = height
        self._surface: pg.Surface = surface
        self.font: pg.font.Font = font
        self.input: Input = ServiceLocator.get(Input)
        self.is_hovered: bool = False
        self.rect: pg.Rect = pg.Rect(self.x, self.y, self.width, self.height)
        if self.font is None:
            self.font = pg.font.Font(None, 36)
        self.text_surface: pg.Surface = self.font.render(text, True, WHITE)
        self.text_rect: pg.Rect = self.text_surface.get_rect(
            center=(self.rect.centerx, self.rect.centery))

        self.surface_manager: SurfaceManager = ServiceLocator.get(
            SurfaceManager)

        self.input.mouse_pos_register(self.on_mouse_pos_change)
        self.input.mouse_left_down_register(self, self.on_click)

    @property
    def surface(self) -> pg.Surface:
        return self._surface

    def draw(self, surface) -> None:
        pass

    def on_hover(self, value: bool) -> None:
        pass

    def on_click(self) -> None:
        pass

    def change_rect(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

    def on_mouse_pos_change(self, global_mouse_pos: tuple[int, int]) -> None:
        top_surface_info: pg.Surface | None = self.surface_manager.get_top_surface_at(
            *global_mouse_pos)
        if top_surface_info:
            t_sur: pg.Surface = top_surface_info["surface"]
            local_mouse_pos: tuple[int, int] | None = self.surface_manager.get_relative_mouse_pos(
                t_sur, global_mouse_pos)
            # print(local_mouse_pos, t_sur.get_rect())
            if t_sur == self.surface:
                if local_mouse_pos:
                    rect: pg.Rect = top_surface_info["rect"]
                    is_collided: bool = self.rect.collidepoint(local_mouse_pos)
                    if is_collided != self.is_hovered:
                        self.is_hovered = is_collided
                        self.on_hover(self.is_hovered)

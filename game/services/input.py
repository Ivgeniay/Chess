from game.entities.abstract.ISurfaceble import ISurfaceble
from game.entities.abstract.IUpdatable import IUpdatable
from typing import Callable
import pygame as pg

from game.services.service_locator import ServiceLocator
from game.ui.surface_manager import SurfaceManager


class Input(IUpdatable):

    def __init__(self):

        self.mouse_left_down_handlers_ui: list[tuple[ISurfaceble, Callable[[], None]]] = [
        ]
        self.mouse_left_up_handlers_ui: list[tuple[ISurfaceble, Callable[[], None]]] = [
        ]
        self.surface_manager = ServiceLocator.get(SurfaceManager)

        self.mouse_pos: tuple[int, int] = (0, 0)
        self.is_mouse_left: bool = False
        self.is_mouse_right: bool = False
        self.mouse_left_down_handlers: list[Callable[[], None]] = []
        self.mouse_left_up_handlers: list[Callable[[], None]] = []
        self.quit_down_handlers: list[Callable[[], None]] = []
        self.mouse_pos_handlers: list[Callable[[tuple[int, int]], None]] = []

    @property
    def mouse_x(self) -> int:
        return self.mouse_pos[0]

    @property
    def mouse_y(self) -> int:
        return self.mouse_pos[1]

    @property
    def mouse(self) -> tuple[int, int]:
        return self.mouse_pos

    @property
    def is_left(self) -> bool:
        return self.is_mouse_left

    @property
    def is_right(self) -> bool:
        return self.is_mouse_right

    def update(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_down()

            if event.type == pg.MOUSEMOTION:
                if self.mouse_pos != event.pos:
                    self.mouse_pos = event.pos
                    for handler in self.mouse_pos_handlers:
                        handler(self.mouse_pos)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_left_down()
                    self.mouse_left_down_ui()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_left_up()
                    self.mouse_left_up_ui()

    def quit_down(self) -> None:
        for handler in self.quit_down_handlers:
            handler()

    def mouser_position(self) -> tuple[int, int]:
        return self.mouse_pos

    def mouse_left_down(self) -> None:
        self.is_mouse_left = True
        for handler in self.mouse_left_down_handlers:
            handler()

    def mouse_left_up(self) -> None:
        self.is_mouse_left = False
        for handler in self.mouse_left_up_handlers:
            handler()

    def mouse_left_down_ui(self) -> None:
        if self.surface_manager is None:
            return
        self.is_mouse_left = True
        upper_sur = self.surface_manager.get_top_surface_at(*self.mouse_pos)
        if upper_sur:
            for handler in self.mouse_left_down_handlers_ui:
                if isinstance(handler[0], ISurfaceble):
                    handler_surface = handler[0].surface
                    if upper_sur["surface"] == handler_surface:
                        handler[1]()

    def mouse_left_up_ui(self) -> None:
        if self.surface_manager is None:
            return
        self.is_mouse_left = False
        upper_sur = self.surface_manager.get_top_surface_at(*self.mouse_pos)
        if upper_sur:
            for handler in self.mouse_left_up_handlers_ui:
                handler_surface = handler[0].surface
                if upper_sur["surface"] == handler_surface:
                    handler[1]()

    def mouse_left_down_register_ui(self, isurfaceble: ISurfaceble, callback: Callable[[], None]) -> None:
        self.mouse_left_down_handlers_ui.append((isurfaceble, callback))

    def mouse_left_up_register_ui(self, isurfaceble: ISurfaceble, callback: Callable[[], None]) -> None:
        self.mouse_left_up_handlers_ui.append((isurfaceble, callback))

    def mouse_left_down_register(self, callback: Callable[[], None]) -> None:
        self.mouse_left_down_handlers.append(callback)

    def mouse_left_up_register(self, callback: Callable[[], None]) -> None:
        self.mouse_left_up_handlers.append(callback)

    def mouse_pos_register(self, callback: Callable[[tuple[int, int]], None]) -> None:
        self.mouse_pos_handlers.append(callback)

    def quit_down_register(self, callback: Callable[[], None]) -> None:
        self.quit_down_handlers.append(callback)

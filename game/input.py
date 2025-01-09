from game.entities.abstract.IUpdatable import IUpdatable
from typing import Callable
import pygame as pg


class Input(IUpdatable):

    def __init__(self):
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.is_mouse_left: bool = False
        self.is_mouse_right: bool = False
        self.key_down_handlers: list[Callable[[any], None]] = []
        self.key_up_handlers: list[Callable[[any], None]] = []
        self.mouse_left_down_handlers: list[Callable[[], None]] = []
        self.mouse_left_up_handlers: list[Callable[[], None]] = []
        self.mouse_right_down_handlers: list[Callable[[], None]] = []
        self.mouse_right_up_handlers: list[Callable[[], None]] = []
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

            if event.type == pg.KEYDOWN:
                self.key_down(event.key)
            if event.type == pg.KEYUP:
                self.key_up(event.key)
            if event.type == pg.MOUSEMOTION:
                if self.mouse_pos != event.pos:
                    self.mouse_pos = event.pos
                    for handler in self.mouse_pos_handlers:
                        handler(self.mouse_pos)

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_left_down()
                if event.button == 3:
                    self.mouse_right_down()
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_left_up()
                if event.button == 3:
                    self.mouse_right_up()

    def quit_down(self) -> None:
        for handler in self.quit_down_handlers:
            handler()

    def mouser_position(self) -> tuple[int, int]:
        return self.mouse_pos

    def key_up(self, key) -> None:
        for handler in self.key_up_handlers:
            handler(key)

    def key_down(self, key) -> None:
        for handler in self.key_down_handlers:
            handler(key)

    def mouse_right_down(self) -> None:
        self.is_mouse_right = True
        for handler in self.mouse_right_down_handlers:
            handler()

    def mouse_right_up(self) -> None:
        self.is_mouse_right = False
        for handler in self.mouse_right_up_handlers:
            handler

    def mouse_left_down(self) -> None:
        self.is_mouse_left = True
        for handler in self.mouse_left_down_handlers:
            handler()

    def mouse_left_up(self) -> None:
        self.is_mouse_left = False
        for handler in self.mouse_left_up_handlers:
            handler()

    def mouse_pos_register(self, callback: Callable[[tuple[int, int]], None]) -> None:
        self.mouse_pos_handlers.append(callback)

    def quit_down_register(self, callback: Callable[[], None]) -> None:
        self.quit_down_handlers.append(callback)

    def quit_down_unregister(self, callback: Callable[[], None]) -> None:
        self.quit_down_handlers.remove(callback)

    def key_down_register(self, callback: Callable[[any], None]) -> None:
        self.key_down_handlers.append(callback)

    def key_down_unregister(self, callback: Callable[[any], None]) -> None:
        self.key_down_handlers.remove(callback)

    def key_up_register(self, callback: Callable[[any], None]) -> None:
        self.key_up_handlers.append(callback)

    def key_up_unregister(self, callback: Callable[[any], None]) -> None:
        self.key_up_handlers.remove(callback)

    def mouse_left_down_register(self, callback: Callable[[], None]) -> None:
        self.mouse_left_down_handlers.append(callback)

    def mouse_left_down_unregister(self, callback: Callable[[], None]) -> None:
        self.mouse_left_down_handlers.remove(callback)

    def mouse_left_up_register(self, callback: Callable[[], None]) -> None:
        self.mouse_left_up_handlers.append(callback)

    def mouse_left_up_unregister(self, callback: Callable[[], None]) -> None:
        self.mouse_left_up_handlers.remove(callback)

    def mouse_right_down_register(self, callback: Callable[[], None]) -> None:
        self.mouse_right_down_handlers.append(callback)

    def mouse_right_down_unregister(self, callback: Callable[[], None]) -> None:
        self.mouse_right_down_handlers.remove(callback)

    def mouse_right_up_register(self, callback: Callable[[], None]) -> None:
        self.mouse_right_up_handlers.append(callback)

    def mouse_right_up_unregister(self, callback: Callable[[], None]) -> None:
        self.mouse_right_up_handlers.remove(callback)
